# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2026-05-12

### Added
- `arxiv/main.tex`: `\section{Conclusion}` — OEA hypothesis restatement, stability/epistemic
  orthogonality finding, explicit scope bounds, 4-item future-work agenda (REQ-OEA-007)
- `arxiv/main.tex`: Table 2 — full ablation study (11 variants, 648 runs each) with stability,
  true-reject, and false-reject means + 95% CI, Cohen's d vs baselines (REQ-OEA-008)
- `arxiv/references.bib`: citation audit header with VERIFIED/NEEDS-HUMAN-CHECK/FLAGGED
  status for all 8 references; `roumeliotis2025trust` flagged for human verification (REQ-OEA-009)
- REQ-OEA-007/008/009 and TEST-OEA-007/008/009 added to belief artifact registry
- Trace vault: SEAL-0004 (cycle 2 architecture), SEAL-0005 (verification), SEAL-0006 (v0.2.0)

### Notes
- Citation lock not yet closed: `roumeliotis2025trust` (arXiv:2507.10571) and
  `fu2025selfverification` (NeurIPS 2025 OpenReview) require human verification
- Credibility suite plan (7,128 runs) deferred; existing `results/credibility/` artifacts used

## [0.1.0] - 2026-05-12

### Added
- specsmith 0.10.1 governance overlay (aee-research project type)
- `AGENTS.md` — agent governance hub with OEA protocol, H13 epistemic boundary requirements
- `docs/ARCHITECTURE.md` — OEA tri-layer architecture, experiment harness components, data flow
- `REQUIREMENTS.md` / `docs/REQUIREMENTS.md` — 6 REQ-OEA-* belief artifacts (all P1, Accepted)
- `docs/TESTS.md` — 6 TEST-OEA-* specifications with 100% REQ coverage
- `docs/governance/` — RULES, SESSION-PROTOCOL, LIFECYCLE, ROLES, CONTEXT-BUDGET,
  VERIFICATION, DRIFT-METRICS, EPISTEMIC-AXIOMS, BELIEF-REGISTRY, FAILURE-MODES, UNCERTAINTY-MAP
- `scaffold.yml` — aee-research type, enable_epistemic=true, epistemic_threshold=0.70
- `LEDGER.md` — specsmith bootstrap session entry added
- `docs/COMPLIANCE.md` — compliance and coverage report
- Trace vault sealed: SEAL-0001 (architecture decision), SEAL-0002 (verification audit-gate)
- Community files: CODE_OF_CONDUCT.md, .github/ISSUE_TEMPLATE/, .editorconfig, .gitattributes

### Existing
- Credibility suite (`experiments/credibility_suite.py`) with full OEA ablation study
- Recursive stability + epistemic friction experiments (n=30 seeds)
- `results/summary_metrics.json` — OEA stability delta +0.121, true-reject delta +0.232
- `arxiv/main.tex` — LaTeX manuscript scaffold
- `docs/methodology.md`, `docs/research-agent-spec.md`, `docs/manifesto.md`

### Notes
- Simulation harness uses bigram proxy models; results are scope-bounded to this regime
- Submission guardrail (REQ-OEA-006) enforced: no external submission until all 4 locks satisfied
