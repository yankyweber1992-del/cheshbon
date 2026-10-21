const CACHE = 'cheshbon-v5';
const FILES = ['./', './index.html', './manifest.json', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png',
  './fonts/frank-hebrew-400.woff2', './fonts/frank-hebrew-500.woff2', './fonts/frank-hebrew-700.woff2',
  './fonts/frank-latin-400.woff2', './fonts/frank-latin-500.woff2', './fonts/frank-latin-700.woff2',
  './fonts/instrument-400.woff2', './fonts/instrument-500.woff2', './fonts/instrument-600.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
