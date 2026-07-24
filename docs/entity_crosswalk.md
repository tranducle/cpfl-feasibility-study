# Brand / Subsidiary → SEC-Filer Entity Crosswalk

**Purpose:** map public-facing brands and operating subsidiaries to the SEC filer (CIK) so that archived policy pages, customer indicators, and SEC events attach to the correct panel unit. Verified against SEC EDGAR submissions JSON + company_tickers + EDGAR full-text search on 2026-07-23.

## Crosswalk

| Public brand / subsidiary | SEC filer (entity name) | CIK | Ticker | SIC | Relation | Crosswalk status | Risk |
|---|---|---|---|---|---|---|---|
| UnitedHealthcare / Change Healthcare | UnitedHealth Group Inc. | 0000731766 | UNH | Hospital & Medical Service Plans | parent / wholly-owned unit (Change Healthcare) | confirmed | event was on **Change Healthcare** (subsidiary) systems; policy page is on **uhc.com** (consumer brand) — the operating unit ≠ the filer ≠ the policy host |
| Cencora (post-Aug-2023) / AmerisourceBergen (legacy) | Cencora, Inc. | 0001140859 | COR | Wholesale-Drugs | renamed entity (same CIK) | confirmed | **2023 rebrand breaks the archived-URL chain**: pre-2023 policy pages live on amerisourcebergen.com; post-2023 on cencora.com |
| loanDepot | loanDepot, Inc. | 0001831631 | LDI | Finance Services | single filer/brand | confirmed | **CFPB canonical name = `LD Holdings Group, LLC`** (DISCOVERED 2026-07-24 during the construct-validity check; the brand "loanDepot" is indexed under its holding-company filer name). This is why loanDepot was absent from the v1 CFPB series (`data/cfpb_firm_quarter_counts.csv`). A full 2022Q1–2026Q2 series is now in `data/cfpb_construct_validity.csv`. SEC filer identity unchanged. |
| HealthEquity | HealthEquity, Inc. | 0001428336 | HQY | Services-Business Services NEC | single filer/brand | confirmed | none |
| Mr. Cooper / Nationstar | **"Maverick Merger Sub 2, LLC"** (current shell at CIK 933136) — historically "Mr. Cooper Group Inc." | 0000933136 | (deregistered) | Finance Services | **ACQUIRED by Rocket Companies, Inc. (CIK 0001805284, RKT)** | **RESOLVED — retained with cap** | RESOLVED 2026-07-23: joint 425 merger filings jointly name CIK 933136 + 0001805284 (Rocket); Form 15-12G deregistration filed 2025-10-14; CFPB complaints migrated from "Mr. Cooper Group Inc." to "Rocket Mortgage, LLC" ~March 2026 (monthly boundary: Dec25=267, Jan26=305, Feb26=198, Mar26=38, Apr26=0). **Retain Mr. Cooper as panel unit for 2022Q1–2025Q4 only** (event Oct-2023 → ~6 pre + ~9 post quarters before merger); right-censor at merger date. The Nov-2023 8-K cyber event was filed by the ORIGINAL Mr. Cooper Group — verified. |
| Navient / Navient Solutions | Navient Corporation | 0001593538 | (JSM in tickers map — verify) | Security Brokers/Dealers | parent / servicing subsidiary | confirmed-name | ticker mapping "JSM" in company_tickers is suspect; verify canonical ticker; Navient Solutions is the servicing sub |

## Crosswalk-derived panel-unit rule

1. The **panel unit is the SEC filer (CIK)**, but the **policy-outcome source URL** and the **customer-indicator record** may attach to a brand/subsidiary. Every observation must carry both `filer_cik` and `operating_brand`.
2. For UnitedHealth, the event is on Change Healthcare (subsidiary) while the policy page is UnitedHealthcare (consumer brand). The estimand is therefore *group-level policy response of the parent*, not Change-Healthcare-specific.
3. For Cencora, the rebrand means pre-event policy observations (if any) are on a different domain. Only **post-event** Cencora captures exist (6 months), so Cencora cannot supply pre/post policy diffs under the current URL chain.
4. For Mr. Cooper, **retain for 2022Q1–2025Q4** (pre-merger, clean CFPB + SEC + policy data); **right-censor at the Rocket acquisition (~Q1 2026 close)**. The Oct-2023 cyber event sits well inside the usable window. Do not extend Mr. Cooper observations past the merger date (CIK 933136 is now a deregistered merger-sub shell; post-merger complaints route to Rocket Mortgage, LLC).

## Entities excluded from the retained set (with reason)

- Microsoft (technology) — outside mortgage/financial + healthcare/fintech scope.
- Clorox (consumer goods) — outside scope.
- MGM Resorts / Caesars (hospitality) — outside scope; Caesars event source not found.
