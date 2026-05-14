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

### REQ-OEA-013
- **Component**: manuscript-operationalization
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Applies to `arxiv/main.tex` methodology section
- **Description**: The manuscript must contain an "Operational Definition of OEA Layers" table
  mapping each layer to: computational meaning, implementation mechanism, and observable effect.
  The section must explicitly state that "Ontology" refers to structured distributional anchoring
  (not formal philosophical ontology) and "Agentic" refers to recursive persistence dynamics
  (not autonomous agency).
- **Evidence**: `arxiv/main.tex` — Operational Definition section

### REQ-OEA-014
- **Component**: manuscript-non-claims
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Applies to `arxiv/main.tex` introduction or dedicated scope section
- **Description**: The manuscript must contain a "Scope and Non-Claims" subsection explicitly
  stating: no claim of AGI, no claim of formal symbolic ontology, no claim of true agency, no
  claim of causal proof, no claim of general intelligence improvement.
- **Evidence**: `arxiv/main.tex` — Scope and Non-Claims subsection

### REQ-OEA-015
- **Component**: manuscript-formalization
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Applies to `arxiv/main.tex` notation section
- **Description**: The manuscript must include a formal notation section with: (a) symbols table,
  (b) recursive generation equation $x_{t+1} \sim P_\theta(x \mid \mathcal{A}(x_t), \mathcal{E}(x_t))$,
  (c) anchoring operator definition, (d) epistemic filter as argmax, (e) TRR/FRR formulas,
  (f) JSD stability metric, (g) log-probability optimization target.
- **Evidence**: `arxiv/main.tex` — Notation and Definitions section

### REQ-OEA-016
- **Component**: baseline-competition
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Bigram proxy harness only; real LLM baselines are future work
- **Description**: `experiments/baseline_competition.py` must compare OEA against at least five
  non-OEA controls: temperature reduction, top-k restriction, entropy-style filtering,
  repetition penalty, and RAG-only reranking. Must emit machine-readable CSV/JSON to
  `results/baseline_competition/` with mean ± CI95 and Cohen's d for the primary metrics.
- **Evidence**: `experiments/baseline_competition.py` + `results/baseline_competition/`

### REQ-OEA-017
- **Component**: agentic-benchmark
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Bigram proxy recursive summarization; full neural agentic tasks are future work
- **Description**: `experiments/recursive_memory_drift.py` must implement a 30-step recursive
  summarization benchmark measuring: (a) entity retention (token-set overlap with initial),
  (b) semantic drift (JSD from initial distribution), (c) hallucination proxy (novel token rate),
  (d) vocabulary collapse (unique token ratio). OEA-controlled and uncontrolled variants must
  be compared. Results written to `results/memory_drift/`.
- **Evidence**: `experiments/recursive_memory_drift.py` + `results/memory_drift/`

### REQ-OEA-018
- **Component**: statistical-appendix
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Appendix in `arxiv/main.tex`
- **Description**: The manuscript appendix must include: (a) exact permutation test methodology
  (two-sided, n_perm=2000), (b) bootstrap CI method, (c) seed policy (torch.manual_seed +
  numpy.random.default_rng), (d) Cohen's d formula, (e) sample-size rationale, and
  (f) multiple-comparison discussion for 12-variant ablation.
- **Evidence**: `arxiv/main.tex` — Appendix A: Statistical Methods

### REQ-OEA-019
- **Component**: figures
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Figures generated from committed result artifacts; no live model inference required
- **Description**: `experiments/generate_figures.py` must produce three publication figures:
  (1) OEA pipeline diagram, (2) calibration trajectory plot (log-prob over 10 iterations for 4
  variants, mean ± CI across 10 seeds), (3) metric dissociation plot (log-prob vs ROUGE-L
  for 4 variants). Figures stored as PDF under `arxiv/figures/` and referenced in `arxiv/main.tex`.
- **Evidence**: `experiments/generate_figures.py` + `arxiv/figures/`

### REQ-OEA-020
- **Component**: reproducibility-package
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Covers the full experiment pipeline; GPU availability required for real LLM runs
- **Description**: The repository must contain: (a) `Dockerfile` reproducing the Python environment,
  (b) `requirements-lock.txt` with pinned versions, (c) `experiments/manifest.json` with SHA-256
  hashes of all result artifacts, (d) `REPRODUCE.md` documenting exact commands and expected
  runtime to reproduce all results from scratch.
- **Evidence**: `Dockerfile`, `requirements-lock.txt`, `experiments/manifest.json`, `REPRODUCE.md`

### REQ-OEA-021
- **Component**: manuscript-hypotheses
- **Priority**: P1
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Applies to `arxiv/main.tex`
- **Description**: The manuscript must contain: (a) a "Core Hypotheses" section listing H1 (correct
  calibration direction improves recursive distributional fidelity), H2 (miscalibration reverses
  discrimination), H3 (RAG without epistemic filtering degrades fidelity), and H4 (OEA-controlled
  recursion resists memory drift better than unconstrained recursion); and (b) a "What Would
  Falsify OEA" subsection specifying the conditions under which each hypothesis would be
  disconfirmed.
- **Evidence**: `arxiv/main.tex` — Core Hypotheses section

### REQ-OEA-022
- **Component**: manuscript-glossary
- **Priority**: P2
- **Status**: Accepted
- **Confidence**: high
- **Boundary**: Appendix in `arxiv/main.tex`
- **Description**: The manuscript must include a glossary defining: stability, fidelity,
  anchoring, calibration, recursive exposure, synthetic contamination, epistemic filtering,
  recursive drift, calibration quality (CQ), and true/false reject rate (TRR/FRR).
- **Evidence**: `arxiv/main.tex` — Appendix B: Glossary
