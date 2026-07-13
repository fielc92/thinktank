# Think Tank

Think Tank is an Agent Skills plugin for exploring ambiguous problems through structured multi-perspective deliberation.

Its first skill, `collaborating`, turns the main agent into an orchestrator. The orchestrator frames one shared inquiry, convenes complementary council roles, protects first-round independence where the host supports subagents, directs targeted critique and revision, builds coherent solution sets, stress-tests them, and preserves consequential dissent.

The plugin is designed for **exploration**, not consensus theater. Several agents repeating a claim does not make the claim true, and the final synthesis is not chosen by majority vote.

## What is included

```text
thinktank/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── package.json
├── skills/
│   └── collaborating/
│       ├── SKILL.md
│       ├── references/
│       │   ├── protocol.md
│       │   ├── roles.md
│       │   ├── prompts.md
│       │   ├── evidence.md
│       │   ├── report.md
│       │   └── example.md
│       └── scripts/
│           └── lint-report.py
├── evals/
├── scripts/
└── tests/
```

The activated `SKILL.md` contains the compact operating contract. Detailed materials are loaded only when needed.

## Fastest local installation

Extract the archive, then copy the skill into the skills directory used by your agent host:

```bash
cd thinktank-0.1.0
./scripts/install-skill.sh /absolute/path/to/your/skills-directory
```

To replace an existing installation:

```bash
./scripts/install-skill.sh --force /absolute/path/to/your/skills-directory
```

The script deliberately requires an explicit destination because skill locations differ by host and configuration.

## Plugin installation

The repository also contains Claude-style and Codex-style plugin manifests. In a host that supports loading a local plugin or repository, point its local plugin flow at the repository root rather than copying only the skill directory.

For a first trial, direct skill copying is the least host-specific method. When publishing the plugin, add your author, repository, homepage, privacy, and marketplace metadata to the manifests as required by your chosen host.

## Invoke it

Explicit invocation is the most reliable way to test a new local skill:

```text
Use thinktank:collaborating in Standard mode to explore this problem:

We have strong enterprise sales but weak self-serve adoption. We have six months,
we cannot double the team, and we do not yet know whether the problem is product,
positioning, onboarding, or channel strategy.
```

Other useful forms:

```text
Use a Quick think tank to map the strongest alternatives and assumptions.
```

```text
Convene a Deep think tank. Preserve dissent, verify factual disputes separately,
and finish with solution sets plus the next validation experiment.
```

```text
Use thinktank:collaborating to challenge the apparent consensus without turning
this into an unbounded debate.
```

## What a run should produce

A full report includes:

1. problem framing;
2. council composition and an honest independence declaration;
3. named perspective briefs;
4. convergence and material disagreement;
5. contested facts, assumptions, inferences, values, and unknowns;
6. two to four coherent solution sets;
7. a pre-mortem or scenario stress test;
8. a provisional synthesis;
9. a minority report;
10. unresolved uncertainty and one concrete validation step.

The three mandatory council functions are constructive exploration, critical challenge, and evidence/assumptions auditing. Standard and Deep runs add adaptive roles such as user advocate, operator, systems thinker, incentives analyst, governance analyst, safety reviewer, or experimentation designer.

## Subagent support

Full mode requires a host with genuinely isolated subagent or task-dispatch contexts. The skill checks the capability actually available.

When isolation exists, first-round prompts are dispatched before any peer proposal or orchestrator preference is shared. When it does not exist, the skill enters **reduced-independence** mode, drafts all role mandates first, runs separated sequential role passes, and states that the perspectives may share context and anchoring biases.

It must never claim that independent agents or human experts participated when they did not.

## Validate a generated report

Save the report as Markdown and run:

```bash
python3 skills/collaborating/scripts/lint-report.py path/to/report.md
```

The linter checks report structure, perspective count, solution-set count, epistemic labels, the independence declaration, and obvious hollow-consensus patterns. It cannot judge factual truth, genuine insight, or semantic role diversity.

## Validate the plugin

```bash
python3 scripts/validate-package.py .
bash tests/run.sh
```

The test suite uses only the Python standard library.

## Run live behavioral evaluations

See [`evals/README.md`](evals/README.md). The evaluation set covers premature consensus, correlated factual error, redundant roles, resource limits, no-subagent fallback, untrusted evidence, and high-stakes boundaries.

This build environment could execute the static RED/GREEN contracts but did not expose a generic isolated-subagent interface. The package therefore does not claim that the live model evaluations passed; run them in the host where you plan to use the skill.

## Build a release archive

```bash
./scripts/package.sh
```

The command validates the package, runs the tests, and writes:

```text
dist/thinktank-0.1.0.zip
```

## Design choices

- **Hybrid council:** three mandatory reasoning functions plus adaptive domain roles.
- **Blind first round:** reduces anchoring before perspectives are compared.
- **Targeted critique:** avoids quadratic all-to-all debate.
- **Revision:** lets proposals improve rather than remain fixed debate positions.
- **Solution sets:** preserve coherent alternatives instead of averaging everything together.
- **Evidence discipline:** separates deliberative diversity from factual verification.
- **Minority report:** keeps consequential dissent available to the user.
- **Bounded depth:** Quick, Standard, and Deep modes prevent token and coordination explosion.

## Known limitations

- Subagents using the same underlying model can share systematic blind spots.
- Role diversity does not equal real demographic, professional, or lived-experience diversity.
- The structural linter cannot evaluate whether the council was genuinely orthogonal.
- External facts still require appropriate research and source verification.
- High-stakes decisions still require relevant qualified humans and real-world validation.

## License

MIT. See [`LICENSE`](LICENSE).
