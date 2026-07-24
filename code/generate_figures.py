#!/usr/bin/env python3
"""
CPFL manuscript figure generator.

Generates two descriptive (feasibility-grade) figures from verified pilot
data artifacts.  No trend lines, no confidence intervals, no regression,
no estimation — only raw descriptive visualization permitted by the
BOUND gate verdict (v3.1 carry-forward, D008).

Figure 1: Policy adaptation composite by event window (20-pair strip plot)
Figure 2: CFPB aggregate complaint counts over time (dual line plot)

Data sources (real artifacts):
  4_Data_Pilot/policy_coded_pairs.csv   — 20 coded snapshot pairs
  4_Data_Pilot/cfpb_firm_quarter_counts.csv — 18 quarters × 2 firms

Output:
  figures/fig_policy_composite.pdf  + .png
  figures/fig_cfpb_timeseries.pdf   + .png

Reproducibility: this script is self-contained and reads only the two
CSV files listed above.  Run from the project root:
  python3 Papers/CUSTOMER-BEHAVIOR/7_Manuscript_Draft/figures/generate_figures.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# ── Publication style (colorblind-aware, IEEE/Elsevier-compatible) ──────────

COLORS = {
    "UnitedHealth": "#0072B2",  # blue
    "HealthEquity": "#E69F00",  # orange
    "loanDepot":    "#009E73",  # green
    "MrCooper":     "#CC79A7",  # pink
    "Navient":      "#56B4E9",  # sky blue
}

WINDOW_MARKERS = {
    "pre":      "o",   # circle
    "boundary": "D",   # diamond
    "post":     "^",   # triangle
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.5,
    "lines.linewidth": 1.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "figure.dpi": 600,
    "savefig.dpi": 600,
})

# ── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
PILOT_DIR  = SCRIPT_DIR.parent.parent / "4_Data_Pilot"
FIG_DIR    = SCRIPT_DIR

POLICY_CSV  = PILOT_DIR / "policy_coded_pairs.csv"
CFPB_CSV    = PILOT_DIR / "cfpb_firm_quarter_counts.csv"


# ── Figure 1: Policy adaptation composite strip plot ─────────────────────────

def generate_fig1_policy_composite() -> list[str]:
    """Lollipop / strip plot of 20 policy-pair composite scores."""
    rows = []
    with open(POLICY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # Sort: group by firm (alphabetical), then by pair_id within firm
    firm_order = ["UnitedHealth", "HealthEquity", "loanDepot", "MrCooper"]
    rows.sort(key=lambda r: (firm_order.index(r["firm"]), int(r["pair_id"])))

    n = len(rows)
    y_positions = list(range(n, 0, -1))  # top-to-bottom

    fig, ax = plt.subplots(figsize=(3.4, 3.2))

    for i, r in enumerate(rows):
        y = y_positions[i]
        comp = float(r["composite_A"])
        firm = r["firm"]
        window = r["window"]
        color = COLORS.get(firm, "#333333")
        marker = WINDOW_MARKERS.get(window, "s")

        # Lollipop stem
        ax.plot([0, comp], [y, y], color=color, linewidth=0.8, alpha=0.5, zorder=1)

        # Marker
        edge = "black" if window == "boundary" else color
        size = 5 if window == "boundary" else 4
        ax.scatter(comp, y, c=color, marker=marker, s=size**2,
                   edgecolors=edge, linewidths=0.5 if window == "boundary" else 0,
                   zorder=3)

    # Firm group labels on y-axis
    labels = []
    for r in rows:
        w = r["window"][0].upper()  # P/B/p
        labels.append(f"{r['firm'][:8]} #{r['pair_id']} ({w})")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=6.5)
    ax.set_xlabel("Policy-adaptation composite (0–1)", fontsize=8.5)
    ax.set_xlim(-0.01, 0.24)
    ax.axvline(0, color="grey", linewidth=0.5, linestyle="-", alpha=0.4)

    # Legend for window types
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="grey",
               markersize=5, label="Pre-event"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="grey",
               markeredgecolor="black", markersize=5, label="Event-boundary"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="grey",
               markersize=5, label="Post-event"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", framealpha=0.8,
              fontsize=7, handletextpad=0.3, borderpad=0.3)

    ax.set_title("")  # no title — caption carries text
    fig.tight_layout()

    outputs = []
    for ext in ("pdf", "png"):
        path = FIG_DIR / f"fig_policy_composite.{ext}"
        fig.savefig(path)
        outputs.append(str(path))
    plt.close(fig)
    return outputs


# ── Figure 2: CFPB aggregate complaint time series ────────────────────────────

def generate_fig2_cfpb_timeseries() -> list[str]:
    """Dual line plot of 18-quarter CFPB aggregate complaint counts."""
    rows = []
    with open(CFPB_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # Parse quarters to datetime for plotting
    def quarter_to_date(q: str) -> datetime:
        year, qnum = int(q[:4]), int(q[-1])
        month = (qnum - 1) * 3 + 1
        return datetime(year, month, 1)

    firms = {}
    for r in rows:
        firm = r["firm"]
        if firm not in firms:
            firms[firm] = {"dates": [], "counts": []}
        firms[firm]["dates"].append(quarter_to_date(r["quarter"]))
        firms[firm]["counts"].append(int(r["complaint_count"]))

    fig, ax = plt.subplots(figsize=(3.4, 2.4))

    for firm, data in firms.items():
        label = "Navient" if firm == "Navient" else "Mr. Cooper"
        color = COLORS.get(firm, "#333333")
        ax.plot(data["dates"], data["counts"], marker="o", markersize=3,
                linewidth=1.2, color=color, label=label, zorder=3)

    # Mark Mr. Cooper intrusion window (Oct 2023)
    mc_event = datetime(2023, 10, 1)
    ax.axvline(mc_event, color=COLORS["MrCooper"], linestyle="--",
               linewidth=0.8, alpha=0.6, zorder=1)
    ax.annotate("Mr. Cooper\nevent", xy=(mc_event, 1100), fontsize=6,
                color=COLORS["MrCooper"], ha="left", va="top",
                xytext=(5, 0), textcoords="offset points")

    # Mark Mr. Cooper censoring (2025Q4 = last clean pre-merger quarter)
    censor = datetime(2026, 1, 1)
    ax.axvline(censor, color=COLORS["MrCooper"], linestyle=":",
               linewidth=0.8, alpha=0.5, zorder=1)
    ax.annotate("merger\ncensor", xy=(censor, 600), fontsize=6,
                color=COLORS["MrCooper"], ha="left", va="top",
                xytext=(3, 0), textcoords="offset points")

    # Annotate Navient 2024Q2-Q3 pre-event spike
    ax.annotate("pre-event\nspike", xy=(datetime(2024, 7, 1), 1165),
                fontsize=6, color=COLORS["Navient"], ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points")

    ax.set_xlabel("Quarter", fontsize=8.5)
    ax.set_ylabel("Aggregate complaint count", fontsize=8.5)
    ax.set_ylim(-30, 1250)
    ax.legend(loc="upper left", framealpha=0.8, fontsize=7.5,
              handletextpad=0.4, borderpad=0.3)

    # Format x-axis as years
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate(rotation=0, ha="center")

    ax.set_title("")  # no title — caption carries text
    fig.tight_layout()

    outputs = []
    for ext in ("pdf", "png"):
        path = FIG_DIR / f"fig_cfpb_timeseries.{ext}"
        fig.savefig(path)
        outputs.append(str(path))
    plt.close(fig)
    return outputs


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating CPFL manuscript figures from verified pilot data...")
    print(f"  Policy CSV: {POLICY_CSV}")
    print(f"  CFPB CSV:   {CFPB_CSV}")

    out1 = generate_fig1_policy_composite()
    print(f"  Figure 1 (policy composite): {out1}")

    out2 = generate_fig2_cfpb_timeseries()
    print(f"  Figure 2 (CFPB time series): {out2}")

    print("Done. All figures are descriptive/feasibility-grade (BOUND gate compliant).")
    print("No trend lines, confidence intervals, regression, or estimation applied.")
