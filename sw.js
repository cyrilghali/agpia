const CACHE_NAME = 'agpeya-7f752427';

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/agpeya-style.css',
  '/agpeya.js',
  '/coptic-cross.png',
  '/cog_wheel.png',
  '/Avva_Shenouda.ttf',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/manifest.json',
  '/en/index.html',
  '/en/prime.html',
  '/en/terce.html',
  '/en/sext.html',
  '/en/none.html',
  '/en/vespers.html',
  '/en/compline.html',
  '/en/midnight.html',
  '/en/veil.html',
  '/en/other.html',
  '/en/about.html',
  '/fr/index.html',
  '/fr/prime.html',
  '/fr/terce.html',
  '/fr/sext.html',
  '/fr/none.html',
  '/fr/vespers.html',
  '/fr/compline.html',
  '/fr/midnight.html',
  '/fr/veil.html',
  '/fr/other.html',
  '/fr/about.html',
  '/ar/index.html',
  '/ar/prime.html',
  '/ar/terce.html',
  '/ar/sext.html',
  '/ar/none.html',
  '/ar/vespers.html',
  '/ar/compline.html',
  '/ar/midnight.html',
  '/ar/veil.html',
  '/ar/other.html',
  '/ar/about.html',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Google Fonts: network-first, cache on success
  if (url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Local assets: cache-first
  event.respondWith(
    caches.match(event.request)
      .then((cached) => cached || fetch(event.request))
  );
});
