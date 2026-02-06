const CACHE_NAME = "agpia-v1";

const PRECACHE_URLS = [
  "/",
  "/index.html",
  "/app.js",
  "/styles.css",
  "/site.webmanifest",
  "/CS%20Avva%20Shenouda.ttf",
  "/favicon-96x96.png",
  "/favicon.svg",
  "/favicon.ico",
  "/apple-touch-icon.png",
  "/web-app-manifest-192x192.png",
  "/web-app-manifest-512x512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((names) => Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.open(CACHE_NAME).then((cache) =>
      cache.match(event.request).then((cached) => {
        if (cached) return cached;
        return fetch(event.request).then(
          (response) => {
            const clone = response.clone();
            cache.put(event.request, clone);
            return response;
          },
          () => {
            if (event.request.mode === "navigate") {
              return cache.match("/index.html").then((index) => index || cache.match("/"));
            }
            return new Response("", { status: 503, statusText: "Service Unavailable" });
          }
        );
      })
    )
  );
});
