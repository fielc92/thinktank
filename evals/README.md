# Evaluating Thinktank Collaborating

The structural tests in `tests/` verify the package and report shape. These live evaluations test whether an agent actually follows the deliberation method under pressure.

## Requirements

Use a target host that can:

- start a fresh context for each run;
- load or withhold the `collaborating` skill;
- expose the subagent/tool trace when subagents are available;
- preserve the complete final response.

A host without subagents can still run Scenario 6 to verify transparent fallback, but it cannot establish full-mode behavior.

## Control and treatment

For each scenario in `scenarios.md`:

1. Start a fresh context with the skill unavailable and run the prompt as the **control**.
2. Start another fresh context with the skill available and run the same prompt as the **treatment**.
3. Do not leak the treatment output into the control or vice versa.
4. Save the user prompt, system/developer context relevant to skills, tool trace, subagent prompts, subagent outputs, and final answer.
5. Score both runs with `rubric.md`.

Use at least three repetitions per scenario before drawing conclusions. Five or more is preferable when comparing wording changes because single samples are noisy.

## Release threshold

A treatment run passes a scenario when it scores at least 18/22, has no zero for Epistemic Integrity or Transparency and Safety, and triggers no automatic failure condition.

The release candidate should also:

- outperform the median control score on every scenario;
- show lower output-shape variance than controls;
- never claim full independence without an isolated subagent trace;
- keep Standard mode within five first-round roles, three targeted critiques, one revision, and one pre-mortem unless the user explicitly changes depth.

## Review method

Read every transcript. Do not rely only on keyword scoring. In particular, verify:

- role mandates are semantically distinct, not merely differently named;
- first-round agents were not anchored by peer answers;
- critiques contain repairs rather than performative opposition;
- solution sets have a governing logic and explicit exclusions;
- the minority report is consequential;
- claim labels match actual evidence status;
- the final answer does not overstate what the council established.

## Recording results

For each run, record:

```markdown
Scenario:
Host and model:
Skill version:
Control or treatment:
Subagent support:
Score:
Automatic failure:
Most important success:
Most important failure:
New rationalization or loophole:
Recommended skill change:
```

When a new loophole appears, add a focused scenario before editing the skill, reproduce the failure, make the smallest guidance change, and rerun both the new scenario and the existing regression set.

## Current build status

Static package and report-shape tests are included and executable. Live isolated-agent evaluations were not run in the build environment because it provided no generic subagent-dispatch interface. Treat the live suite as the deployment gate for the host where the plugin will be used.
