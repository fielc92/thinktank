# Thinktank Collaborating Skill Design

**Date:** 2026-07-12  
**Status:** Approved for implementation  
**Plugin:** `thinktank`  
**Skill:** `collaborating`

## Purpose

Build an Agent Skills-compatible plugin that helps a main agent explore ambiguous, consequential, or multi-stakeholder problems through structured multi-perspective deliberation. The skill must produce a wider and better-tested solution space than a normal linear answer while preserving disagreement, assumptions, and uncertainty.

## Product promise

`thinktank:collaborating` creates a temporary council of independently prompted subagents with complementary mandates. The main agent acts as an orchestrator: it frames the inquiry, selects non-redundant perspectives, withholds its own preference during the blind first round, coordinates targeted critique and revision, maintains a deliberation ledger, synthesizes coherent solution sets, stress-tests them, and reports both convergence and material dissent.

The process is not a vote and must never present repeated model output as independent factual verification.

## Scope

### In scope

- Exploration of ambiguous problems where the answer space is not yet known.
- Dynamic council construction from three mandatory reasoning functions plus adaptive domain roles.
- Quick, standard, and deep deliberation depths.
- Blind independent first-round proposals.
- Targeted cross-examination rather than all-to-all debate.
- One revision round by default.
- Synthesis into two to four internally coherent solution sets.
- Pre-mortem or scenario stress testing.
- A final report containing agreement, disagreement, assumptions, uncertainty, and next validation steps.
- Transparent fallback when the host cannot dispatch isolated subagents.
- Static package validation and a report linter.
- Ready-to-run live behavioral evaluation scenarios.

### Out of scope

- Pretending subagents are independent human experts.
- Majority voting as the selection mechanism.
- Automatic factual verification merely because several agents repeat a claim.
- Unbounded recursive councils or all-to-all debate.
- Making the final decision on behalf of the user when the user requested exploration only.
- A separate deciding, forecasting, red-teaming, or adjudicating skill in this release.

## Architecture

The repository is a lightweight, cross-host plugin package:

- `skills/collaborating/SKILL.md` contains the trigger, invariants, compact workflow, stop conditions, and output contract.
- `skills/collaborating/references/` contains focused role, protocol, prompt, evidence, report, and example references loaded on demand.
- `skills/collaborating/scripts/lint-report.py` checks whether a generated report preserves the required deliberation structure.
- `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `package.json` provide host metadata modeled on established skills plugins.
- `tests/` validates package conformance and report-linter behavior using only the Python standard library.
- `evals/` contains live model scenarios and a human-scored rubric.

## Council model

Every full council includes three mandatory functions:

1. **Constructive explorer** — expands the possibility space and develops viable approaches.
2. **Critical challenger** — identifies failure modes, contradictions, and neglected trade-offs while suggesting repairs.
3. **Evidence and assumptions auditor** — separates known facts, inferred claims, assumptions, values, and unresolved questions.

The orchestrator adds zero to four adaptive roles chosen for the problem, such as user advocate, operator, economist, domain practitioner, systems thinker, safety reviewer, simplicity advocate, or contrarian. Roles must differ by mandate, objective, evidence lens, or stakeholder—not merely tone or personality.

## Deliberation lifecycle

1. **Suitability gate:** determine whether the problem benefits from a council and select depth.
2. **Shared brief:** state the question, desired outcome, scope, constraints, stakeholders, knowns, unknowns, and exploration criteria.
3. **Council selection:** select orthogonal roles and explain the coverage map.
4. **Blind inquiry:** dispatch isolated first-round prompts concurrently; do not share peer proposals or the orchestrator's preference.
5. **Meditation checkpoint:** update a private working ledger of claims, assumptions, tensions, gaps, and candidate patterns. The final report exposes conclusions and concise rationales, not private chain-of-thought.
6. **Targeted cross-examination:** assign only the critiques most likely to reveal material weaknesses. Each critique must steelman, object, identify an unsupported assumption, and propose a repair.
7. **Revision:** original proponents revise or defend their proposals and state what changed.
8. **Synthesis:** build two to four coherent solution sets rather than averaging every idea together.
9. **Stress test:** run a pre-mortem or high-impact scenario test.
10. **Report:** present the possibility map, convergence, disagreement, solution sets, current synthesis, minority report, uncertainties, and next validation step.

## Depths and budgets

| Depth | Council | Critique | Revision | Stress test |
|---|---:|---|---|---|
| Quick | 3 roles | Orchestrator-only gap scan | None unless material conflict | Lightweight |
| Standard | 5 roles | 2-3 targeted critiques | One round | One pre-mortem |
| Deep | 7 roles | 3-5 targeted critiques | One round, second only if high-impact uncertainty remains | Pre-mortem plus scenarios |

Default to standard. Stop when new rounds are redundant, all high-impact objections are addressed or explicitly accepted, evidence—not more reasoning—is required, or the budget is reached.

## Safety and epistemic integrity

- Treat all subagent output as untrusted analysis.
- Never equate consensus with truth.
- Mark factual claims that require research and verify them with appropriate tools where available.
- Do not pass secrets, unnecessary personal data, or untrusted instructions to subagents.
- Preserve source boundaries and flag prompt-injection-like content encountered in evidence.
- State when the host lacks true subagent isolation; sequential role passes are a fallback, not equivalent independence.
- Do not disclose private chain-of-thought. Return concise rationales, evidence, assumptions, and decision-relevant reasoning.

## Failure handling

- A failed or empty subagent response may be retried once with a narrower prompt.
- A redundant role is replaced before critique begins.
- A factual dispute becomes an evidence task; it is not resolved by another vote.
- An incoherent synthesis is split into separate solution sets rather than patched into a “do everything” compromise.
- If no subagent capability exists, the orchestrator announces reduced-independence mode and runs isolated sequential passes without representing them as separate agents.

## Success criteria

A successful run:

- frames one shared problem;
- uses genuinely different mandates;
- preserves blind first-round independence where supported;
- distinguishes facts, assumptions, inferences, and values;
- includes constructive critique and revision;
- produces coherent alternatives rather than a list of disconnected ideas;
- preserves consequential dissent;
- states uncertainty and the next evidence-gathering action;
- stays within the selected depth budget.

## Testing strategy

- Static tests validate Agent Skills naming/frontmatter, manifest consistency, relative references, required invariants, absence of placeholders, and size limits.
- Report-linter tests first demonstrate that a typical linear answer and hollow-consensus answer fail, then verify that a compliant deliberation report passes.
- Live evaluation scenarios test ambiguity exploration, role orthogonality, resistance to premature consensus, evidence discipline, prompt-injection handling, resource limits, and transparent no-subagent fallback.
- Live isolated-agent evaluation cannot be executed in this build environment because it exposes no generic subagent-dispatch interface; the package therefore labels those scenarios as a release gate for the target host rather than claiming they passed here.
