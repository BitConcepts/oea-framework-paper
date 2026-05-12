"""
OEA Real LLM Experiment — distilgpt2 (82M) Recursive Stability
===============================================================
Addresses the "simulation fallacy": replaces hardcoded rejection-rate constants
with genuine neural log-probabilities as the epistemic filter signal.

The OEA epistemic layer selects the highest-log-probability candidate from a pool
of K generated continuations, anchoring the recursive text to the original
distribution. The anti-calibrated (miscalibrated) variant inverts this selection,
demonstrating that the benefit is mechanistic — not definitional.

Variants
--------
control             Raw sampling; no filtering or anchoring.
oea_anchored        K=3 candidates; keep highest log-prob (epistemic filter)
                    + vocabulary anchoring (ontological filter).
oea_miscalibrated   K=3 candidates; keep *lowest* log-prob (anti-calibrated).
                    Expected to degrade faster than control.

Metrics (per iteration)
-----------------------
stability_jsd       JS divergence of current token distribution vs. seed.
                    0 = identical; higher = more drift.
mean_log_prob       Mean per-token log-prob under the *original* model.
                    Measures how in-distribution the current text is.
true_reject_rate    Fraction of out-of-vocabulary tokens correctly flagged by
                    the log-prob threshold (epistemic calibration accuracy).
false_reject_rate   Fraction of in-vocabulary tokens incorrectly flagged
                    (specificity). Lower is better.

Design notes
------------
- Model: distilgpt2 (82M params); CPU-compatible, no authentication required.
- The original model weights are frozen throughout — no fine-tuning.
- "Distributional drift" is measured on the *generated text corpus*, not via
  actual model weight updates. This is the same proxy used by the bigram suite.
- true/false_reject_rate are measured by presenting the model's current context
  and checking whether it assigns log-prob below LOG_PROB_THRESHOLD to tokens
  sampled uniformly from outside the reference vocabulary (true positives) and
  from within it (false positives).

Results written to: results/real_lm/
"""
from __future__ import annotations

import csv
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "real_lm"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_PATH = ROOT / "experiments" / "data" / "public_domain_corpus.txt"

# ── Hyperparameters ────────────────────────────────────────────────────────────
MODEL_NAME = "distilgpt2"
N_SEEDS = 3
N_ITERATIONS = 5
N_CANDIDATES = 3          # candidates per OEA step
GEN_MAX_TOKENS = 60       # new tokens per recursive step
TOP_P = 0.92              # nucleus sampling
TEMPERATURE = 0.9
LOG_PROB_THRESHOLD = -4.5  # tokens below this are "suspicious" (out-of-distribution)
N_EVAL_TOKENS = 80        # tokens sampled for true/false reject measurement

VARIANTS: list[str] = ["control", "oea_anchored", "oea_miscalibrated"]


# ── Progress bar ───────────────────────────────────────────────────────────────

class Progress:
    """Lightweight stderr progress bar with ETA."""

    def __init__(self, total: int, width: int = 40):
        self.total = total
        self.done = 0
        self.width = width
        self._start = time.monotonic()
        self._last = 0.0

    def update(self, n: int = 1, label: str = "") -> None:
        self.done += n
        now = time.monotonic()
        if now - self._last < 0.12 and self.done < self.total:
            return
        self._last = now
        elapsed = now - self._start
        pct = self.done / self.total
        filled = int(self.width * pct)
        bar = "=" * filled + (">" if filled < self.width else "") + " " * (self.width - filled)
        eta = (elapsed / self.done * (self.total - self.done)) if self.done > 0 else 0
        sys.stderr.write(
            f"\r[{bar}] {self.done}/{self.total} ({pct:.0%})"
            f" | {label} | elapsed {_fmt(elapsed)} | ETA {_fmt(eta)}   "
        )
        sys.stderr.flush()

    def finish(self, label: str = "done") -> None:
        self.update(0, label)
        sys.stderr.write("\n")
        sys.stderr.flush()


def _fmt(s: float) -> str:
    s = int(s)
    if s < 60:
        return f"{s}s"
    m, s2 = divmod(s, 60)
    return f"{m}m{s2:02d}s" if m < 60 else f"{m // 60}h{m % 60:02d}m{s2:02d}s"


# ── Corpus helpers ─────────────────────────────────────────────────────────────

def load_seed_text() -> str:
    if CORPUS_PATH.exists():
        return CORPUS_PATH.read_text(encoding="utf-8").strip()
    return (
        "The recursive system generates synthetic text over multiple iterations. "
        "Stability degrades without epistemic constraints anchoring generation."
    )


# ── Statistical helpers ────────────────────────────────────────────────────────

def _token_dist(ids: list[int], vocab_size: int) -> np.ndarray:
    counts = np.zeros(vocab_size, dtype=float)
    for t in ids:
        if 0 <= t < vocab_size:
            counts[t] += 1.0
    s = counts.sum()
    return counts / s if s > 0 else np.full(vocab_size, 1.0 / vocab_size)


