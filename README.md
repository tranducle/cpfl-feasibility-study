# CPFL Feasibility Study — Replication Package

> **Anonymous replication package for double-blind review.**
> All data are derived exclusively from public sources.

## Overview

This repository contains the data and code for a bounded public-data
feasibility study of **customer-conditioned cybersecurity policy
adaptation**. The study asks whether observable cybersecurity-policy
adjustment can be studied as a response to lagged customer state using
publicly available archival data, and establishes the measurement
boundary conditions under which such analysis is — and is not —
possible.

The paper contributes:

1. A **verified local-quadratic benchmark** for the expected excess
   loss of ignoring customer state:
   ΔL = (κ/2) β² Var(b).
2. A **gated feasibility protocol** joining SEC event filings, aggregate
   CFPB complaint counts, Internet Archive privacy-page snapshots, a
   deterministic 10-Q disclosure indicator, and minimum-detectable-effect
   discipline.
3. An **event-boundary null**: across 20 coded privacy-page pairs from
   four firms, 16 receive a zero adaptation composite, and all four
   selected event-boundary pairs score zero after archive-noise
   filtering.

---

## Data Sources

All data are drawn from three **public, openly accessible** sources.
No proprietary, restricted, or personal data were collected.

| Source | URL | What was retrieved |
|--------|-----|--------------------|
| SEC EDGAR | https://www.sec.gov/edgar.shtml | 8-K Items 1.05/8.01 (event dates); 10-Q filings (disclosure indicator) |
| CFPB Consumer Complaint Database | https://www.consumerfinance.gov/data-research/consumer-complaints/ | Firm-level aggregate quarterly complaint counts (`size=0` queries only) |
| Internet Archive Wayback Machine | https://web.archive.org/ | Monthly snapshots of public privacy-policy pages |

**Retrieval date:** 2026-07-23

**Privacy:** CFPB queries used `size=0` aggregate mode exclusively.
No individual complaint records, narratives, consumer names, account
numbers, or personal identifiers were collected, stored, or processed.

---

## Repository Structure

```
cpfl-feasibility-study/
├── README.md                    ← this file
├── LICENSE                      ← MIT License
├── .gitignore
│
├── data/
│   ├── cfpb_firm_quarter_counts.csv      ← 18-quarter aggregate complaints (2 firms)
│   ├── cfpb_construct_validity.csv       ← issue-faceted complaints: total vs security-related (3 firms) [NEW]
│   ├── tenq_customer_disclosure.csv      ← 77 filing-level disclosure scores (6 firms)
│   ├── policy_coded_pairs.csv            ← 20 coded snapshot-pair composites (4 firms)
│   ├── wayback_snapshot_matrix.csv       ← Internet Archive capture availability
│   ├── mde_inputs_computed.json          ← MDE/power planning inputs
│   ├── placebo_test_results.txt          ← longitudinal placebo (pseudo-event) results [NEW]
│   ├── loo_sensitivity.csv               ← leave-one-out outlier sensitivity [NEW]
│   ├── loo_sensitivity_report.txt        ← leave-one-out findings report [NEW]
│   └── policy_raw/                       ← 42 raw archived privacy-page snapshots
│       ├── *.txt                         ← playback text content
│       ├── cdx_*.json                    ← CDX API metadata per firm
│       └── pair_briefs_clean.json        ← cleaned pair-level briefs
│
├── code/
│   ├── generate_figures.py               ← reproducible figure generation (matplotlib)
│   ├── fig_gate_matrix.tex               ← feasibility-gate matrix figure (TikZ standalone) [NEW]
│   ├── cfpb_construct_validity_extractor.py  ← construct-validity CFPB extraction (size=0) [NEW]
│   ├── placebo_test.py                  ← longitudinal placebo (pseudo-event) check [NEW]
│   └── leave_one_out_analysis.py         ← leave-one-out outlier sensitivity [NEW]
│
└── docs/
    ├── data_dictionary.md                ← variable definitions, units, sources
    ├── source_ledger.md                  ← URL-level provenance with evidence grading
    ├── entity_crosswalk.md               ← SEC CIK → brand → operating unit mapping
    ├── policy_diff_codebook.md           ← six-dimensional coding rule definitions
    ├── evidence_gate_verdict.md          ← terminal BOUND gate verdict
    ├── figure_provenance.md              ← figure-to-data traceability
    └── cfpb_construct_validity.md        ← construct-validity findings report [NEW]
```

---

## Reproducing the Figures

```bash
# Requires: Python 3.10+, matplotlib

cd code
python3 generate_figures.py
```

This script reads the CSV files in `data/` and produces two
publication-quality vector figures:

- `fig_policy_composite.pdf` — policy-adaptation composite for 20 pairs
- `fig_cfpb_timeseries.pdf` — CFPB complaint counts over time

No trend lines, confidence intervals, regression, or estimation are
applied. All figures are descriptive/feasibility-grade.

---

## Robustness Diagnostics (CFPB Customer Indicator)

Although the primary policy-outcome coefficient is **not** estimated (the
feasibility gate fails at the estimand level), the CFPB customer-behavior
proxy itself can be stress-tested. Three pre-registered robustness checks
are provided for the financial-servicer subset (Mr. Cooper, loanDepot,
Navient); the remaining pilot firms are outside CFPB jurisdiction. These
characterize the **proxy**, not the estimand — they produce no
coefficient and reinforce the BOUND verdict.

```bash
# Requires: Python 3.10+, pandas, numpy, requests (extractor only)
# Pipeline: extractor (live CFPB API) -> placebo + leave-one-out (read the CSV)

python3 code/cfpb_construct_validity_extractor.py   # queries CFPB size=0; writes data/ + docs/
python3 code/placebo_test.py                        # reads data/cfpb_construct_validity.csv
python3 code/leave_one_out_analysis.py              # reads data/cfpb_construct_validity.csv
```

| Check | What it tests | Result |
|-------|---------------|--------|
| **Construct validity** (`cfpb_construct_validity_extractor.py`) | Whether complaint counts measure a *security* reaction vs generic service dissatisfaction (issue facet) | Security-related issues are only 2–7% of complaints → CFPB is a **general-dissatisfaction** proxy. loanDepot uniquely shows a post-event security-share rise (5.6% → 13–16%). |
| **Longitudinal placebo** (`placebo_test.py`) | Whether the proxy isolates an event-specific reaction (true date vs −1y/−2q pseudo-events) | Mr. Cooper **FAIL** (placebo shift ≥ true); loanDepot **NULL** (no measurable reaction); Navient not interpretable (no post-event data). |
| **Leave-one-out** (`leave_one_out_analysis.py`) | Whether a single firm drives the pooled effect | **Degenerate** — only 2 estimable firms; every LOO cell collapses to N=1. |

All scripts resolve paths relative to the repo root (portable; no
hardcoded machine paths). CFPB queries use `size=0` exclusively — no
individual complaint records are ever retrieved.

---

## Key Results

| Metric | Value |
|--------|-------|
| Firms in pilot | 6 |
| Layer-complete firms | 1 of 6 (Mr. Cooper, pre-merger) |
| Coded snapshot pairs | 20 (from 4 firms) |
| Zero adaptation composites | 16 of 20 |
| Event-boundary zero scores | 4 of 4 |
| Mean composite | 0.023 (SD 0.053) |
| Coding consistency | α_SCOPE = 0.833 (same-LLM double-pass, not human–human) |
| Gate verdict | **BOUND** — point estimation blocked |

---

## License

- **Source data:** Public records (U.S. government databases and public
  web archives). No restrictions.
- **Processed data and code:** Released under the MIT License.
