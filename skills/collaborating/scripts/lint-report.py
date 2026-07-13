#!/usr/bin/env python3
"""Lint the structure of a Think Tank deliberation report.

This is intentionally a structural linter. It can detect missing deliberation
artifacts, but it cannot judge whether a perspective is genuinely insightful
or whether an external factual claim is true.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_SECTIONS = (
    "Problem framing",
    "Council composition",
    "Perspective briefs",
    "Areas of convergence",
    "Material disagreements",
    "Contested assumptions",
    "Solution sets",
    "Stress test",
    "Current synthesis",
    "Minority report",
    "Unresolved uncertainties",
    "Next validation step",
)
EPISTEMIC_TAGS = {"FACT", "ASSUMPTION", "INFERENCE", "VALUE", "UNKNOWN"}
EMPTY_WORDS = {
    "none",
    "none.",
    "n/a",
    "not applicable",
    "no meaningful disagreement.",
    "no meaningful disagreements.",
    "there were no meaningful disagreements.",
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def section_body(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else None


def lint_text(text: str) -> list[Finding]:
    findings: list[Finding] = []

    if not re.search(r"^#\s+Think Tank Report\s*$", text, re.IGNORECASE | re.MULTILINE):
        findings.append(Finding("report-title", "Expected '# Think Tank Report'."))

    for heading in REQUIRED_SECTIONS:
        body = section_body(text, heading)
        if body is None:
            findings.append(Finding("missing-section", f"Missing section: {heading}."))
        elif len(body.split()) < 3:
            findings.append(Finding("thin-section", f"Section is too thin: {heading}."))

    if not re.search(r"^\*\*Mode:\*\*\s+\S+", text, re.IGNORECASE | re.MULTILINE):
        findings.append(Finding("missing-mode", "Report must declare Quick, Standard, or Deep mode."))

    if not re.search(r"^\*\*Independence:\*\*\s+\S+", text, re.IGNORECASE | re.MULTILINE):
        findings.append(
            Finding(
                "missing-independence",
                "Report must declare full or reduced independence and how it was achieved.",
            )
        )

    perspective_count = len(re.findall(r"^###\s+Perspective:\s+.+$", text, re.MULTILINE))
    if perspective_count < 3:
        findings.append(
            Finding(
                "perspective-count",
                f"Expected at least 3 named perspective briefs; found {perspective_count}.",
            )
        )

    solution_count = len(re.findall(r"^###\s+Solution set\s+\d+\s*:\s*.+$", text, re.IGNORECASE | re.MULTILINE))
    if solution_count < 2:
        findings.append(
            Finding(
                "solution-set-count",
                f"Expected at least 2 coherent solution sets; found {solution_count}.",
            )
        )

    used_tags = {tag.upper() for tag in re.findall(r"\[(FACT|ASSUMPTION|INFERENCE|VALUE|UNKNOWN)\]", text, re.IGNORECASE)}
    if len(used_tags) < 3:
        findings.append(
            Finding(
                "epistemic-tags",
                "Use at least 3 distinct epistemic tags from [FACT], [ASSUMPTION], [INFERENCE], [VALUE], and [UNKNOWN].",
            )
        )
    unknown_tags = set(re.findall(r"\[([A-Z][A-Z-]+)\]", text)) - EPISTEMIC_TAGS
    if unknown_tags:
        findings.append(Finding("unknown-tag", f"Unknown epistemic tags: {', '.join(sorted(unknown_tags))}."))

    minority = section_body(text, "Minority report")
    if minority is not None:
        normalized = re.sub(r"\s+", " ", minority.strip().lower())
        if normalized in EMPTY_WORDS or len(normalized.split()) < 8:
            findings.append(
                Finding(
                    "empty-minority-report",
                    "Minority report must preserve a consequential dissent or explain why no dissent survived stress testing.",
                )
            )

    disagreements = section_body(text, "Material disagreements")
    if disagreements is not None:
        normalized = re.sub(r"\s+", " ", disagreements.strip().lower())
        if normalized in EMPTY_WORDS or len(normalized.split()) < 8:
            findings.append(
                Finding(
                    "empty-disagreement",
                    "Material disagreements must identify a real tension, not merely state unanimity.",
                )
            )

    if re.search(r"\b(?:all agents agreed|everyone agreed|unanimous(?:ly)?)\b", text, re.IGNORECASE):
        findings.append(
            Finding(
                "unsupported-consensus",
                "Consensus language is not evidence; describe the shared reasoning and retain material dissent.",
            )
        )

    return findings


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} REPORT.md", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.is_file():
        print(f"error: report not found: {path}", file=sys.stderr)
        return 2

    findings = lint_text(path.read_text(encoding="utf-8"))
    if findings:
        print(f"FAIL {path}")
        for finding in findings:
            print(f"- [{finding.code}] {finding.message}")
        return 1

    print(f"PASS {path}: report contains the required deliberation structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
