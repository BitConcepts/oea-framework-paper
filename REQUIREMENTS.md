# Requirements

Belief artifact registry for the OEA Framework paper. All REQs correspond to falsifiable
claims or engineering constraints. Each must have a matching TEST-OEA-* entry in TESTS.md.

### REQ-OEA-001
- **Component**: recursive-stability
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Simulation harness using bigram proxy models; results are scope-bounded to this regime
- **Description**: The OEA-constrained pipeline must achieve a stability score ≥40% higher than
  the control baseline across n=10 recursive iterations, measured by Jensen-Shannon divergence.
- **Evidence**: `results/summary_metrics.json` — effect_delta_stability = 0.1206 (12.1% absolute,
  pilot n=30 seeds; KLD control mean 2.66 vs OEA mean 0.29)

### REQ-OEA-002
- **Component**: epistemic-friction
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Synthetic falsehood injection using `not_<token>` proxy; calibration proxy only
- **Description**: The OEA epistemic layer must improve true-rejection rate of synthetic falsehoods
  by ≥20 percentage points vs control, without increasing false-rejection rate beyond +5 pp.
- **Evidence**: `results/summary_metrics.json` — true_reject delta +0.232, false_reject delta −0.112

### REQ-OEA-003
- **Component**: oea-tri-layer
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: medium
- **Boundary**: Protocol applies to simulation harness; production LLM integration is future work
- **Description**: The experiment harness must implement all three OEA layers in correct order:
  Ontological Anchoring → Epistemic Filtering → Agentic Closure, as specified in
  `docs/methodology.md` and `docs/research-agent-spec.md`.
- **Evidence**: `experiments/credibility_suite.py` — variant logic encodes O, E, A independently

### REQ-OEA-004
- **Component**: credibility-suite
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Ablation study covers combinations {O, E, A, OE, OA, EA, oea_full} only
- **Description**: The credibility suite must run full ablation coverage over all 7 OEA variant
  combinations and emit machine-readable CSV + JSON artifacts with 95% confidence intervals
  and Cohen’s d effect sizes for all headline metrics.
- **Evidence**: `experiments/credibility_suite.py` — run_suite() + ci95() + cohen_d()

### REQ-OEA-005
- **Component**: statistical-reporting
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Permutation test n_perm=2000; parametric CIs assume approximate normality
- **Description**: All reported effect sizes must include: (a) mean ± 95% CI, (b) Cohen’s d,
  (c) permutation p-value, and (d) documented failure-case analysis (false-accept vs false-reject).
  No claim enters the manuscript without a backing artifact.
- **Evidence**: `experiments/credibility_suite.py` — permutation_pvalue(), cohen_d(), ci95()

### REQ-OEA-006
- **Component**: submission-guardrail
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: medium
- **Boundary**: Gate applies to external submission only; internal review drafts may circulate
- **Description**: No external submission (arXiv, PhilSci-Archive, OpenReview) may proceed until
  all four locks are satisfied: citation lock, evidence lock, manuscript lock, and distribution lock,
  as defined in `docs/research-agent-spec.md` Section VI.
- **Evidence**: `docs/research-agent-spec.md` Section VI; `distribution/distribution-strategy.md`

