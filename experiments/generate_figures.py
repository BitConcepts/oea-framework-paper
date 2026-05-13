"""
Publication Figure Generator (REQ-OEA-019)
==========================================
Generates three publication-quality figures from committed result artifacts.
No live model inference is required; reads only CSV/JSON from results/.

Figure 1 — OEA Pipeline Diagram
    Conceptual flow chart: Input → Retrieval → Epistemic Filter → Anchoring
    → Recursive Generation → Output, with the three OEA layers annotated.

Figure 2 — Calibration Trajectory
    Log-probability over 10 recursive iterations for all four variants
    (mean ± 95% CI across 10 seeds), for distilgpt2 (82M) and gpt2 (124M).
    Shows that oea_anchored maintains higher log-prob while oea_miscalibrated
    degrades fastest.

Figure 3 — Metric Dissociation
    For each variant, plots log-prob vs ROUGE-L recall at the final iteration,
    demonstrating the orthogonal quality dimensions and the dissociation finding.

Output: arxiv/figures/{fig_pipeline.pdf, fig_calibration.pdf, fig_metric_dissociation.pdf}
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend (no display required)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "arxiv" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
COLORS = {
    "control":          "#555555",
    "oea_rag_only":     "#f5a623",
    "oea_anchored":     "#2196f3",
    "oea_miscalibrated":"#e53935",
}
LABELS = {
    "control":          "Control",
    "oea_rag_only":     "RAG-only",
    "oea_anchored":     "OEA (anchored)",
    "oea_miscalibrated":"Anti-calibrated",
}
LINESTYLES = {
    "control":          "-",
    "oea_rag_only":     "--",
    "oea_anchored":     "-",
    "oea_miscalibrated":":",
}
MARKERS = {
    "control":          "o",
    "oea_rag_only":     "s",
    "oea_anchored":     "^",
    "oea_miscalibrated":"v",
}
VARIANTS = ["control", "oea_rag_only", "oea_anchored", "oea_miscalibrated"]
MODELS = ["distilgpt2", "gpt2"]
MODEL_LABELS = {"distilgpt2": "distilgpt2 (82M)", "gpt2": "gpt2 (124M)"}

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 10,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 150,
})


# ── Data loading ─────────────────────────────────────────────────────────────

def _load_runs(model: str) -> dict[str, dict[int, list[float]]]:
    """Load real_lm_runs.csv for a model.
    Returns: {variant: {iteration: [values_across_seeds]}} for each metric.
    Actually returns nested: metric -> variant -> iteration -> [values]
    """
    path = ROOT / "results" / "real_lm" / model / "real_lm_runs.csv"
    if not path.exists():
        sys.stderr.write(f"WARNING: {path} not found — skipping {model}\n")
        return {}

    data: dict[str, dict[str, dict[int, list[float]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            variant = row["variant"]
            iteration = int(row["iteration"])
            for metric in ["mean_log_prob", "stability_jsd", "rouge_l_recall",
                           "true_reject_rate", "false_reject_rate"]:
                if metric in row:
                    data[metric][variant][iteration].append(float(row[metric]))
    return data


def _mean_ci(values: list[float]) -> tuple[float, float]:
    """Return (mean, half_ci95) using t-distribution."""
    arr = np.array(values)
    n = len(arr)
    if n < 2:
        return float(arr.mean()) if n else 0.0, 0.0
    se = arr.std(ddof=1) / np.sqrt(n)
    t = 2.093 if n >= 20 else 2.262  # 95% CI
    return float(arr.mean()), float(t * se)


# ── Figure 1: OEA Pipeline Diagram ───────────────────────────────────────────

def fig_pipeline() -> Path:
    fig, ax = plt.subplots(figsize=(7.0, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)
    ax.axis("off")

    # Boxes: x_center, label, fill color, layer annotation
    boxes = [
        (0.6,  "Input\nContext",       "#e3f2fd", None),
        (2.2,  "Retrieval\n(BM25)",    "#e8f5e9", "Layer 1\nOntological"),
        (4.0,  "Epistemic\nFilter",    "#fff8e1", "Layer 2\nEpistemic"),
        (5.8,  "Anchoring\nOperator",  "#e8f5e9", "Layer 1\nOntological"),
        (7.6,  "Candidate\nSelection", "#fff8e1", "Layer 2\nEpistemic"),
        (9.3,  "Output\n(Accepted)",   "#e3f2fd", None),
    ]

    box_w, box_h = 1.1, 0.9
    cy = 1.3
    for bx, label, color, layer_ann in boxes:
        rect = mpatches.FancyBboxPatch(
            (bx - box_w / 2, cy - box_h / 2), box_w, box_h,
            boxstyle="round,pad=0.08", facecolor=color, edgecolor="#455a64", linewidth=0.8
        )
        ax.add_patch(rect)
        ax.text(bx, cy, label, ha="center", va="center", fontsize=7.5,
                multialignment="center", color="#1a237e")
        if layer_ann:
            ax.text(bx, cy - box_h / 2 - 0.22, layer_ann,
                    ha="center", va="top", fontsize=6, color="#546e7a",
                    multialignment="center", style="italic")

    # Arrows
    arrow_xs = [(b[0] + box_w / 2, boxes[i + 1][0] - box_w / 2)
                for i, b in enumerate(boxes[:-1])]
    for x0, x1 in arrow_xs:
        ax.annotate("", xy=(x1, cy), xytext=(x0, cy),
                    arrowprops=dict(arrowstyle="-|>", color="#37474f", lw=0.9))

    # Recursive feedback arrow
    ax.annotate("", xy=(0.6, cy - box_h / 2 - 0.08), xytext=(9.3, cy - box_h / 2 - 0.08),
                arrowprops=dict(arrowstyle="-|>", color="#78909c", lw=0.7,
                                connectionstyle="arc3,rad=0.0"))
    ax.text(4.95, cy - box_h / 2 - 0.42, "Agentic Closure (Layer 3): recursive feedback loop",
            ha="center", va="top", fontsize=6.5, color="#546e7a", style="italic")

    ax.set_title("OEA Three-Layer Generation Pipeline", pad=6, fontsize=10)
    out = FIGURES_DIR / "fig_pipeline.pdf"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ── Figure 2: Calibration Trajectory ─────────────────────────────────────────

def fig_calibration() -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=False)

    for ax, model in zip(axes, MODELS):
        data = _load_runs(model)
        if not data:
            ax.text(0.5, 0.5, f"No data for {model}", transform=ax.transAxes,
                    ha="center", va="center")
            continue
        metric_data = data.get("mean_log_prob", {})
        for variant in VARIANTS:
            v_data = metric_data.get(variant, {})
            if not v_data:
                continue
            iters = sorted(v_data.keys())
            means, half_cis = [], []
            for it in iters:
                m, hci = _mean_ci(v_data[it])
                means.append(m)
                half_cis.append(hci)
            means = np.array(means)
            half_cis = np.array(half_cis)
            ax.plot(iters, means, color=COLORS[variant],
                    linestyle=LINESTYLES[variant], marker=MARKERS[variant],
                    markersize=3.5, linewidth=1.2, label=LABELS[variant])
            ax.fill_between(iters, means - half_cis, means + half_cis,
                            color=COLORS[variant], alpha=0.12)

        ax.set_xlabel("Recursive Iteration", fontsize=9)
        ax.set_ylabel("Mean Log-Probability (nats)", fontsize=9)
        ax.set_title(MODEL_LABELS[model], fontsize=9)
        ax.axhline(0, color="#bdbdbd", linewidth=0.6, linestyle=":")
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    # Shared legend below
    handles = [mpatches.Patch(color=COLORS[v], label=LABELS[v]) for v in VARIANTS]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=8,
               bbox_to_anchor=(0.5, -0.02), frameon=True, framealpha=0.9)
    fig.suptitle("Calibration Trajectory: Log-Probability over Recursive Iterations",
                 fontsize=10, y=1.01)
    out = FIGURES_DIR / "fig_calibration.pdf"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ── Figure 3: Metric Dissociation ────────────────────────────────────────────

def fig_metric_dissociation() -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=False)
    final_iter = 10

    for ax, model in zip(axes, MODELS):
        data = _load_runs(model)
        if not data:
            ax.text(0.5, 0.5, f"No data for {model}", transform=ax.transAxes,
                    ha="center", va="center")
            continue
        lp_data = data.get("mean_log_prob", {})
        rl_data = data.get("rouge_l_recall", {})

        for variant in VARIANTS:
            lp_vals = lp_data.get(variant, {}).get(final_iter, [])
            rl_vals = rl_data.get(variant, {}).get(final_iter, [])
            if not lp_vals or not rl_vals:
                continue
            lp_m, lp_hci = _mean_ci(lp_vals)
            rl_m, rl_hci = _mean_ci(rl_vals)
            ax.errorbar(lp_m, rl_m,
                        xerr=lp_hci, yerr=rl_hci,
                        fmt=MARKERS[variant], color=COLORS[variant],
                        markersize=7, capsize=3, linewidth=1.0,
                        label=LABELS[variant])
            # Annotate with variant name
            ax.annotate(LABELS[variant],
                        (lp_m, rl_m),
                        textcoords="offset points",
                        xytext=(5, 4),
                        fontsize=6,
                        color=COLORS[variant])

        ax.set_xlabel("Mean Log-Probability (nats)\n← worse    better →", fontsize=8)
        ax.set_ylabel("ROUGE-L Recall\n← worse    better →", fontsize=8)
        ax.set_title(f"{MODEL_LABELS[model]}\nFinal Iteration (iter={final_iter})", fontsize=9)
        ax.grid(alpha=0.25, linewidth=0.5)
        # Quadrant annotation
        ax.axhline(ax.get_ylim()[0] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.5,
                   color="#eeeeee", linewidth=0.5, linestyle="--")

    fig.suptitle(
        "Metric Dissociation: Log-Probability vs ROUGE-L Recall\n"
        "Orthogonal quality dimensions under OEA anchoring",
        fontsize=10, y=1.01
    )
    out = FIGURES_DIR / "fig_metric_dissociation.pdf"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Generating publication figures (REQ-OEA-019)...")

    p1 = fig_pipeline()
    print(f"  Fig 1 (pipeline):            {p1}")

    p2 = fig_calibration()
    print(f"  Fig 2 (calibration):         {p2}")

    p3 = fig_metric_dissociation()
    print(f"  Fig 3 (metric dissociation): {p3}")

    print(f"\nAll figures written to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
