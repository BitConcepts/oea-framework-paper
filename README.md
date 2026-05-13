# Beyond Stochasticism: The OEA Framework

Research design, experimental protocol, and publication package for:
**"Beyond Stochasticism: An Ontological Framework for Agentic Stability."**

Version: v0.4.0 | Status: Submission-ready (Gates A–D closed) | CI: ![CI](https://github.com/BitConcepts/oea-framework-paper/actions/workflows/ci.yml/badge.svg)

## Project Goal

Empirically validate the OEA (Ontology, Epistemic, Agentic) framework as a measurable guardrail against recursive distributional drift in generative pipelines.
Target venues: arXiv cs.AI + cs.CL (primary), PhilSci-Archive.

## Quick Start

```bash
# 1. Bootstrap environment (auto-detects NVIDIA GPU via nvidia-smi)
bash scripts/setup.sh --experiments      # Linux/macOS
scripts\setup.cmd --experiments           # Windows

# 2. Run bigram credibility suite (~2 min)
python experiments/credibility_suite.py

# 3. Run real LLM experiments (GPU recommended)
python experiments/real_lm_experiment.py --model distilgpt2
python experiments/real_lm_experiment.py --model gpt2

# Results written to results/credibility/ and results/real_lm/{model}/
```

## GPU Support

The real LLM experiment (`real_lm_experiment.py`) auto-detects the best available device at startup:

```
Device: cuda (NVIDIA GeForce RTX 4070 SUPER)   # NVIDIA via CUDA
Device: mps (Apple Metal)                       # Apple Silicon
Device: cpu  [NOTE: no GPU detected — ...]      # CPU fallback with install hint
```

Install PyTorch for your hardware (pick one):

| Hardware | Install command |
|---|---|
| NVIDIA RTX 4070 SUPER / 3000–5000 series (CUDA 12.1) | `pip install torch --index-url https://download.pytorch.org/whl/cu121` |
| NVIDIA older cards (CUDA 11.8) | `pip install torch --index-url https://download.pytorch.org/whl/cu118` |
| AMD GPU (ROCm 6.x) | `pip install torch --index-url https://download.pytorch.org/whl/rocm6.1` |
| Apple Silicon (MPS) | `pip install torch` (standard PyPI) |
| CPU only | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |

The setup scripts (`setup.sh --experiments`, `setup.cmd --experiments`) auto-select the CUDA 12.1
wheel when `nvidia-smi` is detected, and fall back to CPU otherwise.

## Repository Structure

- `arxiv/main.tex` — LaTeX manuscript (compiles via CI, arXiv-ready)
- `arxiv/references.bib` — 13/13 citations verified
- `experiments/real_lm_experiment.py` — Two-model real LLM validation (GPU-accelerated)
- `experiments/credibility_suite.py` — Bigram-proxy ablation harness (12 variants)
- `experiments/config/credibility_plan.json` — Reproducible experiment plan
- `experiments/data/` — Public-domain corpora (literary + scientific)
- `results/real_lm/` — Committed experiment artifacts (distilgpt2, gpt2)
- `results/credibility/` — Committed bigram suite artifacts
- `docs/` — Architecture, requirements, tests, governance
- `LEDGER.md` — Change log (every session logged)
- `AGENTS.md` — Agent governance hub

## Experiment Metrics

The real LLM experiment measures per-iteration:
- **Log-probability** — mean per-token log-prob under original frozen model (primary quality metric)
- **ROUGE-L recall** — fraction of seed-corpus content preserved; *independent* of log-prob selection
  criterion (addresses metric-circularity concerns)
- **JSD** — JS divergence from seed token distribution (diversity proxy, not quality metric)
- **TRR / FRR** — true/false rejection rates for OOV token detection

## Core References

- Shumailov et al., 2024 — model collapse empirical evidence
- Fu et al., 2025 — theoretical collapse framing
- Gerstgrasser et al., 2024 — mitigation regimes
- Lewis et al., 2020 — RAG architecture
- Drayson et al., 2025 — detection-based collapse prevention
- Abbasi Yadkori et al., 2024 — epistemic vs aleatoric UQ in LLMs
- Full citation list: `arxiv/references.bib` (13/13 verified)

## Governance

This project uses specsmith 0.10.1 (`aee-research` type). All agent sessions are logged
in `LEDGER.md`. No claim enters the manuscript without an evidence lock and experiment
artifact backing it (see `AGENTS.md` for protocol rules).
