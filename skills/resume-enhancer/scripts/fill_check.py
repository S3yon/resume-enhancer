#!/usr/bin/env python3
"""Show how full each line of a resume PDF is, so bullets can be sized to the right margin.

Usage: fill_check.py <resume.pdf>
Prints each line's fill (% of the widest line) and its text, then a summary. A bullet that
wraps leaves a line starting where bullet text starts, with no bullet mark; it is flagged
'<- wrapped bullet'. Pages after the first are marked P2, P3.
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
        words = [(float(x), unescape(w)) for x, w in re.findall(r'<word xMin="([\d.]+)"[^>]*>([^<]+)</word>', m.group(5))]
        rows.append((n, float(m.group(1)), float(m.group(2)), float(m.group(3)), words))
right = max(r[3] for r in rows)
left = min(r[1] for r in rows)
bottom = max(r[2] for r in rows if r[0] == 1)
# where bullet text starts: the first word after the bullet mark
text_x = min((w[1][0] for *_, w in rows if len(w) > 1 and w[0][1] == "•"), default=None)
wrapped = 0
for n, x0, y, x1, words in rows:
    fill = (x1 - left) / (right - left) * 100
    text = " ".join(w for _, w in words)
    wrap = text_x is not None and words[0][1] != "•" and abs(x0 - text_x) < 2
    wrapped += wrap
    print(f"{'P'+str(n) if n > 1 else '  '} {fill:5.1f}%  {text[:110]}{'  <- wrapped bullet' if wrap else ''}")
print(f"pages={len(pages)}  last line of page 1 at y={bottom:.0f} of 792pt  wrapped bullets: {wrapped}")
