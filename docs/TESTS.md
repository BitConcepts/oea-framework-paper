# Test Specification

Test specifications for the OEA Framework paper. Each TEST-OEA-* entry maps to a
corresponding REQ-OEA-* requirement. Coverage must remain ≥80% to advance phases.

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

