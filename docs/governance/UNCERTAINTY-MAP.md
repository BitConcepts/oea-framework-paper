# Uncertainty Map — oea-framework-paper

The uncertainty map is the explicit catalog of what oea-framework-paper does **not** know.
Every project has unknown unknowns; this map converts them to **known unknowns** — which
are far less dangerous.

An entry here means: "We know we don't know this. Here is what we're doing about it."

Artifacts below the certainty threshold are automatically surfaced by:
`specsmith epistemic-audit`

---

## Epistemic Status Summary

| Status | Count |
|--------|-------|
| UNKNOWN confidence artifacts | [run epistemic-audit] |
| LOW confidence artifacts | [run epistemic-audit] |
| P1 requirements below MEDIUM | [run epistemic-audit] |
| Logic Knots unresolved | [run stress-test] |

---

## Known Unknowns

These are things the project explicitly does not know and has a plan to address.

### UNK-001 — CQ evidence chain mismatch: real LLM TRR does not directly validate bigram-suite CQ

- **Artifact affected**: REQ-OEA-012, `_CALIBRATION_QUALITY` in `credibility_suite.py`
- **Why unknown**: The `real_lm_experiment.py` dynamic threshold (mean_in_vocab - 1.5*std_in_vocab)
  yields CQ=0.446 for `oea_anchored` via the formula `CQ = 0.5 + (trr - trr_control)/(2*(1-trr_control))`.
  This is CQ<0.5 (anti-calibrated), contrary to the design estimate of 0.83. Root cause: vocabulary
  anchoring shifts the full model log-prob distribution, causing the relative threshold to adapt
  proportionally. The TRR metric thus measures threshold discrimination dynamics, not the per-claim
  calibration quality that the bigram suite models.
- **Confidence impact**: REQ-OEA-012 confidence reduced to medium. CQ=0.83 for `oea_full` is retained
  as a principled design estimate, not an empirical measurement.
- **Mitigation**: Direct empirical CQ validation requires held-out ECE measurement on a real LLM
  with explicit falsehood injection (not random OOV sampling). Documented in main.tex Limitations.
- **Target date**: future work (out of scope for this paper)
- **Status**: open

### UNK-002 — ~~Bigram suite corpus self-reference~~ RESOLVED 2026-05-13

- **Artifact affected**: REQ-OEA-004, REQ-OEA-008
- **Resolution**: Removed `arxiv/main.tex` from `collect_repo_docs_corpus()`. Replaced `repo_docs`
  corpus in `credibility_plan.json` with a stable `scientific_snippets` corpus
  (`experiments/data/scientific_corpus.txt`) consisting entirely of public-domain scientific prose
  (Newton, Feynman, Sagan). The credibility suite now uses two independent, stable corpora.
- **Status**: resolved

<!-- Template:
### UNK-001 — [What we don't know]

- **Artifact affected**: [REQ-XXX or "no direct artifact"]
- **Why unknown**: [What evidence or test is missing]
- **Confidence impact**: [Which artifacts' certainty is reduced by this]
- **Mitigation**: [What we're doing to resolve this unknown]
- **Target date**: YYYY-MM-DD
- **Status**: open | investigating | resolved
-->

---

## Accepted Uncertainties

These are things the project has decided to leave uncertain for now, with explicit
acceptance of the risk.

<!-- Template:
### ACC-001 — [Accepted uncertainty]

- **Artifact affected**: [REQ-XXX]
- **Risk level**: low | medium | high
- **Rationale for acceptance**: [Why this uncertainty is acceptable at this stage]
- **Triggers for revisit**: [When this acceptance should be reconsidered]
- **Accepted by**: [human operator]
- **Date**: YYYY-MM-DD
-->

---

## Certainty Threshold

Project threshold: **0.70**

Artifacts are tracked here when their certainty score falls below this threshold.
Run `specsmith epistemic-audit --threshold 0.70` to get the current list.

---

## Update Protocol

1. After every `specsmith epistemic-audit`, review the below-threshold list
2. For each below-threshold artifact: decide whether to track it as a Known Unknown
   or accept it explicitly
3. Add entries to the appropriate section above
4. Record the review in LEDGER.md
