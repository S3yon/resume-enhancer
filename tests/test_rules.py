"""Tests for rules.md and the audit fixture. Run: python3 -m unittest discover tests -v"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "skills" / "resume-enhancer" / "rules.md"
FIXTURES = ROOT / "tests" / "fixtures"


def rule_numbers():
    return [int(n) for n in re.findall(r"^\s*(\d+)\. ", RULES.read_text(), re.M)]


class Rules(unittest.TestCase):
    def test_rules_numbered_1_to_28(self):
        self.assertEqual(rule_numbers(), list(range(1, 29)))

    def test_no_review_tags(self):
        text = RULES.read_text()
        self.assertNotIn("[written]", text)
        self.assertNotIn("[observed]", text)

    def test_expected_rules_exist(self):
        cited = [int(n) for n in re.findall(r"^rule (\d+):", (FIXTURES / "expected.md").read_text(), re.M)]
        self.assertTrue(cited)
        self.assertLessEqual(set(cited), set(rule_numbers()))

    def test_fixture_is_fictional(self):
        emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", (FIXTURES / "messy-resume.txt").read_text())
        self.assertTrue(emails)
        self.assertTrue(all(e.endswith("@example.com") for e in emails), emails)


if __name__ == "__main__":
    unittest.main()
