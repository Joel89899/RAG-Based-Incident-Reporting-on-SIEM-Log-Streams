"""Correctness-vs-faithfulness quadrant figure for the dual-metric evaluation.

Reads rag_metrics.json for the three CIC-IDS models and renders the
divergence between exact-match correctness and retrieval faithfulness.
Output: My_thesis_document/figures/cicids_correctness_faithfulness.png

Run: .venv/bin/python revision_scripts/make_quadrant_figure.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "My_thesis_document/figures/cicids_correctness_faithfulness.png"

LABELS = {
    "mistral-nemo-12b": "Mistral-Nemo-12B",
    "qwen2.5-3b": "Qwen2.5-3B",
    "qwen2.5-coder-7b": "Qwen2.5-Coder-7B",
}

points = {}
for mk, label in LABELS.items():
    m = json.load(open(ROOT / "results/cicids" / mk / "rag_metrics.json"))
    points[label] = (m["rag_faithfulness_mean"], m["rag_exact_match_rate"])
majority = json.load(open(ROOT / "results/cicids/mistral-nemo-12b/rag_metrics.json"))[
    "majority_class_accuracy"]

mean_faith = sum(x for x, _ in points.values()) / len(points)

fig, ax = plt.subplots(figsize=(7.0, 4.6))

# Reference lines: meaningful thresholds, recessive style.
ax.axhline(majority, color="#9a9a9a", linewidth=1, linestyle="--", zorder=1)
ax.axvline(mean_faith, color="#9a9a9a", linewidth=1, linestyle="--", zorder=1)
ax.annotate(f"majority-class accuracy ({majority:.3f})",
            xy=(0.678, majority), xytext=(0, 4), textcoords="offset points",
            ha="right", fontsize=8.5, color="#6d6d6d")
ax.annotate(f"mean faithfulness ({mean_faith:.3f})",
            xy=(mean_faith, 0.60), xytext=(4, 0), textcoords="offset points",
            ha="left", fontsize=8.5, color="#6d6d6d", rotation=90, va="bottom")

# Region annotations in muted ink.
region = dict(fontsize=9, color="#8b8b8b", style="italic", zorder=1)
ax.text(0.425, 0.965, "correct, weakly grounded", ha="left", va="top", **region)
ax.text(0.675, 0.965, "correct and grounded", ha="right", va="top", **region)
ax.text(0.425, 0.05, "neither", ha="left", va="bottom", **region)
ax.text(0.675, 0.05, "grounded but wrong", ha="right", va="bottom", **region)

# Data marks: one hue, identity carried by direct labels.
offsets = {"Mistral-Nemo-12B": (10, 6), "Qwen2.5-3B": (-10, 6),
           "Qwen2.5-Coder-7B": (-10, 8)}
ha = {"Mistral-Nemo-12B": "left", "Qwen2.5-3B": "right", "Qwen2.5-Coder-7B": "right"}
for label, (x, y) in points.items():
    ax.scatter(x, y, s=110, color="#1f77b4", edgecolor="white", linewidth=1.5, zorder=3)
    ax.annotate(f"{label}\n({x:.3f}, {y:.3f})", xy=(x, y),
                xytext=offsets[label], textcoords="offset points",
                ha=ha[label], va="bottom", fontsize=9, color="#333333", zorder=3)

ax.set_xlim(0.42, 0.68)
ax.set_ylim(0.0, 1.0)
ax.set_xlabel("Faithfulness (cosine similarity, summary vs. retrieved ATT&CK text)")
ax.set_ylabel("Correctness (exact-match rate)")
ax.grid(True, linewidth=0.4, color="#e6e6e6", zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, dpi=200)
print(f"wrote {OUT}")
