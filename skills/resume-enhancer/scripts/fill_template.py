#!/usr/bin/env python3
"""Put a resume body into the house-style template.

Usage: fill_template.py <body.tex> <out.tex> [--look dense|roomy] [--template PATH]

Sets the look first, then inserts the body verbatim, so text in the body is never treated as a
marker. Exits 1 if the template is missing a marker.
"""
import argparse
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.tex"
LOOKS = {"dense": "\\roomyfalse", "roomy": "\\roomytrue"}


def main():
    p = argparse.ArgumentParser(description="Put a resume body into the template.")
    p.add_argument("body", help="file holding everything between \\begin{document} and \\end{document}")
    p.add_argument("out", help="where to write the full .tex")
    p.add_argument("--look", choices=LOOKS, default="dense")
    p.add_argument("--template", default=str(TEMPLATE))
    args = p.parse_args()

    tex = Path(args.template).read_text()
    for marker in ("%%LOOK%%", "%%BODY%%"):
        if marker not in tex:
            sys.exit(f"template is missing {marker}")
    tex = tex.replace("%%LOOK%%", LOOKS[args.look], 1)
    tex = tex.replace("%%BODY%%", Path(args.body).read_text(), 1)
    Path(args.out).write_text(tex)


if __name__ == "__main__":
    main()
