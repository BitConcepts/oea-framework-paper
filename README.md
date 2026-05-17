# OEA: Structured Recursive Calibration for Generative Stability

[![CI](https://github.com/BitConcepts/oea-framework-paper/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/oea-framework-paper/actions/workflows/ci.yml)
[![Paper](https://img.shields.io/badge/paper-Academia.edu-blue)](https://www.academia.edu/167119567/OEA_Structured_Recursive_Calibration_for_Generative_Stability)
[![License: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](https://github.com/BitConcepts/oea-framework-paper/releases/tag/v1.0.0)

**Author:** Tristen Pierson, BitConcepts Research

## What This Is

An empirical study of whether recursive generative stability depends more on **directional calibration and epistemic filtering** than on retrieval augmentation or generic decoding constraints.

The OEA (Ontology, Epistemic, Agentic) framework is a three-layer generation-time protocol tested across **4 language models** (82M to 1.5B parameters) and **3 architecture families** (GPT-2, GPT-Neo, Qwen). Key result: inverting the calibration signal degrades log-probability by -0.55 to -1.37 nats, while correct calibration improves it by +0.62 to +1.63 nats.

[Read the paper on Academia.edu](https://www.academia.edu/167119567/OEA_Structured_Recursive_Calibration_for_Generative_Stability)

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### 1. Install dependencies

`ash
# Linux/macOS
bash scripts/setup.sh --experiments

# Windows
scripts\setup.cmd --experiments
`

### 2. Run all bigram experiments (~2 min, no GPU)

`ash
bash scripts/run_all_experiments.sh
`

This runs: pilot stability test, credibility suite (7,776 runs), memory drift benchmark, baseline competition, and generates figures.

### 3. Run real LLM experiments (GPU recommended)

`ash
python experiments/real_lm_experiment.py --model distilgpt2
python experiments/real_lm_experiment.py --model gpt2
python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M
python experiments/real_lm_experiment.py --model Qwen/Qwen2.5-1.5B
`

Each model takes ~10-30 min on GPU. CPU is supported with reduced config: add --n-seeds 3 --n-iterations 5 --gen-tokens 40.

### 4. Verify results

`ash
python experiments/verify_manifest.py
`

Checks SHA-256 hashes of all result artifacts against xperiments/manifest.json.

### 5. Build the manuscript PDF (requires LaTeX)

`ash
# Windows
scripts\build_pdf.cmd

# Linux/macOS
cd arxiv && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
`

## GPU Support

The experiment harness auto-detects the best available device:

| Hardware | Install command |
|---|---|
| NVIDIA (CUDA 12.1) | pip install torch --index-url https://download.pytorch.org/whl/cu121 |
| Apple Silicon (MPS) | pip install torch |
| CPU only | pip install torch --index-url https://download.pytorch.org/whl/cpu |

## What's in This Repo

`
arxiv/
  main.tex              LaTeX manuscript (14 pages)
  references.bib        13 verified citations
  figures/              3 publication figures (pipeline, calibration, dissociation)

experiments/
  credibility_suite.py       Bigram-proxy ablation harness (12 variants)
  real_lm_experiment.py      Real LLM recursive stability experiment
  baseline_competition.py    OEA vs 5 non-OEA controls
  recursive_memory_drift.py  30-step recursive memory benchmark
  generate_figures.py        Generates all publication figures
  verify_manifest.py         SHA-256 artifact integrity checker
  manifest.json              Hashes for all committed results
  data/                      Public-domain corpora (literary + scientific)

results/                     Committed experiment artifacts
scripts/                     Setup, build, and run scripts
tests/                       12 unit tests (pytest)
REPRODUCE.md                 Step-by-step reproduction guide
Dockerfile                   Containerized reproducible environment
`

## Experiments

| Experiment | What it tests | Runtime |
|---|---|---|
| Credibility suite | 12-variant ablation, 648 runs each | ~90s (CPU) |
| Real LLM validation | 4 models, 4 variants, 10 seeds x 10 iterations | ~10-30 min/model (GPU) |
| Memory drift | 30-step recursive summarization, 20 seeds | ~5s (CPU) |
| Baseline competition | OEA vs temperature, top-k, entropy, repetition, RAG-only | ~5s (CPU) |

## Metrics

Per-iteration measurements across all models:

- **Log-probability** — mean per-token log-prob under frozen reference model (primary metric)
- **ROUGE-L recall** — seed-corpus content preservation (independent of log-prob; addresses metric circularity)
- **JSD** — Jensen-Shannon divergence from seed distribution
- **TRR / FRR** — true/false rejection rates for out-of-vocabulary token detection

## Docker

`ash
docker build -t oea-framework .
docker run --rm -v C:\Users\trist\Development\BitConcepts\oea-framework-paper/results:/app/results oea-framework
`

## Citation

`ibtex
@misc{pierson2026oea,
  title={OEA: Structured Recursive Calibration for Generative Stability},
  author={Pierson, Tristen},
  year={2026},
  howpublished={\url{https://github.com/BitConcepts/oea-framework-paper}}
}
`

## License

Code: [MIT](LICENSE) | Paper: CC BY 4.0
