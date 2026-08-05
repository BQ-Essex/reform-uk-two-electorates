# -*- coding: utf-8 -*-
"""Render report/report.html and report/SUMMARY.html to print-tuned PDFs.

Reads the two HTML files exactly as they stand (does not edit them) and applies
print.css on top at render time only, so the screen versions are untouched.
Requires: pip install weasyprint
"""
import os
import sys
from weasyprint import HTML, CSS

REPO = os.path.dirname(os.path.abspath(__file__))
PRINT_CSS = os.path.join(REPO, "print.css")

JOBS = [
    ("report/report.html", "report/One_Coalition_Two_Electorates_report.pdf"),
    ("report/SUMMARY.html", "report/One_Coalition_Two_Electorates_summary.pdf"),
]


def build(src_rel, out_rel, repo_root):
    src = os.path.join(repo_root, src_rel)
    out = os.path.join(repo_root, out_rel)
    HTML(filename=src).write_pdf(out, stylesheets=[CSS(filename=PRINT_CSS)])
    size_mb = os.path.getsize(out) / 1e6
    print(f"wrote {out} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    repo_root = sys.argv[1] if len(sys.argv) > 1 else REPO
    for src_rel, out_rel in JOBS:
        build(src_rel, out_rel, repo_root)
