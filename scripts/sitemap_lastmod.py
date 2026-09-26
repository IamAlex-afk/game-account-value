"""Set every <lastmod> in sitemap.xml to its file's last git commit date.
Run after committing page changes: python scripts/sitemap_lastmod.py
Only the page's own HTML history counts — a change that reaches pages only
through a shared asset (e.g. assets/calculators.js prices) does not bump
their lastmod; touch those pages' HTML if the visible content changed."""
import os, re, subprocess

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def last_commit_date(loc):
    path = loc.replace("https://gameaccountvalue.com/", "")
    if path == "" or path.endswith("/"):
        path += "index.html"
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                         capture_output=True, text=True).stdout.strip()
    if not out:
        raise SystemExit(f"no git history for {path}")
    return out

s = open("sitemap.xml", encoding="utf-8").read()
s, n = re.subn(r"<loc>([^<]*)</loc>(\s*)<lastmod>[^<]*</lastmod>",
               lambda m: f"<loc>{m.group(1)}</loc>{m.group(2)}<lastmod>{last_commit_date(m.group(1))}</lastmod>", s)
open("sitemap.xml", "w", encoding="utf-8", newline="").write(s)
print(n, "entries updated")
