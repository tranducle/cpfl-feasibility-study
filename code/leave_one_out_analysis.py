#!/usr/bin/env python3
"""
Leave-One-Out (LOO) Outlier-Sensitivity Analysis (replication-package edition)
=============================================================================
SCIE Q1 empirical-robustness check #3 (case-study / outlier dominance).

Purpose
-------
The financial-servicer panel is very small (effectively 2-3 firms with usable
CFPB event-study windows). A central threat is that a single large firm drives
the entire conclusion. This analysis iteratively drops one firm at a time and
recomputes the pooled within-firm pre/post effect.

Mechanism
---------
1. d_f = mean(log count|post) - mean(log count|pre), per firm.
2. Pooled = equal-weight mean of d_f across usable firms.
3. LOO: drop each firm, recompute.
4. Report sensitivity (sign flip / collapse). With <=2 estimable firms every LOO
   cell collapses to N=1 -> reported as DEGENERATE (a structural finding).

Paths are repo-relative. Run:
    python3 code/leave_one_out_analysis.py

Input : data/cfpb_construct_validity.csv
Output: data/loo_sensitivity.csv , data/loo_sensitivity_report.txt
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
CSV_OUT = DATA_DIR / "loo_sensitivity.csv"
TXT_OUT = DATA_DIR / "loo_sensitivity_report.txt"


def quarter_start_date(qlabel):
    y, qn = int(qlabel[:4]), int(qlabel[-1])
    return dt.date(y, qn * 3 - 2, 1)


def mean_log(series):
    s = [math.log(c) for c in series if c and c > 0]
    return float(np.mean(s)) if s else float("nan")


def firm_delta(df_firm):
    ev = dt.date.fromisoformat(str(df_firm["event_date"].iloc[0]))
    anchor = dt.date(ev.year, ev.month, 1)
    pre, post = [], []
    for _, r in df_firm.iterrows():
        cnt = int(r["total_count"])
        (post if quarter_start_date(r["quarter"]) >= anchor else pre).append(cnt)
    if not pre or not post:
        return float("nan"), len(pre), len(post)
    return mean_log(post) - mean_log(pre), len(pre), len(post)


def main():
    if not CSV_IN.exists():
        sys.exit(f"ERROR: input not found: {CSV_IN}\nRun cfpb_construct_validity_extractor.py first.")
    df = pd.read_csv(CSV_IN)

    firm_deltas = []
    for firm in ["MrCooper", "loanDepot", "Navient"]:
        sub = df[df["firm"] == firm]
        d, npre, npost = firm_delta(sub)
        firm_deltas.append({"firm": firm, "d_f": d, "n_pre": npre,
                            "n_post": npost, "usable": (not math.isnan(d)) and npost >= 2})

    usable = [f["firm"] for f in firm_deltas if f["usable"]]
    n_usable = len(usable)
    pool_d = [f["d_f"] for f in firm_deltas if f["usable"]]
    full_mean = float(np.mean(pool_d)) if pool_d else float("nan")
    full_sd = float(np.std(pool_d, ddof=1)) if len(pool_d) > 1 else float("nan")

    rows = [{
        "scenario": "FULL_POOL", "firms_included": ";".join(usable), "n_firms": n_usable,
        "pooled_dlog_mean": round(full_mean, 4) if not math.isnan(full_mean) else "",
        "pooled_dlog_sd": round(full_sd, 4) if not math.isnan(full_sd) else "",
        "sign": ("+" if full_mean > 0 else "-") if not math.isnan(full_mean) else "NA",
        "note": "equal-weight mean of within-firm pre/post log-diffs",
    }]
    for f_drop in usable:
        keep = [g for g in usable if g != f_drop]
        kd = [x["d_f"] for x in firm_deltas if x["firm"] in keep]
        m = float(np.mean(kd)) if kd else float("nan")
        sd = float(np.std(kd, ddof=1)) if len(kd) > 1 else float("nan")
        rows.append({
            "scenario": f"LOO_drop_{f_drop}", "firms_included": ";".join(keep) if keep else "(none)",
            "n_firms": len(keep),
            "pooled_dlog_mean": round(m, 4) if not math.isnan(m) else "",
            "pooled_dlog_sd": round(sd, 4) if not math.isnan(sd) else "",
            "sign": ("+" if m > 0 else "-") if not math.isnan(m) else "NA",
            "note": f"dropped {f_drop}; remaining N={len(keep)}"
                    + (" (DEGENERATE: LOO collapses to N=1)" if len(keep) <= 1 else ""),
        })

    pd.DataFrame(rows).to_csv(CSV_OUT, index=False)

    L = []
    A = L.append
    A("=" * 72)
    A("LEAVE-ONE-OUT OUTLIER-SENSITIVITY ANALYSIS  --  SCIE Q1 robustness check #3")
    A("=" * 72)
    A(f"Run: {dt.date.today().isoformat()}")
    A(f"Input: {CSV_IN.relative_to(ROOT)}   Output: {CSV_OUT.relative_to(ROOT)}")
    A("")
    A("Per-firm within-firm pre/post log-difference (CFPB complaint counts):")
    A(f'{"Firm":<10}{"d_f":>10}{"n_pre":>7}{"n_post":>8}  usable')
    A("-" * 50)
    for f in firm_deltas:
        ds = f"{f['d_f']:+.4f}" if not math.isnan(f["d_f"]) else "   nan"
        A(f'{f["firm"]:<10}{ds:>10}{f["n_pre"]:>7}{f["n_post"]:>8}  {f["usable"]}')
    A("")
    A(f"Estimable firms in pool: {usable}  (N={n_usable})")
    A(f"Full-pool equal-weight mean d = {full_mean:+.4f}"
      + (f"  (across-firm SD = {full_sd:.4f})" if not math.isnan(full_sd) else ""))
    A("")
    A("SENSITIVITY VERDICT")
    A("-" * 72)
    if n_usable <= 2:
        A(f"DEGENERATE: only {n_usable} estimable firm(s). Every LOO cell collapses to N=1.")
        A("The panel is too small for the conclusion to be robust to single-firm removal.")
    signs = [r["sign"] for r in rows if r["pooled_dlog_mean"] != ""]
    if len(set(signs)) > 1:
        A("Sign of the pooled estimate CHANGES across LOO cells -> pooled direction is firm-driven.")
    else:
        A("Pooled sign stable across LOO cells, but with N<=2 this is mechanical, not robustness.")
    A("")
    A("Combined with the placebo test and the construct-validity finding, this LOO result is")
    A("consistent with the BOUND verdict: report CFPB-based findings as bounded directional /")
    A("feasibility-grade evidence, never as a robust point estimate.")

    TXT_OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\nCSV saved -> {CSV_OUT}")


if __name__ == "__main__":
    main()
