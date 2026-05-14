# Methodology
## Scope and epistemic posture
This project distinguishes between:
- **Established findings** from cited literature.
- **Working hypotheses** specific to OEA.
- **Evidence claims** that are allowed only after experiment artifacts exist.

## OEA Tri-Layer Protocol
### Phase 1: Ontological Anchoring
- Define ontological jurisdiction and non-negotiable constraints before inference.
- Enumerate domain axioms and invalid output classes.
- Record boundary conditions that trigger abstention or escalation.

### Phase 2: Epistemic Filtering
- Apply retrieval-grounded falsification attempts to generated claims.
- Track provenance for each claim (source, retrieval context, confidence).
- Quantify confidence-quality alignment using calibration diagnostics (e.g., ECE).
- Preserve only evidence-grounded statements in final outputs.

### Phase 3: Recursive Feedback
- Convert claims into testable hypotheses in a digital experiment harness.
- Execute interventions with fixed seeds/config snapshots.
- Feed empirical outcomes back into subsequent hypothesis design.

## Experimental Design
- **Control:** baseline pipeline.
- **Treatment:** OEA-constrained pipeline.
- **Experiment 1:** recursive stability (`n=10`) with divergence/retention scoring.
- **Experiment 2:** epistemic friction under synthetic noise injection.

## Executed pilot run
Runner:
- `python experiments/run_experiments.py`

Generated artifacts:
- `results/recursive_stability_runs.csv`
- `results/epistemic_friction_runs.csv`
- `results/summary_metrics.json`

Observed summary deltas (OEA vs control):
- Stability score: `+0.1206`
- True reject rate (falsehoods): `+0.2320`
- False reject rate (valid claims): `-0.1117`

## Statistical and reporting requirements
- Report uncertainty (confidence intervals or equivalent) for all key metrics.
- Include effect deltas between control and treatment.
- Archive machine-readable outputs (`CSV`/`JSON`) and run metadata.
- Include failure-case analysis (false accept vs false reject) for epistemic filtering.

## Threats to validity
- Current evidence is from a pilot simulation harness; full production harness integration is pending.
- Results may be sensitive to model family and retrieval corpus quality.
- Calibration metrics are necessary but not sufficient proxies for epistemic truth.
- Preprint-stage references can change; citation lock must be revisited before submission.
