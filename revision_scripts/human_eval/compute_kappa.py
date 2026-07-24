"""Cohen's Kappa and per-model score summary for two filled annotation sheets.

Usage: .venv/bin/python revision_scripts/human_eval/compute_kappa.py rater1.csv rater2.csv
Both files must be copies of annotation_sheet.csv with d1/d2/d3 filled (1-5).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DIMS = ["d1_accuracy", "d2_evidence", "d3_actionability"]


def cohen_kappa(a, b, n_cat=5, weighted=False):
    a = np.asarray(a, dtype=int) - 1
    b = np.asarray(b, dtype=int) - 1
    obs = np.zeros((n_cat, n_cat))
    for i, j in zip(a, b):
        obs[i, j] += 1
    obs /= obs.sum()
    pa = obs.sum(axis=1)
    pb = obs.sum(axis=0)
    exp = np.outer(pa, pb)
    if weighted:
        idx = np.arange(n_cat)
        w = 1 - np.abs(idx[:, None] - idx[None, :]) / (n_cat - 1)
    else:
        w = np.eye(n_cat)
    po = (w * obs).sum()
    pe = (w * exp).sum()
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    r1 = pd.read_csv(sys.argv[1])
    r2 = pd.read_csv(sys.argv[2])
    key = pd.read_csv(HERE / "annotation_key.csv")
    merged = r1.merge(r2, on="report_id", suffixes=("_r1", "_r2")).merge(key, on="report_id")

    print(f"{len(merged)} reports scored by both raters\n")
    print(f"{'dimension':<20} {'kappa':>7} {'weighted':>9} {'mean r1':>8} {'mean r2':>8}")
    for d in DIMS:
        a, b = merged[f"{d}_r1"], merged[f"{d}_r2"]
        mask = a.notna() & b.notna()
        k = cohen_kappa(a[mask], b[mask])
        kw = cohen_kappa(a[mask], b[mask], weighted=True)
        print(f"{d:<20} {k:>7.3f} {kw:>9.3f} {a[mask].mean():>8.2f} {b[mask].mean():>8.2f}")

    print("\nPer-model means (average of both raters):")
    for d in DIMS:
        merged[f"{d}_avg"] = (merged[f"{d}_r1"] + merged[f"{d}_r2"]) / 2
    summary = merged.groupby("model")[[f"{d}_avg" for d in DIMS]].mean().round(2)
    print(summary.to_string())


if __name__ == "__main__":
    main()