def _jsd(p: np.ndarray, q: np.ndarray) -> float:
    eps = 1e-12
    p = np.clip(p, eps, 1.0)
    q = np.clip(q, eps, 1.0)
    m = 0.5 * (p + q)
    return float(0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m)))


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


# ── Core experiment ────────────────────────────────────────────────────────────

def run_real_lm_experiment() -> list[dict]:
    """
    Run the real LLM recursive stability experiment.
    Returns list of per-iteration metric rows.
    """
    try:
        import torch
        from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    except ImportError:
        print(
            "ERROR: transformers and torch are required.\n"
            "Install: pip install -r requirements-experiments.txt "
            "--extra-index-url https://download.pytorch.org/whl/cpu",
            file=sys.stderr,
        )
        sys.exit(1)

    sys.stderr.write(f"Loading {MODEL_NAME}...\n")
    sys.stderr.flush()
    tokenizer = GPT2TokenizerFast.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    model.eval()

    seed_text = load_seed_text()
    seed_ids: list[int] = tokenizer.encode(seed_text, truncation=True, max_length=256)
    seed_dist = _token_dist(seed_ids, tokenizer.vocab_size)
    ref_vocab: set[int] = set(seed_ids)  # ontological boundary

    total_steps = N_SEEDS * len(VARIANTS) * (N_ITERATIONS + 1)
    progress = Progress(total_steps)
    sys.stderr.write(
        f"Starting real LLM experiment: {N_SEEDS} seeds × {len(VARIANTS)} variants "
        f"× {N_ITERATIONS} iterations = {N_SEEDS * len(VARIANTS) * N_ITERATIONS} steps\n"
    )

    all_rows: list[dict] = []

    # ── Cached log-prob utility ────────────────────────────────────────────────
    @torch.no_grad()
    def _mean_log_prob(ids: list[int]) -> float:
        """Mean per-token log-prob of sequence under the original model."""
        if len(ids) < 2:
            return -100.0
        t = torch.tensor([ids[-256:]])  # use last 256 tokens as context
        out = model(t)
        lp = torch.nn.functional.log_softmax(out.logits[:, :-1, :], dim=-1)
        per_tok = lp.gather(2, t[:, 1:].unsqueeze(-1)).squeeze(-1)
        return float(per_tok.mean())

    @torch.no_grad()
    def _score_candidate(context_ids: list[int], new_ids: list[int]) -> float:
        """Log-prob of new_ids continuation given context_ids."""
        full = context_ids[-128:] + new_ids
        return _mean_log_prob(full)

    @torch.no_grad()
    def _epistemic_accuracy(
        context_ids: list[int], ref_vocab: set[int]
    ) -> tuple[float, float]:
        """
        Measures calibration: does log-prob < LOG_PROB_THRESHOLD correctly identify
        out-of-distribution tokens?

        Returns (true_reject_rate, false_reject_rate).
        true_reject_rate: fraction of OOV tokens correctly flagged (↑ = good)
        false_reject_rate: fraction of in-vocab tokens incorrectly flagged (↓ = good)
        """
        ctx = torch.tensor([context_ids[-64:]])
        out = model(ctx)
        lp = torch.nn.functional.log_softmax(out.logits[0, -1, :], dim=-1).numpy()

        rng = np.random.default_rng(99)
        vocab_size = tokenizer.vocab_size

        # OOV = tokens NOT in reference vocab (synthetic falsehoods proxy)
        oov_pool = [t for t in rng.integers(0, vocab_size, 500) if t not in ref_vocab]
        oov_sample = oov_pool[:N_EVAL_TOKENS] if len(oov_pool) >= N_EVAL_TOKENS else oov_pool

        # In-vocab = tokens from the reference distribution (true claims proxy)
        inv_sample = rng.choice(list(ref_vocab), size=N_EVAL_TOKENS, replace=True).tolist()

        trr = sum(1 for t in oov_sample if lp[t] < LOG_PROB_THRESHOLD) / max(len(oov_sample), 1)
        frr = sum(1 for t in inv_sample if lp[t] < LOG_PROB_THRESHOLD) / max(len(inv_sample), 1)
        return trr, frr

    @torch.no_grad()
    def _generate(prompt_ids: list[int], gen_seed: int) -> list[int]:
        """Generate GEN_MAX_TOKENS new tokens from prompt."""
        import torch
        t = torch.tensor([prompt_ids[-128:]])
        out = model.generate(
            t,
            max_new_tokens=GEN_MAX_TOKENS,
            do_sample=True,
            top_p=TOP_P,
            temperature=TEMPERATURE,
            pad_token_id=tokenizer.eos_token_id,
        )
        return out[0, t.shape[1]:].tolist()

    # ── Main loop ──────────────────────────────────────────────────────────────
    for seed_idx in range(N_SEEDS):
        for variant in VARIANTS:
            current_ids: list[int] = seed_ids[:]
            n_cands = 1 if variant == "control" else N_CANDIDATES

            for iteration in range(N_ITERATIONS + 1):
                # Measure metrics at current state
                current_dist = _token_dist(current_ids, tokenizer.vocab_size)
                jsd = _jsd(current_dist, seed_dist)
                mlp = _mean_log_prob(current_ids)
                trr, frr = _epistemic_accuracy(current_ids, ref_vocab)

                all_rows.append({
                    "seed": seed_idx,
                    "variant": variant,
                    "iteration": iteration,
                    "stability_jsd": round(jsd, 6),
                    "mean_log_prob": round(mlp, 4),
                    "true_reject_rate": round(trr, 4),
                    "false_reject_rate": round(frr, 4),
                })
                progress.update(
                    label=f"{variant} | seed {seed_idx} | iter {iteration}/{N_ITERATIONS}"
                )

                if iteration == N_ITERATIONS:
                    break

                # Generate next step
                gen_seed = seed_idx * 1000 + iteration * 10
                candidates = [_generate(current_ids, gen_seed + i) for i in range(n_cands)]

                if variant == "control":
                    chosen = candidates[0]
                else:
                    scores = [_score_candidate(current_ids, c) for c in candidates]
                    if variant == "oea_anchored":
                        chosen = candidates[int(np.argmax(scores))]
                        # Ontological anchoring: filter to reference vocabulary
                        chosen_anchored = [t for t in chosen if t in ref_vocab]
                        chosen = chosen_anchored if chosen_anchored else chosen[:10]
                    else:  # oea_miscalibrated
                        chosen = candidates[int(np.argmin(scores))]

                # Accumulate (window to last 512 tokens to avoid unbounded growth)
                current_ids = (current_ids + chosen)[-512:]

    progress.finish()
    return all_rows


