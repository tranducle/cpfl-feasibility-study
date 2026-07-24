# CPFL Data Dictionary — Final

**Manuscript:** Customer-Policy Feedback Loop (CPFL)
**Last updated:** 2026-07-23
**Gate status:** BOUND (v3.1 carry-forward)

---

## Core variables used in the manuscript

### Panel identifiers

| Variable | Type | Source | Unit | Description |
|----------|------|--------|------|-------------|
| `firm` | string | SEC CIK + entity crosswalk | firm | Stable firm identifier (e.g., `MrCooper`, `UnitedHealth`) |
| `quarter` | string | Derived from filing date | firm-quarter | Calendar quarter in `YYYYQN` format (e.g., `2024Q1`) |
| `sector` | category | SEC profile / author coding | firm | Sector classification: financial services, healthcare, fintech |

### Event timing

| Variable | Type | Source | Unit | Description |
|----------|------|--------|------|-------------|
| `event_date` | date | SEC 8-K Item 1.05 or 8.01 | firm | Date of detection or awareness disclosure; **not** intrusion onset |
| `event_item` | string | SEC 8-K | firm | Filing item code: `1.05` (cybersecurity) or `8.01` (other event) |
| `intrusion_onset` | date | — | firm | **Not available** for any pilot firm; blocked by gate |
| `postwin` | binary | Derived | pair/quarter | 1 = post-event window; 0 = pre-event |

### Policy outcome (Internet Archive)

| Variable | Type | Source | Unit | Range | Description |
|----------|------|--------|------|-------|-------------|
| `RET` | binary | Coded from archived privacy page | pair | 0–1 | Retention-language change |
| `NOT` | binary | Coded from archived privacy page | pair | 0–1 | Notification-language change |
| `SEC` | binary | Coded from archived privacy page | pair | 0–1 | Security-language change |
| `SHR` | binary | Coded from archived privacy page | pair | 0–2 | Sharing-language change (0, 1, or 2) |
| `ACC` | binary | Coded from archived privacy page | pair | 0–1 | Access-language change |
| `SCOPE` | ordinal | Coded | pair | 0–2 | Breadth of change (0 = none, 1 = narrow, 2 = broad) |
| `composite_A` | continuous | Derived: (RET+NOT+SEC+SHR+ACC)/15 | pair | 0–1 | Policy-adaptation composite |
| `sim` | continuous | Computed (cosine/Jaccard) | pair | 0–1 | Raw text similarity (before cleaning); **not** the coded outcome |
| `direction` | ordinal | Coded | pair | integer | Direction of change flag |
| `event_ref` | binary | Coded | pair | 0–1 | Whether the coded change explicitly references the breach event |

### Customer indicator 1: CFPB complaint counts

| Variable | Type | Source | Unit | Description |
|----------|------|--------|------|-------------|
| `complaint_count` | integer | CFPB API (`size=0`) | firm-quarter | Aggregate complaint count; **no** individual records |
| `company_canonical` | string | CFPB API | firm | Exact indexed company name (e.g., `Navient Solutions, LLC.`) |
| `date_received_min` | date | CFPB API | firm-quarter | Earliest complaint date in quarter |
| `date_received_max` | date | CFPB API | firm-quarter | Latest complaint date in quarter |

**Privacy note:** `size=0` queries return only the count; no narratives, names, or identifiers.

### Customer indicator 2: 10-Q disclosure intensity

| Variable | Type | Source | Unit | Description |
|----------|------|--------|------|-------------|
| `filing_date` | date | SEC EDGAR | filing | 10-Q filing date |
| `accession` | string | SEC EDGAR | filing | SEC accession number |
| `doc` | string | SEC EDGAR | filing | Primary document filename |
| `doc_chars` | integer | Computed | filing | Total document character count |
| `cust_sec_sentences` | integer | Deterministic keyword rule | filing | Sentences containing both customer-population and security terms |
| `incident_flag` | binary | Deterministic rule | filing | 1 = filing mentions a specific incident |
| `intensity_0_3` | ordinal | Derived from `cust_sec_sentences` | filing | 0 = none, 1 = low (1–3), 2 = moderate (4–6), 3 = high (7+) |

### MDE / power inputs

| Variable | Type | Source | Description |
|----------|------|--------|-------------|
| `policy_residual_sd` | float | Computed from `policy_coded_pairs.csv` | Firm-demeaned policy residual SD ≈ 0.0504 |
| `cfpb_logcount_sd` | float | Computed from `cfpb_firm_quarter_counts.csv` | Mean within-firm CFPB log-count SD ≈ 0.369 |
| `mde_range` | float | Formula-based | 0.068–0.096 under assumed N_eff = 16–32 |

### Robustness artifacts (CFPB customer-indicator diagnostics)

| Artifact | Path | Check | Description |
|----------|------|-------|-------------|
| `cfpb_construct_validity.csv` / `cfpb_construct_validity.md` | `data/` , `docs/` | Construct validity | Per firm-quarter total vs security-related complaint counts and security share; loanDepot canonical name (`LD Holdings Group, LLC`) resolved here |
| `placebo_test_results.txt` | `data/` | Longitudinal placebo | Within-firm pre/post log-diff at true vs −1y/−2q pseudo-event anchors |
| `loo_sensitivity.csv` / `loo_sensitivity_report.txt` | `data/` | Leave-one-out | Pooled effect recomputed dropping each firm; degenerate at N=2 estimable firms |

**Scope:** financial sub-panel only (Mr. Cooper, loanDepot, Navient). Healthcare/HSA firms and Cencora are outside CFPB jurisdiction. These are proxy-level diagnostics (no λ coefficient); reproducible via `code/cfpb_construct_validity_extractor.py` → `code/placebo_test.py` → `code/leave_one_out_analysis.py`.

---

## Measurement status vocabulary

| Status | Meaning |
|--------|---------|
| `point_identified` | Assumptions and scales support a structural point estimate |
| `partially_identified` | Credible bounds or identified set only |
| `composite_only` | Observed proxy composite; no latent structural interpretation |
| `unresolved` | Scale, construct, timing, or support is missing |

**Current terminal status:** BOUND — all empirical constructs are `composite_only` or `unresolved`; no `point_identified` or `partially_identified` constructs exist in the present pilot.

---

## Privacy gate

- CFPB queries used `size=0` aggregate mode exclusively.
- No individual complaint records, narratives, consumer names, account data, or identifiers were collected, stored, or processed.
- SEC and Internet Archive data are public corporate filings and public web pages.
- No human subjects, surveys, or experiments were conducted.
