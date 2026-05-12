# Test Specification

Test specifications for the OEA Framework paper. Each TEST-OEA-\* entry maps to a
corresponding REQ-OEA-\* requirement. Coverage must remain ≥80% to advance phases.

## TEST-OEA-001
- **REQ**: REQ-OEA-001 (recursive stability)
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_recursive_stability_oea_vs_control`
- **Status**: Implemented
- **Assertion**: OEA `stability_score` mean ≥ control mean + 0.10 across 30 seeds
- **Evidence**: `results/summary_metrics.json` — effect_delta_stability = 0.1206

## TEST-OEA-002
- **REQ**: REQ-OEA-002 (epistemic friction)
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_epistemic_friction_true_reject_delta`
- **Status**: Implemented
- **Assertion**: OEA true-reject rate ≥ control + 0.20; false-reject delta ≤ +0.05
- **Evidence**: `results/summary_metrics.json` — true_reject delta +0.232, false_reject delta −0.112

## TEST-OEA-003
- **REQ**: REQ-OEA-003 (OEA tri-layer)
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_oea_layer_ordering_ablation`
- **Status**: Implemented
- **Assertion**: Each ablation variant that removes a layer degrades performance vs `oea_full`;
  variant logic in `credibility_suite.py` encodes O, E, A flags independently
- **Evidence**: Ablation results in `results/credibility/credibility_aggregate_metrics.csv`

## TEST-OEA-004
- **REQ**: REQ-OEA-004 (credibility suite)
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_credibility_suite_artifacts`
- **Status**: Implemented
- **Assertion**: `run_suite()` emits all 5 artifact files; aggregate CSV contains all 7 variant rows;
  95% CI columns present for stability, true-reject, false-reject metrics
- **Evidence**: `experiments/credibility_suite.py` — write_csv(), run_suite()

## TEST-OEA-005
- **REQ**: REQ-OEA-005 (statistical reporting)
- **File**: `tests/test_credibility_suite.py`
- **Method**: `test_statistical_reporting_contract`
- **Status**: Implemented
- **Assertion**: Cohen’s d, permutation p-value, and 95% CI are present and non-degenerate for
  all headline comparisons; no headline claim emitted without backing artifact
- **Evidence**: `experiments/credibility_suite.py` — cohen_d(), permutation_pvalue(), ci95()

## TEST-OEA-006
- **REQ**: REQ-OEA-006 (submission guardrail)
- **File**: `docs/research-agent-spec.md`
- **Method**: Manual gate check (Section VI lock verification)
- **Status**: Planned
- **Assertion**: All four locks (citation, evidence, manuscript, distribution) verified before
  any external submission; enforced by agent-level stop condition in `AGENTS.md`
- **Evidence**: `docs/research-agent-spec.md` Section VI; `distribution/distribution-strategy.md`

## TEST-OEA-007
- **REQ**: REQ-OEA-007 (conclusion section)
- **File**: `arxiv/main.tex`
- **Method**: Manual review of compiled LaTeX
- **Status**: Implemented
- **Assertion**: `\section{Conclusion}` is present; section contains (a) OEA hypothesis restatement,
  (b) summary of pilot evidence with scope bounds, (c) explicit limitations, (d) next steps.
  No universal claims without cross-regime evidence.
- **Evidence**: `arxiv/main.tex` — Conclusion section added in cycle 2

## TEST-OEA-008
- **REQ**: REQ-OEA-008 (full ablation results table)
- **File**: `arxiv/main.tex`
- **Method**: Verify table columns against `results/credibility/credibility_aggregate_metrics.csv`
- **Status**: Implemented
- **Assertion**: Table 2 exists with 7 variant rows; columns include stability mean, stability CI95,
  true-reject mean, true-reject CI95, Cohen's d vs oea_full, permutation p-value. All values
  traceable to `results/credibility/` artifacts.
- **Evidence**: `results/credibility/credibility_aggregate_metrics.csv` + `credibility_summary.json`

## TEST-OEA-009
- **REQ**: REQ-OEA-009 (citation audit)
- **File**: `arxiv/references.bib`
- **Method**: Manual verification of each DOI/URL; cross-check author/year against source
- **Status**: Implemented
- **Assertion**: All 8 citations verified: DOI resolves, author list correct, year matches.
  `roumeliotis2025trust` and `fu2025selfverification` explicitly checked and corrected or
  confirmed. No hallucinated entries remain.
- **Evidence**: `arxiv/references.bib` — audit completed in cycle 2
