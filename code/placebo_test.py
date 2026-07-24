#!/usr/bin/env python3
"""
Longitudinal Placebo (Pseudo-Event) Test (replication-package edition)
=====================================================================
SCIE Q1 empirical-robustness check #2 (parallel-trends / placebo validity).

Purpose
-------
The within-firm event-study compares a customer-behavior proxy (CFPB complaint
log-counts) before vs after a disclosed cyber incident. A threat is that the
proxy has spurious level shifts at arbitrary dates (seasonality, regulatory
churn, operational shocks). If the estimator "detects" a reaction at a date
where NO hack occurred, the design is not credible.

Mechanism
---------
For each financial-servicer firm we compute the within-firm pre/post
log-difference in mean complaint counts:
    delta(firm, anchor) = mean(log count | post(anchor)) - mean(log count | pre(anchor))
anchored at (i) the TRUE detection date and (ii) a PLACEBO anchor shifted
exactly -1 year (secondary: -2 quarters). Conservative binding rule: the
larger-magnitude placebo shift; STRONG PASS / MARGINAL / FAIL / NULL.

Paths are repo-relative. Run:
    python3 code/placebo_test.py

Input : data/cfpb_construct_validity.csv  (produced by cfpb_construct_validity_extractor.py)
Output: data/placebo_test_results.txt
"""
from __future__ import annotations
import os
import sys
import math
import datetime as dt
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CSV_IN = DATA_DIR / "cfpb_construct_validity.csv"
TXT_OUT = DATA_DIR / "placebo_test_results.txt"


def quarter_start_date(qlabel):
    y, qn = int(qlabel[:4]), int(qlabel[-1])
    return dt.date(y, qn * 3 - 2, 1)


def event_month_date(event_iso):
    ev = dt.date.fromisoformat(event_iso)
    return dt.date(ev.year, ev.month, 1)


def shift_iso(iso, years=0, quarters=0):
    ev = dt.date.fromisoformat(iso)
    total = ev.year * 12 + (ev.month - 1) - years * 12 - quarters * 3
    ny, nm0 = divmod(total, 12)
    return f"{ny:04d}-{nm0 + 1:02d}-01"


def mean_log(series):
    s = [math.log(c) for c in series if c and c > 0]
    return float(np.mean(s)) if s else float("nan")


def pre_post_delta(df_firm, anchor_iso):
    anchor_m = event_month_date(anchor_iso)
    pre, post = [], []
    for _, r in df_firm.iterrows():
        qs = quarter_start_date(r["quarter"])
        cnt = int(r["total_count"])
        (post if qs >= anchor_m else pre).append(cnt)
    if not pre or not post:
        return float("nan"), len(pre), len(post)
    return mean_log(post) - mean_log(pre), len(pre), len(post)


def main():
    if not CSV_IN.exists():
        sys.exit(f"ERROR: input not found: {CSV_IN}\nRun cfpb_construct_validity_extractor.py first.")
    df = pd.read_csv(CSV_IN)
    L = []
    A = L.append
    A("=" * 72)
    A("LONGITUDINAL PLACEBO (PSEUDO-EVENT) TEST  --  SCIE Q1 robustness check #2")
    A("=" * 72)
    A(f"Run: {dt.date.today().isoformat()}")
    A("Design: within-firm pre/post log-difference in CFPB complaint counts,")
    A("        compared at the TRUE event anchor vs a PLACEBO anchor shifted -1y (-2q secondary).")
    A(f"Input: {CSV_IN.relative_to(ROOT)}")
    A("")
    A("Data scope: financial sub-panel only (Mr. Cooper, loanDepot, Navient).")
    A("Mr. Cooper right-censored at 2025Q4. Navient real event 2026-06-08 has only a partial 2026Q2 post-quarter.")
    A("")
    A("-" * 72)
    A(f'{"Firm":<10}{"Anchor":<14}{"pre_n":>6}{"post_n":>7}{"dlog":>10}{"note":<24}')
    A("-" * 72)

    summary = []
    for firm in ["MrCooper", "loanDepot", "Navient"]:
        sub = df[df["firm"] == firm].copy()
        if sub.empty:
            A(f"{firm:<10}  -- no CFPB data --")
            continue
        event_iso = str(sub["event_date"].iloc[0])
        d_true, n1, m1 = pre_post_delta(sub, event_iso)
        p1y = shift_iso(event_iso, years=1);  d_p1, n2, m2 = pre_post_delta(sub, p1y)
        p2q = shift_iso(event_iso, quarters=2); d_p2, n3, m3 = pre_post_delta(sub, p2q)
        note = "censored 2025Q4" if firm == "MrCooper" else ("post~0 (recency)" if firm == "Navient" else "")

        def f(x):
            return f"{x:+.4f}" if (isinstance(x, float) and not math.isnan(x)) else "   nan"

        A(f'{firm:<10}{"TRUE":<14}{n1:>6}{m1:>7}{f(d_true):>10}{note:<24}')
        A(f'{"":<10}{p1y+" (-1y)":<14}{n2:>6}{m2:>7}{f(d_p1):>10}{"placebo":<24}')
        A(f'{"":<10}{p2q+" (-2q)":<14}{n3:>6}{m3:>7}{f(d_p2):>10}{"placebo (secondary)":<24}')
        A("-" * 72)
        summary.append((firm, event_iso, d_true, d_p1, d_p2, n1, m1))

    A("")
    A("PLACEBO VERDICT (per firm) -- conservative: binding = larger-magnitude placebo")
    A("-" * 72)
    for (firm, ev, dt_, dp1, dp2, npre, npost) in summary:
        if math.isnan(dt_) or npost < 2:
            A(f"{firm}: NOT INTERPRETABLE -- true-event post-window has {npost} quarter(s).")
            if firm == "Navient":
                A("         Navient event (2026-06-08) too recent; placebo cannot adjudicate parallel trends.")
            continue
        denom = abs(dt_)
        if denom < 0.05:
            A(f"{firm}: true dlog={dt_:+.4f} | placebo(-1y)={dp1:+.4f}, (-2q)={dp2:+.4f} -> NULL")
            A("         True-event log-shift negligible (<0.05): no measurable event reaction.")
            continue
        pmax = max(abs(dp1) if not math.isnan(dp1) else 0.0,
                   abs(dp2) if not math.isnan(dp2) else 0.0)
        verdict = "FAIL" if pmax >= denom else ("MARGINAL" if pmax >= 0.5 * denom else "STRONG PASS")
        A(f"{firm}: true dlog={dt_:+.4f} | placebo(-1y)={dp1:+.4f}, (-2q)={dp2:+.4f} "
          f"| placebo_max={pmax:.4f} -> {verdict}")
        if verdict == "FAIL":
            A("         A no-hack date produces a shift >= the true-event shift; date-invariant")
            A("         trend/operational variance dominates; event-specificity not isolated.")
        elif verdict == "MARGINAL":
            A("         A no-hack date produces a non-trivial shift (50-100% of true); weak specificity.")
    A("-" * 72)
    A("")
    A("INTERPRETATION: a post-event shift NOT clearly larger than the placebo shift")
    A("indicates the CFPB series carries substantial non-event variance. Consistent with")
    A("the construct-validity finding (general-dissatisfaction proxy). Bounds -- but does")
    A("not overturn -- within-firm event-time use, provided effects are reported as bounded")
    A("directional evidence, not point estimates.")

    TXT_OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\nSaved -> {TXT_OUT}")


if __name__ == "__main__":
    main()
