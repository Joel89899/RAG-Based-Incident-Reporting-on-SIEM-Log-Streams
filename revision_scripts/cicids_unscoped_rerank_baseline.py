"""Symmetric ablation for CIC-IDS: the KG-anchored reranker with the KG constraint removed.

Reuses the saved HyDE queries, raw triples, and community assignments from
results/cicids/<model>/, so no LLM call is needed. Scoring is identical to
scoped_rerank() in the notebooks -- max of three cosine similarities
(alert context, raw triples, HyDE query) against technique embeddings --
except the candidate set is all 691 ATT&CK techniques instead of the
KG-bridged subset. Writes results/cicids/<model>/unscoped_rerank_baseline.json.

Run with the project venv: .venv/bin/python revision_scripts/cicids_unscoped_rerank_baseline.py
"""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["mistral-nemo-12b", "qwen2.5-3b", "qwen2.5-coder-7b"]


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


def parent_match(gt, pred):
    if not gt or not pred or pred == "Unknown":
        return False
    return gt.split(".")[0] == pred.split(".")[0]


def macro_exact(rows):
    by_gt = defaultdict(list)
    for gt, ok in rows:
        by_gt[gt].append(ok)
    return float(np.mean([np.mean(v) for v in by_gt.values()]))


def main():
    attck = load_attck(ROOT / "data/attck/enterprise-attack.json")
    tech_ids = list(attck.keys())
    # Same document format the notebooks embed for the reranker fallback.
    tech_texts = [f"ID: {t}\nName: {attck[t]['name']}\nTactic: {attck[t]['tactic']}\n"
                  f"Description: {attck[t]['description']}" for t in tech_ids]
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    tech_embs = embedder.encode(tech_texts, convert_to_tensor=True, show_progress_bar=True)

    for mk in MODELS:
        base = ROOT / "results/cicids" / mk
        rep = pd.read_csv(base / "rag_reports.csv")
        assign = pd.read_csv(base / "community_assignments.csv")

        rows, per_community = [], []
        n_exact = n_parent = 0
        for _, r in rep.iterrows():
            cid = int(r["community_id"])
            gt = r["ground_truth"]
            group = assign[assign["community_id"] == cid]
            alert_context = " ".join(group["alert_text"].dropna().head(3).tolist())

            q_alert = embedder.encode((alert_context or "")[:400], convert_to_tensor=True)
            q_raw = embedder.encode(str(r["raw_triples"]) or "", convert_to_tensor=True)
            q_hyde = embedder.encode((str(r["hyde_query"]) or "")[:400], convert_to_tensor=True)
            sims = np.maximum.reduce([
                util.pytorch_cos_sim(q, tech_embs)[0].cpu().numpy()
                for q in (q_alert, q_raw, q_hyde)
            ])
            pred = tech_ids[int(np.argmax(sims))]

            exact = pred == gt
            par = parent_match(gt, pred)
            n_exact += exact
            n_parent += par
            rows.append((gt, exact))
            per_community.append({"community_id": cid, "ground_truth": gt,
                                  "unscoped_pred": pred, "exact": bool(exact)})

        n = len(rep)
        out = {
            "condition": "unscoped rerank (same max-of-three cosine scoring, no KG candidate restriction)",
            "n_communities": n,
            "exact_match_rate": round(n_exact / n, 4),
            "parent_match_rate": round(n_parent / n, 4),
            "exact_macro": round(macro_exact(rows), 4),
            "per_community": per_community,
        }
        (base / "unscoped_rerank_baseline.json").write_text(json.dumps(out, indent=2))
        print(f"{mk}: exact={out['exact_match_rate']} parent={out['parent_match_rate']} "
              f"macro={out['exact_macro']}")


if __name__ == "__main__":
    main()
