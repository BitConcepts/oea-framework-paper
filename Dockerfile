# OEA Framework Paper — Reproducibility Container (REQ-OEA-020)
# Provides a fully reproducible Python 3.11 environment for all experiments.
#
# Build:
#   docker build -t oea-framework .
#
# Run all experiments (CPU mode):
#   docker run --rm -v $(pwd)/results:/app/results oea-framework \
#     bash scripts/run_all_experiments.sh
#
# GPU mode (NVIDIA):
#   docker run --rm --gpus all -v $(pwd)/results:/app/results oea-framework \
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

# Core experiment dependencies (no GPU)
# numpy==1.26.4 required for torch 2.3.1 ABI compatibility (numpy 2.x breaks torch)
RUN pip install --no-cache-dir \
    "numpy==1.26.4" \
    "matplotlib==3.9.2" \
    "scipy==1.14.1" \
    "pytest==8.3.5"

# Neural LLM dependencies (CPU-only torch for portability)
# For GPU: replace with appropriate CUDA wheel URL
RUN pip install --no-cache-dir \
    "torch==2.3.1" \
    "transformers==4.41.0" \
    "rouge-score==0.1.2" \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Verify installation
RUN python -c "import numpy, matplotlib, torch, transformers; print('Environment OK')"

# Default: run all CPU experiments
CMD ["bash", "scripts/run_all_experiments.sh"]
