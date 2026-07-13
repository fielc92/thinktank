# Thinktank Collaborating Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a cross-host `thinktank` plugin containing a production-ready `collaborating` skill for structured exploration of ambiguous problems.

**Architecture:** Keep the activated `SKILL.md` compact and put detailed protocol, roles, prompts, evidence rules, report forms, and the example in one-level reference files. Add a standard-library Python package validator and report linter, with tests and live evaluation scenarios.

**Tech Stack:** Markdown Agent Skills, JSON plugin manifests, Python 3 standard library, POSIX shell, Git.

## Global Constraints

- The only production skill in v0.1.0 is `collaborating`.
- Full mode requires isolated subagent dispatch; fallback must identify itself as reduced independence.
- The orchestrator must not reveal private chain-of-thought.
- Consensus is not factual verification and majority vote is not the synthesis rule.
- First-round proposals are blind where host capabilities permit.
- No placeholders such as TBD, TODO, or “implement later”.
- `SKILL.md` remains below 500 lines and all referenced files are one level deep.

---

### Task 1: Define failing package and behavior contracts

**Files:**
- Create: `tests/test_package.py`
- Create: `tests/test_report_lint.py`
- Create: `tests/fixtures/linear-answer.md`
- Create: `tests/fixtures/hollow-consensus.md`
- Create: `tests/fixtures/compliant-report.md`
- Create: `tests/run.sh`
- Create: `evals/scenarios.md`
- Create: `evals/rubric.md`
- Create: `evals/baseline-observations.md`

**Interfaces:**
- Consumes: the design specification.
- Produces: executable contracts for plugin structure, skill invariants, and report shape.

- [ ] Write package tests that require manifests, `SKILL.md`, focused references, valid metadata, no placeholders, working links, and consistent version `0.1.0`.
- [ ] Write report-linter tests that require the linear and hollow-consensus fixtures to fail and the compliant fixture to pass.
- [ ] Run `bash tests/run.sh` and verify failure because production files and linter do not yet exist.
- [ ] Commit the failing contracts with `git commit -m "test: define thinktank skill contracts"`.

### Task 2: Implement package metadata and validators

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.codex-plugin/plugin.json`
- Create: `package.json`
- Create: `VERSION`
- Create: `LICENSE`
- Create: `scripts/validate-package.py`
- Create: `scripts/install-skill.sh`
- Create: `scripts/package.sh`
- Create: `skills/collaborating/scripts/lint-report.py`

**Interfaces:**
- Consumes: paths and requirements asserted by Task 1.
- Produces: `validate_package(root: Path) -> list[str]` and CLI report linting with exit code 0 for compliant reports, 1 for violations, 2 for usage errors.

- [ ] Implement the minimal validators and metadata needed for package tests to advance.
- [ ] Run `bash tests/run.sh`; expect remaining failures only for the absent skill and references.
- [ ] Commit with `git commit -m "feat: add plugin metadata and validators"`.

### Task 3: Implement the collaborating skill

**Files:**
- Create: `skills/collaborating/SKILL.md`
- Create: `skills/collaborating/references/protocol.md`
- Create: `skills/collaborating/references/roles.md`
- Create: `skills/collaborating/references/prompts.md`
- Create: `skills/collaborating/references/evidence.md`
- Create: `skills/collaborating/references/report.md`
- Create: `skills/collaborating/references/example.md`

**Interfaces:**
- Consumes: the shared brief and available host subagent tools.
- Produces: a structured Think Tank Report and optional lintable Markdown artifact.

- [ ] Write `SKILL.md` with suitability gate, depth selection, non-negotiable invariants, compact lifecycle, stop conditions, failure handling, and output contract.
- [ ] Write the full protocol state machine and deliberation ledger schema.
- [ ] Write the role-selection library and orthogonality test.
- [ ] Write exact dispatch, critique, revision, stress-test, and fallback prompt forms.
- [ ] Write evidence classification and consensus safeguards.
- [ ] Write the report template and one complete example.
- [ ] Run `bash tests/run.sh`; expect the skill, reference, manifest, and report-linter contracts to pass, with only the release-documentation requirement remaining until Task 4.
- [ ] Commit with `git commit -m "feat: add collaborating think tank skill"`.

### Task 4: Add usage documentation and release packaging

**Files:**
- Create: `README.md`
- Create: `CHANGELOG.md`
- Update: `evals/README.md`

**Interfaces:**
- Consumes: the completed plugin package.
- Produces: local installation, invocation, validation, and live-evaluation instructions.

- [ ] Document the distinction between plugin installation and direct skill copying.
- [ ] Document Quick, Standard, and Deep example invocations.
- [ ] Document limitations, especially model-correlated output and no-subagent fallback.
- [ ] Run `python3 scripts/validate-package.py .`, `bash tests/run.sh`, and `python3 skills/collaborating/scripts/lint-report.py tests/fixtures/compliant-report.md`.
- [ ] Create `dist/thinktank-0.1.0.zip` with `bash scripts/package.sh`.
- [ ] Commit with `git commit -m "docs: add thinktank usage and release package"`.

### Task 5: Final verification

**Files:**
- Verify all tracked files; no new production files required.

**Interfaces:**
- Consumes: repository at v0.1.0 release candidate.
- Produces: verification evidence and downloadable archive.

- [ ] Run the complete test and validation suite from a clean working tree.
- [ ] Inspect the archive contents and extract it to a temporary directory.
- [ ] Run package validation against the extracted archive.
- [ ] Confirm no placeholder text, broken relative references, or version mismatches.
- [ ] Record the live-agent evaluation limitation accurately; do not claim live behavioral tests passed.
