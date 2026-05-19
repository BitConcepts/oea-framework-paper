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

Prerequisites: Python 3.11+ and pip.

```bash
pip install -r requirements-lock.txt
```

Run all bigram experiments (about 2 minutes, no GPU needed):

```bash
bash scripts/run_all_experiments.sh
```

Run real LLM experiments (GPU recommended, 10-30 min per model):

```bash
python experiments/real_lm_experiment.py --model distilgpt2
python experiments/real_lm_experiment.py --model gpt2
python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M
python experiments/real_lm_experiment.py --model Qwen/Qwen2.5-1.5B
```

CPU is supported with reduced config: add `--n-seeds 3 --n-iterations 5 --gen-tokens 40`.

Verify result integrity:

```bash
python experiments/verify_manifest.py
```

Build the manuscript PDF (requires MiKTeX or TeX Live):

```bash
scripts/build_pdf.cmd
```

See [REPRODUCE.md](REPRODUCE.md) for the full step-by-step guide.

## GPU Support

The experiment harness auto-detects the best available device (`cuda > rocm > xpu > mps > cpu`).
Use `--device <backend>` to override.

| Hardware | Install command | Test status |
|---|---|---|
| NVIDIA CUDA 12.1 | `pip install torch==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121` | ✅ Verified (RTX 4070 SUPER, Win 11) |
| NVIDIA CUDA 12.4+ | `pip install torch --index-url https://download.pytorch.org/whl/cu124` | ✅ Verified |
| CPU only | `pip install torch --index-url https://download.pytorch.org/whl/cpu` | ✅ Verified |
| AMD ROCm 6.x | `pip install torch --index-url https://download.pytorch.org/whl/rocm6.3` | ⚠️ Community-tested |
| Intel Arc / Xe XPU | `pip install torch --index-url https://download.pytorch.org/whl/xpu` | ⚠️ Community-tested |
| Apple Silicon (MPS) | `pip install torch` (macOS 13+, auto-detected) | ⚠️ Community-tested |

> **CI note:** GPU paths are not tested in CI — GitHub-hosted runners have no GPU hardware.
> Only CPU-based unit tests and the LaTeX compile run automatically.
> If you run on ROCm, XPU, or MPS, please report your result (pass or fail) using
> the [Hardware Compatibility template](https://github.com/BitConcepts/oea-framework-paper/issues/new?template=hardware_compat.md).

### Docker

| Image | GPU | Build command |
|---|---|---|
| `Dockerfile` | CPU only | `docker build -t oea-framework .` |
| `Dockerfile.cuda` | NVIDIA CUDA 12.1 | `docker build -f Dockerfile.cuda -t oea-framework-cuda .` |

For AMD ROCm or Intel XPU Docker, see `requirements-lock.txt` for install commands
and open a [Hardware Compatibility issue](https://github.com/BitConcepts/oea-framework-paper/issues/new?template=hardware_compat.md) with your result.

## Repository Structure

```text
arxiv/
  main.tex              LaTeX manuscript (14 pages)
  references.bib        13 verified citations
  figures/              3 publication figures

experiments/
  credibility_suite.py       Bigram-proxy ablation harness (12 variants)
  real_lm_experiment.py      Real LLM recursive stability experiment
  baseline_competition.py    OEA vs 5 non-OEA controls
  recursive_memory_drift.py  30-step recursive memory benchmark
  generate_figures.py        Generates all publication figures
  verify_manifest.py         SHA-256 artifact integrity checker
  manifest.json              Hashes for all committed results
  data/                      Public-domain corpora

results/                     Committed experiment artifacts
scripts/                     Setup, build, and run scripts
tests/                       12 unit tests (pytest)
REPRODUCE.md                 Step-by-step reproduction guide
Dockerfile                   CPU reproducibility container
Dockerfile.cuda              NVIDIA CUDA GPU container
```

## Experiments

| Experiment | What it tests | Runtime |
|---|---|---|
| Credibility suite | 12-variant ablation, 648 runs each | ~90s (CPU) |
| Real LLM validation | 4 models, 4 variants, 10 seeds x 10 iterations | ~10-30 min/model (GPU) |
| Memory drift | 30-step recursive summarization, 20 seeds | ~5s (CPU) |
| Baseline competition | OEA vs temperature, top-k, entropy, repetition, RAG-only | ~5s (CPU) |

## Metrics

- **Log-probability** — mean per-token log-prob under frozen reference model (primary metric)
- **ROUGE-L recall** — seed-corpus content preservation (independent of log-prob)
- **JSD** — Jensen-Shannon divergence from seed distribution
- **TRR / FRR** — true/false rejection rates for out-of-vocabulary token detection

## Citation

```bibtex
@misc{pierson2026oea,
  title={OEA: Structured Recursive Calibration for Generative Stability},
  author={Pierson, Tristen},
  year={2026},
  howpublished={https://github.com/BitConcepts/oea-framework-paper}
}
```

## License

Code: [MIT](LICENSE) | Paper: CC BY 4.0
