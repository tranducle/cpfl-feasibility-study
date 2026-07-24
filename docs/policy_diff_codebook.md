# CPFL Policy-Diff Codebook v1 + Inter-Rater Reliability Protocol

**Scope:** codes the *change in public-facing cybersecurity/privacy policy language* between consecutive Internet Archive snapshots of a firm's privacy/security policy page. The coded quantity is the policy-OUTCOME variable `Δpolicy` for the event panel.

**Codebook status:** v1 DRAFT, ready for first-pass coding. **IRR status: NOT YET COMPUTED — no second coder available in this session; protocol designed below, not executed. No reliability statistic is fabricated.**

## Unit of analysis

A **snapshot pair** = (snapshot at t, snapshot at t+1) of the same canonical policy URL for one firm. The diff is the set of textual/structural changes between the two rendered snapshots.

## Codebook dimensions (each coded ordinally 0–3)

| Code | Construct | 0 (none) | 1 (minor) | 2 (moderate) | 3 (major) |
|---|---|---|---|---|---|
| `RET` | Retention/data-minimization language | no change | wording tweak | new retention period or category | new data-minimization commitment or deletion right |
| `NOT` | Breach-notification / incident-notice language | no change | contact-channel tweak | new notification commitment or timeframe | new standing incident-notice section |
| `SEC` | Customer-facing security features (MFA, alerts, session) | no change | added/removed a feature mention | new security-feature section | structural security-feature overhaul |
| `SHR` | Data-sharing / third-party-sharing restrictions | no change | partner-list tweak | new sharing restriction/opt-out | structural sharing-control change |
| `ACC` | Access/credential controls (password, 2FA rules) | no change | policy tweak | new access policy | structural access-control change |
| `SCOPE` | Overall magnitude of change | identical | cosmetic (dates/links) | substantive (new clauses) | page restructure / rewrite |

Plus binary flags:
- `post_event_window` (1 if the later snapshot is within +12 months of the firm's detection date)
- `direction` (+ strengthens customer protection; − weakens; 0 neutral/cosmetic)
- `event_referenced` (1 if the text references a specific recent incident)

## Composite policy-adaptation score

`Δpolicy_it = (RET+NOT+SEC+SHR+ACC) / 15` ∈ [0,1], sign given by `direction`. This is the **observed proxy** for the formal policy action `θ*`; per the formal-to-empirical mapping it is **composite-only** unless measurement-scale identification passes.

## Coding procedure

1. For each retained firm, select the canonical policy URL (from `wayback_snapshot_matrix.csv`).
2. Pull consecutive monthly snapshots from the CDX-verified capture list.
3. Render each snapshot via the Wayback playback URL; extract visible policy text (boilerplate/nav stripped).
4. Diff consecutive pairs; code all 6 dimensions + 3 flags.
5. Record the diff artifact (snapshot timestamps, URL, raw text excerpts supporting each code).

## Coding target for this pilot pass

- **≥20 snapshot pairs** to be coded across the 4 firms with passing snapshot counts (UnitedHealth, HealthEquity, Mr. Cooper, loanDepot).
- Pairs should span pre-event and post-event windows per firm.

## Inter-Rater Reliability (IRR) protocol — DESIGNED, NOT YET EXECUTED

**Blocker (recorded honestly):** No second human coder or independent automated coding tool is available in this session. Therefore **no IRR statistic (Cohen's κ, Krippendorff's α, or percent agreement) has been computed. Any number reported now would be fabricated.**

**Protocol to be executed when a second coder is available:**

1. **Double-code** a calibration set of 20 snapshot pairs independently (coder A = this protocol; coder B = second coder or an independent LLM-assisted coder configured with this codebook only).
2. Blind coder B to event dates and firm identity (de-identified pairs) to prevent event-driven anchoring.
3. Compute, per ordinal dimension:
   - percent raw agreement,
   - **Cohen's κ** (2 raters) and/or **Krippendorff's α** (ordinal; preferred because it handles missing codes and more than 2 raters).
4. Acceptance thresholds (pre-registered): α ≥ 0.80 acceptable; 0.667 ≤ α < 0.80 tentative (revise codebook + recalibrate); α < 0.667 codebook rejected.
5. Disagreements adjudicated by discussion; revised codes form the analytic dataset. Report both pre-adjudication α and post-adjudication final codes.
6. If only an automated (LLM) second coder is available, treat it as an **assistant coder**, report human–LLM α, and flag that LLM-assisted coding is a known reliability threat requiring sensitivity analysis.

## Single-coder fallback (current reality)

With one coder only, the policy-diff series is **coded but not reliability-validated**. Therefore:
- Manuscript claims must label the policy-outcome variable as **"single-coded, reliability not yet established."**
- `Δpolicy` cannot be promoted beyond **composite-only** status regardless of codebook quality until IRR is computed.
- A sensitivity analysis must report how robust the feedback coefficient is to reasonable alternative codings of ambiguous pairs.

## Integrity notes

- Snapshot captures may be **endogenous to the event** (firms that suffer breaches may receive more archival attention). Mitigation: prefer the CDX monthly-collapse schedule over user-requested captures; model snapshot-frequency as a confounder; report capture-source (scheduled vs on-demand) where Wayback metadata allows.
- Public policy text ≠ internal policy/configuration (see formal-to-empirical mapping: `y` is a noisy measurement of `θ*`).
