#!/usr/bin/env bash
# OEA Framework Paper — Run All CPU Experiments
# Referenced by Dockerfile and REPRODUCE.md.
#
# Usage:
#   bash scripts/run_all_experiments.sh
#
# All experiments here run on CPU (no GPU required).
# For real LLM experiments, run separately:
#   python experiments/real_lm_experiment.py --model distilgpt2
set -euo pipefail

echo "=== OEA Framework: Running all CPU experiments ==="

echo ""
echo "[1/5] Pilot recursive stability + epistemic friction..."
python experiments/run_experiments.py

echo ""
echo "[2/5] Credibility suite (12 variants, 648 runs each)..."
python experiments/credibility_suite.py

echo ""
echo "[3/5] Recursive memory drift benchmark..."
python experiments/recursive_memory_drift.py

echo ""
echo "[4/5] Baseline competition..."
python experiments/baseline_competition.py

echo ""
echo "[5/5] Generating figures..."
python experiments/generate_figures.py

echo ""
echo "=== All CPU experiments complete ==="
echo "Results in: results/"
echo "Figures in: arxiv/figures/"
echo ""
echo "To verify artifact integrity:"
echo "  python experiments/verify_manifest.py"
echo ""
echo "For real LLM experiments (requires torch + transformers):"
echo "  python experiments/real_lm_experiment.py --model distilgpt2"
echo "  python experiments/real_lm_experiment.py --model gpt2"
echo "  python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M"
