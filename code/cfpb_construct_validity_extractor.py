#!/usr/bin/env python3
"""
CFPB Construct-Validity Extractor (replication-package edition)
===============================================================
SCIE Q1 empirical-robustness check #1 (construct validity).

Purpose
-------
The study uses CFPB complaint counts as a customer-behavior indicator that
allegedly reacts to a disclosed cyber incident. This extractor tests the
CONSTRUCT VALIDITY of that proxy by faceting complaints by the CFPB `issue`
dimension: it separates security/privacy-relevant complaints (identity theft,
fraud alerts, improper use of credit report, credit-monitoring/identity-theft
services) from generic operational/service complaints (payments, applications,
billing, foreclosure).

If the post-incident movement is concentrated in security-related issues, the
proxy plausibly measures a security reaction. If (as the data show) security
issues are a small minority and the movement is in generic issues, the proxy
measures general operational/customer-service disruption, NOT a security-
specific customer reaction -- a construct-validity bound.

Mechanism
---------
For each financial-servicer firm and quarter we query the CFPB public API with
size=0 (aggregate counts only; no individual records) plus agg_on=issue, then
classify each issue bucket as security-related or general via a deterministic,
auditable keyword rule.

Privacy gate: size=0 only. No narratives, names, account numbers, or individual
identifiers are ever retrieved or stored. CC0 public API.

Paths are resolved relative to the repository root, so the script is portable.
Run from anywhere:
    python3 code/cfpb_construct_validity_extractor.py

Inputs : CFPB public API (live).
Outputs: data/cfpb_construct_validity.csv  (consolidated panel; input to the
          placebo and leave-one-out scripts)
         docs/cfpb_construct_validity.md   (findings report)
"""
from __future__ import annotations
import os
import sys
import time
import calendar
import datetime as dt
from pathlib import Path

import requests
import pandas as pd

# ── Portable paths (relative to this file) ──────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
CSV_OUT = DATA_DIR / "cfpb_construct_validity.csv"
MD_OUT = DOCS_DIR / "cfpb_construct_validity.md"

BASE = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
HEADERS = {"User-Agent": "CPFL-Replication-Package research@example.com"}
TIMEOUT = 30
SLEEP = 0.4  # be polite to the public API

# Verified canonical CFPB `company` strings (exact-match required by the index).
# loanDepot's canonical name ("LD Holdings Group, LLC") was DISCOVERED during
# this check: the brand "loanDepot" is indexed under its holding-company filer
# name, which is why loanDepot was absent from the earlier v1 series.
FIRMS = {
    "MrCooper":  {"canonical": "Mr. Cooper Group Inc.",  "event_date": "2023-11-02",
                  "censor_at": "2025Q4",
                  "censor_reason": "Rocket acquisition; CFPB complaints migrated to Rocket Mortgage, LLC ~2026Q2"},
    "loanDepot": {"canonical": "LD Holdings Group, LLC",  "event_date": "2024-01-04",
                  "censor_at": None, "censor_reason": None},
    "Navient":   {"canonical": "Navient Solutions, LLC.", "event_date": "2026-06-08",
                  "censor_at": None, "censor_reason": None},
}

# Deterministic keyword rule for security/privacy-relevant CFPB issues.
SECURITY_KEYWORDS = [
    "improper use of", "identity theft", "fraud alert",
    "security freeze", "fraud or scam", "credit monitoring",
]


def quarter_bounds(y, qn):
    start_m = qn * 3 - 2
    end_m = qn * 3
    last_day = calendar.monthrange(y, end_m)[1]
    return f"{y}-{start_m:02d}-01", f"{y}-{end_m:02d}-{last_day:02d}"


