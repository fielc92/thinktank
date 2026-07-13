from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "skills" / "collaborating" / "scripts" / "lint-report.py"
FIXTURES = ROOT / "tests" / "fixtures"


class ReportLinterBehaviorTests(unittest.TestCase):
    def run_linter(self, fixture: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(LINTER), str(FIXTURES / fixture)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_typical_linear_answer_is_rejected(self) -> None:
        result = self.run_linter("linear-answer.md")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing-section", result.stdout)
        self.assertIn("solution-set-count", result.stdout)

    def test_hollow_consensus_is_rejected(self) -> None:
        result = self.run_linter("hollow-consensus.md")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("perspective-count", result.stdout)
        self.assertIn("epistemic-tags", result.stdout)
        self.assertIn("empty-minority-report", result.stdout)

    def test_complete_deliberation_report_is_accepted(self) -> None:
        result = self.run_linter("compliant-report.md")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_input_uses_usage_exit_code(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LINTER)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("usage:", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
