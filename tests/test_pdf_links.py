"""Tests for skills/resume-enhancer/scripts/pdf_links.py. Run: python3 -m unittest discover tests -v"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_render import SCRIPTS, doc, needs_latex, render  # noqa: E402

LINKS = SCRIPTS / "pdf_links.py"


def links(tex):
    with tempfile.TemporaryDirectory() as d:
        pdf = Path(d) / "l.pdf"
        code, out, _ = render(tex, keep=pdf)
        assert code == 0, out
        return subprocess.run([sys.executable, str(LINKS), str(pdf)], capture_output=True, text=True)


@needs_latex
@unittest.skipUnless(shutil.which("pdftohtml"), "pdftohtml not installed")
class PdfLinks(unittest.TestCase):
    def test_links_listed_with_their_text(self):
        tex = doc(1, "\\usepackage{hyperref}\n").replace(
            "Page 1", "\\href{https://example.com/a}{\\textbf{Alpha}} and "
                      "\\href{mailto:me@example.com}{me@example.com}")
        r = links(tex)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Alpha -> https://example.com/a", r.stdout)
        self.assertIn("me@example.com -> mailto:me@example.com", r.stdout)

    def test_no_links_prints_nothing(self):
        r = links(doc(1))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
