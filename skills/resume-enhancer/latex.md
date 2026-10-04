# LaTeX setup

Rendering needs `pdflatex` and `pdftotext`. Without LaTeX, hand the person `resume.tex` with
the steps below and stop. Install nothing for them.

| System | Install |
|---|---|
| macOS | `brew install --cask mactex-no-gui` (full TeX Live) and `brew install poppler` |
| Ubuntu, Debian | `sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-extra poppler-utils` |
| Windows | The scripts need bash, so run them in WSL: `wsl --install` in an administrator PowerShell installs Ubuntu, then use the Ubuntu line above. MiKTeX (https://miktex.org/download) can compile `resume.tex` on Windows itself and installs missing packages on its own. |

Checked against https://formulae.brew.sh/cask/mactex-no-gui, the Debian package contents
search at https://packages.debian.org (which package holds each `.sty` the template loads, and
`pdftotext`), https://miktex.org/howto/install-miktex, and
https://learn.microsoft.com/en-us/windows/wsl/install, 2026-10-04.

## Compile online instead

1. Zip `resume.tex` on its own.
2. In Overleaf (a free account works), click **New project**, pick **Existing project (.zip)**,
   and choose the zip.
3. The project opens and compiles with pdfLaTeX, Overleaf's default. Download the PDF.

Checked against https://www.overleaf.com/learn/how-to/Uploading_a_project and
https://www.overleaf.com/learn/how-to/Changing_compiler, 2026-10-04.
