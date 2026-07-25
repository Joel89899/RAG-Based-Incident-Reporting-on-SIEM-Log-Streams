---
name: run-siem-rag-thesis
description: Build, run, and verify the SIEM RAG thesis repo — compile the thesis PDF (latexmk), run the offline analyses behind its figures and tables, regenerate the quadrant figure, and screenshot a PDF page. Use when asked to build/compile the thesis, run the analyses, regenerate figures, or check the document compiles. NOT for the full LLM pipeline (that needs a GPU + GGUF weights).
---

# Run: SIEM RAG thesis

This repo produces a master's thesis (`My_thesis_document/`, LaTeX → PDF) plus
the Python analyses behind its figures and tables (`revision_scripts/`, reading
saved outputs in `results/`). The deployable artifact is the **PDF**; the
analyses are how its numbers are reproduced.

The primary agent path is one script: **`.claude/skills/run-siem-rag-thesis/driver.sh`**,
run from the repo root. It builds the PDF, runs the offline analyses,
regenerates the figure, and renders a page to PNG. It is fully headless — **no
GPU, no GGUF model weights, no `llama-cpp`**. All paths below are relative to
the repo root.

The three-model LLM pipeline (the `notebook_CIC-IDS/` and `notebook_DARPA/`
Jupyter notebooks that produced `results/`) is a separate GPU path — it needs
`llama-cpp-python`, the GGUF weights in `models/`, and ~4 GB VRAM, and does not
run in a headless container. The driver does not touch it; it consumes the
already-saved `results/`.

## Prerequisites

TeX toolchain and Poppler (for the PNG visual check):

```bash
sudo apt-get install -y texlive-full latexmk poppler-utils
```

Python venv for the analyses (CPU-only Torch is enough — the analyses embed with
all-MiniLM-L6-v2, no LLM):

```bash
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install sentence-transformers matplotlib pandas numpy
```

Verify the stack is importable:

```bash
.venv/bin/python -c "import sentence_transformers, matplotlib, pandas, numpy; print('offline stack OK')"
```

## Run (agent path)

Everything, from the repo root:

```bash
.claude/skills/run-siem-rag-thesis/driver.sh all
```

Or a single stage — `build`, `analyses`, `figure`, or `verify`:

```bash
.claude/skills/run-siem-rag-thesis/driver.sh build
```

`build` fails loudly if there are any undefined references or the page count
drops below 100 (either signals a broken build). A clean build takes ~18s and
prints, verified this session:

```
PDF: .../My_thesis_document/main.pdf | pages=112 | undefined-refs=0
```

`analyses` reproduces the ablation and set-widening numbers from the Results
chapter (reads `results/`, writes JSON back there):

```
mistral-nemo-12b: exact=0.0 parent=0.0 macro=0.0
qwen2.5-3b: exact=0.0556 parent=0.0556 macro=0.0179
qwen2.5-coder-7b: exact=0.0 parent=0.0 macro=0.0
```

`verify` renders page 79 (the correctness-vs-faithfulness figure) to
`/tmp/thesis_verify/page-079.png`. **Open it and look** — a blank or
error page means the build is broken even if `build` passed. Override the
output dir with `THESIS_VERIFY_DIR`.

## Force a clean rebuild

latexmk caches aggressively and will report "up-to-date" after edits that only
touch `\input` files it tracks indirectly. To force a full rebuild:

```bash
cd My_thesis_document && latexmk -C && latexmk -pdf -interaction=nonstopmode main.tex
```

## Pending GPU-only experiments (do not run headless)

`revision_scripts/` also holds two scripts the driver deliberately skips because
they need the GGUF weights or a second human:

- `darpa_llm_only_baseline.py` — needs `.venv/bin/pip install llama-cpp-python`
  and the `models/*.gguf` weights; run once per model key.
- `human_eval/` — generates a blinded annotation sheet; scoring needs two raters.

See `revision_scripts/README.md`. Do not add their numbers to the thesis until
their JSON outputs exist.

## Gotchas

- **`My_thesis_document/` is its own nested git repo** (separate from the outer
  repo) and a commit hook auto-commits edits there as "Thesis revisions" — so
  `git status` in that directory can read clean right after you edit files.
  Don't take that as "nothing changed."
- **`llama-cpp` is intentionally absent** in the headless container. If you try
  to run the notebooks or `darpa_llm_only_baseline.py` you get
  `ModuleNotFoundError: No module named 'llama_cpp'`. That is expected; those
  are the GPU path.
- **`srhthesis.cls` is a local class file** in `My_thesis_document/`, not a
  texlive package. Build from inside that directory (the driver `cd`s there) or
  `kpsewhich` won't find it.
- **`bib/ludography.bib` still contains the Lincoln template's Atari entries**
  (Breakout, Space Invaders). Nothing cites them so they don't render in the
  PDF, but `\printLudography` in `main.tex` still runs. Harmless; ignore.
- The build emits ~9 `Overfull \hbox` warnings from the verbatim prompt blocks
  in the appendix. Cosmetic, not errors.

## Troubleshooting

- `latexmk: command not found` → install `texlive-full latexmk` (Prerequisites).
- `pdftoppm: command not found` → install `poppler-utils`.
- Analyses raise `ModuleNotFoundError: sentence_transformers` → the venv isn't
  set up; run the Python install lines in Prerequisites.
- `build` fails with a nonzero exit → `tail -20 /tmp/thesis_verify/build.log`
  (or `$THESIS_VERIFY_DIR/build.log`) for the LaTeX error.
