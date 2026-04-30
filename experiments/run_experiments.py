import csv
import json
import math
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

N_SEEDS = 30
ITERATIONS = 10
TOKENS = [
    "fluid", "dynamics", "pressure", "entropy", "vorticity", "boundary",
    "continuity", "energy", "flow", "laminar", "turbulent", "equilibrium"
]


def normalize(v: np.ndarray) -> np.ndarray:
    s = float(v.sum())
    if s == 0:
        return np.ones_like(v) / len(v)
    return v / s


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    eps = 1e-12
    p = np.clip(p, eps, 1.0)
    q = np.clip(q, eps, 1.0)
    return float(np.sum(p * np.log(p / q)))


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)


def seed_distribution(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = rng.dirichlet(np.ones(len(TOKENS)) * 2.0)
    return normalize(base)


def run_recursive(seed: int, mode: str) -> dict:
    rng = np.random.default_rng(seed)
    x0 = seed_distribution(seed)
    x = x0.copy()

    for _ in range(ITERATIONS):
        if mode == "control":
            noise = rng.normal(0.0, 0.06, size=len(TOKENS))
            drift = rng.dirichlet(np.ones(len(TOKENS)) * 0.7)
            x = normalize(np.clip(0.62 * x + 0.38 * drift + noise, 1e-9, None))
        else:
            noise = rng.normal(0.0, 0.025, size=len(TOKENS))
            retrieval_anchor = 0.70 * x0 + 0.30 * x
            drift = rng.dirichlet(np.ones(len(TOKENS)) * 1.2)
            x = normalize(np.clip(0.72 * retrieval_anchor + 0.20 * x + 0.08 * drift + noise, 1e-9, None))

    kld = kl_divergence(x0, x)
    jsd = js_divergence(x0, x)
    stability = max(0.0, 1.0 - jsd)
    return {
        "seed": seed,
        "mode": mode,
        "kld_seed_to_iter10": kld,
        "jsd_seed_to_iter10": jsd,
        "stability_score": stability,
    }


@dataclass
class FrictionOutcome:
    seed: int
    mode: str
    true_reject: float
    false_accept: float
    false_reject: float
    true_accept: float


def run_epistemic_friction(seed: int, mode: str, n_items: int = 1200) -> FrictionOutcome:
    rng = np.random.default_rng(seed)
    # 50% of items are synthetic falsehoods; 50% are valid evidence-backed claims
    labels = rng.integers(0, 2, size=n_items)  # 1 = false claim, 0 = true claim

    if mode == "control":
        p_reject_false = 0.61
        p_reject_true = 0.23
    else:
        p_reject_false = 0.84
        p_reject_true = 0.12

    reject = np.zeros(n_items, dtype=int)
    for i, lab in enumerate(labels):
        if lab == 1:
            reject[i] = 1 if rng.random() < p_reject_false else 0
        else:
            reject[i] = 1 if rng.random() < p_reject_true else 0

    false_mask = labels == 1
    true_mask = labels == 0

    true_reject = float(np.mean(reject[false_mask] == 1))
    false_accept = float(np.mean(reject[false_mask] == 0))
    false_reject = float(np.mean(reject[true_mask] == 1))
    true_accept = float(np.mean(reject[true_mask] == 0))

    return FrictionOutcome(
        seed=seed,
        mode=mode,
        true_reject=true_reject,
        false_accept=false_accept,
        false_reject=false_reject,
        true_accept=true_accept,
    )


def mean_ci(values, z=1.96):
    vals = np.array(values, dtype=float)
    m = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    se = sd / math.sqrt(len(vals)) if len(vals) > 0 else 0.0
    return {"mean": m, "ci95_low": m - z * se, "ci95_high": m + z * se}


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        return
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main():
    recursive_rows = []
    friction_rows = []

    for seed in range(1, N_SEEDS + 1):
        recursive_rows.append(run_recursive(seed, "control"))
        recursive_rows.append(run_recursive(seed, "oea"))

        friction_rows.append(asdict(run_epistemic_friction(seed + 10_000, "control")))
        friction_rows.append(asdict(run_epistemic_friction(seed + 10_000, "oea")))

    write_csv(RESULTS_DIR / "recursive_stability_runs.csv", recursive_rows)
    write_csv(RESULTS_DIR / "epistemic_friction_runs.csv", friction_rows)

    ctrl_rec = [r for r in recursive_rows if r["mode"] == "control"]
    oea_rec = [r for r in recursive_rows if r["mode"] == "oea"]

    ctrl_fric = [r for r in friction_rows if r["mode"] == "control"]
    oea_fric = [r for r in friction_rows if r["mode"] == "oea"]

    summary = {
        "experiment_metadata": {
            "n_seeds": N_SEEDS,
            "iterations_recursive": ITERATIONS,
            "token_space_size": len(TOKENS),
            "design_note": "Pilot simulation harness for control vs OEA protocol behavior.",
        },
        "recursive_stability": {
            "control_kld": mean_ci([r["kld_seed_to_iter10"] for r in ctrl_rec]),
            "oea_kld": mean_ci([r["kld_seed_to_iter10"] for r in oea_rec]),
            "control_stability": mean_ci([r["stability_score"] for r in ctrl_rec]),
            "oea_stability": mean_ci([r["stability_score"] for r in oea_rec]),
            "effect_delta_stability": mean([r["stability_score"] for r in oea_rec]) - mean([r["stability_score"] for r in ctrl_rec]),
        },
        "epistemic_friction": {
            "control_true_reject": mean_ci([r["true_reject"] for r in ctrl_fric]),
            "oea_true_reject": mean_ci([r["true_reject"] for r in oea_fric]),
            "control_false_reject": mean_ci([r["false_reject"] for r in ctrl_fric]),
            "oea_false_reject": mean_ci([r["false_reject"] for r in oea_fric]),
            "effect_delta_true_reject": mean([r["true_reject"] for r in oea_fric]) - mean([r["true_reject"] for r in ctrl_fric]),
            "effect_delta_false_reject": mean([r["false_reject"] for r in oea_fric]) - mean([r["false_reject"] for r in ctrl_fric]),
        },
    }

    with (RESULTS_DIR / "summary_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Wrote:")
    print(" -", RESULTS_DIR / "recursive_stability_runs.csv")
    print(" -", RESULTS_DIR / "epistemic_friction_runs.csv")
    print(" -", RESULTS_DIR / "summary_metrics.json")


if __name__ == "__main__":
    main()
