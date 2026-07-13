# RED-Phase Baseline Evidence

## Environment limitation

This build environment does not expose a generic isolated-subagent dispatch interface or an external model API. A true fresh-context control/treatment experiment therefore could not be run here. The live scenarios in `scenarios.md` are a mandatory release gate for the target host, and this package does not claim that those behavioral evaluations passed.

## Executable control available here

The fixture `tests/fixtures/linear-answer.md` represents the common no-skill failure shape: immediate convergence on one recommendation, no shared brief, no independent perspectives, no assumptions ledger, no dissent, no stress test, and no next evidence step.

The fixture `tests/fixtures/hollow-consensus.md` represents a second failure shape: it copies report headings but uses unspecified “experts,” asserts unanimous agreement, provides one solution, labels no claims, and erases the minority report.

Before the skill and report linter exist, the test suite must fail. After implementation, the report linter must continue rejecting both control fixtures while accepting `tests/fixtures/compliant-report.md`. This is structural RED/GREEN evidence, not a substitute for live behavioral evaluation.

## Failure patterns the skill must address

- The orchestrator chooses a recommendation before hearing independent proposals.
- Role names differ while mandates remain nearly identical.
- Agents see one another's answers too early and converge through anchoring.
- Debate becomes all-to-all, repetitive, and expensive.
- Consensus is treated as factual verification.
- Criticism attacks proposals without offering repairs.
- Synthesis averages incompatible proposals into an incoherent compromise.
- Minority views disappear from the final answer.
- The host lacks subagents but the answer still claims independent experts were consulted.
