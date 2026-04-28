# Specsmith Experimental Protocol
## Target Branch
`BitConcepts/specsmith` - `develop`

## Methods
### `specsmith.initialize_environment`
- Create control and OEA-agent cohorts.
- Load arXiv + PhilSci-Archive corpora for RAG grounding.

### `specsmith.execute_recursive_stability_test`
1. Seed a high-complexity scientific statement.
2. Run `n=10` recursive iterations (`Output_{t-1} -> Input_t`).
3. Compute KL divergence between final state and original seed.
4. Require OEA stability margin `> 40%` over baseline.

### `specsmith.epistemic_friction_analysis`
1. Inject plausible synthetic falsehoods into context.
2. Trigger epistatic layer filters.
3. Score true rejection rate and false rejection rate.

## Reporting Contract
- Emit machine-readable metric artifacts (CSV/JSON).
- Generate publication tables for manuscript insertion.
- Preserve experiment seed/config metadata for reproducibility.
