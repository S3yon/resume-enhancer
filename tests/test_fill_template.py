"""Tests for skills/resume-enhancer/scripts/fill_template.py. Run: python3 -m unittest discover tests -v"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILL = ROOT / "skills" / "resume-enhancer" / "scripts" / "fill_template.py"


def fill(body, *args):
    """Run the filler on body text; return (result, output tex or None)."""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "body.tex"
        src.write_text(body)
        out = Path(d) / "out.tex"
        r = subprocess.run([sys.executable, str(FILL), str(src), str(out), *args],
                           capture_output=True, text=True)
        return r, out.read_text() if out.exists() else None


class FillTemplate(unittest.TestCase):
    def test_fill_replaces_markers(self):
        r, out = fill("\\section{Experience}\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("%%LOOK%%", out)
        self.assertNotIn("%%BODY%%", out)
        self.assertIn("\\roomyfalse", out)
        self.assertIn("\\section{Experience}", out)
        r, out = fill("x", "--look", "roomy")
        self.assertIn("\\roomytrue", out)

    def test_body_kept_verbatim(self):
        body = "C\\#, R\\&D, \\1 and the text %%BODY%% and %%LOOK%% stay as written\n"
        r, out = fill(body)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(body, out)

    def test_bad_look_exits_nonzero(self):
        r, out = fill("x", "--look", "huge")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("invalid choice", r.stderr)
        self.assertIsNone(out)

    def test_missing_marker_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            template = Path(d) / "t.tex"
            template.write_text("\\newif\\ifroomy\n%%LOOK%%\n\\begin{document}\n\\end{document}\n")
            r, out = fill("x", "--template", str(template))
        self.assertEqual(r.returncode, 1)
        self.assertIn("template is missing %%BODY%%", r.stderr)
        self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
