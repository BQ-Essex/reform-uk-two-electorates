# -*- coding: utf-8 -*-
"""Render report/SUMMARY.md to report/SUMMARY.html in the report's house style.

SUMMARY.html used to be maintained by hand. It drifted from the rest of the project
three separate times -- a mistitled figure, a reworded claim and an added reference
all had to be patched into it manually, and CI could not catch any of them because it
only diffs report.html. Generating it from SUMMARY.md removes that whole class of
failure: the markdown is the single source, and the styling comes from report_style,
which build_report.py imports too.

    pip install markdown
    python build_summary.py
"""
import os, re
import markdown
from report_style import b64, FONTS, CSS

REPO = os.path.dirname(os.path.abspath(__file__))
SRC = REPO + '/report/SUMMARY.md'
FIGDIR = REPO + '/figures'
OUT = REPO + '/report/SUMMARY.html'

md = markdown.Markdown(extensions=['extra', 'sane_lists', 'smarty'])

raw = open(SRC, encoding='utf-8').read()

# The cover is built from the markdown's own front matter rather than duplicated here,
# so editing SUMMARY.md is genuinely the only place the summary is authored.
def _inline(t):
    # push cover text through the same smarty filter as the body, so the apostrophes
    # and dashes in the title block match the prose rather than staying ASCII
    return re.sub(r'</?p>', '', md.convert(t)).strip()

title = _inline(re.search(r'^#\s+(.*)', raw, re.M).group(1).strip())
standfirst = _inline(re.search(r'^###\s+(.*)', raw, re.M).group(1).strip())
md.reset()
body_md = raw.split('---', 1)[1] if '---' in raw else raw
# drop the byline and the "this is the plain-language version" italic note from the body;
# both are represented in the cover block instead
body_md = re.sub(r'^\*Bradley Quinlan[^\n]*\*\s*$', '', body_md, flags=re.M)
body_md = re.sub(r'^\*This is the plain-language version.*?\*\s*$', '', body_md,
                 flags=re.M | re.S)

BODY = md.convert(body_md)

# Markdown images point at ../figures/NAME.png; inline them as base64 so the file is
# self-contained, and promote each to a <figure> with its alt text as the caption.
def inline_figure(m):
    alt, src = m.group(1), m.group(2)
    fn = os.path.basename(src)
    path = os.path.join(FIGDIR, fn)
    if not os.path.exists(path):
        return m.group(0)
    return (f'<figure><img alt="{alt}" src="data:image/png;base64,{b64(path)}">'
            f'<figcaption>{alt}</figcaption></figure>')

BODY = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)"\s*/?></p>', inline_figure, BODY)

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}&mdash;summary</title><meta name="author" content="Bradley Quinlan">
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>{FONTS}{CSS}</style></head><body><div class="wrap">
<header class="cover"><p class="eyebrow">Plain-language summary &middot; 2026</p>
<h1 class="title">{title}</h1>
<p class="standfirst">{standfirst}</p>
<div class="meta"><span><b>Bradley Quinlan</b></span><span>University of Essex</span><span>Artificial Intelligence and Machine Learning with Applications</span><span><a href="report.html">Full report</a> &middot; <a href="../notebook/">Notebook</a></span></div>
</header><main>{BODY}</main></div></body></html>'''

open(OUT, 'w', encoding='utf-8').write(HTML)
print("wrote", OUT, f"({len(HTML)/1e6:.2f} MB)")
