const CACHE_NAME = 'agpeya-8a5f72cf';

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
  '/fr-unofficial/index.html',
  '/fr-unofficial/prime.html',
  '/fr-unofficial/terce.html',
  '/fr-unofficial/sext.html',
  '/fr-unofficial/none.html',
  '/fr-unofficial/vespers.html',
  '/fr-unofficial/compline.html',
  '/fr-unofficial/midnight.html',
  '/fr-unofficial/veil.html',
  '/fr-unofficial/other.html',
  '/fr-unofficial/about.html',
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
  '/fr-lsg/index.html',
  '/fr-lsg/prime.html',
  '/fr-lsg/terce.html',
  '/fr-lsg/sext.html',
  '/fr-lsg/none.html',
  '/fr-lsg/vespers.html',
  '/fr-lsg/compline.html',
  '/fr-lsg/midnight.html',
  '/fr-lsg/veil.html',
  '/fr-lsg/other.html',
  '/fr-lsg/about.html',
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
