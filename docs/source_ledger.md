# Public Archival Pilot Source Ledger

**Retrieval date:** 2026-07-23  
**Pilot scope:** metadata and direct public-record accessibility only; no personal complaint text collected.

## Verified infrastructure

| Source | URL | Observed evidence | Grade | Limitation |
|---|---|---|---|---|
| SEC submissions JSON | `https://data.sec.gov/submissions/CIK##########.json` | Programmatic company filing metadata, forms, dates, accession numbers, item codes, primary documents | verified_portal + metadata | Item 8.01 is broad; record content must be checked individually |
| SEC filing documents | `https://www.sec.gov/Archives/edgar/data/...` | Direct documents retrieved with an identifying academic User-Agent for UnitedHealth, Microsoft, HealthEquity, loanDepot | verified_record for 3 cyber-keyword checks; one candidate ambiguous | Bulk access must follow SEC fair-access policy |
| CFPB Complaint Database API | `https://cfpb.github.io/ccdb5-api/` | API documentation confirms JSON/CSV/XLS/XLSX search; daily updates; company/date/response fields; narratives de-identified before publication | verified_portal | Coverage emphasizes CFPB-regulated companies and excludes some institutions |
| CFPB company query | `https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?company=loanDepot&size=0` | Response returned successfully (large JSON), demonstrating company-filtered public access | verified_record/access | Detailed count parsing deferred; company-size normalization required |
| Internet Archive / UnitedHealthcare | `https://web.archive.org/web/20240201000000/https://www.uhc.com/privacy` | Resolved to 2024-02-03 capture; toolbar reported 352 captures (2004-08-10 to 2026-07-21); policy content and effective date observed | verified_record | One firm/URL only; capture counts do not prove usable quarterly diffs |
| Internet Archive / loanDepot candidate URL | `https://web.archive.org/web/20240101000000/https://www.loandepot.com/privacy-policy` | Returned 404 | not_found for checked path | Other historical URLs may exist; URL discovery required |

## Firm-level SEC checks

| Firm | CIK | Candidate event metadata observed | Record-level content status |
|---|---:|---|---|
| UnitedHealth | 0000731766 | 2024-02-22, Item 1.05 | cyber wording detected |
| HealthEquity | 0001428336 | 2024-07-02, Item 8.01 | cybersecurity wording detected |
| loanDepot | 0001831631 | 2024-01-08, Item 8.01 | cyber/unauthorized wording detected |
| Mr. Cooper | 0000933136 | 2023-11-02, Item 8.01 | cybersecurity/cyber-incident/security-incident wording detected |
| Clorox | 0000021076 | 2023-08-14 and 2023-09-18, Item 8.01 | cybersecurity/unauthorized-activity wording detected in both checked filings |
| MGM Resorts | 0000789570 | 2023-11-08, Item 8.01 | document retrieved; simple cyber-keyword test inconclusive |
| Caesars | 0000858339 | no recent 8-K rows returned under checked CIK | event source not verified; CIK/entity mapping requires review |
| Microsoft | 0000789019 | 2024-01-19, Item 1.05 | cyber wording detected |

## Evidence grading rule

- `verified_record`: a direct firm-level record or query response was observed.
- `verified_portal`: source/API capability was observed, not necessarily firm-level coverage.
- `candidate_source`: plausible source named but no repeated firm-level records verified.
- `blocked`: technical/access limitation prevented verification.
- `not_found`: checked route produced no candidate record; this is not proof of absence.

## Integrity notes

- Item 1.05 is cyber-specific; Item 8.01 is not, so keyword/content review is mandatory.
- SEC data showed future/current 2026 filings because the environment date is 2026-07-23; the intended causal panel window must be fixed prospectively.
- SEC accessibility does not establish archived policy outcome or customer-state coverage.
