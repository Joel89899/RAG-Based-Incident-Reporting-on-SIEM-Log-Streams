# Revision scripts

Post-hoc analyses supporting the Results chapter. Each one reads experimental
outputs already produced by the notebooks in `results/` and re-scores them; none
calls a language model, loads GGUF weights, or generates new experimental data.
All three are deterministic and run on CPU in under a minute.

Run from the repo root with the project venv:

```bash
.venv/bin/python revision_scripts/cicids_unscoped_rerank_baseline.py
.venv/bin/python revision_scripts/cicids_multilabel_check.py
.venv/bin/python revision_scripts/make_quadrant_figure.py
```

| Script | Output | Where it appears in the thesis |
|---|---|---|
| `cicids_unscoped_rerank_baseline.py` | `results/cicids/<model>/unscoped_rerank_baseline.json` | Ablation: the notebook's own `scoped_rerank` scoring with the KG candidate restriction removed, i.e. its `grounded == False` fallback forced on for every community. Collapses exact match to 0.0 / 0.056 / 0.0. Reported in Results §6.4, the Conclusions contributions, and the abstract. |
| `cicids_multilabel_check.py` | `results/cicids/<model>/multilabel_check.json` | Set-widening check: scores each community against every technique reachable from any extracted relation rather than the single best guess. Changes no outcome (15/18, 5/18, 2/18), so single-label scoring does not undersell the pipeline. Reported in Results §6.5. |
| `make_quadrant_figure.py` | `My_thesis_document/figures/cicids_correctness_faithfulness.png` | Correctness-versus-faithfulness quadrant, Figure 6.6. |
| `cicids_preference_ablation.py` | `results/cicids/<model>/preference_ablation.json` | Ablation of the reranker's 90% preference-table rule (second-reviewer request). Validates that the recomputed rerank reproduces the pipeline's saved assignments 18/18 per model, then disables the rule: predictions change for 0 (Mistral), 0 (3B), and 1 (coder) communities. Reported in Results §6.4. |

Both analyses are described as part of the evaluation protocol in the Experiment
chapter ("Two further checks complete the CIC-IDS protocol").
