/* GameAccountValue Service Worker — offline + PWA install */
const CACHE = 'gav-landing-2026-7';
const PRECACHE = [
  './', './index.html', './404.html', './manifest.json',
  './favicon.png', './favicon.svg', './apple-touch-icon.png', './og-image.png',
  './icon-192.png', './icon-512-maskable.png', './icon-192-maskable.png',
  './assets/style.css', './assets/nav.js', './assets/cursor-trail.js', './assets/tilt.js',
  './assets/interactions.js', './assets/counter.js',
  './ru/', './de/', './es/', './fr/', './it/', './ja/', './ko/', './pt/',
  './th/', './tr/', './vi/', './ar/', './hi/', './id/',
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

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        }
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
