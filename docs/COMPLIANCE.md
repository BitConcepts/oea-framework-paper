# Compliance Report — oea-framework-paper

**Generated:** 2026-05-13

## Project Summary

- **Name**: oea-framework-paper
- **Type**: AEE research project
- **Language**: python
- **VCS Platform**: github
- **Spec Version**: 0.10.1

## Verification Tools

- **Lint**: vale, specsmith stress-test
- **Typecheck**: none
- **Test**: pytest, specsmith epistemic-audit
- **Security**: none
- **Build**: none
- **Format**: prettier
- **Compliance**: specsmith trace verify

## Requirements Coverage Matrix

**Coverage**: 22/22 (100%)

- ✓ REQ-OEA-001
- ✓ REQ-OEA-002
- ✓ REQ-OEA-003
- ✓ REQ-OEA-004
- ✓ REQ-OEA-005
- ✓ REQ-OEA-006
- ✓ REQ-OEA-007
- ✓ REQ-OEA-008
- ✓ REQ-OEA-009
- ✓ REQ-OEA-010
- ✓ REQ-OEA-011
- ✓ REQ-OEA-012
- ✓ REQ-OEA-013
- ✓ REQ-OEA-014
- ✓ REQ-OEA-015
- ✓ REQ-OEA-016
- ✓ REQ-OEA-017
- ✓ REQ-OEA-018
- ✓ REQ-OEA-019
- ✓ REQ-OEA-020
- ✓ REQ-OEA-021
- ✓ REQ-OEA-022

## Audit Summary

- **Passed**: 28
- **Failed**: 1
- **Fixable**: 0
- **Status**: Issues found

- ✓ Required file AGENTS.md exists
- ✓ Required file LEDGER.md exists
- ✓ Governance file docs/governance/RULES.md exists
- ✓ Governance file docs/governance/SESSION-PROTOCOL.md exists
- ✓ Governance file docs/governance/LIFECYCLE.md exists
- ✓ Governance file docs/governance/ROLES.md exists
- ✓ Governance file docs/governance/CONTEXT-BUDGET.md exists
- ✓ Governance file docs/governance/VERIFICATION.md exists
- ✓ Governance file docs/governance/DRIFT-METRICS.md exists
- ✓ Recommended file docs/REQUIREMENTS.md exists
- ✓ Recommended file docs/TESTS.md exists
- ✓ Recommended file docs/ARCHITECTURE.md exists
- ✓ Recommended file CONTRIBUTING.md exists
- ✓ Recommended file LICENSE exists
- ✓ All 22 accepted REQ(s) have test coverage
- ✓ LEDGER.md has 126 lines (within threshold)
- ✓ 0 open, 0 closed TODOs
- ✓ AGENTS.md: 49 lines
- ✓ docs/governance/RULES.md: 76 lines
- ✓ docs/governance/SESSION-PROTOCOL.md: 80 lines
- ✓ docs/governance/LIFECYCLE.md: 44 lines
- ✓ docs/governance/ROLES.md: 30 lines
- ✓ docs/governance/CONTEXT-BUDGET.md: 62 lines
- ✓ docs/governance/VERIFICATION.md: 42 lines
- ✓ docs/governance/DRIFT-METRICS.md: 54 lines
- ✓ CI config missing lint tool (lint:vale); test tool is present. Consider adding vale.
- ✗ scaffold.yml type is aee-research but detected cli-python from project files
- ✓ Trace vault intact (12 seals)
- ✓ Phase 🚀 Release: 100% ready

## Recent Activity

- `713b3ee feat: v0.5.0 - GPU experiments, ROUGE-L metric, 5 vulnerability fixes`
- `e69fa86 feat: GPU device detection and multi-platform torch install support`
- `adba965 chore: v0.4.0 submission-prep - citation audit cycle 3, Gate C verified`
- `8dc6e68 feat: v0.4.0 - multi-domain corpus, two-model LLM validation, 5 new citations`
- `27a6075 fix: reproducibility + artifact commit + REQ-OEA-012 finding (2026-05-13)`
- `937b57f feat: v0.3.2 - real LLM results, manuscript lock closed, SEAL-0008`
- `6c1d34a fix: resolve LaTeX \citet error; add -bibtex flag to CI latexmk`
- `36cac31 feat: v0.3.2-pre - manuscript complete, 12 tests passing, distribution strategy fixed`
- `89800f1 feat: v0.3.1 - real RAG (BM25Retriever), oea_rag_only variant, REQ-OEA-010/011/012`
- `f8fd878 feat!: v0.3.0 - real LLM experiment, calibration-quality formula, semver/CHANGELOG`

**Contributors:**
- 25 Tristen Pierson

## Governance File Inventory

- ✓ `AGENTS.md`
- ✓ `LEDGER.md`
- ✓ `scaffold.yml`
- ✓ `docs/REQUIREMENTS.md`
- ✓ `docs/TESTS.md`
- ✓ `docs/ARCHITECTURE.md`
- ✓ `docs/governance/RULES.md`
- ✓ `docs/governance/SESSION-PROTOCOL.md`
- ✓ `docs/governance/LIFECYCLE.md`
- ✓ `docs/governance/ROLES.md`
- ✓ `docs/governance/VERIFICATION.md`
