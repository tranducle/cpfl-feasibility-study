# CPFL Figure Provenance Record

**Generated:** 2026-07-23
**Gate status:** BOUND (v3.1 carry-forward, D008)
**Permitted scope:** descriptive / feasibility-grade figures only

## Figure 1 — Policy adaptation composite by event window

| Field | Value |
|---|---|
| File | `figures/fig_policy_composite.pdf` (+ `.png`) |
| Script | `figures/generate_figures.py` → `generate_fig1_policy_composite()` |
| Data source | `4_Data_Pilot/policy_coded_pairs.csv` (20 rows, real coded pairs) |
| Plot type | Horizontal lollipop / strip plot |
| X-axis | Policy-adaptation composite (0–1 scale) |
| Y-axis | Pair ID grouped by firm, marker shape by window |
| Colors | Colorblind-aware palette (Okabe-Ito) per firm |
| Markers | Circle=pre, Diamond=boundary, Triangle=post |
| Evidence claim | 16/20 pairs have zero composite; 4/4 event-boundary pairs have zero composite |
| Claim discipline | Descriptive only; no trend, no CI, no estimation; BOUND-compliant |
| Manuscript section | §6.2 Descriptive policy variation and event-boundary result |

## Figure 2 — CFPB aggregate complaint counts over time

| Field | Value |
|---|---|
| File | `figures/fig_cfpb_timeseries.pdf` (+ `.png`) |
| Script | `figures/generate_figures.py` → `generate_fig2_cfpb_timeseries()` |
| Data source | `4_Data_Pilot/cfpb_firm_quarter_counts.csv` (36 rows, 18 quarters × 2 firms) |
| Plot type | Dual line plot (raw data, no fitted trend) |
| X-axis | Quarter (2022Q1–2026Q2) |
| Y-axis | Aggregate complaint count (unnormalized volume proxy) |
| Lines | Navient (sky blue), Mr. Cooper (pink) |
| Annotations | Mr. Cooper event (Oct 2023, dashed line); merger censor (2026Q1, dotted line); Navient pre-event spike |
| Evidence claim | Within-firm temporal variation in complaint volume; no common denominator |
| Claim discipline | Descriptive only; no trend line, no regression, no CI; BOUND-compliant |
| Manuscript section | §6.2 Descriptive policy variation (customer indicators paragraph) |

## Gate compliance

- **SCIE Q1 evidence gate:** BOUND (v3.1 carry-forward). Point estimation BLOCKED.
- **Permitted:** Descriptive visualization of raw pilot data.
- **Prohibited:** Fitted trends, confidence intervals, regression lines, effect-size markers, interpolated values, smoothed curves.
- **Privacy:** CFPB data are aggregate counts (`size=0` queries); no individual records, narratives, or identifiers plotted or stored.

## Reproducibility

```bash
cd Papers/CUSTOMER-BEHAVIOR
python3 7_Manuscript_Draft/figures/generate_figures.py
```

This script reads only the two verified CSV files listed above and produces
both figures. No external data, no network calls, no random seeds.
