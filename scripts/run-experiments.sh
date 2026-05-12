#!/usr/bin/env bash
# oea-framework-paper — run experiments (Linux / macOS)
# Usage: bash scripts/run-experiments.sh [--all]
#   --all  also run real LLM experiment (requires --experiments setup, ~3 min)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$PROJECT_ROOT/.venv"
RUN_ALL=false
for arg in "$@"; do [[ "$arg" == "--all" ]] && RUN_ALL=true; done

if [ -d "$VENV" ]; then
    # shellcheck disable=SC1091
    source "$VENV/bin/activate"
fi

cd "$PROJECT_ROOT"

echo "=== [1/3] Pilot experiment (run_experiments.py) ==="
python experiments/run_experiments.py
echo "Pilot done. Results in results/"

echo
echo "=== [2/3] Credibility suite — fast validation (credibility_plan_fast.json) ==="
python - <<'PYEOF'
from experiments.credibility_suite import load_plan, run_suite
from pathlib import Path
plan = load_plan(Path("experiments/config/credibility_plan_fast.json"))
summary = run_suite(plan)
print("Fast credibility suite done.")
PYEOF

echo
if [ "$RUN_ALL" = true ]; then
    echo "=== [3/3] Real LLM experiment (distilgpt2, ~3 min) ==="
    python experiments/real_lm_experiment.py
    echo "Real LLM done. Results in results/real_lm/"
else
    echo "=== [3/3] Real LLM experiment — SKIPPED (pass --all to enable) ==="
fi

echo
echo "All experiments complete."
echo "Results:"
echo "  results/recursive_stability_runs.csv"
echo "  results/epistemic_friction_runs.csv"
echo "  results/summary_metrics.json"
echo "  results/credibility/  (full credibility suite — run manually)"
echo "  results/real_lm/      (real LLM — if --all was used)"
