#!/usr/bin/env python3
"""Show how full each line of a resume PDF is, so bullets can be sized to the right margin.

Usage: fill_check.py <resume.pdf>
Prints each line's fill (% of the widest line) and its text. A bullet that wraps shows as a
short line with no leading bullet straight after a full one. Pages after the first are flagged.
"""
import re
import subprocess
import sys
from html import unescape

xml = subprocess.run(["pdftotext", "-bbox-layout", sys.argv[1], "-"], capture_output=True, text=True).stdout
pages = xml.split("<page ")[1:]
rows = []
for n, page in enumerate(pages, 1):
    for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', page, re.S):
        words = [unescape(w) for w in re.findall(r">([^<]+)</word>", m.group(5))]
        rows.append((n, float(m.group(1)), float(m.group(2)), float(m.group(3)), " ".join(words)))
right = max(r[3] for r in rows)
left = min(r[1] for r in rows)
bottom = max(r[2] for r in rows if r[0] == 1)
for n, x0, y, x1, text in rows:
    fill = (x1 - left) / (right - left) * 100
    print(f"{'P'+str(n) if n > 1 else '  '} {fill:5.1f}%  {text[:110]}")
print(f"pages={len(pages)}  last line of page 1 at y={bottom:.0f} of 792pt")
