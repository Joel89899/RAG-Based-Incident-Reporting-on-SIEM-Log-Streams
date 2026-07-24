"""DARPA symmetric baseline: LLM-only technique assignment, no retrieval, no KG.

Mirrors the CIC-IDS baseline condition on the DARPA data so both datasets have
both non-grounded baselines. For each malicious-dominant community (loaded from
the saved darpa_cadets_run.json), the model receives the alert texts and its
own extracted triples and must name 1-5 ATT&CK technique IDs directly. Scored
per window at parent level, macro-averaged, with a 2,000-resample bootstrap
over windows -- identical to the notebook's scoring.

REQUIRES the GGUF models in models/ and llama-cpp-python:
    .venv/bin/pip install llama-cpp-python
Run one model at a time (12B takes the longest to load):
    .venv/bin/python revision_scripts/darpa_llm_only_baseline.py qwen2.5-3b
    .venv/bin/python revision_scripts/darpa_llm_only_baseline.py qwen2.5-coder-7b
    .venv/bin/python revision_scripts/darpa_llm_only_baseline.py mistral-nemo-12b

Writes results/darpa/<model>/llm_only_baseline.json.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SEED = 42

MODEL_FILES = {
    "mistral-nemo-12b": "Mistral-Nemo-Instruct-2407-Q5_K_M.gguf",
    "qwen2.5-3b": "qwen2.5-3b-instruct-q4_k_m.gguf",
    "qwen2.5-coder-7b": "qwen2.5-coder-7b-instruct-q5_k_m.gguf",
}

GT = {
    "W1": {"T1190", "T1071", "T1105", "T1059", "T1055", "T1222"},
    "W2": {"T1190", "T1071", "T1105", "T1059", "T1055"},
    "W3": {"T1190", "T1071", "T1105", "T1059", "T1070.004", "T1222"},
    "W4": {"T1190", "T1071", "T1105", "T1059", "T1055", "T1222"},
}


def parent(t):
    return t.split(".")[0] if t else t


def parents(ts):
    return {parent(t) for t in ts}


def window_f1(preds_by_window):
    f1s = {}
    for wid, gt in GT.items():
        P = parents(preds_by_window.get(wid, set()))
        G = parents(gt)
        if not P and wid not in preds_by_window:
            continue
        tp = P & G
        prec = len(tp) / len(P) if P else 0.0
        rec = len(tp) / len(G) if G else 0.0
        f1s[wid] = {"precision": prec, "recall": rec,
                    "f1": 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0}
    return f1s


def bootstrap_ci(per_window_f1, n_boot=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    wins = list(per_window_f1.keys())
    boots = []
    for _ in range(n_boot):
        sample = rng.choice(wins, size=len(wins), replace=True)
        boots.append(float(np.mean([per_window_f1[w]["f1"] for w in sample])))
    return [round(float(np.percentile(boots, 2.5)), 4),
            round(float(np.percentile(boots, 97.5)), 4)]


def main():
    model_key = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-3b"
    model_path = ROOT / "models" / MODEL_FILES[model_key]
    run = json.load(open(ROOT / "results/darpa" / model_key / "darpa_cadets_run.json"))
    texts = [a["text"] for a in run["alerts"]]
    communities = run["communities"]
    mal_comms = run["mal_comms"]
    community_triples = run["community_triples"]

    from llama_cpp import Llama
    print(f"Loading {model_path.name} ...")
    llm = Llama(model_path=str(model_path), n_ctx=4096, n_gpu_layers=-1,
                seed=SEED, verbose=False)

    preds_by_window, per_community = {}, []
    for cid in mal_comms:
        info = community_triples[str(cid)]
        win = info["window"]
        alert_block = "\n".join(f"- {texts[j]}" for j in communities[cid][:6])
        triple_block = "\n".join(
            f"- ({t['subject']}, {t['relation']}, {t['target']})" for t in info["triples"])
        prompt = f"""[INST] You are a cybersecurity analyst. Based on the host audit
events and extracted relationships below, identify the MITRE ATT&CK
technique(s) the adversary used. Do not explain.

EVENTS:
{alert_block}

RELATIONSHIPS:
{triple_block}

Reply with exactly this JSON and nothing else:
{{"technique_ids": ["Txxxx", "..."]}}
List 1 to 5 technique IDs, most likely first. [/INST]"""
        out = llm(prompt, max_tokens=128, temperature=0, seed=SEED,
                  repeat_penalty=1.0, stop=["[/INST]"])
        raw = out["choices"][0]["text"]
        ids = re.findall(r"T\d{4}(?:\.\d{3})?", raw)[:5]
        preds_by_window.setdefault(win, set()).update(ids)
        per_community.append({"cid": cid, "window": win, "pred_multi": ids})
        print(f"C{cid} ({win}): {ids}")

    f1s = window_f1(preds_by_window)
    macro = {k: round(float(np.mean([v[k] for v in f1s.values()])), 4)
             for k in ("precision", "recall", "f1")}
    result = {
        "condition": "LLM-only (no retrieval, no KG), parent-level per-window scoring",
        "model_key": model_key,
        "per_window": {w: {k: round(v, 4) for k, v in d.items()} for w, d in f1s.items()},
        "macro": macro,
        "f1_ci95": bootstrap_ci(f1s),
        "per_community": per_community,
    }
    out_path = ROOT / "results/darpa" / model_key / "llm_only_baseline.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"\nmacro: {macro}  CI95: {result['f1_ci95']}\nwrote {out_path}")


if __name__ == "__main__":
    main()
