---
name: Hardware Compatibility Report
about: Report a success or failure running real_lm_experiment.py on specific hardware (GPU/CPU). Especially useful for ROCm, Intel XPU, and other untested backends.
title: "hw: [hardware] [pass/fail] — <model>"
labels: hardware-compat
---

## Hardware

- **GPU / CPU**: <!-- e.g. AMD RX 7900 XTX, Intel Arc A770, NVIDIA RTX 4080, Apple M3 Max -->
- **Backend**: <!-- cuda / rocm / xpu / mps / cpu -->
- **Driver / ROCm / CUDA version**: <!-- e.g. ROCm 6.3, CUDA 12.4, Metal 3 -->
- **OS**: <!-- e.g. Ubuntu 24.04, Windows 11, macOS 15 -->
- **Python version**:
- **PyTorch version** (`python -c "import torch; print(torch.__version__)"`):

## Install command used

```bash
# Paste the pip install command you used for torch
```

## Result

- [ ] All 4 models ran successfully
- [ ] Partial — some models failed (describe below)
- [ ] Complete failure

## Models tested

<!-- Check all that ran to completion -->

- [ ] distilgpt2 (82M)
- [ ] gpt2 (124M)
- [ ] EleutherAI/gpt-neo-125M
- [ ] Qwen/Qwen2.5-1.5B

## Command used

```bash
python experiments/real_lm_experiment.py --model distilgpt2
# or with --device override:
python experiments/real_lm_experiment.py --model distilgpt2 --device rocm
```

## Error output (if failed)

```
# Paste traceback or error output here
```

## Additional context

<!-- Anything else that might help: memory size, driver quirks, workarounds found -->
