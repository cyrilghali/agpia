const CACHE_NAME = 'agpeya-bff7aa2c';
const CACHE_MAX_AGE_MS = 60 * 60 * 1000; // 1 hour
const CACHE_TIMESTAMP_KEY = '__cache_created_at__';

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
  '/fonts/avva-shenouda.woff2',
  '/cop/index.html',
  '/cop/prime.html',
  '/cop/terce.html',
  '/cop/sext.html',
  '/cop/none.html',
  '/cop/vespers.html',
  '/cop/compline.html',
  '/cop/midnight.html',
  '/cop/veil.html',
  '/cop/other.html',
  '/cop/about.html',
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
      .then((cache) => cache.addAll(PRECACHE_URLS).then(() => {
        const timestamp = new Response(JSON.stringify({ createdAt: Date.now() }));
        return cache.put(CACHE_TIMESTAMP_KEY, timestamp);
      }))
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

// Check cache age and refresh if expired
async function checkCacheAge() {
  const cache = await caches.open(CACHE_NAME);
  const response = await cache.match(CACHE_TIMESTAMP_KEY);
  if (!response) return;
  const { createdAt } = await response.json();
  if (Date.now() - createdAt > CACHE_MAX_AGE_MS) {
    await caches.delete(CACHE_NAME);
    const fresh = await caches.open(CACHE_NAME);
    await fresh.addAll(PRECACHE_URLS);
    await fresh.put(CACHE_TIMESTAMP_KEY, new Response(JSON.stringify({ createdAt: Date.now() })));
    const clients = await self.clients.matchAll();
    clients.forEach((client) => client.postMessage({ type: 'CACHE_REFRESHED' }));
  }
}

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) {
    return;
  }
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        checkCacheAge();
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
