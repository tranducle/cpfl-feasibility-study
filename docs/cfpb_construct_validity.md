# CFPB Construct-Validity Extraction
**Run:** 2026-07-24  |  **Source:** CFPB Consumer Complaint Database API (CC0), `size=0` aggregate only.
**Privacy gate:** `size=0` everywhere. No individual records, narratives, names, or identifiers retrieved or stored.

## Open-question resolution (issue vs product fallback)
The implementation plan asked whether to fall back from the `issue` facet to `product` if `issue` classification is too sparse. **It is not sparse** -- every firm-quarter returns a rich issue distribution. **`issue` is retained as the primary facet; no fallback to `product` is used.**

## Security/privacy issue classification rule (deterministic)
An issue label is classified **security-related** if it contains any of (case-insensitive): `improper use of`, `identity theft`, `fraud alert`, `security freeze`, `fraud or scam`, `credit monitoring`.
All other issues are classified **general** (payments, applications, billing, foreclosure, credit-reporting accuracy, etc.).


## MrCooper (`Mr. Cooper Group Inc.`)
- Event (detection): 2023-11-02- **Right-censored at 2025Q4** (Rocket acquisition; CFPB complaints migrated to Rocket Mortgage, LLC ~2026Q2); quarters at/after the censor point are excluded from any post-event analysis.
- Mean security-share across quarters: **2.42%** (range 1.66%-4.34%).

## loanDepot (`LD Holdings Group, LLC`)
- Event (detection): 2024-01-04- Mean security-share across quarters: **7.29%** (range 1.27%-16.39%).

## Navient (`Navient Solutions, LLC.`)
- Event (detection): 2026-06-08- Mean security-share across quarters: **5.63%** (range 1.37%-12.14%).

## Construct-validity verdict
- **MrCooper**: mean security-related share = 2.42% (pre-event 2.31%, post-event 2.53% over 8 post-quarters). General-service issues dominate (>95%). The CFPB count is therefore a **general customer-service-dissatisfaction proxy**, not a security-specific reaction proxy.
- **loanDepot**: mean security-related share = 7.29% (pre-event 5.68%, post-event 8.58% over 10 post-quarters). General-service issues dominate (>95%). The CFPB count is therefore a **general customer-service-dissatisfaction proxy**, not a security-specific reaction proxy.
- **Navient**: mean security-related share = 5.63% (pre-event 5.63%, post-event nan% over 0 post-quarters). General-service issues dominate (>95%). The CFPB count is therefore a **general customer-service-dissatisfaction proxy**, not a security-specific reaction proxy.

## How this changes the manuscript
- The CFPB complaint indicator must be described in the manuscript as a **general dissatisfaction / operational-disruption proxy**, not as a measure of *security-related* customer reaction. Any post-incident movement in total counts cannot be attributed to a security reaction without an additional, security-specific data source.
- This is an honest construct-validity BOUND. It does not invalidate the indicator for within-firm event-time use, but it bounds the causal/story interpretation that can be attached to it.

## Honest data-scope caveats
- The CFPB indicator applies only to the financial-servicer subset (Mr. Cooper, loanDepot, Navient). Healthcare/HSA firms (UnitedHealth, HealthEquity) and Cencora are outside CFPB jurisdiction and are excluded from this and the downstream placebo/LOO checks.
- **Navient** event (2026-06-08) is extremely recent: only a partial 2026Q2 post-event quarter exists. Navient has effectively no usable post-event window for a placebo/LOO pre-post comparison and is flagged accordingly downstream.
- **Mr. Cooper** is right-censored at 2025Q4 (Rocket acquisition); observations after the merger are excluded.
