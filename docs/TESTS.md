# Test Specification

Test specifications for the OEA Framework paper. Each TEST-OEA-\* entry maps to a
corresponding REQ-OEA-\* requirement. Coverage must remain ≥80% to advance phases.

## TEST-OEA-001
- Covers: REQ-OEA-001
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_recursive_stability_oea_vs_control`
- **Status**: Implemented
- **Assertion**: OEA `stability_score` mean ≥ control mean + 0.10 across 30 seeds
- **Evidence**: `results/summary_metrics.json` — effect_delta_stability = 0.1206

## TEST-OEA-002
- Covers: REQ-OEA-002
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_epistemic_friction_true_reject_delta`
- **Status**: Implemented
- **Assertion**: OEA true-reject rate ≥ control + 0.20; false-reject delta ≤ +0.05
- **Evidence**: `results/summary_metrics.json` — true_reject delta +0.232, false_reject delta −0.112

## TEST-OEA-003
- Covers: REQ-OEA-003
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_oea_layer_ordering_ablation`
- **Status**: Implemented
- **Assertion**: Each ablation variant that removes a layer degrades performance vs `oea_full`;
  variant logic in `credibility_suite.py` encodes O, E, A flags independently
- **Evidence**: Ablation results in `results/credibility/credibility_aggregate_metrics.csv`

## TEST-OEA-004
- Covers: REQ-OEA-004
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_credibility_suite_artifacts`
- **Status**: Implemented
- **Assertion**: `run_suite()` emits all 5 artifact files; aggregate CSV contains all 7 variant rows;
  95% CI columns present for stability, true-reject, false-reject metrics
- **Evidence**: `experiments/credibility_suite.py` — write_csv(), run_suite()

