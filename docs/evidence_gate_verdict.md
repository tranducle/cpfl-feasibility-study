# SCIE Q1 Evidence Coverage Gate — CPFL v3

**Run:** 2026-07-23 (session 10, post Tier-1 work). **Paper root:** `Papers/CUSTOMER-BEHAVIOR`.
**Skill:** `scie-q1-evidence-coverage-gate`. **Venue target:** Computers & Security (SCIE Q1).
**Evidence base:** all v3 artifacts in `4_Data_Pilot/` (CFPB series, 10-Q coding, 20 policy pairs + IRR, MDE, entity resolution). Nothing fabricated.

## Verdict

# **BOUND** (concurrent **BLOCK POINT ESTIMATION** + **BLOCK BROAD CLAIM**)

Progress over v2 is real (0→1 layer-complete firm; CFPB extraction solved; 10-Q indicator built; 20 policy pairs coded; MDE computed), but the evidence package **still cannot defend the core reduced-form claim** as a point estimate. The design is **bound-qualified**: it can support sign/direction and feasibility-protocol claims, but not a publishable feedback coefficient. Official point estimation, structural β_customer, and quantitative welfare **remain blocked**.

## What changed vs v2 (honest progress register)

| Tier-1 blocker (v2) | Status (v3) | Evidence |
|---|---|---|
| CFPB canonical-name extraction | **SOLVED** | `cfpb_firm_quarter_counts.csv` (Navient=`Navient Solutions, LLC.`; Mr. Cooper=`Mr. Cooper Group Inc.`) |
| Mr. Cooper entity continuity | **RESOLVED** | acquired by Rocket/RKT; retained 2022–2025, right-censored at merger (`entity_crosswalk.md`) |
| Second customer indicator (≥4 firms) | **PARTIAL** | 10-Q disclosure coded for 4 usable firms; but only Mr. Cooper reaches 2 indicators (CFPB+10-Q) |
| ≥20 policy pairs + IRR | **DONE (with caveat)** | 20 pairs coded; **intra-coder LLM double-pass α_SCOPE=0.833, NOT human IRR**; near-null variance |
| MDE / power | **COMPUTED** | σ_ε=0.050, σ_x=0.369; MDE(λ)≈0.068–0.096; N=4 clusters → BOUND |

## Claim-to-Experiment Matrix (v3)

| Claim | Evidence required | Coverage (v3) | Verdict |
|---|---|---|---|
| C1: customer behavior → policy adjustment (reduced-form feedback) | ≥4 layer-complete firms; human-validated Δpolicy; N_eff sufficient | **1/6 layer-complete** (Mr. Cooper); LLM-only IRR; N=4 clusters; Δpolicy near-null | **UNSUPPORTED as point estimate** → reframe to sign/feasibility/bound |
| C1-alt (null/boundary): public privacy pages do NOT observably respond to disclosed breaches | coded pairs + event-boundary null | 20 pairs; **4/4 event-boundary pairs identical** | **PARTIALLY SUPPORTED** (but needs human IRR + more firms) |
| C2: ΔL local-quadratic benchmark | κ calibration + scale | theory only; no κ | directional/model only |
| C3: 4 construct→policy paths falsifiable | tested paths | none estimable | untested hypotheses |

## Coverage Audit (v3)

| Dimension | v2 | v3 | Change |
|---|---|---|---|
| Source/dataset breadth | 0 layer-complete | **1/6 layer-complete** | +Mr. Cooper |
| External/cross-source validation | none | CFPB + 10-Q + policy (3 sources, 1 firm) | partial |
| Baselines | n/a | n/a | — |
| Ablations | gated | gated (behind C1) | — |
| Scientific gates | G0 partial | G0 partial; G1 n/a | — |
| Statistics/uncertainty | none | σ_ε, σ_x, MDE computed; N=4 cluster plan | **computed but BOUND** |
| Robustness | none | small-cluster plan specified | unrun |
| Reproducibility | probe scripts | + CFPB/10-Q/policy scripts | improved |
| Claim boundary | over-broad | must narrow to feasibility + bound | **action required** |

## Tiered decisions (v3)

- **STOP trying to estimate a point λ on the public-policy outcome.** The outcome variance is near-null and N=4 clusters forbid it.
- **BOUND is the operating verdict**: report sign/direction, within-firm qualitative patterns, and the event-boundary null honestly. Frame C1 as a *gated feasibility protocol + verified benchmark theory + boundary-condition finding*, not a measured coefficient.
- **Hard requirements before any point estimate (all unmet):** (a) ≥4 layer-complete firms each with ≥2 customer indicators; (b) **human second-coder-validated Δpolicy** (LLM double-pass is NOT publication-grade); (c) N≥8–10 treated clusters; (d) a higher-variance outcome (internal policy/config/threat-model, not public privacy page).
- **Structural β_customer + welfare**: still blocked (curvature κ + scale identification absent).

## Claim Boundary Edits (Hard Downgrade, v3)

