from __future__ import annotations

import json
import re
import stat
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "collaborating"
SKILL_FILE = SKILL_DIR / "SKILL.md"
VERSION = "0.1.0"

REQUIRED_FILES = [
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / "package.json",
    ROOT / "VERSION",
    ROOT / "LICENSE",
    ROOT / "README.md",
    SKILL_FILE,
    SKILL_DIR / "references" / "protocol.md",
    SKILL_DIR / "references" / "roles.md",
    SKILL_DIR / "references" / "prompts.md",
    SKILL_DIR / "references" / "evidence.md",
    SKILL_DIR / "references" / "report.md",
    SKILL_DIR / "references" / "example.md",
    SKILL_DIR / "scripts" / "lint-report.py",
    ROOT / "scripts" / "validate-package.py",
    ROOT / "scripts" / "install-skill.sh",
    ROOT / "scripts" / "package.sh",
]

REQUIRED_SKILL_MARKERS = [
    "## Non-negotiable invariants",
    "## Workflow",
    "## Stop conditions",
    "## Failure handling",
    "## Output contract",
    "blind first round",
    "reduced-independence",
    "consensus is not evidence",
    "private chain-of-thought",
    "targeted cross-examination",
    "minority report",
]


def read_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} does not start with YAML frontmatter")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise AssertionError(f"{path} has unclosed YAML frontmatter") from exc

    result: dict[str, object] = {}
    current_map: dict[str, str] | None = None
    for original in raw.splitlines():
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        if original.startswith("  "):
            if current_map is None or ":" not in original:
                raise AssertionError(f"Unsupported nested frontmatter line: {original}")
            key, value = original.strip().split(":", 1)
            current_map[key.strip()] = value.strip().strip('"\'')
            continue
        if ":" not in original:
            raise AssertionError(f"Invalid frontmatter line: {original}")
        key, value = original.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            nested: dict[str, str] = {}
            result[key] = nested
            current_map = nested
        else:
            result[key] = value.strip('"\'')
            current_map = None
    return result, body


class PackageContractTests(unittest.TestCase):
    def test_required_release_files_exist(self) -> None:
        missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
        self.assertEqual([], missing, f"Missing release files: {missing}")

    def test_version_is_consistent_across_manifests_and_skill(self) -> None:
        self.assertEqual(VERSION, (ROOT / "VERSION").read_text(encoding="utf-8").strip())

        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        meta, _ = read_frontmatter(SKILL_FILE)

        self.assertEqual("thinktank", claude["name"])
        self.assertEqual("thinktank", codex["name"])
        self.assertEqual("thinktank", package["name"])
        self.assertEqual(VERSION, claude["version"])
        self.assertEqual(VERSION, codex["version"])
        self.assertEqual(VERSION, package["version"])
        self.assertEqual(VERSION, meta["metadata"]["version"])
        self.assertEqual("./skills/", codex["skills"])
        self.assertEqual(["./skills"], package["pi"]["skills"])

    def test_skill_frontmatter_matches_agent_skills_contract(self) -> None:
        meta, _ = read_frontmatter(SKILL_FILE)
        name = str(meta.get("name", ""))
        description = str(meta.get("description", ""))
        compatibility = str(meta.get("compatibility", ""))

        self.assertEqual(SKILL_DIR.name, name)
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertTrue(description.startswith("Use when "), description)
        self.assertGreater(len(description), 40)
        self.assertLessEqual(len(description), 1024)
        self.assertIn("ambiguous", description.lower())
        self.assertIn("perspective", description.lower())
        self.assertLessEqual(len(compatibility), 500)
        self.assertEqual("MIT", meta.get("license"))
        self.assertEqual("thinktank", meta["metadata"]["plugin"])

    def test_skill_contains_behavioral_invariants(self) -> None:
        text = SKILL_FILE.read_text(encoding="utf-8").lower()
        missing = [marker for marker in REQUIRED_SKILL_MARKERS if marker.lower() not in text]
        self.assertEqual([], missing, f"Missing skill markers: {missing}")

    def test_skill_is_progressively_disclosed_and_links_are_shallow(self) -> None:
        text = SKILL_FILE.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLessEqual(len(text.split()), 5000)

        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        local_links = [link for link in links if "://" not in link and not link.startswith("#")]
        self.assertGreaterEqual(len(local_links), 6)
        for link in local_links:
            self.assertLessEqual(len(Path(link).parts), 2, f"Reference is too deeply nested: {link}")
            self.assertTrue((SKILL_DIR / link).is_file(), f"Broken relative link: {link}")

    def test_production_files_have_no_placeholders(self) -> None:
        targets = [
            ROOT / "README.md",
            ROOT / "CHANGELOG.md",
            *[path for path in REQUIRED_FILES if path.suffix in {".md", ".py", ".sh", ".json"}],
        ]
        pattern = re.compile(r"\b(?:TBD|TODO|FIXME|IMPLEMENT LATER)\b", re.IGNORECASE)
        violations: list[str] = []
        for path in targets:
            if not path.is_file():
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if pattern.search(line):
                    violations.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
        self.assertEqual([], violations, "Placeholder text found:\n" + "\n".join(violations))

    def test_shell_and_python_scripts_are_executable(self) -> None:
        scripts = [
            ROOT / "scripts" / "validate-package.py",
            ROOT / "scripts" / "install-skill.sh",
            ROOT / "scripts" / "package.sh",
            SKILL_DIR / "scripts" / "lint-report.py",
            ROOT / "tests" / "run.sh",
        ]
        not_executable = [
            str(path.relative_to(ROOT))
            for path in scripts
            if path.is_file() and not (path.stat().st_mode & stat.S_IXUSR)
        ]
        self.assertEqual([], not_executable, f"Scripts are not executable: {not_executable}")


if __name__ == "__main__":
    unittest.main()
