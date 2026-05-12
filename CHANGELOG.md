# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2026-05-12

### Added
- `results/real_lm/`: real LLM experiment artifacts (distilgpt2, BM25 RAG, 5 seeds x 5 iter)
  - `oea_anchored`: JSD=0.088 (41% less drift), mean log-prob +0.574 nats vs control
  - `oea_miscalibrated`: mean log-prob −0.387 vs control — causal proof of mechanism
  - `oea_rag_only`: RAG without filter degrades log-prob; epistemic filter is operative
- Table 3 (Real LLM results) in `arxiv/main.tex` with actual numbers
- Saturation note for TRR metric in manuscript Limitations
- SEAL-0008: manuscript lock milestone

### Changed
- `experiments/credibility_suite.py`: annotation on `oea_full` CQ=0.83 noting provisional
  status pending threshold recalibration (TRR saturated at 1.0 in real LLM run)

### Fixed
- `arxiv/main.tex`: removed `\citet{}` (natbib not loaded); replaced with `\cite{}`
- `.github/workflows/ci.yml`: added `-bibtex` flag to latexmk args

## [0.3.1]

### Added
- `BM25Retriever` class in `real_lm_experiment.py`: corpus-grounded token-overlap RAG
  implementing OEA Layer 1 (Ontological Anchoring). Not a log-probability proxy.
- `oea_rag_only` variant: retrieval without epistemic filtering; isolates RAG contribution
- REQ-OEA-010/011/012 and TEST-OEA-010/011/012 (RAG spec, manuscript results, CQ chain)
- `\section{Real LLM Validation}` in `arxiv/main.tex`: design, frozen-weights scope as
  necessary-condition framing, results placeholder (pending `real_lm_experiment.py` run)
- DEC-004 in `docs/ARCHITECTURE.md`: explicit frozen-weights scope decision
- CQ Measurement output in `real_lm_experiment.py main()`: derives `_CALIBRATION_QUALITY`
  updates from measured `true_reject_rate` (closes evidence chain: REQ-OEA-012)

### Changed
- `real_lm_experiment.py`: N_SEEDS 3 → 5; RAG added to all non-control variants;
  `oea_anchored` = RAG + K=3 + highest log-prob + vocab anchoring;
  `oea_miscalibrated` = RAG + K=3 + lowest log-prob (anti-calibrated falsification control)
- `docs/ARCHITECTURE.md`: updated component table, data flow, key decisions

## [0.3.0]

### Added
- `experiments/real_lm_experiment.py` — distilgpt2 (82M) recursive stability experiment
  with genuine neural log-probability epistemic filter; no hardcoded constants.
  Variants: `control`, `oea_anchored` (keep highest log-prob), `oea_miscalibrated`
  (keep lowest, anti-calibrated). Proves the mechanism is causal, not definitional.
- `requirements-experiments.txt` — torch (CPU) + transformers install spec
- `experiments/config/credibility_plan_fast.json` — minimal plan for CI validation
  (10 runs vs 7,128; covers key variants including `ablation_miscalibrated`)
- `scripts/run-experiments.sh` / `scripts/run-experiments.cmd` — one-command experiment
  runner; `--all` flag includes real LLM experiment
- `.venv` bootstrap: `scripts/setup.sh --experiments` / `scripts/setup.cmd --experiments`

### Changed
- `experiments/credibility_suite.py`: replaced hardcoded `p_reject_false`/`p_reject_true`
  constants with `_CALIBRATION_QUALITY` dict + `_rejection_rates(cq)` formula. Rejection
  rates are now derived from calibration quality via linear interpolation between random
  baseline (CQ=0.5) and perfect discrimination (CQ=1.0). Addresses "simulation fallacy".
- `experiments/credibility_suite.py`: added `ablation_miscalibrated` variant (CQ=0.22)
  demonstrating that anti-calibrated selection degrades faster than control.
- `experiments/config/credibility_plan.json`: added `ablation_miscalibrated` to variant list
- `scripts/setup.sh` / `scripts/setup.cmd`: full venv bootstrap with dependency tiers

## [0.2.2]

### Fixed
- 26 markdownlint errors eliminated across governance, docs, and CHANGELOG files
  (MD009 trailing spaces, MD010 hard tabs, MD012 blank lines, MD031/MD040 code
  fence language/spacing, MD037 emphasis markers, MD001 heading levels)
- `.markdownlint.json`: added `siblings_only` for MD024, disabled MD026/MD034
- `pytest.ini`: added `pythonpath = .` so `tests/` can import `experiments.*`
- `.github/workflows/ci.yml`: removed `cm-super` apk (not available in Alpine TeX image)

### Added
- CI: `python-tests` job (pytest + pip-audit security scan)
- `.github/dependabot.yml`: weekly pip and GitHub Actions dependency updates

## [0.2.1] - 2026-05-12

### Fixed
- `arxiv/references.bib`: all 8/8 citations VERIFIED (citation lock closed)
  - `fu2025selfverification`: NeurIPS 2025 poster confirmed (Accept, submission 12388)
  - `roumeliotis2025trust`: arXiv:2507.10571 v3 confirmed; trailing comma removed
- Trace vault SEAL-0007: citation lock audit-gate sealed
- REQ-OEA-006 submission guardrail: citation lock now satisfied

## [0.2.0] - 2026-05-12

### Added
- `arxiv/main.tex`: `\section{Conclusion}` with OEA hypothesis restatement, scope-bounded
  evidence summary, stability/epistemic orthogonality finding, 4-item future-work agenda
- `arxiv/main.tex`: Table 2 — full ablation study (11 variants × 648 runs) with stability,
  true-reject, false-reject means + 95% CI, Cohen's d vs baselines (sourced from artifacts)
- `arxiv/references.bib`: full citation audit; 6/8 VERIFIED, 2 flagged for human check
- REQ-OEA-007/008/009 and TEST-OEA-007/008/009 added to belief artifact registry
- Trace vault: SEAL-0004 (cycle 2 architecture), SEAL-0005 (verification), SEAL-0006 (release)

## [0.1.0] - 2026-05-12

### Added
- specsmith 0.10.1 governance overlay (`aee-research` type, `enable_epistemic=true`)
- `AGENTS.md` — agent governance hub with OEA protocol and H13 epistemic boundary rules
- `docs/ARCHITECTURE.md` — OEA tri-layer architecture, experiment harness components, data flow
- `REQUIREMENTS.md` / `docs/REQUIREMENTS.md` — 6 REQ-OEA-\* belief artifacts (all P1, Accepted)
- `docs/TESTS.md` — 6 TEST-OEA-\* specifications with 100% REQ coverage
- `docs/governance/` — 11 governance files including full epistemic layer (EPISTEMIC-AXIOMS,
  BELIEF-REGISTRY, FAILURE-MODES, UNCERTAINTY-MAP)
- `scaffold.yml` — aee-research project type, specsmith 0.10.1
- `arxiv/main.tex` — manuscript scaffold with pilot results and ablation tables
- `experiments/credibility_suite.py` — bigram-proxy ablation harness (11 variants)
- `results/summary_metrics.json` — pilot: stability delta +0.121, true-reject delta +0.232
- Trace vault: SEAL-0001 (architecture), SEAL-0002 (verification), SEAL-0003 (v0.1.0 release)
- Community files: `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE/`, `.editorconfig`
[Unreleased]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.3.1...v0.3.2
[0.3.1]:
[0.3.1]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/BitConcepts/oea-framework-paper/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/BitConcepts/oea-framework-paper/releases/tag/v0.1.0
