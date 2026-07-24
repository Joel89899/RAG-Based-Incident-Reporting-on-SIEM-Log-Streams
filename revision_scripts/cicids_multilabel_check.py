"""Set-widening check for CIC-IDS: does single-label scoring undersell the pipeline?

For each evaluated community, builds the full prediction set: every technique
reachable from any extracted relation via RELATION_TO_TECHNIQUES, plus the
report's assigned identifier. Scores ground-truth membership in that set.
Needs only the saved artifacts (community_triples.json, rag_reports.csv);
no LLM, no embedder. Writes results/cicids/<model>/multilabel_check.json.

Run: .venv/bin/python revision_scripts/cicids_multilabel_check.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MODELS = ["mistral-nemo-12b", "qwen2.5-3b", "qwen2.5-coder-7b"]

REL2TECH = {
    "PERFORMS_RECONNAISSANCE": ["T1046"],
    "PERFORMS_PORT_SCAN": ["T1046"],
    "BRUTE_FORCES_CREDENTIAL": ["T1110", "T1110.001", "T1110.003"],
    "EXPLOITS_VULNERABILITY": ["T1190", "T1203"],
    "ESTABLISHES_C2": ["T1071", "T1071.001", "T1071.004"],
    "PERFORMS_BEACONING": ["T1071", "T1071.004"],
    "CAUSES_DENIAL_OF_SERVICE": ["T1498", "T1499", "T1499.001"],
}


def parent(t):
    return t.split(".")[0]


def main():
    for mk in MODELS:
        base = ROOT / "results/cicids" / mk
        triples = json.load(open(base / "community_triples.json"))
        rep = pd.read_csv(base / "rag_reports.csv")

        n = len(rep)
        hits_exact = hits_parent = 0
        set_sizes, per_community = [], []
        for _, r in rep.iterrows():
            cid = str(int(r["community_id"]))
            gt = r["ground_truth"]
            pred_set = []
            for t in triples.get(cid, []):
                for tid in REL2TECH.get(t["relation"], []):
                    if tid not in pred_set:
                        pred_set.append(tid)
            rid = r["rag_technique_id"]
            if rid and rid not in pred_set:
                pred_set.append(rid)
            set_sizes.append(len(pred_set))
            ex = gt in pred_set
            pa = parent(gt) in {parent(p) for p in pred_set}
            hits_exact += ex
            hits_parent += pa
            per_community.append({"community_id": int(r["community_id"]), "ground_truth": gt,
                                  "prediction_set": pred_set, "gt_in_set": bool(ex)})

        out = {
            "condition": "set-widening: GT-in-set over all reachable techniques + assigned ID",
            "n_communities": n,
            "gt_in_set_exact": round(hits_exact / n, 4),
            "gt_in_set_parent": round(hits_parent / n, 4),
            "mean_set_size": round(sum(set_sizes) / n, 2),
            "per_community": per_community,
        }
        (base / "multilabel_check.json").write_text(json.dumps(out, indent=2))
        print(f"{mk}: exact={out['gt_in_set_exact']} parent={out['gt_in_set_parent']} "
              f"mean_set_size={out['mean_set_size']}")


if __name__ == "__main__":
    main()
