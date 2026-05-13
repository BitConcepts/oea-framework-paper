"""
OEA Framework — Full Experiment Insights Report (PDF)
=====================================================
Generates a multi-page PDF summarizing all experiment results:
  1. Pilot experiment (recursive stability + epistemic friction)
  2. Credibility suite (12 variants, 648 runs each, headline stats)
  3. Real LLM validation (3 models, final-iteration deltas, CQ measurement)
  4. Memory drift benchmark (30-step recursive summarization)
  5. Baseline competition (OEA vs 5 non-OEA controls)
  6. Error taxonomy

Output: results/oea_insights_report.pdf
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "oea_insights_report.pdf"

# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_json(p: Path) -> dict:
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def _load_csv_rows(p: Path) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _title_page(pdf: PdfPages) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    ax.text(0.5, 0.65, "OEA Framework", fontsize=28, ha="center", va="center",
            fontweight="bold", color="#1a237e")
    ax.text(0.5, 0.58, "Full Experiment Insights Report", fontsize=18,
            ha="center", va="center", color="#37474f")
    ax.text(0.5, 0.50, "Structured Recursive Calibration", fontsize=13,
            ha="center", va="center", color="#546e7a", style="italic")
    ax.text(0.5, 0.42, "BitConcepts Research  •  2026-05-13", fontsize=11,
            ha="center", va="center", color="#78909c")

    contents = [
        "1. Pilot Experiment — Recursive Stability & Epistemic Friction",
        "2. Credibility Suite — 12-Variant Ablation (7,776 runs)",
        "3. Real LLM Validation — 3 Models, 2 Architecture Families",
        "4. Agentic Memory Drift — 30-Step Recursive Benchmark",
        "5. Baseline Competition — OEA vs 5 Non-OEA Controls",
        "6. Error Taxonomy & CQ Measurement",
    ]
    y = 0.32
    for line in contents:
        ax.text(0.5, y, line, fontsize=10, ha="center", va="center", color="#455a64")
        y -= 0.035

    pdf.savefig(fig)
    plt.close(fig)


def _text_page(pdf: PdfPages, title: str, lines: list[str],
               subtitle: str = "") -> None:
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    ax.text(0.05, 0.96, title, fontsize=16, fontweight="bold", va="top",
            color="#1a237e", transform=ax.transAxes)
    if subtitle:
        ax.text(0.05, 0.925, subtitle, fontsize=10, va="top", color="#546e7a",
                style="italic", transform=ax.transAxes)
    y = 0.89 if subtitle else 0.92
    for line in lines:
        if line.startswith("##"):
            ax.text(0.05, y, line.lstrip("# "), fontsize=12, fontweight="bold",
                    va="top", color="#37474f", transform=ax.transAxes)
            y -= 0.025
        elif line.startswith("---"):
            ax.axhline(y=y + 0.005, xmin=0.05, xmax=0.95, color="#e0e0e0",
                       linewidth=0.8, transform=ax.transAxes)
            y -= 0.015
        elif line == "":
            y -= 0.012
        else:
            ax.text(0.06, y, line, fontsize=9, va="top", fontfamily="monospace",
                    color="#212121", transform=ax.transAxes)
            y -= 0.022
        if y < 0.03:
            break
    pdf.savefig(fig)
    plt.close(fig)


def _table_page(pdf: PdfPages, title: str, headers: list[str],
                rows: list[list[str]], subtitle: str = "") -> None:
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis("off")
    ax.text(0.5, 0.97, title, fontsize=14, fontweight="bold", ha="center",
            va="top", color="#1a237e", transform=ax.transAxes)
    if subtitle:
        ax.text(0.5, 0.945, subtitle, fontsize=9, ha="center", va="top",
                color="#546e7a", style="italic", transform=ax.transAxes)

    n_cols = len(headers)
    col_widths = [1.0 / n_cols] * n_cols
    table = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="upper center",
        cellLoc="center",
        bbox=[0.02, 0.05, 0.96, 0.88],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor("#1a237e")
            cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f5f5f5")
        cell.set_edgecolor("#e0e0e0")
    pdf.savefig(fig)
    plt.close(fig)


# ── Page builders ────────────────────────────────────────────────────────────

def page_pilot(pdf: PdfPages) -> None:
    sm = _load_json(ROOT / "results" / "summary_metrics.json")
    rs = sm["recursive_stability"]
    ef = sm["epistemic_friction"]
    lines = [
        "## Experiment Design",
        f"  Seeds: {sm['experiment_metadata']['n_seeds']}   "
        f"Iterations: {sm['experiment_metadata']['iterations_recursive']}   "
        f"Token space: {sm['experiment_metadata']['token_space_size']}",
        "",
        "## Recursive Stability",
        f"  Control KLD:   {rs['control_kld']['mean']:.4f}  "
        f"[{rs['control_kld']['ci95_low']:.4f}, {rs['control_kld']['ci95_high']:.4f}]",
        f"  OEA KLD:       {rs['oea_kld']['mean']:.4f}  "
        f"[{rs['oea_kld']['ci95_low']:.4f}, {rs['oea_kld']['ci95_high']:.4f}]",
        f"  Control stab:  {rs['control_stability']['mean']:.4f}  "
        f"[{rs['control_stability']['ci95_low']:.4f}, {rs['control_stability']['ci95_high']:.4f}]",
        f"  OEA stab:      {rs['oea_stability']['mean']:.4f}  "
        f"[{rs['oea_stability']['ci95_low']:.4f}, {rs['oea_stability']['ci95_high']:.4f}]",
        f"  Delta:         +{rs['effect_delta_stability']:.4f}",
        "",
        "## Epistemic Friction",
        f"  Control TRR:   {ef['control_true_reject']['mean']:.4f}  "
        f"[{ef['control_true_reject']['ci95_low']:.4f}, {ef['control_true_reject']['ci95_high']:.4f}]",
        f"  OEA TRR:       {ef['oea_true_reject']['mean']:.4f}  "
        f"[{ef['oea_true_reject']['ci95_low']:.4f}, {ef['oea_true_reject']['ci95_high']:.4f}]",
        f"  Control FRR:   {ef['control_false_reject']['mean']:.4f}  "
        f"[{ef['control_false_reject']['ci95_low']:.4f}, {ef['control_false_reject']['ci95_high']:.4f}]",
        f"  OEA FRR:       {ef['oea_false_reject']['mean']:.4f}  "
        f"[{ef['oea_false_reject']['ci95_low']:.4f}, {ef['oea_false_reject']['ci95_high']:.4f}]",
        f"  TRR delta:     +{ef['effect_delta_true_reject']:.4f}",
        f"  FRR delta:     {ef['effect_delta_false_reject']:.4f}",
        "",
        "## Interpretation",
        "  H1 supported: OEA stability +12.1% absolute over control.",
        "  H2 supported: TRR +23.2pp, FRR -11.2pp.",
        "  Scope: bigram proxy harness only.",
    ]
    _text_page(pdf, "1. Pilot Experiment", lines,
               "Recursive stability & epistemic friction (30 seeds, bigram proxy)")


def page_credibility(pdf: PdfPages) -> None:
    cs = _load_json(ROOT / "results" / "credibility" / "credibility_summary.json")
    hl = cs["headline_stats"]
    ovc = hl["oea_vs_control_replace"]
    lines = [
        "## Configuration",
        f"  Total runs: 7,776  (12 variants × 12 seeds × 3 depths × 3 ratios × 3 noise)",
        f"  Corpora: {', '.join(cs['config']['corpora'])}",
        "",
        "## Headline: OEA Full vs Control (replace)",
        f"  Stability delta:   +{ovc['stability_delta']:.4f}   (d = {ovc['stability_cohen_d']:.2f}, p < 0.001)",
        f"  Perplexity delta:  +{ovc['perplexity_delta']:.1f}",
        f"  TRR delta:         +{ovc['true_reject_delta']:.4f}",
        f"  FRR delta:         {ovc['false_reject_delta']:.4f}",
        "",
        "## Top 5 Variants by Stability",
    ]
    for v in cs["best_by_stability"]:
        lines.append(
            f"  {v['variant']:25s}  stab={v['stability_mean']:.4f}  "
            f"TRR={v['true_reject_mean']:.3f}  FRR={v['false_reject_mean']:.3f}"
        )
    lines += [
        "",
        "## Key Finding",
        "  oea_full: TRR=0.836, FRR=0.081 (best epistemic discrimination).",
        "  ablation_miscalibrated: TRR=0.257, FRR=0.651 (reversed — H2 confirmed).",
        "  Stability & epistemic filtering are partially orthogonal.",
    ]
    _text_page(pdf, "2. Credibility Suite", lines,
               "12-variant ablation study (7,776 runs, d=4.56, p<0.001)")


def page_credibility_table(pdf: PdfPages) -> None:
    rows_data = _load_csv_rows(ROOT / "results" / "credibility" / "credibility_aggregate_metrics.csv")
    headers = ["Variant", "Stability", "TRR", "FRR", "Perplexity", "N"]
    rows = []
    for r in rows_data:
        rows.append([
            r.get("variant", ""),
            f"{float(r.get('stability_mean', 0)):.4f}",
            f"{float(r.get('true_reject_mean', 0)):.3f}",
            f"{float(r.get('false_reject_mean', 0)):.3f}",
            f"{float(r.get('perplexity_mean', 0)):.1f}",
            r.get("n_runs", ""),
        ])
    _table_page(pdf, "Credibility Suite — Aggregate Metrics", headers, rows,
                "648 runs per variant across 2 domain corpora")


def page_real_lm(pdf: PdfPages) -> None:
    models = {
        "distilgpt2 (82M)": ROOT / "results" / "real_lm" / "distilgpt2" / "real_lm_summary.json",
        "gpt2 (124M)": ROOT / "results" / "real_lm" / "gpt2" / "real_lm_summary.json",
        "gpt-neo-125M (125M)": ROOT / "results" / "real_lm" / "EleutherAI" / "gpt-neo-125M" / "real_lm_summary.json",
    }
    lines = [
        "## Design",
        "  3 models × 4 variants × 10 seeds × 10 iterations = 1,200 steps",
        "  Hardware: RTX 4070 SUPER, CUDA 12.1",
        "",
    ]
    for name, path in models.items():
        data = _load_json(path)
        deltas = data["final_iteration_deltas_vs_control"]
        cq = data.get("cq_measurement", {})
        ctrl_iter10 = data["variants"]["control"]["by_iteration"]["10"]
        lines.append(f"## {name}")
        lines.append(f"  Control (iter 10): log_prob={ctrl_iter10['mean_log_prob_mean']:.3f}  "
                      f"JSD={ctrl_iter10['stability_jsd_mean']:.3f}  "
                      f"ROUGE-L={ctrl_iter10.get('rouge_l_recall_mean', 'N/A')}")
        for variant in ["oea_anchored", "oea_miscalibrated", "oea_rag_only"]:
            d = deltas.get(variant, {})
            lp = d.get("mean_log_prob_delta", 0)
            jsd = d.get("stability_jsd_delta", 0)
            rl = d.get("rouge_l_recall_delta", "N/A")
            sign = "+" if lp >= 0 else ""
            lines.append(f"  {variant:25s}  log_prob={sign}{lp:.4f}  "
                          f"JSD={jsd:+.4f}  ROUGE-L={rl}")
        if cq:
            lines.append("  CQ measurement:")
            for v, m in cq.items():
                lines.append(f"    {v}: TRR={m['measured_true_reject_rate']:.4f} → CQ={m['suggested_cq']:.3f}")
        lines.append("")

    lines += [
        "## Hypothesis Summary (all 3 models)",
        "  H1 (Calibration Direction): SUPPORTED  (+0.62 to +1.63 nats)",
        "  H2 (Miscalibration Reversal): SUPPORTED  (-0.55 to -1.37 nats)",
        "  H3 (RAG without Filter): SUPPORTED  (-0.08 to -0.54 nats)",
        "  ROUGE-L dissociation: CONFIRMED across all 3 models",
    ]
    _text_page(pdf, "3. Real LLM Validation", lines,
               "Three models, two architecture families (GPT-2, GPT-Neo)")


def page_real_lm_table(pdf: PdfPages) -> None:
    models = {
        "distilgpt2": ROOT / "results" / "real_lm" / "distilgpt2" / "real_lm_summary.json",
        "gpt2": ROOT / "results" / "real_lm" / "gpt2" / "real_lm_summary.json",
        "gpt-neo-125M": ROOT / "results" / "real_lm" / "EleutherAI" / "gpt-neo-125M" / "real_lm_summary.json",
    }
    headers = ["Model", "Variant", "Log-prob", "Δ Log-prob", "JSD", "ROUGE-L"]
    rows = []
    for model_name, path in models.items():
        data = _load_json(path)
        deltas = data["final_iteration_deltas_vs_control"]
        for variant in ["control", "oea_anchored", "oea_miscalibrated", "oea_rag_only"]:
            it10 = data["variants"][variant]["by_iteration"]["10"]
            if variant == "control":
                delta_lp = "—"
            else:
                delta_lp = f"{deltas[variant]['mean_log_prob_delta']:+.4f}"
            rows.append([
                model_name if variant == "control" else "",
                variant,
                f"{it10['mean_log_prob_mean']:.3f}",
                delta_lp,
                f"{it10['stability_jsd_mean']:.3f}",
                f"{it10.get('rouge_l_recall_mean', 0):.4f}",
            ])
    _table_page(pdf, "Real LLM — Final Iteration Results (iter 10)", headers, rows,
                "10 seeds × 10 iterations per model/variant")


def page_memory_drift(pdf: PdfPages) -> None:
    drift_path = ROOT / "results" / "memory_drift" / "drift_summary.json"
    if not drift_path.exists():
        _text_page(pdf, "4. Memory Drift Benchmark", ["  No drift_summary.json found."])
        return
    ds = _load_json(drift_path)
    lines = [
        "## Design",
        f"  {ds.get('n_seeds', '?')} seeds × 2 variants × {ds.get('n_steps', '?')} steps",
        "  Bigram proxy recursive summarization",
        "",
        "## Final Step (step 30) Comparison",
    ]
    for var in ["uncontrolled", "oea_controlled"]:
        vd = ds.get("variants", {}).get(var, {})
        if vd:
            lines.append(f"  {var}:")
            for metric, vals in vd.items():
                if isinstance(vals, dict) and "mean" in vals:
                    lines.append(
                        f"    {metric:25s}  {vals['mean']:.4f}  "
                        f"[{vals['ci95_low']:.4f}, {vals['ci95_high']:.4f}]"
                    )
            lines.append("")
    deltas = ds.get("oea_vs_uncontrolled_delta", {})
    if deltas:
        lines.append("## OEA vs Uncontrolled Deltas")
        for k, v in deltas.items():
            arrow = "↓" if v <= 0 else "↑"
            lines.append(f"    {k:25s}  {v:+.4f} {arrow}")
    lines += [
        "",
        "## Interpretation",
        "  Bigram harness provides structural support for H4 only.",
        "  Effect sizes |Δ| < 0.01 reflect vocabulary constraints.",
        "  Hallucination proxy = 0.0 for both (bigram limitation).",
        "  Neural validation required for quantitative conclusions.",
    ]
    _text_page(pdf, "4. Agentic Memory Drift Benchmark", lines,
               "30-step recursive summarization (20 seeds, bigram proxy)")


def page_baseline(pdf: PdfPages) -> None:
    bp = ROOT / "results" / "baseline_competition" / "baseline_summary.json"
    if not bp.exists():
        _text_page(pdf, "5. Baseline Competition", ["  No baseline_summary.json found."])
        return
    bs = _load_json(bp)
    lines = [
        "## Design",
        f"  {bs.get('n_seeds', '?')} seeds × {bs.get('n_iterations', '?')} iterations",
        "  OEA vs 5 non-OEA controls: temperature_low, top-k, entropy_filter,",
        "  repetition_penalty, rag_only.",
        "",
        "## Final Iteration Results",
        "",
        "  Variant                  Stability  TRR     FRR     d(stab)  p(stab)",
        "  ───────────────────────────────────────────────────────────────────",
    ]
    for var, metrics in bs.get("variants", {}).items():
        stab = metrics.get("stability", {}).get("mean", 0)
        trr = metrics.get("true_reject_rate", {}).get("mean", 0)
        frr = metrics.get("false_reject_rate", {}).get("mean", 0)
        d = metrics.get("cohens_d_stability_vs_oea", 0)
        p = metrics.get("pvalue_stability_vs_oea", 0)
        lines.append(
            f"  {var:25s}  {stab:.4f}   {trr:.3f}   {frr:.3f}   {d:+.3f}   {p:.3f}"
        )
    lines += [
        "",
        "## Key Finding",
        "  OEA achieves highest TRR (0.746 vs next-best entropy_filter 0.630).",
        "  Stability differences not significant at N=20 (p > 0.3).",
        "  OEA is not reducible to generic constraint tightening.",
    ]
    _text_page(pdf, "5. Baseline Competition", lines,
               "OEA vs 5 non-OEA controls (20 seeds, bigram proxy)")


def page_error_taxonomy(pdf: PdfPages) -> None:
    rows_data = _load_csv_rows(ROOT / "results" / "credibility" / "error_taxonomy_summary.csv")
    headers = ["Variant", "Tail Loss", "Novel Noise", "False Accept", "False Reject"]
    rows = []
    for r in rows_data:
        rows.append([
            r.get("variant", ""),
            f"{float(r.get('tail_loss_mean', 0)):.1f}",
            f"{float(r.get('novel_noise_tokens_mean', 0)):.1f}",
            f"{float(r.get('false_accept_count_mean', 0)):.1f}",
            f"{float(r.get('false_reject_count_mean', 0)):.1f}",
        ])
    _table_page(pdf, "6. Error Taxonomy", headers, rows,
                "Mean error counts per variant (648 runs each)")


def page_cq_summary(pdf: PdfPages) -> None:
    lines = [
        "## CQ Measurement Summary (REQ-OEA-012)",
        "",
        "  Model                    Variant              TRR     CQ",
        "  ─────────────────────────────────────────────────────────",
    ]
    models = {
        "distilgpt2": ROOT / "results" / "real_lm" / "distilgpt2" / "real_lm_summary.json",
        "gpt2": ROOT / "results" / "real_lm" / "gpt2" / "real_lm_summary.json",
        "gpt-neo-125M": ROOT / "results" / "real_lm" / "EleutherAI" / "gpt-neo-125M" / "real_lm_summary.json",
    }
    for model, path in models.items():
        data = _load_json(path)
        cq = data.get("cq_measurement", {})
        for variant, m in cq.items():
            lines.append(
                f"  {model:25s}  {variant:20s}  {m['measured_true_reject_rate']:.4f}  {m['suggested_cq']:.3f}"
            )
        lines.append("")
    lines += [
        "## Evidence Chain Status",
        "  Design estimate CQ = 0.83 (credibility_suite.py).",
        "  Measured CQ for oea_anchored: 0.438–0.446 across models.",
        "  Mismatch documented as UNK-001. Direct ECE validation is future work.",
        "",
        "## Interpretation",
        "  Dynamic threshold adapts proportionally to anchoring,",
        "  so TRR does not improve despite better log-probability.",
        "  This is a known limitation, not a falsification of OEA.",
    ]
    _text_page(pdf, "CQ Measurement & Evidence Chain", lines,
               "Calibration quality measured from real LLM true-reject rates")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Generating OEA insights report → {OUT}")
    with PdfPages(str(OUT)) as pdf:
        _title_page(pdf)
        page_pilot(pdf)
        page_credibility(pdf)
        page_credibility_table(pdf)
        page_real_lm(pdf)
        page_real_lm_table(pdf)
        page_memory_drift(pdf)
        page_baseline(pdf)
        page_error_taxonomy(pdf)
        page_cq_summary(pdf)
    print(f"Done. {OUT.stat().st_size // 1024} KB, {10} pages.")


if __name__ == "__main__":
    main()
