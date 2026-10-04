#!/usr/bin/env python3
"""List the links in a PDF with the text they sit on, since pdftotext drops link targets.

Usage: pdf_links.py <resume.pdf>
Prints one 'text -> url' line per link, in page order. Prints nothing when there are none.
Needs pdftohtml, which comes with pdftotext (poppler).
"""
import html
import re
import shutil
import subprocess
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if not shutil.which("pdftohtml"):
        sys.exit("pdftohtml not found; it comes with pdftotext (poppler)")
    xml = subprocess.run(["pdftohtml", "-xml", "-i", "-stdout", sys.argv[1]],
                         capture_output=True, text=True, check=True).stdout
    for url, inner in re.findall(r'<a href="([^"]*)">(.*?)</a>', xml, re.S):
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", "", inner)).split()).rstrip(",")
        print(f"{text} -> {html.unescape(url)}")


if __name__ == "__main__":
    main()
