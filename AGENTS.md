# oea-framework-paper — Agent Governance

**Project**: OEA: Structured Recursive Calibration for Generative Stability
**Phase**: See `scaffold.yml` — advance with `specsmith phase next`
**Spec**: specsmith 0.11.3.dev427 / research-python

## specsmith Installation Policy (HARD RULE)

specsmith is installed **globally via pipx** on this machine (`~/.local/bin/specsmith`).

- **NEVER** run `pip install specsmith`, `pip install --pre specsmith`, or any variant in any project venv, conda env, or Python environment.
- **NEVER** add specsmith as a project dependency in any package manifest.
- specsmith is available machine-wide as the `specsmith` CLI command.
- Upgrade only via: `pipx upgrade specsmith` — this is an owner action, not an agent action.
- When specsmith prompts **"Migrate now? [Y/n]"**, **always answer `Y`** without hesitation.

## Mission
Empirically validate the OEA (Ontology, Epistemic, Agentic) Framework as a measurable
guardrail against recursive model collapse. Produce a peer-reviewed publication artifact.

## Project Summary
- **Type**: research-python with AEE epistemic governance (`enable_epistemic: true`)
- **Language**: Python 3.x
- **Test framework**: pytest
- **Experiment harness**: `experiments/credibility_suite.py`, `experiments/run_experiments.py`
- **Results**: `results/` (CSV + JSON artifacts, reproducible with fixed seeds)
- **Manuscript**: `arxiv/main.tex` (LaTeX, PhilSci-Archive / arXiv target)
- **VCS**: GitHub, gitflow

## Agent Role
You are a **Principal Research Engineer** operating under the OEA protocol.
Objective: maintain epistemic integrity across all research artifacts and manuscript edits.
No claim enters the manuscript without an evidence lock and experiment artifact backing it.

## Epistemic Boundary Requirements (H13)
Before executing any task, state:
1. Which REQ-IDs are in scope
2. What assumptions this task relies on
3. What adversarial challenge could break the proposal
4. Whether any P1 requirement is currently at LOW confidence

## Workflow Rules
1. Read AGENTS.md fully before starting any task.
2. Log all changes in LEDGER.md (no ledger entry = work not done, H1).
3. Map changes to requirements in docs/REQUIREMENTS.md.
4. Verify against docs/TESTS.md.
5. No external submission until citation lock, evidence lock, and manuscript lock are satisfied.
6. Run `specsmith audit` after each session.

## Key Governance Files
- `docs/ARCHITECTURE.md` — OEA tri-layer system architecture
- `docs/REQUIREMENTS.md` — belief artifact registry (REQ-OEA-*)
- `docs/TESTS.md` — test specification (TEST-OEA-*)
- `docs/governance/EPISTEMIC-AXIOMS.md` — five AEE axioms
- `docs/governance/BELIEF-REGISTRY.md` — technology decisions and assumptions
- `docs/governance/FAILURE-MODES.md` — stress-test breakpoints
- `docs/governance/UNCERTAINTY-MAP.md` — known unknowns catalog
- `docs/methodology.md` — OEA tri-layer process and experimental design
- `docs/research-agent-spec.md` — canonical research agent specification

---
## Governance commands (specsmith_run / /specsmith)

All specsmith governance operations should be invoked through the
``specsmith_run`` agent tool or the ``/specsmith`` REPL slash command.

**In the Nexus REPL:**

```text
/specsmith save               # backup + commit + push governance state
/specsmith load               # pull + restore governance state
/specsmith audit --strict     # strict governance audit
/specsmith status             # show governance status
/specsmith push               # git push governance changes
/specsmith pull               # git pull governance changes
/specsmith sync               # full two-way sync
/specsmith watch              # watch CI and block until green
```

**Verb shortcuts** (single word, no prefix needed in tool calls):
``save``, ``load``, ``push``, ``pull``, ``sync``, ``audit``, ``status``,
``watch``, ``commit``, ``validate``, ``doctor``, ``run``.

These are all equivalent: ``specsmith_run("save")``,
``specsmith_run("/specsmith save")``, ``specsmith_run("specsmith save")``.

---
## Session Governance Protocol

This section is non-negotiable. Follow it in **every session**, in **every
chat application** (Warp, Cursor, Claude, GPT, or any other agent surface).

### Session start (run once, output result verbatim)

```bash
specsmith kill-session 2>/dev/null || true   # kill orphaned processes
specsmith audit --project-dir .              # verify governance health
specsmith sync --project-dir .              # confirm machine state
specsmith checkpoint --project-dir .        # emit GOVERNANCE ANCHOR
```

**Output the `specsmith checkpoint` block verbatim as your first response.**

### Before every code change

```bash
specsmith preflight "<describe the change>" --json
```

- `decision == "accepted"` → proceed; note the `work_item_id`.
- `decision == "needs_clarification"` → surface the `instruction` first.
- **Never make a code change without an accepted preflight.**

### Governance heartbeat (every 8–10 turns, or when context feels compressed)

```bash
specsmith checkpoint --project-dir .
```

Output the GOVERNANCE ANCHOR block verbatim in your response, tagged:

```text
⎠ GOVERNANCE ANCHOR:
<paste checkpoint output here>
```

### When producing any context summary

1. Run `specsmith checkpoint` first.
2. Place the GOVERNANCE ANCHOR at the **top** of the summary.
3. Never omit phase, work items, or health status from a summary.

### Drift detection — if you cannot answer these from memory, you have drifted

- What is the current AEE phase?
- What work item is active?
- What was the last preflight decision?
- Is the audit currently healthy?

If any answer is unknown: **run `specsmith checkpoint` and re-anchor immediately.**

### Session end

```bash
specsmith save --project-dir .   # ESDB backup + commit + push
specsmith kill-session           # stop governance-serve and tracked processes
```

Never end a session with uncommitted governance changes.

### Quick reference

| When | Command |
|---|---|
| Session start | `specsmith audit && specsmith sync && specsmith checkpoint` |
| Before any code change | `specsmith preflight "<intent>" --json` |
| Every 8–10 turns | `specsmith checkpoint` (output verbatim) |
| Context summary | Checkpoint output at top |
| Session end | `specsmith save && specsmith kill-session` |
| Drift detected | `specsmith checkpoint` immediately |
