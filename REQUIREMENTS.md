# Requirements

Belief artifact registry for the OEA Framework paper. All REQs correspond to falsifiable
claims or engineering constraints. Each must have a matching TEST-OEA-\* entry in TESTS.md.

## Belief Artifacts

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
  Ontological Anchoring → Epistemic Filtering → Recursive Feedback, as specified in
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

### REQ-OEA-007
- **Component**: manuscript
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Applies to `arxiv/main.tex`; does not constrain supplementary materials
- **Description**: The manuscript must contain a Conclusion section that (a) restates the OEA
  hypothesis, (b) summarises the pilot evidence with explicit scope bounds, (c) honestly
  states limitations, and (d) identifies next steps for production-harness validation.
- **Evidence**: `arxiv/main.tex` — currently has no \\section{Conclusion}; must be added

### REQ-OEA-008
- **Component**: manuscript
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Ablation table covers the 7 variants run by `credibility_suite.py`; no external benchmarks
- **Description**: The manuscript must include a full ablation results table showing all 7 OEA
  variant combinations with stability mean ± CI95, true-reject mean ± CI95, Cohen’s d vs
  `oea_full`, and permutation p-value. Table must be sourced from `results/credibility/`.
- **Evidence**: `experiments/credibility_suite.py` — run_suite() emits aggregate CSV with all stats

### REQ-OEA-009
- **Component**: citation-audit
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: medium
- **Boundary**: Audit covers `arxiv/references.bib` only; gray literature outside scope
- **Description**: All 8 citations in `references.bib` must be verified: correct DOI/URL resolves,
  author list and year match the actual publication, no placeholder or hallucinated entries.
  Any unresolvable reference must be flagged and either corrected or removed before citation lock.
- **Evidence**: `arxiv/references.bib` — `roumeliotis2025trust` (arXiv:2507.10571) and
  `fu2025selfverification` (NeurIPS 2025 OpenReview) require verification

### REQ-OEA-010
- **Component**: real-lm-rag
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Covers `real_lm_experiment.py` only; bigram suite uses calibration-quality formula
- **Description**: The real LLM experiment RAG component must use actual corpus-grounded
  token-overlap retrieval (`BM25Retriever`), not log-probability as a retrieval proxy.
  Retrieval must index the seed corpus into passage-level units and prepend the highest-scoring
  passage to the generation prompt before each epistemic filter step.
- **Evidence**: `experiments/real_lm_experiment.py` — `BM25Retriever.from_text()` + `_rag_prompt()`

### REQ-OEA-011
- **Component**: manuscript
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: medium
- **Boundary**: Results section pending run completion; methodology pre-registered
- **Description**: A "Real LLM Validation" section must appear in `arxiv/main.tex` covering:
  (a) experimental design with BM25 RAG and 4-variant ablation, (b) frozen-weights scope as
  explicit necessary-condition framing, (c) actual results from `results/real_lm/` once run,
  (d) updated CQ values for `_CALIBRATION_QUALITY` sourced from `real_lm_summary.json`.
- **Evidence**: `arxiv/main.tex` — section skeleton added; results pending

### REQ-OEA-012
- **Component**: calibration-chain
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: medium
- **Boundary**: Applies to `_CALIBRATION_QUALITY` dict in `credibility_suite.py`
- **Description**: `_CALIBRATION_QUALITY["oea_full"]` (and optionally `oea_rag_only`) must be
  updated from the measured `true_reject_rate` output of `real_lm_experiment.py` before
  submission. The `cq_measurement` block in `real_lm_summary.json` provides the formula.
  This closes the evidence chain: real log-probs → measured TRR → CQ → suite parameters.
- **Evidence**: `experiments/real_lm_experiment.py` — CQ Measurement output in `main()`
