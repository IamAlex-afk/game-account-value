/* GameAccountValue Service Worker — offline + PWA install */
const CACHE = 'gav-landing-2026-22';
const PRECACHE = [
  './', './index.html', './404.html', './manifest.json',
  './favicon.png', './favicon.svg', './apple-touch-icon.png', './og-image.jpg',
  './icon-192.png', './icon-512-maskable.png', './icon-192-maskable.png',
  './assets/style.css', './assets/nav.js', './assets/cursor-trail.js', './assets/tilt.js',
  './assets/interactions.js', './assets/counter.js',
  './ru/', './de/', './es/', './fr/', './it/', './ja/', './ko/', './pt/',
  './th/', './tr/', './vi/', './ar/', './hi/', './id/', './zh/', './pl/',
  './tl/', './sw/', './ms/', './uz/', './kk/', './tk/', './ky/',
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

  // Stale-while-revalidate: answer from cache instantly, refresh the cached
  // copy in the background, so an edited JS/CSS file reaches returning
  // visitors on their next load without needing a CACHE version bump.
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
      return network.catch(() => caches.match('./index.html'));
    })
  );
});
