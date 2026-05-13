"""
Recursive Memory Drift Benchmark (REQ-OEA-017)
===============================================
Implements Option A from the vNext hardening spec: repeated summarization over
30 recursive steps, measuring how well OEA-controlled generation preserves
information compared to unconstrained generation.

This is a bigram-proxy agentic benchmark. No neural model is required.

OEA-Controlled variant: applies epistemic filtering (keeps highest-quality
candidate by unigram overlap with the seed) and ontological anchoring
(restricts tokens to the reference vocabulary).

Uncontrolled variant: pure bigram sampling, no filtering.

Metrics per iteration
---------------------
entity_retention   Jaccard overlap of token set vs initial token set.
                   Measures how many key "entities" (proxy: vocabulary items)
                   are preserved as the system recurses. Decline = memory loss.
semantic_drift     JSD from the initial token distribution. Measures how far
                   the generated text has drifted from the seed distribution.
hallucination_proxy Fraction of generated tokens NOT in the seed vocabulary.
                   Proxy for tokens that "come from nowhere" — unsupported
                   content introduced by the generative process.
vocab_collapse     Unique token ratio (unique tokens / total tokens) in the
                   current output. Decline indicates vocabulary impoverishment.

Results written to: results/memory_drift/
"""
from __future__ import annotations

import csv
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "memory_drift"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Hyperparameters ─────────────────────────────────────────────────────────
N_SEEDS = 20          # seeds for statistical robustness
N_STEPS = 30          # recursive steps (iterations)
N_CANDIDATES = 5      # candidates per filtered step (OEA-controlled only)
GEN_TOKENS = 80       # tokens generated per step
HELDOUT_FRAC = 0.2    # fraction withheld as "heldout" (not used in corpus train)
SMOOTHING = 0.1       # bigram model smoothing

VARIANTS: list[str] = ["uncontrolled", "oea_controlled"]


# ── Corpus helpers ───────────────────────────────────────────────────────────

def _load_corpus() -> str:
    path = ROOT / "experiments" / "data" / "public_domain_corpus.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return (
        "Alice was beginning to get very tired of sitting by her sister. "
        "She peeped into the book her sister was reading. It had no pictures or conversations "
        "and Alice thought it no use a book without pictures or conversations. "
        "The rabbit with pink eyes ran close by her. "
        "Curiosity and wonder filled the little girl as she followed it down the hole."
    )


def _tokenize(text: str) -> list[str]:
    toks = []
    cur: list[str] = []
    for ch in text.lower():
        if ch.isalnum() or ch in "-'":
            cur.append(ch)
        else:
            if cur:
                toks.append("".join(cur))
                cur = []
    if cur:
        toks.append("".join(cur))
    return toks


# ── Bigram model ─────────────────────────────────────────────────────────────

class _BigramModel:
    def __init__(self, smoothing: float = SMOOTHING):
        self.smoothing = smoothing
        self.uni: Counter[str] = Counter()
        self.bi: dict[str, Counter[str]] = {}
        self.vocab: list[str] = []

    def fit(self, tokens: list[str]) -> None:
        self.uni = Counter(tokens)
        self.vocab = sorted(set(tokens))
        self.bi = {}
        for a, b in zip(tokens[:-1], tokens[1:]):
            if a not in self.bi:
                self.bi[a] = Counter()
            self.bi[a][b] += 1

    def sample(self, start: str, length: int, rng: random.Random,
               anchor_vocab: set[str] | None = None) -> list[str]:
        """Sample a token sequence.  If anchor_vocab is given, restrict output
        to that set (OEA ontological anchoring)."""
        if not self.vocab:
            return []
        vocab = [w for w in self.vocab if anchor_vocab is None or w in anchor_vocab]
        if not vocab:
            vocab = self.vocab
        v = len(vocab)
        w2i = {w: i for i, w in enumerate(vocab)}
        out = [start if start in set(vocab) else vocab[rng.randint(0, v - 1)]]
        rng_np = np.random.default_rng(rng.randint(0, 2**31 - 1))
        for _ in range(length - 1):
            prev = out[-1]
            counts = self.bi.get(prev, Counter())
            denom = sum(c for w, c in counts.items() if anchor_vocab is None or w in anchor_vocab) \
                    + self.smoothing * v
            if denom <= 0:
                out.append(vocab[int(rng_np.integers(v))])
                continue
            probs = np.full(v, self.smoothing / denom)
            for w, c in counts.items():
                idx = w2i.get(w)
                if idx is not None:
                    probs[idx] = (c + self.smoothing) / denom
            probs = np.clip(probs, 0, None)
            s = probs.sum()
            if s <= 0:
                out.append(vocab[int(rng_np.integers(v))])
                continue
            probs /= s
            out.append(vocab[int(rng_np.choice(v, p=probs))])
        return out

    def score(self, tokens: list[str]) -> float:
        """Mean log-prob of a token sequence under the model (epistemic score)."""
        if len(tokens) < 2:
            return -1e6
        total = 0.0
        v = max(1, len(self.vocab))
        for a, b in zip(tokens[:-1], tokens[1:]):
            counts = self.bi.get(a, Counter())
            denom = sum(counts.values()) + self.smoothing * v
            num = counts.get(b, 0) + self.smoothing
            total += math.log(max(num / denom, 1e-12))
        return total / (len(tokens) - 1)