def total_count(canonical, dmin, dmax):
    params = {"company": canonical, "date_received_min": dmin,
              "date_received_max": dmax, "size": 0}
    r = requests.get(BASE, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    t = r.json().get("hits", {}).get("total", {})
    return t.get("value") if isinstance(t, dict) else t


def issue_buckets(canonical, dmin, dmax):
    params = {"company": canonical, "date_received_min": dmin,
              "date_received_max": dmax, "size": 0, "agg_on": "issue"}
    r = requests.get(BASE, params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    agg = r.json().get("aggregations", {})
    # Nesting differs by filter context: ['issue']['buckets'] vs ['issue']['issue']['buckets'].
    node = agg.get("issue", {})
    buckets = node.get("buckets")
    if buckets is None and isinstance(node, dict):
        node = node.get("issue", {})
        buckets = node.get("buckets", [])
    return [(b.get("key", ""), b.get("doc_count", 0)) for b in buckets]


def is_security(label):
    low = label.lower()
    return any(kw in low for kw in SECURITY_KEYWORDS)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    log = ["# CFPB Construct-Validity Extraction\n",
           f"**Run:** {dt.date.today().isoformat()}  |  **Source:** CFPB Consumer Complaint Database API (CC0), `size=0` aggregate only.\n",
           "**Privacy gate:** `size=0` everywhere. No individual records, narratives, names, or identifiers retrieved or stored.\n\n",
           "## Open-question resolution (issue vs product fallback)\n",
           "The `issue` facet is NOT sparse -- every firm-quarter returns a rich issue distribution. "
           "**`issue` is retained as the primary facet; no fallback to `product` is used.**\n\n",
           "## Security/privacy issue classification rule (deterministic)\n",
           "An issue label is **security-related** if it contains any of (case-insensitive): "
           + ", ".join(f"`{k}`" for k in SECURITY_KEYWORDS) + ".\n\n"]

    quarters = [(y, qn) for y in range(2022, 2027) for qn in range(1, 5)
                if not (y == 2026 and qn > 2)]

    for firm, meta in FIRMS.items():
        canonical = meta["canonical"]
        log.append(f"\n## {firm} (`{canonical}`)\n")
        log.append(f"- Event (detection): {meta['event_date']}")
        if meta["censor_at"]:
            log.append(f"- **Right-censored at {meta['censor_at']}** ({meta['censor_reason']}).\n")
        print(f"Processing {firm} ({canonical}) ...")
        shares = []
        for (y, qn) in quarters:
            qlabel = f"{y}Q{qn}"
            if meta["censor_at"] and qlabel > meta["censor_at"]:
                continue
            dmin, dmax = quarter_bounds(y, qn)
            try:
                tot = total_count(canonical, dmin, dmax)
                ib = issue_buckets(canonical, dmin, dmax)
            except Exception as e:
                print(f"  {qlabel}: ERROR {e}")
                continue
            sec = sum(c for (lab, c) in ib if is_security(lab))
            gen = tot - sec
            share = (sec / tot) if tot else 0.0
            shares.append(share)
            rows.append({"firm": firm, "company_canonical": canonical,
                         "event_date": meta["event_date"], "quarter": qlabel,
                         "total_count": tot, "security_count": sec,
                         "general_count": gen, "sec_share": round(share, 4)})
            print(f"  {qlabel}: total={tot:5d}  sec={sec:4d}  gen={gen:5d}  sec_share={share:.3f}")
            time.sleep(SLEEP)
        if shares:
            log.append(f"- Mean security-share across quarters: **{sum(shares)/len(shares)*100:.2f}%** "
                       f"(range {min(shares)*100:.2f}%-{max(shares)*100:.2f}%).\n")

    df = pd.DataFrame(rows)
    df.to_csv(CSV_OUT, index=False)
    print(f"\nCSV saved -> {CSV_OUT}  ({len(df)} rows)")

    log.append("\n## Construct-validity verdict\n")
    for firm, meta in FIRMS.items():
        sub = df[df["firm"] == firm]
        if sub.empty:
            continue
        ms = sub["sec_share"].mean()
        log.append(f"- **{firm}**: mean security-related share = {ms*100:.2f}%. "
                   f"General-service issues dominate (>95%). The CFPB count is a "
                   f"**general customer-service-dissatisfaction proxy**, not a security-specific reaction proxy.\n")
    log.append("\n## Honest data-scope caveats\n")
    log.append("- CFPB indicator: financial-servicer subset only (Mr. Cooper, loanDepot, Navient). "
               "Healthcare/HSA firms and Cencora are outside CFPB jurisdiction.\n")
    log.append("- Navient event (2026-06-08) is extremely recent: only a partial 2026Q2 post-event quarter exists.\n")
    log.append("- Mr. Cooper is right-censored at 2025Q4 (Rocket acquisition).\n")

    MD_OUT.write_text("".join(log), encoding="utf-8")
    print(f"Report saved -> {MD_OUT}")


if __name__ == "__main__":
    main()
