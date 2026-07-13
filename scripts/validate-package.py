#!/usr/bin/env python3
"""Validate the Thinktank plugin using only the Python standard library."""

from __future__ import annotations

import json
import re
import stat
import sys
from pathlib import Path

EXPECTED_VERSION = "0.1.0"
REQUIRED_REFERENCES = (
    "protocol.md",
    "roles.md",
    "prompts.md",
    "evidence.md",
    "report.md",
    "example.md",
)
PLACEHOLDER_TERMS = ("T" + "BD", "TO" + "DO", "FIX" + "ME", "IMPLEMENT" + " LATER")
PLACEHOLDER = re.compile(r"\b(?:" + "|".join(re.escape(term) for term in PLACEHOLDER_TERMS) + r")\b", re.IGNORECASE)


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    data: dict[str, object] = {}
    current: dict[str, str] | None = None
    for original in raw.splitlines():
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        if original.startswith("  "):
            if current is None or ":" not in original:
                raise ValueError(f"unsupported nested frontmatter: {original}")
            key, value = original.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"\'')
            continue
        if ":" not in original:
            raise ValueError(f"invalid frontmatter line: {original}")
        key, value = original.split(":", 1)
        if value.strip():
            data[key.strip()] = value.strip().strip('"\'')
            current = None
        else:
            current = {}
            data[key.strip()] = current
    return data, body


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = root / "skills" / "collaborating"
    skill = skill_dir / "SKILL.md"

    required = [
        root / ".claude-plugin" / "plugin.json",
        root / ".codex-plugin" / "plugin.json",
        root / "package.json",
        root / "VERSION",
        root / "LICENSE",
        root / "README.md",
        skill,
        skill_dir / "scripts" / "lint-report.py",
        root / "scripts" / "install-skill.sh",
        root / "scripts" / "package.sh",
    ] + [skill_dir / "references" / name for name in REQUIRED_REFERENCES]

    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(root)}")
    if errors:
        return errors

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if version != EXPECTED_VERSION:
        errors.append(f"VERSION must be {EXPECTED_VERSION}, found {version!r}")

    manifests = {
        ".claude-plugin/plugin.json": json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")),
        ".codex-plugin/plugin.json": json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")),
        "package.json": json.loads((root / "package.json").read_text(encoding="utf-8")),
    }
    for name, manifest in manifests.items():
        if manifest.get("name") != "thinktank":
            errors.append(f"{name}: name must be thinktank")
        if manifest.get("version") != version:
            errors.append(f"{name}: version must match VERSION ({version})")

    try:
        meta, body = parse_frontmatter(skill)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    name = str(meta.get("name", ""))
    description = str(meta.get("description", ""))
    compatibility = str(meta.get("compatibility", ""))
    metadata = meta.get("metadata", {})
    if name != skill_dir.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("SKILL.md name must match the collaborating directory and use lowercase letters, numbers, and hyphens")
    if len(name) > 64:
        errors.append("SKILL.md name exceeds 64 characters")
    if not description.startswith("Use when "):
        errors.append("SKILL.md description must start with 'Use when '")
    if not (1 <= len(description) <= 1024):
        errors.append("SKILL.md description must be 1-1024 characters")
    if len(compatibility) > 500:
        errors.append("SKILL.md compatibility exceeds 500 characters")
    if meta.get("license") != "MIT":
        errors.append("SKILL.md license must be MIT")
    if not isinstance(metadata, dict) or metadata.get("plugin") != "thinktank" or metadata.get("version") != version:
        errors.append("SKILL.md metadata must identify thinktank and match VERSION")
    if len(skill.read_text(encoding="utf-8").splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines")
    if len(skill.read_text(encoding="utf-8").split()) > 5000:
        errors.append("SKILL.md exceeds 5000 words")

    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", body)
    for link in links:
        if "://" in link or link.startswith("#"):
            continue
        if len(Path(link).parts) > 2:
            errors.append(f"deep relative link in SKILL.md: {link}")
        elif not (skill_dir / link).is_file():
            errors.append(f"broken relative link in SKILL.md: {link}")

    production = [path for path in required if path.suffix in {".md", ".json", ".py", ".sh"}]
    production.extend([root / "CHANGELOG.md"] if (root / "CHANGELOG.md").is_file() else [])
    for path in production:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if PLACEHOLDER.search(line):
                errors.append(f"placeholder in {path.relative_to(root)}:{number}")

    executable = [
        root / "scripts" / "validate-package.py",
        root / "scripts" / "install-skill.sh",
        root / "scripts" / "package.sh",
        skill_dir / "scripts" / "lint-report.py",
        root / "tests" / "run.sh",
    ]
    for path in executable:
        if path.is_file() and not path.stat().st_mode & stat.S_IXUSR:
            errors.append(f"script is not executable: {path.relative_to(root)}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print(f"usage: {Path(argv[0]).name} [PLUGIN_ROOT]", file=sys.stderr)
        return 2
    root = Path(argv[1] if len(argv) == 2 else ".").resolve()
    if not root.is_dir():
        print(f"error: plugin root not found: {root}", file=sys.stderr)
        return 2

    errors = validate(root)
    if errors:
        print(f"FAIL {root}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS {root}: thinktank {EXPECTED_VERSION} package is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
