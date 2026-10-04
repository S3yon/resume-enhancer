# Changelog

## 0.1.0 (2026-10-04)

- New skill `resume-enhancer`: setup questions, a facts file, an audit against 28 house-style
  rules, a change table to approve, and a render within the page limit.
- Scripts: `fill_template.py` (dense or roomy look); `render.sh` (page limit 1 or 2, clear exits
  for no LaTeX and missing packages, keeps an `-overflow.pdf` when over the limit);
  `fill_check.py` (line fill, wrapped bullets and skill lines, lines past page 1);
  `pdf_links.py` (link targets from a PDF, which pdftotext drops).
- `latex.md` with install lines for macOS, Ubuntu/Debian and Windows (WSL), and online compile
  steps. The template's MIT notice ships inside the skill folder.
- Manifests for the same tools as skill-kit. Tests and `validate.py` run in CI.
