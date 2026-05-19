# OEA Framework Paper — Reproducibility Container (REQ-OEA-020)
# CPU-only image. For NVIDIA GPU support, use Dockerfile.cuda.
#
# Hardware test status:
#   This image (CPU):         verified by maintainer
#   Dockerfile.cuda (NVIDIA): verified by maintainer
#   AMD ROCm / Intel XPU:     community-tested only — no Dockerfile provided
#   Report hardware issues:   https://github.com/BitConcepts/oea-framework-paper/issues
#
# Build:
#   docker build -t oea-framework .
#
# Run bigram experiments (CPU, ~2 min, no torch needed):
#   docker run --rm -v $(pwd)/results:/app/results oea-framework
#
# Run real LLM experiment (CPU, slower):
#   docker run --rm -v $(pwd)/results:/app/results oea-framework \
#     python experiments/real_lm_experiment.py --model distilgpt2 \
#     --n-seeds 3 --n-iterations 5 --gen-tokens 40
#
# For NVIDIA GPU runs, use Dockerfile.cuda instead:
#   docker build -f Dockerfile.cuda -t oea-framework-cuda .
#   docker run --rm --gpus all -v $(pwd)/results:/app/results oea-framework-cuda \
#     python experiments/real_lm_experiment.py --model distilgpt2

FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Core experiment dependencies (no GPU required)
RUN pip install --no-cache-dir \
    "numpy==2.4.5" \
    "matplotlib==3.10.9" \
    "scipy==1.17.1" \
    "pytest==9.0.3" \
    "reportlab==4.5.1"

# Neural LLM dependencies — CPU-only torch for portability
RUN pip install --no-cache-dir \
    "torch" \
    "transformers==4.41.0" \
    "rouge-score==0.1.2" \
    --index-url https://download.pytorch.org/whl/cpu

# Verify installation
RUN python -c "import numpy, matplotlib, torch, transformers; print('Environment OK')"

# Default: run all CPU bigram experiments
CMD ["bash", "scripts/run_all_experiments.sh"]
