# OEA: Structured Recursive Calibration for Generative Stability

Research code, experiments, and publication package for the OEA framework paper.

[![CI](https://github.com/BitConcepts/oea-framework-paper/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/oea-framework-paper/actions/workflows/ci.yml)

Version: v1.0.0 | Code: MIT | Paper: CC BY 4.0

## Paper

Investigates whether recursive generative stability depends more strongly on directional
calibration and epistemic filtering than on unconstrained retrieval augmentation or
generic decoding constraints.

Four experiments: bigram-proxy ablation (12 variants, 7,776 runs), four-model real LLM
validation (distilgpt2, gpt2, gpt-neo-125M, Qwen2.5-1.5B), 30-step recursive memory
drift benchmark, and baseline competition against 5 non-OEA controls.

Manuscript: `arxiv/main.tex` | Build PDF: `scripts\build_pdf.cmd` | [Read on Academia.edu](https://www.academia.edu/167119567/OEA_Structured_Recursive_Calibration_for_Generative_Stability)

## Quick Start

```bash
# 1. Setup environment
bash scripts/setup.sh --experiments      # Linux/macOS
scripts\setup.cmd --experiments           # Windows

# 2. Run all CPU experiments (~2 min)
bash scripts/run_all_experiments.sh

# 3. Run real LLM experiments (GPU recommended)
python experiments/real_lm_experiment.py --model distilgpt2
python experiments/real_lm_experiment.py --model gpt2
python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M
python experiments/real_lm_experiment.py --model Qwen/Qwen2.5-1.5B

# 4. Build manuscript PDF
scripts\build_pdf.cmd
```

## GPU Support

The experiment harness auto-detects CUDA, MPS, or CPU:

```text
Device: cuda (NVIDIA GeForce RTX 4070 SUPER)
Device: mps (Apple Metal)
Device: cpu  [NOTE: no GPU detected]
```

| Hardware | Install command |
|---|---|
| NVIDIA (CUDA 12.1) | `pip install torch --index-url https://download.pytorch.org/whl/cu121` |
| Apple Silicon (MPS) | `pip install torch` |
| CPU only | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |

## Repository Structure

- `arxiv/main.tex` — LaTeX manuscript (arXiv-ready)
- `arxiv/references.bib` — bibliography (13 verified citations)
- `arxiv/figures/` — 3 publication figures (pipeline, calibration, dissociation)
- `experiments/` — all experiment scripts
- `experiments/manifest.json` — SHA-256 hashes for result artifacts
- `results/` — committed experiment artifacts
- `REPRODUCE.md` — full reproduction guide
- `Dockerfile` — containerized reproducible environment
- `docs/` — architecture, requirements, tests, governance
- `LEDGER.md` — session-by-session change log

## Experiment Metrics

Per-iteration measurements across 4 models (82M–1.5B, 3 architecture families):

- **Log-probability** — mean per-token log-prob under frozen reference model (primary)
- **ROUGE-L recall** — seed-corpus content preservation (independent of log-prob)
- **JSD** — Jensen-Shannon divergence from seed distribution
- **TRR / FRR** — true/false rejection rates for OOV token detection

## Reproducibility

All experiments are seeded and reproducible. See `REPRODUCE.md` for exact commands.
Artifact integrity: `python experiments/verify_manifest.py`

## License

Code: MIT | Paper: CC BY 4.0