# ── Statistical helpers ───────────────────────────────────────────────────────

def _token_dist(tokens: list[str], vocab: list[str]) -> np.ndarray:
    c = Counter(tokens)
    arr = np.array([c.get(w, 0) for w in vocab], dtype=float)
    s = arr.sum()
    return arr / s if s > 0 else np.ones(len(vocab)) / max(len(vocab), 1)


def _jsd(p: np.ndarray, q: np.ndarray) -> float:
    eps = 1e-12
    p = np.clip(p, eps, 1.0)
    q = np.clip(q, eps, 1.0)
    m = 0.5 * (p + q)
    return float(0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m)))


def _ci95(values: list[float]) -> tuple[float, float, float]:
    """Return (mean, ci_low, ci_high) using t-based 95% CI."""
    if not values:
        return 0.0, 0.0, 0.0
    arr = np.array(values)
    n = len(arr)
    mean = float(arr.mean())
    if n < 2:
        return mean, mean, mean
    se = float(arr.std(ddof=1)) / math.sqrt(n)
    # t-critical for 95% CI, df=n-1; use 2.093 for df=19 (conservative)
    t = 2.093 if n >= 20 else 2.262  # df=9 for n=10
    return mean, mean - t * se, mean + t * se


# ── Core experiment ───────────────────────────────────────────────────────────

