const CACHE_NAME = 'techexe-lms-v2';

// Essential assets to cache on install
const STATIC_ASSETS = [
  '/LMS/offline/',
  'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css',
  'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js'
];

// 1. Install & Cache Essential Assets Safely
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of STATIC_ASSETS) {
        try {
          const response = await fetch(asset, { credentials: 'same-origin' });
          if (response.status === 200) {
            await cache.put(asset, response);
            console.log(`✅ Cached asset: ${asset}`);
          }
        } catch (err) {
          console.warn(`⚠️ Skipped caching ${asset}:`, err);
        }
      }
    })
  );
  self.skipWaiting();
});

// 2. Clear Old Caches on Activation
self.addEventListener('activate', (event) => {
  event.waitUntil(
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

// 3. Network First Strategy with Offline Fallback
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // Cache valid 200 OK responses dynamically as the user navigates
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(async () => {
        // Serve cached version or offline fallback page when offline
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) return cachedResponse;

        // Return offline fallback page for standard HTML page navigation
        if (event.request.headers.get('accept')?.includes('text/html')) {
          return caches.match('/LMS/offline/');
        }
      })
  );
});