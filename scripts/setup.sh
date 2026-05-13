#!/usr/bin/env bash
# oea-framework-paper — bootstrap (Linux / macOS)
# Usage: bash scripts/setup.sh [--experiments]
#   --experiments  also install torch + transformers for real_lm_experiment.py
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
WITH_EXPERIMENTS=false
for arg in "$@"; do [[ "$arg" == "--experiments" ]] && WITH_EXPERIMENTS=true; done

echo "oea-framework-paper setup (Linux/macOS)"
python3 --version 2>/dev/null || { echo "ERROR: Python 3 not found." >&2; exit 1; }

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Installing core dependencies (requirements.txt)..."
pip install --upgrade pip -q
pip install -r "$PROJECT_ROOT/requirements.txt" -q

pip install pytest -q

if [ "$WITH_EXPERIMENTS" = true ]; then
    echo "Installing experiment dependencies (requires ~2 GB: torch + transformers)..."
    # Auto-detect GPU type and select the appropriate torch wheel index
    if command -v nvidia-smi &>/dev/null && nvidia-smi &>/dev/null 2>&1; then
        echo "  NVIDIA GPU detected — installing torch with CUDA 12.1 support."
        TORCH_INDEX="https://download.pytorch.org/whl/cu121"
    elif [[ "$(uname)" == "Darwin" ]]; then
        echo "  macOS detected — installing torch with MPS (Apple Metal) support."
        TORCH_INDEX=""  # standard PyPI torch includes MPS
    else
        echo "  No GPU detected — installing CPU-only torch."
        echo "  For GPU support: install CUDA/ROCm drivers, then re-run or see requirements-experiments.txt."
        TORCH_INDEX="https://download.pytorch.org/whl/cpu"
    fi
    if [ -n "$TORCH_INDEX" ]; then
        pip install -r "$PROJECT_ROOT/requirements-experiments.txt" \
            --index-url "$TORCH_INDEX" -q
    else
        pip install -r "$PROJECT_ROOT/requirements-experiments.txt" -q
    fi
    echo "Experiment dependencies installed."
fi

echo
echo "Setup complete. Activate with:"
echo "  source .venv/bin/activate"
echo
echo "Run experiments:"
echo "  bash scripts/run-experiments.sh              # pilot + credibility suite (fast)"
echo "  bash scripts/run-experiments.sh --all        # includes real LLM (~3 min)"
echo "  python experiments/real_lm_experiment.py     # real LLM only (needs --experiments)"
