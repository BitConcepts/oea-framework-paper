# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-05-19

### Added
- `Dockerfile.cuda`: NVIDIA CUDA 12.1 GPU image (verified on RTX 4070 SUPER)
- `Dockerfile.rocm`: AMD ROCm 6.x GPU image (community-tested; `rocm/dev-ubuntu-22.04:6.3` base)
- `Dockerfile.xpu`: Intel Arc / Xe XPU image (community-tested; `ubuntu:22.04` + PyTorch XPU wheel)
- `.github/ISSUE_TEMPLATE/hardware_compat.md`: hardware compatibility report template
  for community contributors running on AMD ROCm, Intel XPU, Apple MPS, etc.
- `real_lm_experiment.py`: `--device` flag for explicit backend selection
  (`cuda`, `rocm`, `xpu`, `mps`, `cpu`); auto-detection extended to ROCm and Intel XPU
- `requirements-lock.txt`: added install instructions for AMD ROCm 6.x, Intel XPU/Arc,
  NVIDIA CUDA 12.4+, and Apple MPS with per-backend test status notes
- `docs/REQUIREMENTS.md`: REQ-OEA-023 (hardware abstraction / multi-backend device support)
- `docs/TESTS.md`: TEST-OEA-023 covering REQ-OEA-023 (code inspection + Docker image check)

### Fixed
- `scaffold.yml`: type changed `aee-research` → `research-python` to match scanner detection
  (AEE epistemic governance preserved via `enable_epistemic: true`); resolves specsmith
  audit type-mismatch warning — audit now passes 30/30 checks with no issues

### Changed
- `Dockerfile`: updated to current pinned versions (`numpy==2.4.5`, etc.)
- `README.md`: Docker table expanded with ROCm/XPU images and MPS native-only note
- `REPRODUCE.md`: Step 4 rewritten with direct pip commands per backend (removed stale
  setup script references); stale numpy<2 compat note removed; Docker section updated
  with ROCm/XPU run commands; `--device` flag examples added to Step 5
- `docs/ARCHITECTURE.md`: DEC-005 added (hardware abstraction layer); reproducibility
  package table updated with all four Dockerfiles; tooling section updated
- `docs/REQUIREMENTS.md`: REQ-OEA-020 updated to reference `Dockerfile.cuda` alongside
  `Dockerfile`
- `docs/TESTS.md`: TEST-OEA-020 updated to reference `Dockerfile.cuda`
- `AGENTS.md`: spec version updated `0.10.1` → `0.11.3.dev427`; type updated to `research-python`

## [1.0.0] - 2026-05-14

### Added
- Qwen/Qwen2.5-1.5B (1.5B, 2024 architecture) real LLM validation: H1/H2/H3 all confirmed
- EleutherAI/gpt-neo-125M real LLM validation: cross-architecture consistency confirmed
- Systems Implications section (§13): recursive planning drift, hallucinated refinement,
  synthetic contamination, spec degradation — carefully scoped as suggestive
- Mechanistic baseline comparison table (Table 6): why OEA differs from generic constraints
- Formal stability metric S_t = 1 - JSD(p_{x_t}, p_{x_0}) and R_t retrieval context
- Operational definitions expanded: Calibration, Miscalibration, Recursive Drift rows
- Non-claims paragraph: explicit disclaimer on consciousness, cognition, AGI
- Related work positioning paragraph: RAG vs OEA vs generic constraints vs agent-system work
- `experiments/verify_manifest.py` — SHA-256 artifact integrity checker
- `experiments/generate_insights_pdf.py` — 10-page experiment insights report
- `scripts/run_all_experiments.sh` — runs all CPU experiments
- `scripts/build_pdf.cmd` — LaTeX manuscript build script
- BFloat16 compatibility fix for modern models (Qwen, Llama, etc.)

### Changed
- Title: "OEA: Structured Recursive Calibration for Generative Stability" (narrowed)
- "Agentic Closure" → "Recursive Feedback" throughout manuscript and figures
- "agentic systems" → "recursive generative systems" in abstract/conclusion
- Claim discipline: "confirms" → "supports"/"is consistent with" throughout
- Figure captions: tightened with explicit what-to-notice guidance
- Table 3: expanded to 4 models × 3 architecture families (12-column)
- Figures: 4-panel calibration trajectory and metric dissociation plots
- Pipeline figure label: "Recursive Feedback Loop (Layer 3)"
- requirements-lock.txt: numpy==1.26.4 (torch 2.3.1 ABI compatibility)
- Dockerfile: fixed numpy pin, CMD uses run_all_experiments.sh
- .gitignore: added LaTeX build artifacts, result allow-list expanded

### Fixed
- LaTeX: \DeclareMathOperator for \argmax/\argmin (undefined control sequence)
- Markdown lint: MD010/MD040/MD060 violations resolved
- Dependabot: all 5 GitHub Actions PRs merged (checkout v6, setup-python v6, etc.)

[Unreleased]: https://github.com/BitConcepts/oea-framework-paper/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/BitConcepts/oea-framework-paper/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/BitConcepts/oea-framework-paper/releases/tag/v1.0.0
