# Think Tank Report Contract

Use this template for the final answer or saved Markdown artifact. Keep the report proportional to the problem, but retain every section. A Quick report may use shorter sections; it still needs at least three perspective briefs and two coherent solution sets.

```markdown
# Think Tank Report

**Mode:** Quick | Standard | Deep  
**Independence:** Full | Reduced — <how first-round separation was achieved and the remaining model-correlation limitation>  
**Question:** <the shared core question>

## Problem framing

<State the exploration goal, scope, constraints, stakeholders, and the most material knowns and unknowns. Use epistemic tags where status could mislead.>

## Council composition

- <Role> — <unique mandate>
- <Role> — <unique mandate>
- <Role> — <unique mandate>
<Add adaptive roles used.>

## Perspective briefs

### Perspective: <role name>

<Thesis, visible possibilities, strongest contribution, assumptions, evidence need, and disconfirming signal. Summarize; do not paste private reasoning or excessive raw output.>

### Perspective: <role name>

<Brief.>

### Perspective: <role name>

<Brief.>

## Areas of convergence

<Shared mechanisms, principles, constraints, or observations. Say why they converge. Do not imply that convergence verifies factual claims.>

## Material disagreements

<The tensions that would change a solution set, the positions, and why they matter. Include the result of targeted critique and revision.>

## Contested assumptions

- [ASSUMPTION] <claim and why it matters>
- [INFERENCE] <derived claim under dispute>
- [UNKNOWN] <missing information>
<Include [FACT] and [VALUE] where needed.>

## Solution sets

### Solution set 1: <name>

**Optimizes for:** <objectives>

**Core components:** <reinforcing mechanisms>

**Deliberately excludes:** <incompatible mechanisms>

**Assumptions and dependencies:** <conditions>

**Trade-offs and risk owners:** <who gains, who pays, who carries risk>

**Safeguards and mitigations:** <controls>

**Early test or signal:** <reversible experiment or indicator>

**Choose this when:** <conditions>

### Solution set 2: <name>

<Use the same fields.>

<Add solution sets 3-4 only when they are genuinely distinct.>

## Stress test

<Pre-mortem or scenario results, early warning signs, mitigations, and whether the findings changed the solution sets.>

## Current synthesis

<State the strongest current interpretation or direction and why it best fits the brief. Make it provisional unless the user explicitly requested a decision. State what it excludes. Do not say it won a vote.>

## Minority report

<Preserve the strongest consequential dissent. Explain the conditions or evidence under which it would become the better view. If no dissent survives, explain the critiques tested and why they were resolved; do not write only “None.”>

## Unresolved uncertainties

<The remaining evidence gaps and what they could change.>

## Next validation step

<One bounded research, experiment, stakeholder, prototype, or measurement action that most reduces the leading uncertainty.>
```

## Report quality checks

Before returning the report:

- The independence declaration matches the tools actually used.
- At least three named perspective briefs are present.
- At least two solution sets are internally coherent and have explicit exclusions.
- Agreement is separated from fact verification.
- The strongest disagreement has not been summarized away.
- Decision-relevant claim status is visible through tags.
- The stress test changes a condition, mitigation, or confidence—or explains why it does not.
- The minority report contains a real alternative or a substantive resolution explanation.
- The next validation step is concrete enough to execute.

## Structural linter

When the report is stored as Markdown, run:

```bash
python3 scripts/lint-report.py path/to/report.md
```

The linter checks structure, perspective count, solution-set count, epistemic tags, independence declaration, and hollow consensus patterns. It cannot verify factual accuracy, true role diversity, or the quality of synthesis; those require human or live-agent evaluation.
