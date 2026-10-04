"""Tests for render.sh, fill_check.py and the template. Run: python3 -m unittest discover tests -v

Tests that need LaTeX skip when it isn't installed, so CI runs without it.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "resume-enhancer" / "scripts"
RENDER = SCRIPTS / "render.sh"
SAMPLE = ROOT / "tests" / "fixtures" / "sample-body.tex"
HAS_LATEX = bool(shutil.which("pdflatex")) or Path("/Library/TeX/texbin/pdflatex").exists()
HAS_PDFTOTEXT = bool(shutil.which("pdftotext"))
needs_latex = unittest.skipUnless(HAS_LATEX, "pdflatex not installed")


def doc(pages, preamble=""):
    body = "\n\\newpage\n".join(f"Page {i + 1}" for i in range(pages))
    return f"\\documentclass{{article}}\n{preamble}\\begin{{document}}\n{body}\n\\end{{document}}\n"


def render(tex, *args, env=None, keep=None):
    """Render tex with render.sh; return (exit code, stdout+stderr, pdf written?)."""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "r.tex"
        src.write_text(tex)
        out = Path(keep) if keep else Path(d) / "r.pdf"
        r = subprocess.run(["bash", str(RENDER), str(src), str(out), *args],
                           capture_output=True, text=True, env={**os.environ, **(env or {})})
        return r.returncode, r.stdout + r.stderr, out.exists()


def filled(look, body=None):
    with tempfile.TemporaryDirectory() as d:
        src, out = Path(d) / "body.tex", Path(d) / "out.tex"
        src.write_text(body if body is not None else SAMPLE.read_text())
        subprocess.run([sys.executable, str(SCRIPTS / "fill_template.py"), str(src), str(out),
                        "--look", look], check=True)
        return out.read_text()


def fill_check(tex):
    """Render tex and return fill_check.py's stdout."""
    with tempfile.TemporaryDirectory() as d:
        pdf = Path(d) / "s.pdf"
        code, out, _ = render(tex, keep=pdf)
        assert code == 0, out
        return subprocess.run([sys.executable, str(SCRIPTS / "fill_check.py"), str(pdf)],
                              capture_output=True, text=True, check=True).stdout


def left_edge(pdf):
    xml = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True).stdout
    return min(float(x) for x in re.findall(r'xMin="([\d.]+)"', xml))


class Render(unittest.TestCase):
    def test_no_latex_exits_3(self):
        code, out, pdf = render(doc(1), env={"PDFLATEX": "/nonexistent/pdflatex"})
        self.assertEqual(code, 3, out)
        self.assertIn("no LaTeX found", out)
        self.assertFalse(pdf)

    def test_bad_pages(self):
        for pages in ("abc", "0", "3"):
            code, out, _ = render(doc(1), pages)
            self.assertEqual(code, 1, f"{pages}: {out}")
            self.assertIn("must be 1 or 2", out)

    @needs_latex
    def test_one_page_ok(self):
        code, out, pdf = render(doc(1))
        self.assertEqual(code, 0, out)
        self.assertIn("OK — 1 page", out)
        self.assertTrue(pdf)

    @needs_latex
    def test_two_pages_rejected_by_default(self):
        code, out, pdf = render(doc(2))
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: rendered 2 pages, limit is 1", out)
        self.assertFalse(pdf)

    @needs_latex
    def test_overflow_pdf_kept_for_cutting(self):
        with tempfile.TemporaryDirectory() as d:
            src, out = Path(d) / "r.tex", Path(d) / "r.pdf"
            src.write_text(doc(2))
            r = subprocess.run(["bash", str(RENDER), str(src), str(out)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertFalse(out.exists())
            self.assertTrue((Path(d) / "r-overflow.pdf").exists())
            self.assertIn("r-overflow.pdf", r.stdout)

    @needs_latex
    def test_two_pages_ok_with_limit_2(self):
        code, out, pdf = render(doc(2), "2")
        self.assertEqual(code, 0, out)
        self.assertTrue(pdf)

    @needs_latex
    def test_three_pages_rejected_with_limit_2(self):
        code, out, _ = render(doc(3), "2")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: rendered 3 pages, limit is 2", out)

    @needs_latex
    def test_missing_package_named(self):
        code, out, _ = render(doc(1, "\\usepackage{nosuchpkg}\n"))
        self.assertEqual(code, 1, out)
        self.assertIn("missing LaTeX package: nosuchpkg.sty", out)


@needs_latex
@unittest.skipUnless(HAS_PDFTOTEXT, "pdftotext not installed")
class Template(unittest.TestCase):
    def test_dense_one_page(self):
        code, out, _ = render(filled("dense"))
        self.assertEqual(code, 0, out)
        self.assertIn("OK — 1 page", out)

    def test_roomy_margin_wider(self):
        with tempfile.TemporaryDirectory() as d:
            dense, roomy = Path(d) / "dense.pdf", Path(d) / "roomy.pdf"
            self.assertEqual(render(filled("dense"), keep=dense)[0], 0)
            self.assertEqual(render(filled("roomy"), keep=roomy)[0], 0)
            self.assertGreaterEqual(left_edge(roomy) - left_edge(dense), 15)

    def test_fill_check_reports_each_line(self):
        with tempfile.TemporaryDirectory() as d:
            pdf = Path(d) / "s.pdf"
            self.assertEqual(render(filled("dense"), keep=pdf)[0], 0)
            r = subprocess.run([sys.executable, str(SCRIPTS / "fill_check.py"), str(pdf)],
                               capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("pages=1", r.stdout)
        self.assertRegex(r.stdout, r"100\.0%\s+\S")


    def test_fill_check_flags_wrapped_bullet(self):
        long_item = ("        \\resumeItem{Built a reporting service in Python that pulls data from four "
                     "internal systems, cleans it, and emails a summary to every regional manager each morning "
                     "before the daily planning call starts}\n")
        body = SAMPLE.read_text().replace("      \\resumeItemListEnd", long_item + "      \\resumeItemListEnd", 1)
        out = fill_check(filled("dense", body))
        self.assertIn("wrapped lines: 1", out)
        self.assertRegex(out, r"<- wrapped")

    def test_fill_check_no_false_wrap(self):
        out = fill_check(filled("dense"))
        self.assertIn("wrapped lines: 0", out)
        self.assertIn("lines past page 1: 0", out)
        self.assertNotIn("<- wrapped", out)

    def test_fill_check_flags_wrapped_skill_line(self):
        long_line = ("     \\textbf{Tools}{: Git, Docker, Linux, Kubernetes, Terraform, Ansible, Jenkins, "
                     "GitHub Actions, Prometheus, Grafana, Postman, Figma, Jira, Confluence, Notion, Slack, "
                     "Visual Studio Code}")
        body = SAMPLE.read_text().replace("     \\textbf{Tools}{: Git, Docker, Linux}", long_line, 1)
        self.assertNotEqual(body, SAMPLE.read_text())
        out = fill_check(filled("dense", body))
        self.assertIn("wrapped lines: 1", out)

    def test_fill_check_counts_lines_past_the_limit(self):
        with tempfile.TemporaryDirectory() as d:
            pdf = Path(d) / "two.pdf"
            self.assertEqual(render(doc(2, "\\pagestyle{empty}\n"), "2", keep=pdf)[0], 0)
            r = subprocess.run([sys.executable, str(SCRIPTS / "fill_check.py"), str(pdf)],
                               capture_output=True, text=True, check=True)
        self.assertIn("lines past page 1: 1", r.stdout)


if __name__ == "__main__":
    unittest.main()
