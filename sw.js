// Service Worker pha-troi-v62-1789494666 cho Web Reader Phá Trời
const CACHE_NAME = 'pha-troi-v62-1789494666';
const ASSETS_TO_CACHE = [
  './manifest.json',
  './icon.svg',
  './cover.svg',
  './assets/logo.webp',
  './assets/cover_vertical.webp',
  './assets/hero_horizontal.webp'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // 1. Đối với HTML pages (Navigate / Document) và data/chapters.json:
  // CHIẾN LƯỢC: NETWORK-FIRST (Luôn lấy mới nhất trên mạng, chỉ dùng cache khi offline)
  if (e.request.mode === 'navigate' || e.request.destination === 'document' || url.pathname.includes('/data/')) {
    e.respondWith(
      fetch(e.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const resClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(e.request).then((cached) => cached || caches.match('./index.html'));
        })
    );
    return;
  }

  // 2. Đối với hình ảnh và static assets: Stale-While-Revalidate
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
        }
        return networkResponse;
      }).catch(() => null);

      return cachedResponse || fetchPromise;
    })
  );
});
