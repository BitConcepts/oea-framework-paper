# Compliance Report — oea-framework-paper

**Generated:** 2026-05-17

## Project Summary

- **Name**: oea-framework-paper
- **Type**: AEE research project
- **Language**: python
- **VCS Platform**: github
- **Spec Version**: 0.11.3

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

- **Passed**: 29
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
- ✓ Recommended file docs/SPECSMITH.yml exists
- ✓ Recommended file CONTRIBUTING.md exists
- ✓ Recommended file LICENSE exists
- ✓ All 22 accepted REQ(s) have test coverage
- ✓ LEDGER.md has 244 lines (within threshold)
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

- `5341d17 docs: document IJAIA journal submission in LEDGER`
- `a2c1e29 Merge branch 'main' of https://github.com/BitConcepts/oea-framework-paper`
- `3bfd3c3 chore: replace we/our with solo-author voice throughout, rename oea-submission.docx`
- `23c719e Add academia ReportLab report; pin reportlab==4.5.1`
- `53b657d Add compiled paper PDF, regenerated insights report, fix .gitignore`
- `774a46d Remove specsmith references from paper, docs, and requirements; regenerate figures`
- `eba968b docs: document Academia.edu publication, add link to README`
- `28356b7 chore: fix stale references, gitignore submission zip, clean live docs`
- `dd4f55b chore: author name (Tristen Pierson), rebuild PDF and submission zip`
- `894801d fix: README MD036 lint - remove bold emphasis as heading`

**Contributors:**
- 46    Tristen Pierson
- 5    dependabot[bot]

## AI System Inventory (REG-010)

### Agent Capabilities
- **run_shell**: Execute a shell command. Safety-checked; destructive commands are blocked.
  *Epistemic claims:* EXEC-001: no python -c for non-trivial code
- **read_file**: Read a text file from the repository.
  *Epistemic claims:* read-only: does not modify files
- **write_file**: Write content to a file (creates or overwrites).
  *Epistemic claims:* modifies filesystem: logged in audit chain
- **patch_file**: Apply a unified diff patch to a file.
  *Epistemic claims:* modifies filesystem: logged in audit chain
- **list_files**: List files matching a glob pattern in a directory.
  *Epistemic claims:* read-only: does not modify files
- **grep**: Search for a pattern in files.
  *Epistemic claims:* read-only: does not modify files
- **git_diff**: Show the git diff for the working tree.
  *Epistemic claims:* read-only: does not modify files
- **git_status**: Show git status for the working tree.
  *Epistemic claims:* read-only: does not modify files
- **run_tests**: Run the project test suite.
  *Epistemic claims:* may modify test artifacts but not source
- **open_url**: Fetch text content from a URL.
  *Epistemic claims:* network: reads external resources
- **search_docs**: Search documentation files in the repo.
  *Epistemic claims:* read-only: does not modify files
- **remember_project_fact**: Store a named fact in the local project index (.repo-index/facts.json).
  *Epistemic claims:* modifies .repo-index/facts.json only

### Risk Classification
- **EU AI Act tier**: GPAI (general-purpose; systemic risk assessment required if >10^25 FLOP)
- **NIST AI RMF**: GOVERN + MAP + MEASURE + MANAGE controls applied
- **Use-case scope**: software development governance; not Annex III high-risk

### Human Oversight Controls
- Preflight gate: all governed actions require human-language approval
- Kill-switch: `specsmith kill-session` halts all active agent sessions
- Escalation: `specsmith preflight --escalate-threshold <float>` gates low-confidence actions
- Retry budget: `agents_max_iterations` in docs/SPECSMITH.yml bounds self-improvement loops

## Governance File Inventory

- ✓ `AGENTS.md`
- ✓ `LEDGER.md`
- ✗ `docs/SPECSMITH.yml`
- ✓ `scaffold.yml`
- ✓ `docs/REQUIREMENTS.md`
- ✓ `docs/TESTS.md`
- ✓ `docs/ARCHITECTURE.md`
- ✓ `docs/governance/RULES.md`
- ✓ `docs/governance/SESSION-PROTOCOL.md`
- ✓ `docs/governance/LIFECYCLE.md`
- ✓ `docs/governance/ROLES.md`
- ✓ `docs/governance/VERIFICATION.md`
