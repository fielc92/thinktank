# Think Tank Report

**Mode:** Standard  
**Independence:** Full — five isolated first-round subagents  
**Question:** How should a growing software company organize product teams without losing speed or coherence?

## Problem framing

The company needs enough autonomy for teams to move quickly while avoiding duplicated platform work and incompatible product decisions. [FACT] The brief states that headcount will double within a year. [ASSUMPTION] Product lines share meaningful technical foundations. [UNKNOWN] The present cost of cross-team dependency delays has not been measured.

## Council composition

- Constructive explorer — expands viable organizational forms.
- Critical challenger — tests failure modes and hidden trade-offs.
- Evidence and assumptions auditor — classifies claims and evidence gaps.
- Product-team operator — assesses day-to-day coordination and ownership.
- Customer advocate — tests effects on user journeys spanning products.

## Perspective briefs

### Perspective: Constructive explorer

Proposes three models: autonomous product cells, a platform-and-stream model, and a federated model with common standards. Its strongest claim is that the design should vary by dependency density rather than use one structure everywhere.

### Perspective: Critical challenger

Warns that autonomy language often hides unresolved decision rights. It challenges every model to specify who can block a launch, who owns shared reliability, and what happens when local goals conflict with company goals.

### Perspective: Evidence and assumptions auditor

Finds that the case for reorganization relies on unmeasured coordination cost. It marks the expected headcount growth as [FACT], the relationship between centralization and consistency as [INFERENCE], and leadership's preference for a single roadmap as [VALUE].

### Perspective: Product-team operator

Argues for durable stream-aligned ownership with a small enabling platform group. It predicts that rotating project teams would destroy accountability and increase onboarding cost.

### Perspective: Customer advocate

Notes that customers experience cross-product workflows, not the org chart. It favors shared journey metrics and a cross-team escalation mechanism regardless of structural model.

## Areas of convergence

The council converges on durable ownership, explicit decision rights, and a small number of shared standards. No perspective supports complete centralization or unconstrained team autonomy.

## Material disagreements

The operator favors a permanent platform group, while the constructive explorer believes platform capability could remain embedded until repeated demand is demonstrated. The challenger considers this disagreement consequential because premature platform teams can become bottlenecks, while delayed platform investment can multiply duplication.

## Contested assumptions

- [ASSUMPTION] Shared technical work is large enough to justify a permanent platform group.
- [ASSUMPTION] Leadership will delegate roadmap authority after defining guardrails.
- [INFERENCE] Common journey metrics will reduce local optimization.
- [UNKNOWN] Whether current delivery delays arise from structure, staffing, architecture, or planning practice.

## Solution sets

### Solution set 1: Federated product cells

Create durable product cells with full outcome ownership, a small architecture council, and a mandatory interface contract for shared systems. This optimizes for local speed. It risks duplicated infrastructure and depends on strong observability of cross-team costs.

### Solution set 2: Platform and streams

Create stream-aligned product teams plus a permanent internal platform team with a published service catalogue and adoption metrics. This optimizes for leverage and consistency. It risks platform overreach and requires teams to be able to reject low-value platform offerings.

### Solution set 3: Staged hybrid

Start with federated cells, measure repeated shared-work demand for one quarter, and graduate only proven shared capabilities into a platform team. This optimizes for reversibility and learning. It delays some economies of scale but tests the most contested assumption before locking in structure.

## Stress test

Pre-mortem: one year after adopting the staged hybrid, delivery is slower. Likely causes are vague decision rights, a platform backlog driven by executives rather than users, and metrics that reward local output. Mitigations are a written decision-rights matrix, platform adoption and satisfaction measures, and a quarterly review that can return capabilities to product teams.

## Current synthesis

The staged hybrid is the strongest current direction because it preserves local ownership while treating the need for permanent platform investment as a hypothesis to test. This is a provisional synthesis, not a vote. It should be reconsidered if measurement shows that shared-work demand is already large and stable.

## Minority report

The product-team operator still favors creating the platform group immediately. Its warning should remain visible: waiting may allow each product cell to establish incompatible foundations that are expensive to unwind.

## Unresolved uncertainties

The largest uncertainty is the source and size of current coordination cost. The report also lacks evidence about developer experience, customer-journey breakage, and the proportion of roadmap work that is genuinely shared.

## Next validation step

For four weeks, tag blocked work by dependency type, interview each product lead and two engineers per team, inventory duplicated infrastructure work, and measure two cross-product customer journeys. Use the evidence to decide whether the platform threshold has already been crossed.
