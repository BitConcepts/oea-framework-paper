# Belief Registry — oea-framework-paper

The belief registry is the catalog of all `BeliefArtifact` instances in this project:
core architectural assumptions, technology decisions, and external dependencies.
Each entry has an ID, propositions, epistemic boundary, confidence, and last stress-test date.

For a full interactive view: `specsmith belief-graph`
For stress-test results: `specsmith stress-test`
For certainty scores: `specsmith epistemic-audit`

---

## Technology Decisions

Technology decisions are beliefs about the project's chosen implementation approach.
They must satisfy Axiom 1 (Observability) — alternatives must be stated.

<!-- Template entry — copy and fill in:
### DEC-001 — [Technology name]

- **Propositions**: [What this decision claims]
- **Epistemic boundary**: [Context and constraints within which this holds]
- **Alternatives considered**: [What was rejected and why]
- **Confidence**: low | medium | high
- **Status**: draft | accepted | stress-tested | reconstructed | deprecated
- **Evidence**: [What supports this decision]
- **Decided by**: [human operator name/role]
- **Date**: YYYY-MM-DD
-->

---

## Core Architectural Assumptions

Assumptions about the system that are not explicitly verified but are relied upon.
Unverified assumptions reduce confidence in all dependent artifacts.

### ARCH-001 — scaffold.yml type:aee-research vs specsmith auto-detection

- **Propositions**: `type: aee-research` in scaffold.yml is the correct authoritative project type; specsmith's `detect_project()` heuristic classifies any Python-file project as `cli-python` when `aee-research` is not in its detection ruleset.
- **Epistemic boundary**: Applies to specsmith 0.10.1 audit check `type-mismatch`. Detection heuristic is source-inspectable at `specsmith/importer.py`.
- **Risk if false**: Low — `type: aee-research` affects tool selection and threshold overrides only; no runtime behavior depends on this field.
- **Confidence**: high
- **Status**: accepted
- **Verification plan**: Track specsmith releases; if `aee-research` is added to detection rules, mismatch warning will clear automatically.

<!-- Template entry:
### ARCH-002 — [Assumption statement]

- **Propositions**: [The assumption, stated as a falsifiable claim]
- **Epistemic boundary**: [When/where this assumption holds]
- **Risk if false**: [What breaks if this assumption is violated]
- **Confidence**: low | medium | high
- **Status**: draft | accepted
- **Verification plan**: [How this assumption will eventually be verified]
-->

---

## External Dependencies

Third-party libraries, services, and APIs that the project relies on.
Each dependency is a belief that it will behave as documented.

<!-- Template entry:
### DEP-001 — [Dependency name and version]

- **Propositions**: [What we depend on this for]
- **Epistemic boundary**: [Version range and conditions]
- **Failure mode**: [What happens if this dependency fails or changes]
- **Confidence**: low | medium | high
- **Last verified**: YYYY-MM-DD
-->

---

## Belief Artifact Statistics

Run `specsmith epistemic-audit` to get current statistics:
- Total beliefs: ?
- Equilibrium: ?
- Overall certainty: ?
- Logic knots: ?
- Below threshold: ?

Last audit: [not yet run]
