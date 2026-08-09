# -*- coding: utf-8 -*-
"""Repo-wide consistency checks. Run before publishing; also run by CI.

    python check_consistency.py            # all checks
    python check_consistency.py --quick    # skip the PDF layout audit

WHY THIS EXISTS
---------------
Every defect found in this project during final review was found by accident or by
a human reading carefully, not by a check. Three in particular are worth naming,
because the design here is a direct response to them:

1. A figure's title contradicted its own caption. Nothing compared them.
2. A claim was bounded in the notebook but left standing in `build_report.py`, which
   hardcodes the report's cover. Every scan searched notebook/markdown/HTML and none
   looked in the build scripts -- the claim was living in Python.
3. A keyword scan was built from the vocabulary of the claims already fixed
   ("benefit-reliant"), so it could not find the same claim in different words
   ("welfare-reliant").

The lesson in all three is the same: verification that enumerates where to look will
inherit the blind spots of whoever wrote the list. So SURFACES ARE DISCOVERED, NOT
LISTED. This script globs every text-bearing file in the repo and scans all of them.
Adding a new file type or a new build script cannot silently escape it.
"""
import argparse, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'.git', 'figures', 'fonts', 'data', '__pycache__', '.ipynb_checkpoints'}
TEXT_EXT = {'.md', '.py', '.js', '.css', '.yml', '.yaml', '.ipynb', '.html', '.txt'}

failures, warnings = [], []


def fail(check, msg):
    failures.append(f"[{check}] {msg}")


def warn(check, msg):
    warnings.append(f"[{check}] {msg}")


def discover():
    """Every text-bearing file in the repo. Not a hand-maintained list, deliberately."""
    out = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() in TEXT_EXT:
                out.append(os.path.join(root, f))
    return sorted(out)


def readable(path):
    """Prose from a file. For notebooks, markdown cells plus code comments -- a claim
    can hide in a comment, and did."""
    raw = open(path, encoding='utf-8', errors='replace').read()
    if path.endswith('.ipynb'):
        try:
            nb = json.loads(raw)
        except Exception:
            return raw
        parts = []
        for c in nb['cells']:
            src = ''.join(c['source'])
            if c['cell_type'] == 'markdown':
                parts.append(src)
            else:
                parts.append('\n'.join(l for l in src.splitlines() if l.lstrip().startswith('#')))
                for o in c.get('outputs', []):
                    if o.get('output_type') == 'stream':
                        parts.append(''.join(o.get('text', [])))
        return '\n'.join(parts)
    if path.endswith('.html'):
        raw = re.sub(r'<style.*?</style>', ' ', raw, flags=re.S)
        raw = re.sub(r'data:[^"\')]+', ' ', raw)
        raw = re.sub(r'<[^>]+>', ' ', raw)
    return raw


# --------------------------------------------------------------------------------
# 1. Claims that must not appear anywhere, in any surface.
#    Each entry is (label, regex, why). These are claims the analysis has retired or
#    bounded; an unqualified restatement anywhere is a contradiction of the report.
# --------------------------------------------------------------------------------
RETIRED = [
    ("benefit-reliance overclaim",
     r"disproportionately (benefit|welfare)[- ]relian|a majority (of these voters |)"
     r"(receive|reliant on|on) benefit|majority on benefits",
     "Section 7a bounds this: 53% CI [45,62], ns overall, and largely age."),
    ("unevidenced income shorthand",
     r"low-income-exposed",
     "Superseded by the measured household-income gap in Section 7a."),
    ("module code in reader-facing text",
     r"MA336(?!_Project_Notebook)",
     "Dropped in favour of the module title; the .ipynb filename is the exception."),
    ("superseded-draft reference",
     r"earlier version of this analysis",
     "Readers of the released version have no reason to care what a draft reported."),
]


def check_retired(files):
    for path in files:
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        text = readable(path)
        for label, pat, why in RETIRED:
            for m in re.finditer(pat, text, re.I):
                ctx = re.sub(r'\s+', ' ', text[max(0, m.start()-70):m.end()+70])
                fail(label, f"{os.path.relpath(path, REPO)}: ...{ctx}...\n           -> {why}")


# --------------------------------------------------------------------------------
# 2. Headline numbers must agree wherever they are stated.
# --------------------------------------------------------------------------------
# Only high-precision rules live here. A first version tried to validate every
# "<n> Reform voters" against an allow-list; it matched years ("2024 Reform voters")
# and legitimate valid-n subtotals, producing seventeen false positives. A check that
# cries wolf is worse than no check -- it gets ignored, and an ignored check still
# reads as reassurance. So these target specific stale values only, and a stale figure
# in a form not listed here will get past them. That limit is stated rather than hidden.
WRONG_VALUES = [
    ('2014 UKIP share', r'\b58%[^.]{0,40}(UKIP|left-behind)'),
    ('weighted split',  r'5[13]\s*/\s*4[35]\s*/\s*4'),
    ('analytic n',      r'\b3,9[0-5]\d\b'),
]


