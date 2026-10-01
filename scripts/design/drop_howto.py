"""Remove HowTo from JSON-LD (Google retired HowTo rich results in 2023; dead markup). Idempotent."""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.sep
n = 0
for f in glob.glob(ROOT + '**/*.html', recursive=True):
    if os.sep + 'scripts' + os.sep in f:
        continue
    s = open(f, encoding='utf-8').read()
    if '"HowTo"' not in s:
        continue
    def fix(m):
        j = json.loads(m.group(1))
        if isinstance(j, dict) and '@graph' in j:
            j['@graph'] = [x for x in j['@graph'] if x.get('@type') != 'HowTo']
        elif isinstance(j, dict) and j.get('@type') == 'HowTo':
            return ''
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, indent=2) + '</script>'
    t = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)
    if t != s:
        open(f, 'w', encoding='utf-8', newline='').write(t); n += 1
print('pages fixed', n)