def run_memory_drift() -> list[dict]:
    """Run the recursive memory drift experiment. Returns per-iteration rows."""
    corpus_text = _load_corpus()
    corpus_tokens = _tokenize(corpus_text)
    cut = int(len(corpus_tokens) * (1 - HELDOUT_FRAC))
    train_tokens = corpus_tokens[:cut]

    model = _BigramModel()
    model.fit(train_tokens)

    seed_vocab_set = set(train_tokens)
    seed_vocab_list = sorted(seed_vocab_set)
    initial_token_set = set(train_tokens)

    # Seed distribution for JSD
    seed_dist = _token_dist(train_tokens, seed_vocab_list)

    all_rows: list[dict] = []

    total = N_SEEDS * len(VARIANTS) * (N_STEPS + 1)
    done = 0
    sys.stderr.write(
        f"Memory drift: {N_SEEDS} seeds × {len(VARIANTS)} variants "
        f"× {N_STEPS} steps = {N_SEEDS * len(VARIANTS) * N_STEPS} steps\n"
    )
    sys.stderr.flush()

    for seed_idx in range(N_SEEDS):
        rng = random.Random(seed_idx * 1000 + 42)

        for variant in VARIANTS:
            use_oea = variant == "oea_controlled"
            anchor_vocab: set[str] | None = seed_vocab_set if use_oea else None

            # Initial context = first GEN_TOKENS of training corpus
            start_token = train_tokens[rng.randint(0, max(1, len(train_tokens) // 4))]
            current_tokens = model.sample(start_token, GEN_TOKENS, rng, anchor_vocab)

            for step in range(N_STEPS + 1):
                current_set = set(current_tokens)

                # Entity retention: Jaccard overlap with initial corpus vocabulary
                if initial_token_set:
                    retention = len(current_set & initial_token_set) / len(
                        current_set | initial_token_set
                    )
                else:
                    retention = 0.0

                # Semantic drift: JSD from seed distribution
                if seed_vocab_list:
                    cur_dist = _token_dist(current_tokens, seed_vocab_list)
                    drift = _jsd(seed_dist, cur_dist)
                else:
                    drift = 0.0

                # Hallucination proxy: fraction of tokens NOT in seed vocab
                if current_tokens:
                    halluc = sum(1 for t in current_tokens if t not in seed_vocab_set) / len(current_tokens)
                else:
                    halluc = 0.0

                # Vocabulary collapse: unique token ratio
                vocab_collapse = len(current_set) / max(len(current_tokens), 1)

                all_rows.append({
                    "seed": seed_idx,
                    "variant": variant,
                    "step": step,
                    "entity_retention": round(retention, 6),
                    "semantic_drift": round(drift, 6),
                    "hallucination_proxy": round(halluc, 6),
                    "vocab_collapse": round(vocab_collapse, 6),
                })
                done += 1
                if done % 200 == 0:
                    sys.stderr.write(f"\r  {done}/{total} steps...   ")
                    sys.stderr.flush()

                if step < N_STEPS:
                    # Generate next iteration
                    start = current_tokens[-1] if current_tokens else start_token
                    if use_oea:
                        # Epistemic filtering: generate N_CANDIDATES, keep highest score
                        candidates = [
                            model.sample(start, GEN_TOKENS, rng, anchor_vocab)
                            for _ in range(N_CANDIDATES)
                        ]
                        scored = [(model.score(c), c) for c in candidates]
                        current_tokens = max(scored, key=lambda x: x[0])[1]
                    else:
                        current_tokens = model.sample(start, GEN_TOKENS, rng, anchor_vocab)

    sys.stderr.write(f"\r  {total}/{total} steps done.   \n")
    sys.stderr.flush()
    return all_rows


# ── Aggregation ───────────────────────────────────────────────────────────────

def _aggregate(rows: list[dict]) -> dict:
    """Compute summary statistics at final step for each variant."""
    metrics = ["entity_retention", "semantic_drift", "hallucination_proxy", "vocab_collapse"]
    final_step = N_STEPS
    summary: dict = {"n_seeds": N_SEEDS, "n_steps": N_STEPS, "variants": {}}

    for variant in VARIANTS:
        var_rows = [r for r in rows if r["variant"] == variant and r["step"] == final_step]
        entry: dict[str, object] = {}
        for m in metrics:
            vals = [r[m] for r in var_rows]
            mean, lo, hi = _ci95(vals)
            entry[m] = {"mean": round(mean, 6), "ci95_low": round(lo, 6), "ci95_high": round(hi, 6)}
        summary["variants"][variant] = entry

    # Compute deltas: oea_controlled - uncontrolled at final step
    if "oea_controlled" in summary["variants"] and "uncontrolled" in summary["variants"]:
        deltas: dict[str, float] = {}
        for m in metrics:
            oea_mean = summary["variants"]["oea_controlled"][m]["mean"]
            unc_mean = summary["variants"]["uncontrolled"][m]["mean"]
            deltas[m] = round(oea_mean - unc_mean, 6)
        summary["oea_vs_uncontrolled_delta"] = deltas

    return summary


# ── Output ────────────────────────────────────────────────────────────────────

def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    print("Running Recursive Memory Drift Benchmark (REQ-OEA-017)...")
    rows = run_memory_drift()

    csv_path = RESULTS_DIR / "drift_runs.csv"
    _write_csv(csv_path, rows)
    print(f"Raw runs: {csv_path} ({len(rows)} rows)")

    summary = _aggregate(rows)
    json_path = RESULTS_DIR / "drift_summary.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary: {json_path}")

    # Print headline results
    print("\n=== Memory Drift Summary (final step) ===")
    for variant in VARIANTS:
        print(f"\n  {variant}:")
        for metric, stats in summary["variants"][variant].items():
            print(f"    {metric}: {stats['mean']:.4f} [{stats['ci95_low']:.4f}, {stats['ci95_high']:.4f}]")

    if "oea_vs_uncontrolled_delta" in summary:
        print("\n  OEA - Uncontrolled deltas:")
        for m, d in summary["oea_vs_uncontrolled_delta"].items():
            direction = "↑" if d > 0 else "↓"
            print(f"    {m}: {d:+.4f} {direction}")


if __name__ == "__main__":
    main()
