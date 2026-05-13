#!/usr/bin/env bash
# oea-framework-paper — Linux/macOS Setup
#
# Usage:
#   ./setup.sh                    Core dependencies only (numpy, matplotlib, pytest)
#   ./setup.sh --experiments      + CPU torch + transformers + rouge-score
#   ./setup.sh --experiments --cuda   + CUDA 12.1 torch build
#   ./setup.sh --experiments --mps    + Apple Metal (MPS) torch build
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
EXPERIMENTS=0
CUDA=0
MPS=0

for arg in "$@"; do
  case $arg in
    --experiments) EXPERIMENTS=1 ;;
    --cuda)        CUDA=1 ;;
    --mps)         MPS=1 ;;
  esac
done

echo "oea-framework-paper setup (Linux/macOS)"
command -v python3 &>/dev/null || { echo "ERROR: Python 3 not found." >&2; exit 1; }

[ -d "$VENV_DIR" ] || { echo "Creating virtual environment..."; python3 -m venv "$VENV_DIR"; }
source "$VENV_DIR/bin/activate"

echo "Installing core dependencies..."
pip install "numpy==1.26.4" matplotlib scipy pytest specsmith

if [ "$EXPERIMENTS" -eq 1 ]; then
  echo "Installing neural LLM experiment dependencies..."
  if [ "$CUDA" -eq 1 ]; then
    echo "  [CUDA 12.1 build]"
    pip install torch==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121
  elif [ "$MPS" -eq 1 ]; then
    echo "  [Apple Metal (MPS) build]"
    pip install torch==2.3.1
  else
    echo "  [CPU build - use --cuda or --mps for GPU acceleration]"
    pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu
  fi
  pip install transformers==4.41.0 rouge-score==0.1.2
  echo "Neural dependencies installed."
  echo
  echo "Run GPT-Neo validation:"
  echo "  GPU:  python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M"
  echo "  CPU:  python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M \\"
  echo "          --n-seeds 3 --n-iterations 5 --gen-tokens 40"
fi

echo "Setup complete."
