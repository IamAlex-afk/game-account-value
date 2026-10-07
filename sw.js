/* GameAccountValue Service Worker — offline + PWA install */
const CACHE = 'gav-landing-2026-31';
// Only the shell: other languages' homepages are NOT precached any more — on a
// phone that was ~1.5 MB of background download competing with the page.
const PRECACHE = [
  './', './404.html', './manifest.json',
  './favicon.png', './favicon.ico', './favicon-192.png', './apple-touch-icon.png',
  './assets/style.css', './assets/glass.css', './assets/glass.js', './assets/nav.js',
  './assets/calculators.js', './assets/fonts/inter-latin.woff2',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || !e.request.url.startsWith(self.location.origin)) return;

  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => caches.match(e.request).then(cached => cached || caches.match('./index.html')))
    );
    return;
  }

  // CSS/JS: network first, cache only as the offline fallback. Stale-while-
  // revalidate served the previous deploy's CSS with the new HTML on the first
  // visit after every update (shifted buttons, missing art). Images/fonts keep
  // cache-first-then-refresh since they never change under the same name.
  const isCode = /\.(css|js)(\?|$)/.test(e.request.url);
  if (isCode) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => {
      const network = fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      });
      if (cached) {
        e.waitUntil(network.catch(() => {}));
        return cached;
      }
      return network.catch(() => caches.match('./404.html'));
    })
  );
});
