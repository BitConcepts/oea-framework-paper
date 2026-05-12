# Architecture — oea-framework-paper

## Project Purpose
Empirically validate the OEA (Ontology, Epistemic, Agentic) Framework as a guardrail against
model collapse in recursive agentic systems. Produce an arXiv/PhilSci-Archive submission.

## OEA Tri-Layer Architecture

### Layer 1: Ontological Anchoring
Constrains agent output to first principles before inference begins. Defines jurisdiction,
invalid output classes, and boundary conditions that trigger abstention or escalation.
- **Decision DEC-001**: Ontological layer applied before any content synthesis (accepted)
- **Boundary**: Domain axioms are immutable across experiment runs

### Layer 2: Epistemic Filtering
Applies retrieval-grounded falsification to generated claims. Tracks provenance, quantifies
confidence-quality alignment (ECE), and discards unsupported statements.
- **Decision DEC-002**: RAG-grounded corpus used for claim validation (accepted)
- **Metric**: Expected Calibration Error (ECE) + true/false reject rates

### Layer 3: Agentic Closure
Converts accepted claims into testable hypotheses, executes them in a reproducible harness,
and feeds empirical outcomes back into subsequent hypothesis design.
- **Decision DEC-003**: Python simulation harness with fixed seeds for reproducibility (accepted)
- **Output contract**: CSV + JSON artifacts per run; config fingerprint required

## Experiment Harness Components

| Component | Path | Role |
|---|---|---|
| Credibility suite | `experiments/credibility_suite.py` | Bigram model stability + epistemic friction |
| Run runner | `experiments/run_experiments.py` | Orchestrates experiment plans |
| Config plans | `experiments/config/` | JSON plans controlling variant/seed/depth sweep |
| Corpus data | `experiments/data/` | Public domain corpus for RAG grounding |
| Raw results | `results/` | CSV/JSON experiment artifacts |
| LaTeX manuscript | `arxiv/main.tex` | Publication scaffold |

## Data Flow

```text
experiments/config/*.json
        ↓
credibility_suite.run_suite()
        ↓
results/credibility/{raw_runs.csv, aggregate.csv, summary.json, insights.txt}
        ↓
arxiv/main.tex  (tables + figures imported)
        ↓
PhilSci-Archive / arXiv submission
```

## Key Architectural Decisions
- **Simulation harness**: Bigram model used as proxy for recursive LLM degradation (scope-bounded)
- **Variants**: `control_replace`, `control_accumulate`, ablations (O, E, A, OE, OA, EA), `oea_full`
- **Statistics**: Cohen's d + permutation p-value for treatment-control deltas
- **Reproducibility**: Fixed random seeds; all artifacts are machine-readable

## Primary Language & Tooling
- **Language**: Python 3.x
- **Test framework**: pytest
- **Dependencies**: numpy (see `requirements.txt`)
- **VCS**: GitHub (`main` branch, gitflow strategy)
