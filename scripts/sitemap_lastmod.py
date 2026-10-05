"""Set every <lastmod> in sitemap.xml to its file's last git commit date.
Run after committing page changes: python scripts/sitemap_lastmod.py
Only the page's own HTML history counts — a change that reaches pages only
through a shared asset (e.g. assets/calculators.js prices) does not bump
their lastmod; touch those pages' HTML if the visible content changed.
Template-only commits listed in scripts/lastmod-ignore-revs.txt are skipped."""
import os, re, subprocess

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IGNORE = {l.split()[0] for l in open("scripts/lastmod-ignore-revs.txt", encoding="utf-8")
          if l.strip() and not l.startswith("#")}

def last_commit_date(loc):
    path = loc.replace("https://gameaccountvalue.com/", "")
    if path == "" or path.endswith("/"):
        path += "index.html"
    out = subprocess.run(["git", "log", "--format=%H %cs", "--", path],
                         capture_output=True, text=True).stdout.split("\n")
    for line in out:
        if line.strip() and line.split()[0] not in IGNORE:
            return line.split()[1]
    raise SystemExit(f"no content commit for {path}")

s = open("sitemap.xml", encoding="utf-8").read()
s, n = re.subn(r"<loc>([^<]*)</loc>(\s*)<lastmod>[^<]*</lastmod>",
               lambda m: f"<loc>{m.group(1)}</loc>{m.group(2)}<lastmod>{last_commit_date(m.group(1))}</lastmod>", s)
open("sitemap.xml", "w", encoding="utf-8", newline="").write(s)
print(n, "entries updated")
