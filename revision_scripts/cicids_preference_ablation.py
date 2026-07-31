"""Ablation of the 90% preference-table rule in the KG-scoped rerank.

The reranker in the notebooks selects the max-cosine candidate within the
KG-scoped set, but overrides it with a fixed per-relation preferred technique
(RELATION_TECHNIQUE_PREFERENCE) whenever that preference scores within 90% of
the top candidate. Because the preference table encodes expert knowledge that
partially mirrors the ground-truth label mapping, this rule is the sharpest
point of potential circularity. This script recomputes the rerank twice from
the saved artifacts -- once with the rule (to validate that the recomputation
reproduces the pipeline's assignments) and once without it -- and reports both.

No LLM involved; deterministic given the saved HyDE queries, triples, and
alert texts. Writes results/cicids/<model>/preference_ablation.json.

Run: .venv/bin/python revision_scripts/cicids_preference_ablation.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["mistral-nemo-12b", "qwen2.5-3b", "qwen2.5-coder-7b"]

RELATION_TO_TECHNIQUES = {
    "PERFORMS_RECONNAISSANCE": ["T1046"],
    "PERFORMS_PORT_SCAN": ["T1046"],
    "BRUTE_FORCES_CREDENTIAL": ["T1110", "T1110.001", "T1110.003"],
    "EXPLOITS_VULNERABILITY": ["T1190", "T1203"],
    "ESTABLISHES_C2": ["T1071", "T1071.001", "T1071.004"],
    "PERFORMS_BEACONING": ["T1071", "T1071.004"],
    "CAUSES_DENIAL_OF_SERVICE": ["T1498", "T1499", "T1499.001"],
}
RELATION_TECHNIQUE_PREFERENCE = {
    "PERFORMS_PORT_SCAN": "T1046",
    "PERFORMS_RECONNAISSANCE": "T1046",
    "BRUTE_FORCES_CREDENTIAL": "T1110.001",
    "CAUSES_DENIAL_OF_SERVICE": "T1498.001",
    "ESTABLISHES_C2": "T1071.001",
    "PERFORMS_BEACONING": "T1071.001",
    "EXPLOITS_VULNERABILITY": "T1190",
}


def load_attck(path):
    bundle = json.load(open(path))
    techs = {}
    for obj in bundle["objects"]:
        if obj.get("type") != "attack-pattern" or obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        tid = next((r["external_id"] for r in obj.get("external_references", [])
                    if r.get("source_name") == "mitre-attack"), None)
        if not tid:
            continue
        tac = [p["phase_name"] for p in obj.get("kill_chain_phases", [])
               if p.get("kill_chain_name") == "mitre-attack"]
        techs[tid] = {"name": obj.get("name", ""), "description": obj.get("description", ""),
                      "tactic": tac[0] if tac else ""}
    return techs


def macro_exact(rows):
    by_gt = defaultdict(list)
    for gt, ok in rows:
        by_gt[gt].append(ok)
    return float(np.mean([np.mean(v) for v in by_gt.values()]))


def main():
    attck = load_attck(ROOT / "data/attck/enterprise-attack.json")
    tech_ids = list(attck.keys())
    tid_to_idx = {t: i for i, t in enumerate(tech_ids)}
    tech_texts = [f"ID: {t}\nName: {attck[t]['name']}\nTactic: {attck[t]['tactic']}\n"
                  f"Description: {attck[t]['description']}" for t in tech_ids]
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    tech_embs = embedder.encode(tech_texts, convert_to_tensor=True, show_progress_bar=True)

    for mk in MODELS:
        base = ROOT / "results/cicids" / mk
        rep = pd.read_csv(base / "rag_reports.csv")
        assign = pd.read_csv(base / "community_assignments.csv")
        triples = json.load(open(base / "community_triples.json"))

        rows_with, rows_wo = [], []
        n_with = n_wo = n_match_saved = n_rule_fired = 0
        per_community = []
        for _, r in rep.iterrows():
            cid = int(r["community_id"])
            gt = r["ground_truth"]
            rels = [t["relation"] for t in triples.get(str(cid), [])]
            cands, seen = [], set()
            for rel in rels:
                for tid in RELATION_TO_TECHNIQUES.get(rel, []):
                    if tid in tid_to_idx and tid not in seen:
                        cands.append(tid); seen.add(tid)
            group = assign[assign["community_id"] == cid]
            alert_context = " ".join(group["alert_text"].dropna().head(3).tolist())
            cand_idx = [tid_to_idx[t] for t in cands] if cands else list(range(len(tech_ids)))
            cand_embs = tech_embs[cand_idx]

            qs = [embedder.encode((alert_context or "")[:400], convert_to_tensor=True),
                  embedder.encode(str(r["raw_triples"]) or "", convert_to_tensor=True),
                  embedder.encode((str(r["hyde_query"]) or "")[:400], convert_to_tensor=True)]
            combined = np.maximum.reduce(
                [util.pytorch_cos_sim(q, cand_embs)[0].cpu().numpy() for q in qs])

            best_i = int(np.argmax(combined))
            pred_wo = (cands or tech_ids)[best_i] if cands else tech_ids[best_i]
            best_score = float(combined[best_i])

            pred_with = pred_wo
            dom = Counter(rels).most_common(1)[0][0] if rels else None
            pref = RELATION_TECHNIQUE_PREFERENCE.get(dom) if dom else None
            fired = False
            if pref and pref in cands:
                p_i = cands.index(pref)
                if combined[p_i] >= best_score * 0.90 and pref != pred_wo:
                    pred_with, fired = pref, True
                elif combined[p_i] >= best_score * 0.90:
                    pred_with = pref
            n_rule_fired += fired

            n_with += pred_with == gt
            n_wo += pred_wo == gt
            n_match_saved += pred_with == r["rag_technique_id"]
            rows_with.append((gt, pred_with == gt))
            rows_wo.append((gt, pred_wo == gt))
            per_community.append({"community_id": cid, "ground_truth": gt,
                                  "saved_rag_id": r["rag_technique_id"],
                                  "with_rule": pred_with, "without_rule": pred_wo,
                                  "rule_changed_outcome": fired})

        n = len(rep)
        out = {
            "condition": "KG-scoped rerank with vs without the 90% preference-table rule",
            "n_communities": n,
            "recomputed_matches_saved_assignment": f"{n_match_saved}/{n}",
            "rule_fired_and_changed_prediction": n_rule_fired,
            "with_rule": {"exact": round(n_with / n, 4), "macro": round(macro_exact(rows_with), 4)},
            "without_rule": {"exact": round(n_wo / n, 4), "macro": round(macro_exact(rows_wo), 4)},
            "per_community": per_community,
        }
        (base / "preference_ablation.json").write_text(json.dumps(out, indent=2))
        print(f"{mk}: reproduces saved {n_match_saved}/{n} | rule changed pred on "
              f"{n_rule_fired} | with={out['with_rule']['exact']} "
              f"without={out['without_rule']['exact']}")


if __name__ == "__main__":
    main()