def check_numbers(files):
    for path in files:
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        text = readable(path)
        rel = os.path.relpath(path, REPO)
        for label, bad in WRONG_VALUES:
            for m in re.finditer(bad, text, re.I):
                ctx = re.sub(r'\s+', ' ', text[max(0, m.start()-70):m.end()+70])
                fail(f"number: {label}", f"{rel}: ...{ctx}...")


# --------------------------------------------------------------------------------
# 3. Typography, in the built PDFs -- where the reader actually meets it.
#    Checking sources would miss the fact that the markdown pipeline smart-quotes
#    body text but not strings hardcoded in the build scripts. That gap put the one
#    straight apostrophe in the project on the summary's cover.
# --------------------------------------------------------------------------------
def check_typography(pdfs):
    for pdf in pdfs:
        if not os.path.exists(pdf):
            continue
        txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
        # program output blocks legitimately contain ASCII quotes; those live in
        # monospace stdout, which pdftotext gives us no way to isolate. So only the
        # summary (which contains no code output) is checked strictly.
        strict = 'summary' in os.path.basename(pdf).lower()
        name = os.path.basename(pdf)
        if strict:
            if txt.count('"'):
                fail("typography", f"{name}: {txt.count(chr(34))} straight double quote(s)")
            if txt.count("'"):
                fail("typography", f"{name}: {txt.count(chr(39))} straight apostrophe(s)")
        if ' — ' in txt:
            fail("typography", f"{name}: spaced em dash (house style is closed)")


# --------------------------------------------------------------------------------
# 4. Page layout of the built PDFs.
# --------------------------------------------------------------------------------
def check_layout(pdfs, section_break_ok=()):
    try:
        import pdfplumber
    except ImportError:
        warn("layout", "pdfplumber not installed; skipping layout audit")
        return
    for pdf in pdfs:
        if not os.path.exists(pdf):
            continue
        name = os.path.basename(pdf)
        lenient = any(k in name for k in section_break_ok)
        with pdfplumber.open(pdf) as doc:
            for i, pg in enumerate(doc.pages, 1):
                H = pg.height
                # chars and images only: the full-bleed page tint is a rect spanning
                # every page, and counting it made an earlier version of this check
                # report a two-thirds-empty page as full.
                body = [o for o in list(pg.chars) + list(pg.images) if 45 < o['top'] < H - 55]
                if not body:
                    continue
                usable = (H - 55) - 45
                trail = ((H - 55) - max(o['bottom'] for o in body)) / usable * 100
                limit = 88 if lenient else 45
                if trail > limit:
                    warn("layout", f"{name} p{i}: {trail:.0f}% of the page below the last content")


# --------------------------------------------------------------------------------
# 5. The generated HTML must match what is committed.
# --------------------------------------------------------------------------------
def check_reproducible():
    for script, target in [('build_report.py', 'report/report.html'),
                           ('build_summary.py', 'report/SUMMARY.html')]:
        before = open(os.path.join(REPO, target), encoding='utf-8').read()
        r = subprocess.run([sys.executable, script], cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            fail("reproducible", f"{script} failed: {r.stderr.strip()[:200]}")
            continue
        after = open(os.path.join(REPO, target), encoding='utf-8').read()
        if before != after:
            fail("reproducible", f"{target} is not what {script} produces; rebuild and commit")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true', help='skip the PDF layout audit')
    args = ap.parse_args()

    files = discover()
    pdfs = [os.path.join(REPO, 'report', f) for f in (
        'One_Coalition_Two_Electorates_report.pdf',
        'One_Coalition_Two_Electorates_summary.pdf')]

    print(f"scanning {len(files)} text-bearing files (discovered, not listed)\n")
    check_retired(files)
    check_numbers(files)
    check_typography(pdfs)
    check_reproducible()
    if not args.quick:
        # the report opens each numbered section on a new page by design, so trailing
        # space there is intentional and judged leniently
        check_layout(pdfs, section_break_ok=('report.pdf',))

    for w in warnings:
        print("WARN ", w)
    for f in failures:
        print("FAIL ", f)
    print(f"\n{len(failures)} failure(s), {len(warnings)} warning(s)")
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
