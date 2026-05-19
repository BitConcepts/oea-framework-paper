# Reproduction Guide

Reproduce all results from the OEA Framework paper in under 10 minutes
(bigram experiments; real LLM experiments require GPU and ~30 min).

## Prerequisites

- Python 3.11+
- `pip install numpy matplotlib scipy pytest`
- For real LLM experiments: `pip install torch transformers rouge-score`

## Step 1 — Clone and install

```bash
git clone https://github.com/BitConcepts/oea-framework-paper
cd oea-framework-paper
pip install -r requirements-lock.txt
```

## Step 2 — Run bigram proxy experiments (~2 min, no GPU)

```bash
# Pilot recursive stability + epistemic friction
python experiments/run_experiments.py

# Full credibility suite (12 variants, 648 runs each)
python experiments/credibility_suite.py

# Recursive memory drift benchmark (REQ-OEA-017)
python experiments/recursive_memory_drift.py

# Baseline competition (REQ-OEA-016)
python experiments/baseline_competition.py
```

## Step 3 — Generate figures (~10 sec, no GPU)

```bash
python experiments/generate_figures.py
# Outputs: arxiv/figures/{fig_pipeline.pdf, fig_calibration.pdf, fig_metric_dissociation.pdf}
```

## Step 4 — Install neural LLM dependencies

```bash
# Windows (GPU with CUDA 12.1):
scripts\setup.cmd --experiments --cuda

# Windows (CPU only):
scripts\setup.cmd --experiments

# Linux/macOS (GPU with CUDA 12.1):
bash scripts/setup.sh --experiments --cuda

# Linux/macOS (Apple Metal):
bash scripts/setup.sh --experiments --mps

# Linux/macOS (CPU only):
bash scripts/setup.sh --experiments
```

> **numpy compatibility note**: torch 2.3.1 requires numpy<2. The setup scripts
> install `numpy==1.26.4` automatically. If you manage dependencies manually:
> `pip install "numpy==1.26.4"`

## Step 5 — Run real LLM experiments

```bash
# GPU (full config, ~20-30 min per model):
python experiments/real_lm_experiment.py --model distilgpt2
python experiments/real_lm_experiment.py --model gpt2
python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M
python experiments/real_lm_experiment.py --model Qwen/Qwen2.5-1.5B

# CPU (reduced config, ~15-25 min per model):
python experiments/real_lm_experiment.py --model distilgpt2 --n-seeds 3 --n-iterations 5 --gen-tokens 40
python experiments/real_lm_experiment.py --model gpt2 --n-seeds 3 --n-iterations 5 --gen-tokens 40
python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M --n-seeds 3 --n-iterations 5 --gen-tokens 40
python experiments/real_lm_experiment.py --model Qwen/Qwen2.5-1.5B --n-seeds 3 --n-iterations 5 --gen-tokens 40
```

> CPU results (reduced config) are valid for mechanism verification but have
> wider confidence intervals than the full GPU config. Annotate in manuscript
> with `(CPU, n_seeds=3, n_iter=5)` to distinguish from full runs.

## Step 6 — Verify artifact integrity

```bash
python experiments/verify_manifest.py
# Compares SHA-256 hashes against experiments/manifest.json
```

## Step 7 — Run tests

```bash
pytest tests/
# Expected: 12 tests passing
```

## Docker (fully reproducible environment)

```bash
docker build -t oea-framework .
docker run --rm -v $(pwd)/results:/app/results oea-framework
```

## Expected outputs

| Experiment | Runtime | Output |
|---|---|---|
| Bigram pilot (run_experiments.py) | ~5s | `results/summary_metrics.json` |
| Credibility suite | ~90s | `results/credibility/` |
| Memory drift | ~5s | `results/memory_drift/` |
| Baseline competition | ~5s | `results/baseline_competition/` |
| Figure generation | ~5s | `arxiv/figures/` |
| Real LLM (distilgpt2, GPU) | ~20 min | `results/real_lm/distilgpt2/` |
| Real LLM (gpt2, GPU) | ~25 min | `results/real_lm/gpt2/` |
| Real LLM (gpt-neo-125M, GPU) | ~25 min | `results/real_lm/EleutherAI/gpt-neo-125M/` |
| Real LLM (Qwen2.5-1.5B, GPU) | ~27 min | `results/real_lm/Qwen/Qwen2.5-1.5B/` |
| Real LLM (any model, CPU reduced) | ~15-25 min | same paths, `n_seeds=3 n_iter=5` |

## Seed policy

All experiments use fixed random seeds. Per-experiment seed parameters:
Bigram experiments: `random.Random(seed_idx)` and `numpy.random.default_rng(seed)`.
Real LLM: `torch.manual_seed(gen_seed)`, where `gen_seed = seed_idx * 1000 + iteration * 10`.

## Hardware notes

All bigram experiments run on CPU (no GPU required).
Full GPU real LLM experiments conducted on: NVIDIA RTX 4070 SUPER, CUDA 12.1, Windows 11.
CPU validation (reduced config: `--n-seeds 3 --n-iterations 5 --gen-tokens 40`) is supported
and produces valid directional results. Use CPU results only for mechanism verification;
report full GPU results in the manuscript for statistical power.

### Hardware test matrix

| Hardware | Status | Notes |
|---|---|---|
| CPU (x86-64, AMD or Intel) | ✅ Verified | All platforms |
| NVIDIA CUDA 12.1 | ✅ Verified | RTX 4070 SUPER, Windows 11 |
| NVIDIA CUDA 12.4+ | ✅ Verified | Newer drivers / GPUs |
| AMD ROCm 6.x | ⚠️ Community-tested | Use `--device rocm` |
| Intel Arc / Xe XPU | ⚠️ Community-tested | Use `--device xpu` |
| Apple Silicon MPS | ⚠️ Community-tested | Auto-detected on macOS 13+ |

> **CI:** GPU paths are not CI-tested. GitHub-hosted runners have no GPU hardware.
> Only CPU-based unit tests run automatically on every push.

### Untested hardware — help wanted

If you run the real LLM experiments on AMD ROCm, Intel XPU, or Apple MPS,
please report your result (success or failure) using the
[Hardware Compatibility issue template](https://github.com/BitConcepts/oea-framework-paper/issues/new?template=hardware_compat.md).
Include your GPU model, driver/ROCm/CUDA version, OS, and PyTorch version.

## Compute budget

| Experiment | GPU-hours | CPU-hours (reduced) |
|---|---|---|
| distilgpt2 (82M) | ~0.3 | ~0.4 |
| gpt2 (124M) | ~0.4 | ~0.5 |
| gpt-neo-125M (non-GPT2) | ~0.4 | ~0.5 |
| Qwen2.5-1.5B (modern 2024) | ~0.45 | ~0.6 |
| All bigram experiments | 0.0 (CPU) | 0.0 (CPU) |
