"""Build a blinded, shuffled annotation sheet from the saved CIC-IDS reports.

Pools all 3 models x 18 reports, shuffles with the project seed, and splits
into a rater-facing sheet (no model, no ground truth) and a key file.

Run: .venv/bin/python revision_scripts/human_eval/generate_annotation_sheet.py
"""
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
MODELS = ["mistral-nemo-12b", "qwen2.5-3b", "qwen2.5-coder-7b"]
SEED = 42

rows = []
for mk in MODELS:
    rep = pd.read_csv(ROOT / "results/cicids" / mk / "rag_reports.csv")
    assign = pd.read_csv(ROOT / "results/cicids" / mk / "community_assignments.csv")
    for _, r in rep.iterrows():
        cid = int(r["community_id"])
        alerts = assign[assign["community_id"] == cid]["alert_text"].dropna().head(3)
        rows.append({
            "model": mk,
            "community_id": cid,
            "ground_truth": r["ground_truth"],
            "alert_evidence": " || ".join(alerts.tolist()),
            "technique_id": r["rag_technique_id"],
            "tactic": r["rag_tactic"],
            "summary": r["rag_summary"],
            "evidence": r["rag_evidence"],
            "next_step": r["rag_next_step"],
        })

random.Random(SEED).shuffle(rows)
df = pd.DataFrame(rows)
df.insert(0, "report_id", [f"R{i:03d}" for i in range(1, len(df) + 1)])

key_cols = ["report_id", "model", "community_id", "ground_truth"]
df[key_cols].to_csv(HERE / "annotation_key.csv", index=False)

sheet = df.drop(columns=["model", "ground_truth", "community_id"]).copy()
for col in ("d1_accuracy", "d2_evidence", "d3_actionability", "comments"):
    sheet[col] = ""
sheet.to_csv(HERE / "annotation_sheet.csv", index=False)

print(f"wrote {HERE / 'annotation_sheet.csv'} ({len(sheet)} reports, blinded)")
print(f"wrote {HERE / 'annotation_key.csv'} (keep away from raters)")
