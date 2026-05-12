# External Distribution Strategy

## Submission Sequence

### 1) arXiv (cs.AI) — first, immediately after manuscript lock

- Category: cs.AI (primary), cs.CL (cross-list).
- Pre-print establishes priority and citable DOI via 10.48550/arXiv.*
- Blocks: manuscript lock + distribution lock satisfied (REQ-OEA-006).
- Positioning: OEA as a practical epistemic engineering framework; cite real LLM validation.

### 2) PhilSci-Archive — same day as arXiv

- Category: Philosophy of Science / AI and Computation.
- Link to arXiv version; PhilSci accepts preprints already on arXiv.
- Positioning: emphasize Popperian falsifiability and ontological grounding thesis.

### 3) NeurIPS / ICML Workshop — next deadline after real LLM results are in

- Target: workshop on synthetic data, model collapse, or reliable AI.
- Submission requires actual `real_lm_experiment.py` results in the manuscript.
- This is the venue for community feedback before journal submission.

### 4) ResearchGate

- Host canonical PDF for visibility and citation tracking after arXiv submission.

### 5) BitConcepts Whitepaper Series

- Publish branded version: "The BitConcepts Epistemic Standard."
- Reuse manuscript source with publication-specific front matter and branding.

## Locks Required Before Submission (REQ-OEA-006)

- **Citation lock**: CLOSED (SEAL-0007, all 8/8 verified)
- **Evidence lock**: CLOSED (pilot artifacts + real LLM artifacts in `results/`)
- **Manuscript lock**: PENDING (run `real_lm_experiment.py`, fill results, read PDF)
- **Distribution lock**: PENDING (set target venue, confirm submission metadata)