## TEST-OEA-005
- Covers: REQ-OEA-005
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_statistical_reporting_contract`
- **Status**: Implemented
- **Assertion**: Cohen’s d, permutation p-value, and 95% CI are present and non-degenerate for
  all headline comparisons; no headline claim emitted without backing artifact
- **Evidence**: `experiments/credibility_suite.py` — cohen_d(), permutation_pvalue(), ci95()

## TEST-OEA-006
- Covers: REQ-OEA-006
- **File**: `docs/research-agent-spec.md`
- **Method**: Manual gate check (Section VI lock verification)
- **Status**: Planned
- **Assertion**: All four locks (citation, evidence, manuscript, distribution) verified before
  any external submission; enforced by agent-level stop condition in `AGENTS.md`
- **Evidence**: `docs/research-agent-spec.md` Section VI; `distribution/distribution-strategy.md`

## TEST-OEA-007
- Covers: REQ-OEA-007
- **File**: `arxiv/main.tex`
- **Method**: Manual review of compiled LaTeX
- **Status**: Implemented
- **Assertion**: `\section{Conclusion}` is present; section contains (a) OEA hypothesis restatement,
  (b) summary of pilot evidence with scope bounds, (c) explicit limitations, (d) next steps.
  No universal claims without cross-regime evidence.
- **Evidence**: `arxiv/main.tex` — Conclusion section added in cycle 2

## TEST-OEA-008
- Covers: REQ-OEA-008
- **File**: `arxiv/main.tex`
- **Method**: Verify table columns against `results/credibility/credibility_aggregate_metrics.csv`
- **Status**: Implemented
- **Assertion**: Table 2 exists with 7 variant rows; columns include stability mean, stability CI95,
  true-reject mean, true-reject CI95, Cohen's d vs oea_full, permutation p-value. All values
  traceable to `results/credibility/` artifacts.
- **Evidence**: `results/credibility/credibility_aggregate_metrics.csv` + `credibility_summary.json`

## TEST-OEA-009
- Covers: REQ-OEA-009
- **File**: `arxiv/references.bib`
- **Method**: Manual verification of each DOI/URL; cross-check author/year against source
- **Status**: Implemented
- **Assertion**: All 8 citations verified: DOI resolves, author list correct, year matches.
  `roumeliotis2025trust` and `fu2025selfverification` explicitly checked and corrected or
  confirmed. No hallucinated entries remain.
- **Evidence**: `arxiv/references.bib` — audit completed in cycle 2

## TEST-OEA-010
- Covers: REQ-OEA-010
- **File**: `experiments/real_lm_experiment.py`
- **Method**: Code inspection + unit test of `BM25Retriever.retrieve()`
- **Status**: Implemented
- **Assertion**: `BM25Retriever.from_text()` splits corpus into passages; `retrieve()` returns
  the passage with highest token-overlap score, not the lowest log-probability candidate.
  `_rag_prompt()` prepends the retrieved passage to the generation context.
- **Evidence**: `BM25Retriever` class + `_rag_prompt()` in `real_lm_experiment.py`

## TEST-OEA-011
- Covers: REQ-OEA-011
- **File**: `arxiv/main.tex`
- **Method**: Manual review of manuscript after `real_lm_experiment.py` completes
- **Status**: Implemented
- **Assertion**: Section \\section{Real LLM Validation} exists in `main.tex` with:
  (a) two-model ablation table (distilgpt2 + gpt2) sourced from committed artifacts, (b) explicit
  frozen-weights scope note as necessary-condition framing, (c) threshold recalibration note,
  (d) vocabulary anchoring interaction finding documented.
- **Evidence**: `arxiv/main.tex` — Table 3 two-model format; artifacts committed to
  `results/real_lm/distilgpt2/` and `results/real_lm/gpt2/`. 10 seeds x 10 iters. UNK-002 resolved.

## TEST-OEA-012
- Covers: REQ-OEA-012
- **File**: `experiments/credibility_suite.py`
- **Method**: Verify `_CALIBRATION_QUALITY` comment references `real_lm_summary.json` measurement
- **Status**: Implemented (with finding)
- **Assertion**: After `real_lm_experiment.py` runs, `_CALIBRATION_QUALITY["oea_full"]` comment
  documents the measured `suggested_cq` value (0.446) and explains the evidence chain finding:
  the dynamic threshold TRR metric does not directly validate bigram-suite CQ because vocabulary
  anchoring shifts the full log-prob distribution. CQ=0.83 retained as principled design estimate.
- **Evidence**: `credibility_suite.py` comment block on `oea_full`; `real_lm_summary.json`
  `cq_measurement` block; UNCERTAINTY-MAP.md entry for CQ evidence chain mismatch.

## TEST-OEA-013
- Covers: REQ-OEA-013
- **File**: `arxiv/main.tex`
- **Method**: Manual review of compiled LaTeX
- **Status**: Implemented
- **Assertion**: An "Operational Definition of OEA Layers" table exists with columns: Layer,
  Computational Meaning, Mechanism, Observable Effect. The section explicitly states "Ontology"
  refers to distributional anchoring and "Agentic" refers to recursive persistence dynamics.
- **Evidence**: `arxiv/main.tex` — Operational Definition subsection

## TEST-OEA-014
- Covers: REQ-OEA-014
- **File**: `arxiv/main.tex`
- **Method**: Manual review; keyword scan for each required non-claim
- **Status**: Implemented
- **Assertion**: A "Scope and Non-Claims" subsection is present and contains all five required
  disclaimers: no AGI claim, no formal symbolic ontology, no true agency, no causal proof,
  no general intelligence improvement.
- **Evidence**: `arxiv/main.tex` — Scope and Non-Claims subsection

## TEST-OEA-015
- Covers: REQ-OEA-015
- **File**: `arxiv/main.tex`
- **Method**: Manual review of compiled LaTeX
- **Status**: Implemented
- **Assertion**: A notation/definitions section exists with symbols table and all seven required
  formal elements: recursive generation equation, anchoring operator, epistemic filter as argmax,
  TRR formula, FRR formula, JSD definition, log-probability optimization target.
- **Evidence**: `arxiv/main.tex` — Notation and Formal Definitions section

## TEST-OEA-016
- Covers: REQ-OEA-016
- **File**: `experiments/baseline_competition.py`
- **Method**: Run `python experiments/baseline_competition.py` and inspect artifacts
- **Status**: Implemented
- **Assertion**: `results/baseline_competition/` contains `baseline_runs.csv` and `baseline_summary.json`;
  CSV includes all five non-OEA control variants; summary includes mean ± CI95 and Cohen's d
  vs `oea_full` for stability, true-reject, and false-reject metrics.
- **Evidence**: `results/baseline_competition/baseline_summary.json`

## TEST-OEA-017
- Covers: REQ-OEA-017
- **File**: `experiments/recursive_memory_drift.py`
- **Method**: Run `python experiments/recursive_memory_drift.py` and inspect artifacts
- **Status**: Implemented
- **Assertion**: `results/memory_drift/` contains `drift_runs.csv` and `drift_summary.json`;
  CSV covers 30 iterations × 2 variants (oea_controlled, uncontrolled) × N_SEEDS seeds;
  summary reports entity_retention, semantic_drift, hallucination_proxy, vocab_collapse
  with mean ± CI95 for both variants at final step.
- **Evidence**: `results/memory_drift/drift_summary.json`

## TEST-OEA-018
- Covers: REQ-OEA-018
- **File**: `arxiv/main.tex`
- **Method**: Manual review of appendix section
- **Status**: Implemented
- **Assertion**: Appendix A: Statistical Methods contains all six required elements:
  permutation test description, CI derivation, seed policy, Cohen's d formula,
  sample-size rationale, multiple-comparison discussion.
- **Evidence**: `arxiv/main.tex` — Appendix A

## TEST-OEA-019
- Covers: REQ-OEA-019
- **File**: `experiments/generate_figures.py`
- **Method**: Run `python experiments/generate_figures.py` and inspect `arxiv/figures/`
- **Status**: Implemented
- **Assertion**: Three PDF files exist: `fig_pipeline.pdf`, `fig_calibration.pdf`,
  `fig_metric_dissociation.pdf`. All three are referenced with `\includegraphics` in `arxiv/main.tex`.
- **Evidence**: `arxiv/figures/` + `arxiv/main.tex`

## TEST-OEA-020
- Covers: REQ-OEA-020
- **File**: `Dockerfile`, `requirements-lock.txt`, `experiments/manifest.json`, `REPRODUCE.md`
- **Method**: Confirm all four files exist and are non-empty; verify manifest hashes match
  committed artifact files
- **Status**: Implemented
- **Assertion**: All four reproducibility artifacts exist. `REPRODUCE.md` documents complete
  reproduction commands. `experiments/manifest.json` contains SHA-256 hashes for all files
  in `results/`.
- **Evidence**: `REPRODUCE.md`, `experiments/manifest.json`

## TEST-OEA-021
- Covers: REQ-OEA-021
- **File**: `arxiv/main.tex`
- **Method**: Manual review of hypotheses section
- **Status**: Implemented
- **Assertion**: A "Core Hypotheses" section lists H1-H4 as stated in REQ-OEA-021.
  A "What Would Falsify OEA" subsection lists at least one disconfirmation criterion for each
  hypothesis. No hypothesis is stated without a corresponding falsification condition.
- **Evidence**: `arxiv/main.tex` — Core Hypotheses and Falsification sections

## TEST-OEA-022
- Covers: REQ-OEA-022
- **File**: `arxiv/main.tex`
- **Method**: Manual review of glossary appendix
- **Status**: Implemented
- **Assertion**: Appendix B: Glossary contains definitions for all ten required terms:
  stability, fidelity, anchoring, calibration, recursive exposure, synthetic contamination,
  epistemic filtering, recursive drift, calibration quality (CQ), TRR/FRR.
- **Evidence**: `arxiv/main.tex` — Appendix B: Glossary
