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
- **Implementation**: `BM25Retriever` (token-overlap over corpus passages) prepends retrieved
  evidence to generation prompt; K=3 candidates scored by `log G_0(y|x)` under frozen model
- **Metric**: Expected Calibration Error (ECE) + true/false reject rates

### Layer 3: Agentic Closure
Converts accepted claims into testable hypotheses, executes them in a reproducible harness,
and feeds empirical outcomes back into subsequent hypothesis design.
- **Decision DEC-003**: Python simulation harness with fixed seeds for reproducibility (accepted)
- **Decision DEC-004**: Real LLM experiment uses frozen weights as a *necessary-condition* test.
  If OEA log-prob filtering cannot reduce distributional drift in the idealized frozen setting,
  it cannot do so during training. Results establish a lower bound on in-training efficacy.
  (Scope boundary: does not substitute for fine-tuning experiments; see Threats to Validity.)
- **Output contract**: CSV + JSON artifacts per run; config fingerprint required

## Experiment Harness Components

| Component | Path | Role |
|---|---|---|
| Credibility suite | `experiments/credibility_suite.py` | Bigram proxy ablation (12 variants, calibration-quality formula) |
| Run runner | `experiments/run_experiments.py` | Pilot recursive stability + epistemic friction (n=30 seeds) |
| Real LLM harness | `experiments/real_lm_experiment.py` | distilgpt2 + BM25Retriever RAG (necessary-condition test) |
| BM25 retriever | `BM25Retriever` class in `real_lm_experiment.py` | Token-overlap corpus retrieval (OEA Layer 1 RAG) |
| Config plans | `experiments/config/` | JSON plans controlling variant/seed/depth sweep |
| Corpus data | `experiments/data/` | Public domain corpus (Alice, P&P, Moby Dick) for RAG grounding |
| Raw results | `results/` | CSV/JSON experiment artifacts (reproducible, fixed seeds) |
| LaTeX manuscript | `arxiv/main.tex` | Publication scaffold |

## Data Flow

```text
experiments/data/public_domain_corpus.txt
        ↓
  BM25Retriever.from_text()           <- OEA Layer 1: corpus index
        ↓
experiments/real_lm_experiment.py
  control / oea_rag_only / oea_anchored / oea_miscalibrated
        ↓
results/real_lm/{real_lm_runs.csv, real_lm_summary.json}
  -> cq_measurement: suggested _CALIBRATION_QUALITY updates
        ↓
experiments/config/credibility_plan.json
        ↓
credibility_suite.run_suite()         <- calibration-quality formula
        ↓
results/credibility/{raw_runs.csv, aggregate.csv, summary.json}
        ↓
arxiv/main.tex  (pilot table + ablation table + real LLM validation)
        ↓
arXiv / PhilSci-Archive submission
```

## Key Architectural Decisions
- **Simulation harness** (DEC-003): Bigram proxy for recursive LLM degradation; scope-bounded
- **RAG implementation** (DEC-002): `BM25Retriever` — token-overlap, not log-prob proxy (REQ-OEA-010)
- **Frozen-weights scope** (DEC-004): real LLM experiment is a necessary-condition test, not a
  substitute for fine-tuning experiments; establishes mechanism lower bound
- **Calibration-quality formula**: `_CALIBRATION_QUALITY` values updated from real LLM measurement
  after `real_lm_experiment.py` runs (REQ-OEA-012); closes evidence chain
- **Variants**: `control`, `oea_rag_only`, `oea_anchored`, `oea_miscalibrated` + 12 bigram ablations
- **Statistics**: Cohen's d + permutation p-value for treatment-control deltas
- **Reproducibility**: Fixed random seeds; all artifacts machine-readable; pre-registered design

## Primary Language & Tooling
- **Language**: Python 3.x
- **Test framework**: pytest
- **Dependencies**: numpy (see `requirements.txt`)
- **VCS**: GitHub (`main` branch, gitflow strategy)
