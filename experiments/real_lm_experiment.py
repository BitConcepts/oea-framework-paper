"""
OEA Real LLM Experiment — Recursive Stability with RAG
=======================================================
Validates the OEA mechanism using genuine neural log-probabilities and
corpus-grounded retrieval-augmented generation (RAG). No hardcoded constants.

Supported models (pass via --model flag)
----------------------------------------
GPT-2 family (validated):
  distilgpt2                    82M  — default
  gpt2                         124M
  gpt2-medium                  345M

Non-GPT2 family (validated):
  EleutherAI/gpt-neo-125M      125M  — different architecture family (GPT-Neo
                                       local attention), same tokenizer vocab.
                                       Addresses external validity (P4). VERIFIED.
  EleutherAI/gpt-neo-1.3B     1.3B  — requires more GPU memory.

Install dependencies:
  pip install torch transformers rouge-score  (CPU)
  pip install torch==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121  (CUDA/NVIDIA)
  pip install torch --index-url https://download.pytorch.org/whl/rocm6.3  (ROCm/AMD — community-tested)
  pip install torch --index-url https://download.pytorch.org/whl/xpu  (Intel XPU/Arc — community-tested)
  pip install torch transformers rouge-score  (MPS/Apple Silicon — community-tested)
  pip install transformers==4.41.0 rouge-score==0.1.2  (then from PyPI)
  NOTE: requires numpy<2 for torch 2.3.1 ABI compatibility:
    pip install "numpy==1.26.4"

Hardware test status:
  Verified by maintainer:   CPU (x86-64), NVIDIA CUDA 12.1 (RTX 4070 SUPER, Windows 11)
  Community-tested only:    AMD ROCm, Intel XPU/Arc, Apple MPS
  Report hardware issues:   https://github.com/BitConcepts/oea-framework-paper/issues
  Use hardware template:    .github/ISSUE_TEMPLATE/hardware_compat.md

Device selection:
  Auto-detect (default): cuda > rocm > xpu > mps > cpu
  Force device:  --device cuda | rocm | xpu | mps | cpu

CPU vs GPU usage:
  GPU (full config, ~30 min per model):
    python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M
  CPU (reduced config, ~20 min):
    python experiments/real_lm_experiment.py --model EleutherAI/gpt-neo-125M \
      --n-seeds 3 --n-iterations 5 --gen-tokens 40
  Force ROCm:
    python experiments/real_lm_experiment.py --model distilgpt2 --device rocm
  Force Intel XPU:
    python experiments/real_lm_experiment.py --model distilgpt2 --device xpu

OEA Layer Implementation
------------------------
Layer 1 — Ontological Anchoring:
    BM25Retriever fetches the most relevant passage from the seed corpus
    (token-overlap similarity) and prepends it to the generation prompt.
    Vocabulary anchoring further constrains generated tokens to the
    reference domain boundary.

Layer 2 — Epistemic Filtering:
    K=3 candidates are scored by their mean log-probability under the
    *original frozen model*. The highest-scoring candidate is kept.
    This directly implements the verification score of Fu et al. (2025):
    s_verify(y|x) = log G_0(y|x).

Layer 3 — Recursive Feedback:
    The running corpus accumulates over iterations; held-out calibration
    accuracy feeds back into variant selection at each step.

Variants (ablation design)
--------------------------
control             Raw sampling; no retrieval, no filtering.
oea_rag_only        RAG prepended to prompt; 1 candidate (no epistemic filter).
                    Isolates the retrieval contribution from filtering.
oea_anchored        RAG + K=3 candidates + highest log-prob selection
                    + vocabulary anchoring. Full OEA protocol.
oea_miscalibrated   RAG + K=3 candidates + *lowest* log-prob selection.
                    Anti-calibrated control. Expected to degrade faster
                    than even the no-RAG control — proving calibration is
                    the causal mechanism, not filtering per se.

Metrics (per iteration)
-----------------------
stability_jsd       JS divergence vs. seed distribution (lower = stable).
mean_log_prob       Mean per-token log-prob under the original model.
                    Directly measures how in-distribution the corpus is.
true_reject_rate    Fraction of OOV tokens flagged by log-prob threshold.
                    Measures epistemic calibration accuracy.
false_reject_rate   Fraction of in-vocab tokens incorrectly flagged.
                    Measures specificity. Lower is better.
rouge_l_recall      ROUGE-L recall of generated text against seed corpus.
                    Fully independent of log-probability: measures how much
                    seed-corpus content is preserved in the generated output.
                    Breaks the selection-criterion/metric circularity.

Frozen-weights scope note
-------------------------
Model weights are NOT updated; this is a generation-time experiment.
This is an intentional design choice providing a *necessary-condition* test:
if the OEA epistemic filter cannot reduce distributional drift even in the
idealized frozen setting (where the model is unchanged), it cannot do so
during training. Demonstrating the mechanism here establishes a lower bound
on in-training efficacy. See REQ-OEA-010 and DEC-004.

CQ Measurement Output
---------------------
After the run, the script prints suggested _CALIBRATION_QUALITY updates
for credibility_suite.py, derived from the measured true_reject_rates.
This closes the evidence chain: real log-probs -> measured CQ -> suite params.
See REQ-OEA-012.

Results written to: results/real_lm/
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "experiments" / "data" / "public_domain_corpus.txt"

# ── CLI argument parsing ───────────────────────────────────────────────────────
_parser = argparse.ArgumentParser(
    description="OEA Real LLM Recursive Stability Experiment",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
_parser.add_argument(
    "--model",
    default="distilgpt2",
    help=(
        "HuggingFace model name (default: distilgpt2). "
        "E.g. gpt2 (124M), EleutherAI/gpt-neo-125M (non-GPT2-family, REQ-OEA P4)."
    ),
)
_parser.add_argument(
    "--n-seeds",
    type=int,
    default=10,
    help="Number of random seeds (default: 10 for GPU; use 3 on CPU for ~20 min runtime).",
)
_parser.add_argument(
    "--n-iterations",
    type=int,
    default=10,
    help="Recursive iterations per seed (default: 10 for GPU; use 5 on CPU).",
)
_parser.add_argument(
    "--gen-tokens",
    type=int,
    default=60,
    help="New tokens generated per step (default: 60 for GPU; use 40 on CPU).",
)
_parser.add_argument(
    "--device",
    default=None,
    choices=["cuda", "rocm", "xpu", "mps", "cpu"],
    help=(
        "Force compute device. Default: auto-detect (cuda > rocm > xpu > mps > cpu). "
        "Use 'rocm' for AMD GPUs (ROCm build of PyTorch). "
        "Use 'xpu' for Intel Arc/Xe GPUs (Intel Extension for PyTorch). "
        "ROCm and XPU are community-tested only — report issues via the hardware template."
    ),
)
_args, _unknown = _parser.parse_known_args()

# ── Hyperparameters ────────────────────────────────────────────────────────────
MODEL_NAME = _args.model
RESULTS_DIR = ROOT / "results" / "real_lm" / MODEL_NAME
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
N_SEEDS = _args.n_seeds
N_ITERATIONS = _args.n_iterations
N_CANDIDATES = 3          # candidates per OEA epistemic-filter step
RAG_PASSAGE_TOKENS = 64   # max tokens prepended from retrieval
GEN_MAX_TOKENS = _args.gen_tokens
TOP_P = 0.92              # nucleus sampling
TEMPERATURE = 0.9
# Dynamic rejection threshold (replaces the fixed -4.5 absolute value that caused TRR=1.0
# saturation for distilgpt2 on a small corpus).
# Threshold = mean(in-vocab log-probs) - LOG_PROB_SIGMA * std(in-vocab log-probs)
# At LOG_PROB_SIGMA=1.5 this flags ~7% of in-vocab tokens (FRR baseline) and a much
# larger fraction of OOV tokens, providing meaningful discrimination. See REQ-OEA-012.
LOG_PROB_SIGMA = 1.5      # std-dev multiplier for dynamic threshold
LOG_PROB_THRESHOLD_FALLBACK = -4.5  # used only when ref_vocab is too small (<4 tokens)
N_EVAL_TOKENS = 80        # tokens sampled for true/false reject measurement

# oea_rag_only isolates the retrieval contribution from the epistemic filter
VARIANTS: list[str] = ["control", "oea_rag_only", "oea_anchored", "oea_miscalibrated"]


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


# ── BM25 Retriever (OEA Ontological Anchoring / Epistemic Grounding) ──────────

class BM25Retriever:
    """Token-overlap retriever over seed corpus passages.

    Implements the retrieval-augmented generation (RAG) component of OEA Layer 1
    (Ontological Anchoring): the retrieved passage is prepended to the generation
    prompt, grounding synthesis within the domain boundary of the original corpus.
    This is corpus-grounded retrieval, not a log-probability proxy.

    Similarity metric: cosine-style token overlap
        score(q, p) = |q ∩ p| / sqrt(|q| * |p|)
    """

    def __init__(self, passages: list[str], passage_token_ids: list[set[int]]):
        self.passages = passages
        self._ids = passage_token_ids

    @classmethod
    def from_text(cls, text: str, tokenizer: object) -> "BM25Retriever":
        """Build retriever by splitting text on blank lines into passages."""
        raw = [p.strip() for p in text.split("\n\n") if p.strip()]
        # Fallback: split on single newlines if no double-newline paragraphs
        if len(raw) < 3:
            raw = [p.strip() for p in text.split("\n") if p.strip()]
        passages = raw if raw else [text]
        passage_ids = [set(tokenizer.encode(p)) for p in passages]
        return cls(passages, passage_ids)

    def retrieve(self, query_ids: list[int]) -> tuple[str, float]:
        """Return (passage, score) with highest token overlap with last 50 query tokens."""
        if not self.passages:
            return "", 0.0
        q = set(query_ids[-50:])
        if not q:
            return self.passages[0], 0.0
        scores = [
            len(q & p_ids) / math.sqrt(max(len(q) * len(p_ids), 1))
            for p_ids in self._ids
        ]
        best = int(np.argmax(scores))
        return self.passages[best], float(scores[best])


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
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        print(
            "ERROR: transformers and torch are required.\n"
            "Install: pip install -r requirements-experiments.txt\n"
            "For GPU: see requirements-experiments.txt for CUDA/ROCm/MPS install commands.\n"
            "For GPT-Neo: pip install transformers>=4.28 torch>=2.0",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from rouge_score import rouge_scorer as _rs_module
        _rouge_scorer_inst = _rs_module.RougeScorer(["rougeL"], use_stemmer=False)
        _rouge_available = True
    except ImportError:
        _rouge_scorer_inst = None
        _rouge_available = False
        sys.stderr.write(
            "NOTE: rouge-score not installed; rouge_l_recall will be 0.0.\n"
            "Install: pip install rouge-score\n"
        )

    sys.stderr.write(f"Loading {MODEL_NAME}...\n")
    sys.stderr.flush()
    # AutoTokenizer and AutoModelForCausalLM support GPT-2, GPT-Neo, and other
    # causal LM families transparently — no architecture-specific imports needed.
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()

    # ── Device selection (cuda > rocm > xpu > mps > cpu, or --device override) ─
    _COMMUNITY_NOTE = (
        " [community-tested — report issues: "
        "https://github.com/BitConcepts/oea-framework-paper/issues]"
    )
    _forced = getattr(_args, "device", None)
    if _forced:
        if _forced == "rocm":
            device = torch.device("cuda")  # ROCm uses the cuda device string
            sys.stderr.write(f"Device: cuda/ROCm (forced){_COMMUNITY_NOTE}\n")
        elif _forced == "xpu":
            device = torch.device("xpu")
            sys.stderr.write(f"Device: xpu/Intel (forced){_COMMUNITY_NOTE}\n")
        else:
            device = torch.device(_forced)
            sys.stderr.write(f"Device: {_forced} (forced via --device)\n")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        _gpu_name = torch.cuda.get_device_name(0)
        # Detect ROCm build (HIP runtime) vs standard CUDA
        if hasattr(torch.version, "hip") and torch.version.hip:
            sys.stderr.write(
                f"Device: cuda/ROCm ({_gpu_name}){_COMMUNITY_NOTE}\n"
            )
        else:
            sys.stderr.write(f"Device: cuda ({_gpu_name})\n")
    elif hasattr(torch, "xpu") and torch.xpu.is_available():
        device = torch.device("xpu")
        sys.stderr.write(f"Device: xpu/Intel{_COMMUNITY_NOTE}\n")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = torch.device("mps")
        sys.stderr.write(f"Device: mps (Apple Metal){_COMMUNITY_NOTE}\n")
    else:
        device = torch.device("cpu")
        sys.stderr.write(
            "Device: cpu  [no GPU detected — CUDA/ROCm/XPU/MPS would be faster; "
            "see requirements-lock.txt for install commands]\n"
        )
    model = model.to(device)

    seed_text = load_seed_text()
    seed_ids: list[int] = tokenizer.encode(seed_text, truncation=True, max_length=256)
    seed_dist = _token_dist(seed_ids, tokenizer.vocab_size)
    ref_vocab: set[int] = set(seed_ids)  # ontological boundary (DEC-004)

    def _rouge_l_recall(ids: list[int]) -> float:
        """ROUGE-L recall: fraction of seed-corpus content preserved in generated text.

        This metric is fully independent of log-probability — it measures content
        preservation using n-gram overlap, not model scores.  It directly counters
        the circularity concern: selecting by log-prob and then evaluating by
        ROUGE-L against the seed corpus are completely orthogonal measurements.
        Higher recall = more seed-domain content retained in the output.
        """
        if not _rouge_available or len(ids) < 4:
            return 0.0
        generated = tokenizer.decode(ids[-256:], skip_special_tokens=True)
        scores = _rouge_scorer_inst.score(seed_text, generated)  # ref=seed, hyp=generated
        return float(scores["rougeL"].recall)

    # Build RAG retriever from corpus passages (OEA Layer 1 — Ontological Anchoring)
    retriever = BM25Retriever.from_text(seed_text, tokenizer)
    sys.stderr.write(
        f"RAG index: {len(retriever.passages)} passages from corpus.\n"
    )
    sys.stderr.flush()

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
        t = torch.tensor([ids[-256:]]).to(device)  # use last 256 tokens as context
        out = model(t)
        lp = torch.nn.functional.log_softmax(out.logits[:, :-1, :].float(), dim=-1)
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
        Measures calibration: does a dynamic log-prob threshold correctly identify
        out-of-distribution (OOV) tokens vs in-vocabulary tokens?

        Threshold is computed as:
            mean(in-vocab log-probs) - LOG_PROB_SIGMA * std(in-vocab log-probs)
        This self-calibrates to the model's distribution, avoiding the saturation
        (TRR=1.0) caused by the previous fixed threshold (-4.5) on small corpora.

        Returns (true_reject_rate, false_reject_rate).
        true_reject_rate: fraction of OOV tokens correctly flagged (↑ = good)
        false_reject_rate: fraction of in-vocab tokens incorrectly flagged (↓ = good)
        """
        ctx = torch.tensor([context_ids[-64:]]).to(device)
        out = model(ctx)
        lp = torch.nn.functional.log_softmax(out.logits[0, -1, :].float(), dim=-1).cpu().numpy()

        rng = np.random.default_rng(99)
        vocab_size = tokenizer.vocab_size

        # Dynamic threshold calibrated to the in-vocab log-prob distribution
        inv_lps_all = np.array([lp[t] for t in ref_vocab if 0 <= t < vocab_size])
        if len(inv_lps_all) >= 4:
            threshold = float(inv_lps_all.mean() - LOG_PROB_SIGMA * inv_lps_all.std())
        else:
            threshold = LOG_PROB_THRESHOLD_FALLBACK  # degenerate corpus fallback

        # OOV = tokens NOT in reference vocab (synthetic falsehoods proxy)
        oov_pool = [t for t in rng.integers(0, vocab_size, 500) if t not in ref_vocab]
        oov_sample = oov_pool[:N_EVAL_TOKENS] if len(oov_pool) >= N_EVAL_TOKENS else oov_pool

        # In-vocab = tokens from the reference distribution (true claims proxy)
        inv_sample = rng.choice(list(ref_vocab), size=N_EVAL_TOKENS, replace=True).tolist()

        trr = sum(1 for t in oov_sample if lp[t] < threshold) / max(len(oov_sample), 1)
        frr = sum(1 for t in inv_sample if lp[t] < threshold) / max(len(inv_sample), 1)
        return trr, frr

    @torch.no_grad()
    def _generate(prompt_ids: list[int], gen_seed: int) -> list[int]:
        """Generate GEN_MAX_TOKENS new tokens from prompt.

        gen_seed is used to set the global torch RNG before each generation call,
        making results fully reproducible across runs on the same platform.
        """
        import torch
        torch.manual_seed(gen_seed)  # fix: seed was computed but never applied
        t = torch.tensor([prompt_ids[-128:]]).to(device)
        out = model.generate(
            t,
            max_new_tokens=GEN_MAX_TOKENS,
            do_sample=True,
            top_p=TOP_P,
            temperature=TEMPERATURE,
            pad_token_id=tokenizer.eos_token_id,
        )
        return out[0, t.shape[1]:].cpu().tolist()

    def _rag_prompt(current_ids: list[int]) -> list[int]:
        """Build a RAG-augmented prompt: retrieved passage + current context.

        Implements OEA Layer 1 (Ontological Anchoring): the retrieval grounds
        generation in corpus-domain evidence before the epistemic filter acts.
        """
        passage, _score = retriever.retrieve(current_ids)
        rag_ids = tokenizer.encode(passage, truncation=True, max_length=RAG_PASSAGE_TOKENS)
        # Prepend retrieved passage to the current context window
        context = current_ids[-64:]
        return (rag_ids + context)[-128:]

    # ── Main loop ──────────────────────────────────────────────────────────────
    for seed_idx in range(N_SEEDS):
        for variant in VARIANTS:
            current_ids: list[int] = seed_ids[:]

            for iteration in range(N_ITERATIONS + 1):
                # Measure metrics at current state
                current_dist = _token_dist(current_ids, tokenizer.vocab_size)
                jsd = _jsd(current_dist, seed_dist)
                mlp = _mean_log_prob(current_ids)
                trr, frr = _epistemic_accuracy(current_ids, ref_vocab)
                rl = _rouge_l_recall(current_ids)

                all_rows.append({
                    "seed": seed_idx,
                    "variant": variant,
                    "iteration": iteration,
                    "stability_jsd": round(jsd, 6),
                    "mean_log_prob": round(mlp, 4),
                    "true_reject_rate": round(trr, 4),
                    "false_reject_rate": round(frr, 4),
                    "rouge_l_recall": round(rl, 4),
                })
                progress.update(
                    label=f"{variant} | seed {seed_idx} | iter {iteration}/{N_ITERATIONS}"
                )

                if iteration == N_ITERATIONS:
                    break

                gen_seed = seed_idx * 1000 + iteration * 10

                if variant == "control":
                    # No retrieval, no filtering — raw sampling baseline
                    prompt = current_ids[-128:]
                    chosen = _generate(prompt, gen_seed)

                elif variant == "oea_rag_only":
                    # RAG only — retrieval without epistemic filtering.
                    # Ablation: isolates the retrieval contribution.
                    prompt = _rag_prompt(current_ids)
                    chosen = _generate(prompt, gen_seed)

                elif variant == "oea_anchored":
                    # Full OEA: RAG (Layer 1) + K-candidate epistemic filter (Layer 2)
                    # + vocabulary anchoring (Layer 1 boundary enforcement)
                    prompt = _rag_prompt(current_ids)
                    candidates = [_generate(prompt, gen_seed + i) for i in range(N_CANDIDATES)]
                    scores = [_score_candidate(current_ids, c) for c in candidates]
                    chosen = candidates[int(np.argmax(scores))]  # epistemic filter
                    # Ontological anchoring: constrain to reference vocabulary boundary
                    anchored = [t for t in chosen if t in ref_vocab]
                    chosen = anchored if anchored else chosen[:10]

                else:  # oea_miscalibrated
                    # Anti-calibrated: RAG context but WORST log-prob candidate.
                    # Critical falsification control: if miscalibration degrades faster
                    # than even control, calibration quality is the causal variable.
                    prompt = _rag_prompt(current_ids)
                    candidates = [_generate(prompt, gen_seed + i) for i in range(N_CANDIDATES)]
                    scores = [_score_candidate(current_ids, c) for c in candidates]
                    chosen = candidates[int(np.argmin(scores))]  # anti-epistemic filter

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
                    "rouge_l_recall_mean": round(
                        mean(r.get("rouge_l_recall", 0.0) for r in irows), 4
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
            "rouge_l_recall_delta": round(
                _final_mean(v, "rouge_l_recall") - _final_mean("control", "rouge_l_recall"),
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
            f"true_reject_delta={sign(d['true_reject_rate_delta'])}{d['true_reject_rate_delta']:.4f}  "
            f"rouge_l_delta={sign(d.get('rouge_l_recall_delta', 0))}{d.get('rouge_l_recall_delta', 0):.4f}"
        )
    print(f"\nDone. Artifacts in {RESULTS_DIR}")

    # ── CQ Measurement (REQ-OEA-012) ───────────────────────────────────────────
    # Derive suggested _CALIBRATION_QUALITY values for credibility_suite.py.
    # Evidence chain: real log-probs -> measured TRR -> CQ -> suite parameters.
    #
    # Formula: CQ = 0.5 + (trr_variant - trr_control) / (2 * (1 - trr_control))
    # At trr == trr_control: CQ = 0.5 (random baseline)
    # At trr == 1.0:         CQ = 1.0 (perfect discrimination)
    # At trr < trr_control:  CQ < 0.5 (anti-calibrated)
    def _fm(variant: str, key: str) -> float:
        fr = [r for r in rows if r["variant"] == variant and r["iteration"] == N_ITERATIONS]
        return sum(r[key] for r in fr) / max(len(fr), 1)

    base_trr = _fm("control", "true_reject_rate")
    print("\n=== CQ Measurement for credibility_suite._CALIBRATION_QUALITY (REQ-OEA-012) ===")
    print(f"Baseline (control) true_reject_rate: {base_trr:.4f}")
    print("Update _CALIBRATION_QUALITY in experiments/credibility_suite.py:")
    cq_out = {}
    for v in VARIANTS:
        if v == "control":
            continue
        measured_trr = _fm(v, "true_reject_rate")
        denom = max(2.0 * (1.0 - base_trr), 0.02)
        cq = 0.5 + (measured_trr - base_trr) / denom
        cq = round(max(0.01, min(0.99, cq)), 3)
        cq_out[v] = {"measured_true_reject_rate": round(measured_trr, 4), "suggested_cq": cq}
        print(f"  {v:30s}: trr={measured_trr:.4f} -> CQ={cq:.3f}")
    summary["cq_measurement"] = cq_out
    with (RESULTS_DIR / "real_lm_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    print("\nUpdate _CALIBRATION_QUALITY['oea_full'] using 'oea_anchored' CQ above.")
    print("Then re-run: python experiments/credibility_suite.py")


if __name__ == "__main__":
    main()
