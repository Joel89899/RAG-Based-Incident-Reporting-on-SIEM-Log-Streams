# Revision scripts

Post-hoc analyses and pending experiments supporting the thesis revision.
All paths are relative to the repo root; use the project venv.

## Already run (results in the thesis)

| Script | Output | What it shows |
|---|---|---|
| `cicids_unscoped_rerank_baseline.py` | `results/cicids/<m>/unscoped_rerank_baseline.json` | Ablation: identical rerank scoring without the KG constraint collapses to 0.0 / 0.056 / 0.0 exact match. Offline; uses saved HyDE queries + triples. |
| `cicids_multilabel_check.py` | `results/cicids/<m>/multilabel_check.json` | Set-widening check: scoring against all reachable techniques changes no outcome (15/18, 5/18, 2/18). Offline. |
| `make_quadrant_figure.py` | `My_thesis_document/figures/cicids_correctness_faithfulness.png` | Correctness-vs-faithfulness quadrant figure (Results chapter). |

## Pending — needs the GGUF models (run these, then tell Claude to add the numbers)

| Script | How to run | Purpose |
|---|---|---|
| `darpa_llm_only_baseline.py` | `.venv/bin/pip install llama-cpp-python`, then run once per model key (see docstring) | Symmetric baseline: LLM-only condition on DARPA, so both datasets have both non-grounded baselines. Writes `results/darpa/<m>/llm_only_baseline.json`. |
| `human_eval/` | `generate_annotation_sheet.py`, two raters fill copies of the sheet, `compute_kappa.py r1.csv r2.csv` | Small expert evaluation (54 blinded reports, 3 dimensions, Cohen's Kappa). Rubric in `human_eval/RUBRIC.md`. |

Do not add claims about the pending experiments to the thesis until the
JSON outputs exist — the text currently makes no promises about them.
