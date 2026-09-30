// Pre-format event date labels for all 17 languages with CLDR (Intl).
// Output: scripts/design/event_dates.json  { eventId: { lang: "label" } }
const fs = require('fs');
const LANGS = ['en','ru','es','pt','id','tr','ar','vi','hi','fr','de','it','ja','ko','th','pl','zh','ms','uz'];
const EV = {
  'bs-bow': { month: '2026-10' }, 'bs-lcq': { start: '2026-10-17', end: '2026-10-18' }, 'bs-wf': { start: '2026-11-20', end: '2026-11-22' },
  'bs-8y': { start: '2026-12-12' }, 'ml-enc': { start: '2026-11-23', end: '2026-11-29' }, 'ml-m8': { month: '2027-01' },
  'ff-wsgf': { start: '2026-11-06' }, 'coc-lcq': { month: '2026-10' }, 'gi-6y': { start: '2026-09-28' },
  'r-bswf25': { start: '2025-11-28', end: '2025-11-30' }, 'r-msc26': { start: '2026-08-01' }, 'r-m7': { start: '2026-01-03', end: '2026-01-25' },
  'r-ffewc26': { start: '2026-07-18' }, 'r-fncs26': { start: '2026-09-26', end: '2026-09-27' }, 'r-crl25': { start: '2025-10-31', end: '2025-11-02' }, 'r-cocwc25': { start: '2025-10-31', end: '2025-11-02' },
};
const loc = l => (l === 'zh' ? 'zh-Hans' : l);
const d = s => new Date(s + 'T12:00:00Z');
const out = {};
for (const [id, e] of Object.entries(EV)) {
  out[id] = {};
  for (const l of LANGS) {
    if (e.month) {
      out[id][l] = new Intl.DateTimeFormat(loc(l), { month: 'long', year: 'numeric', timeZone: 'UTC' }).format(d(e.month + '-01'));
    } else {
      const f = new Intl.DateTimeFormat(loc(l), { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
      out[id][l] = e.end ? f.formatRange(d(e.start), d(e.end)) : f.format(d(e.start));
    }
  }
}
fs.writeFileSync(__dirname + '/event_dates.json', JSON.stringify(out));
console.log(out['bs-wf'].ru, '|', out['ml-enc'].ja, '|', out['ml-m8'].ar, '|', out['ff-wsgf'].th);
