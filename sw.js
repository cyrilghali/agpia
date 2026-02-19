const CACHE_NAME = 'agpeya-82f53f2c';

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
  '/fonts/crimson-pro.woff2',
  '/fonts/eb-garamond.woff2',
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
  '/fr-old/index.html',
  '/fr-old/prime.html',
  '/fr-old/terce.html',
  '/fr-old/sext.html',
  '/fr-old/none.html',
  '/fr-old/vespers.html',
  '/fr-old/compline.html',
  '/fr-old/midnight.html',
  '/fr-old/veil.html',
  '/fr-old/other.html',
  '/fr-old/about.html',
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
  event.respondWith(
    caches.match(event.request)
      .then((cached) => cached || fetch(event.request))
  );
});
