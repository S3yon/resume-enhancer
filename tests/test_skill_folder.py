"""The skill folder must work when copied alone. Run: python3 -m unittest discover tests -v"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "resume-enhancer"
TEXT_FILES = [p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts
              and (p.suffix in {".md", ".json", ".tex", ".py", ".sh"} or p.name == "NOTICE")]


class SkillFolder(unittest.TestCase):
    def test_notice_travels_with_the_template(self):
        notice = SKILL / "NOTICE"
        self.assertTrue(notice.exists())
        text = notice.read_text()
        self.assertIn("Copyright (c) 2020 Jake Gutierrez", text)
        self.assertIn("Permission is hereby granted", text)
        self.assertIn("NOTICE in this skill folder", (SKILL / "assets" / "template.tex").read_text())

    def test_no_references_outside_the_folder(self):
        for p in TEXT_FILES:
            text = p.read_text()
            for outside in ("../", "README", "tests/"):
                self.assertNotIn(outside, text, f"{p.relative_to(ROOT)} mentions {outside}")

    def test_commands_run_from_the_persons_folder(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertIsNone(re.search(r"(python3|bash) scripts/", text))
        self.assertIn("<skill>/scripts/", text)
        self.assertIn("from the person's folder", text)

    def test_windows_route_is_workable(self):
        row = next(l for l in (SKILL / "latex.md").read_text().splitlines() if l.startswith("| Windows"))
        self.assertIn("WSL", row)


if __name__ == "__main__":
    unittest.main()