# ── Aggregate & summary ────────────────────────────────────────────────────────

def _aggregate(rows: list[dict]) -> dict:
    from statistics import mean

    variants = sorted(set(r["variant"] for r in rows))
    iterations = sorted(set(r["iteration"] for r in rows))
    summary: dict = {"variants": {}}

    for v in variants:
        v_rows = [r for r in rows if r["variant"] == v]
        by_iter: dict[int, list] = {i: [] for i in iterations}
        for r in v_rows:
            by_iter[r["iteration"]].append(r)

        summary["variants"][v] = {
            "by_iteration": {
                str(i): {
                    "stability_jsd_mean": round(mean(r["stability_jsd"] for r in irows), 6),
                    "mean_log_prob_mean": round(mean(r["mean_log_prob"] for r in irows), 4),
                    "true_reject_rate_mean": round(mean(r["true_reject_rate"] for r in irows), 4),
                    "false_reject_rate_mean": round(
                        mean(r["false_reject_rate"] for r in irows), 4
                    ),
                    "n": len(irows),
                }
                for i, irows in by_iter.items()
                if irows
            }
        }

    # Final-iteration deltas vs control
    def _final_mean(variant: str, key: str) -> float:
        fr = [r for r in rows if r["variant"] == variant and r["iteration"] == N_ITERATIONS]
        return sum(r[key] for r in fr) / max(len(fr), 1)

    summary["final_iteration_deltas_vs_control"] = {
        v: {
            "stability_jsd_delta": round(
                _final_mean("control", "stability_jsd") - _final_mean(v, "stability_jsd"), 6
            ),
            "mean_log_prob_delta": round(
                _final_mean(v, "mean_log_prob") - _final_mean("control", "mean_log_prob"), 4
            ),
            "true_reject_rate_delta": round(
                _final_mean(v, "true_reject_rate") - _final_mean("control", "true_reject_rate"),
                4,
            ),
        }
        for v in variants
        if v != "control"
    }

    return summary


def main() -> None:
    print(f"OEA Real LLM Experiment — {MODEL_NAME}")
    print(f"Seeds: {N_SEEDS}  Iterations: {N_ITERATIONS}  Candidates: {N_CANDIDATES}")
    print(f"Results → {RESULTS_DIR}")

    rows = run_real_lm_experiment()
    _write_csv(RESULTS_DIR / "real_lm_runs.csv", rows)
    summary = _aggregate(rows)

    with (RESULTS_DIR / "real_lm_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print("\nFinal-iteration deltas vs control:")
    for v, d in summary["final_iteration_deltas_vs_control"].items():
        sign = lambda x: "+" if x >= 0 else ""
        print(
            f"  {v:30s}  "
            f"jsd_delta={sign(d['stability_jsd_delta'])}{d['stability_jsd_delta']:.4f}  "
            f"log_prob_delta={sign(d['mean_log_prob_delta'])}{d['mean_log_prob_delta']:.4f}  "
            f"true_reject_delta={sign(d['true_reject_rate_delta'])}{d['true_reject_rate_delta']:.4f}"
        )
    print(f"\nDone. Artifacts in {RESULTS_DIR}")


if __name__ == "__main__":
    main()