- **Title/Abstract:** must NOT claim a measured feedback coefficient or that customer behavior causes policy adjustment. Permitted framing: "a gated feasibility protocol and reduced-form evidence on the *direction* of customer-conditioned policy response, with a verified local-quadratic benchmark; the public-policy-outcome signal is near-null and N=4 clusters preclude point estimation."
- **Contributions:** keep (1) policy-endogeneity MDP formulation, (2) gated measurement/identification design, (3) the **event-boundary null as a boundary-condition finding** (public privacy pages do not observably respond to disclosed breaches in the window). Mark all empirical evidence as **bounded/feasibility-grade**.
- **Limitations:** state explicitly: 1/6 layer-complete firms; LLM-double-pass IRR only (human second coder required); N=4 clusters; public-policy outcome near-null (σ_ε≈0.050, 80% identical pairs); customer-state composite resolved for 1 firm only; intrusion onset missing (no-anticipation capped).

## Launch Decision

**Official point estimation: NOT AUTHORIZED.** No point λ, no structural β_customer, no quantitative welfare. Permitted: sign/direction reporting, the feasibility-protocol framing, the event-boundary null, and the verified benchmark theorem — all clearly labeled bounded/feasibility-grade. **Final gate verdict: BOUND** (between REDUCE and a full STOP; continue as a bounded feasibility/protocol paper, do not pursue point estimates).

## Output contract
- **scope:** CPFL empirical evidence plan, post Tier-1 pilot work.
- **actions_taken:** re-audited claims against v3 evidence; recomputed layer-complete (1/6); computed MDE→BOUND; downgraded IRR to LLM-double-pass; applied hard claim-boundary rules.
- **evidence_or_inputs:** `4_Data_Pilot/cfpb_*`, `second_indicator_10q_disclosure.md`, `policy_coding_irr_report.md`, `mde_power_plan.md` (v3), `entity_crosswalk.md`, `missingness_identification_report.md` (v3).
- **result:** **BOUND** + BLOCK POINT ESTIMATION + BLOCK BROAD CLAIM. 1/6 layer-complete; point λ, structural β, welfare all blocked; sign/feasibility/bound reporting permitted.
- **risks_or_gaps:** Δpolicy near-null + construct validity (public page ≠ θ*); LLM-only IRR; N=4 clusters; customer composite 1 firm only.
- **next_step:** either (a) pivot the paper to a feasibility-protocol + boundary-condition contribution with bounded directional evidence, OR (b) acquire ≥4 layer-complete firms + human IRR + higher-variance outcome before any point estimate. Do not draft point-coefficient result claims.

---

## v3.1 Carry-Forward Note — PATH (a) reframe (session 11, 2026-07-23)

**Strategic decision:** the user selected **PATH (a)** — pivot to a bounded feasibility-protocol + boundary-condition paper (option (b) demoted to a pre-registered Future-Work roadmap).

**Gate verdict: UNCHANGED — still BOUND.** Rationale (per the gate skill's output contract, a verdict changes only when new evidence changes claim coverage):
- PATH (a) introduces **no new evidence, datasets, sample sizes, coefficients, or reliability statistics**. It reframes existing v3 artifacts (CFPB series, 10-Q indicator, 20 policy pairs + LLM-double-pass IRR, MDE, entity resolution, event-boundary null).
- The v3 claim-to-experiment matrix is therefore identical: C1 (point feedback coefficient) remains **UNSUPPORTED as a point estimate**; C1-alt (event-boundary null) remains **PARTIALLY SUPPORTED** (now promoted to the paper's lead empirical contribution, still pending human IRR + more firms); C2 (local-quadratic benchmark) remains **directional/model only**; C3 remains **untested hypotheses**.
- The reframe *strengthens claim-to-evidence alignment* (it removes overclaiming), which can only hold or relax a BLOCK, never tighten it. It does not relax any BLOCK: point λ, structural β_customer, and quantitative welfare remain BLOCKED for the same v3 reasons (N=4 clusters; Δpolicy near-null; LLM-only IRR; 1/6 layer-complete).

**Permitted under the unchanged BOUND verdict:** (i) the gated public-data feasibility protocol as a methodological contribution; (ii) the verified local-quadratic benchmark theorem (D001); (iii) the event-boundary null reported as a **boundary-condition finding** (4/4 event-boundary pairs identical); (iv) within-firm directional/qualitative policy patterns; (v) MDE (0.068–0.096) and LLM-double-pass α_SCOPE=0.833 reported as **honest feasibility-grade** evidence with their explicit caveats.

**Still BLOCKED:** any point-coefficient feedback estimate, structural β_customer, quantitative welfare, and any causal "customer behavior caused policy adjustment" claim. A full gate re-run is **not triggered** because no new evidence was added; the next mandatory re-run occurs when PATH (b)'s Future-Work probes actually land new evidence (human-coder IRR, higher-variance outcome, additional layer-complete firms).
