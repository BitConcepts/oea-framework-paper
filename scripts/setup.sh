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
    pip install -r "$PROJECT_ROOT/requirements-experiments.txt" \
        --extra-index-url https://download.pytorch.org/whl/cpu -q
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
