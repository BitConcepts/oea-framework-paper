# Compliance Report — oea-framework-paper

**Generated:** 2026-05-12

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

**Coverage**: 0/6 (0%)

- ✗ REQ-OEA-001
- ✗ REQ-OEA-002
- ✗ REQ-OEA-003
- ✗ REQ-OEA-004
- ✗ REQ-OEA-005
- ✗ REQ-OEA-006

## Audit Summary

- **Passed**: 26
- **Failed**: 3
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
- ✗ 6 REQ(s) without test coverage: REQ-OEA-001, REQ-OEA-002, REQ-OEA-003, REQ-OEA-004, REQ-OEA-005, REQ-OEA-006
- ✓ LEDGER.md has 22 lines (within threshold)
- ✓ 0 open, 0 closed TODOs
- ✓ AGENTS.md: 49 lines
- ✓ docs/governance/RULES.md: 76 lines
- ✓ docs/governance/SESSION-PROTOCOL.md: 80 lines
- ✓ docs/governance/LIFECYCLE.md: 44 lines
- ✓ docs/governance/ROLES.md: 30 lines
- ✓ docs/governance/CONTEXT-BUDGET.md: 62 lines
- ✓ docs/governance/VERIFICATION.md: 42 lines
- ✓ docs/governance/DRIFT-METRICS.md: 54 lines
- ✗ CI config missing expected tools: test:pytest, lint:vale
- ✗ scaffold.yml type is aee-research but detected cli-python from project files
- ✓ Trace vault intact (2 seals)
- ✓ Phase 🚀 Release: 100% ready

## Recent Activity

- `14c0716 Fix LaTeX-safe artifact references in pilot results section`
- `a69a1df Add executed pilot experiment artifacts`
- `c4715ba Execute OEA pilot experiments and integrate measured results`
- `131d230 Harden manuscript with evidence-backed citations and methods`
- `c1a4d71 Upload compiled PDF artifact from CI`
- `0e6900d Fix CI pathing and markdown lint configuration`
- `f2f704f Add GitHub Actions CI for markdown and LaTeX smoke tests`
- `90bd7a1 Add issue and PR templates for research workflow`
- `c34917a Add MIT licensing and repository governance metadata`
- `e17723b Initialize OEA framework research paper scaffold`

**Contributors:**
- 10	Tristen Pierson

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
