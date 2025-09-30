const CACHE_NAME = 'us-trip-2025-v1.7';
const VERSION = '1.7';
const urlsToCache = [
  '.',
  './index.html',
  `./manifest.json?v=${VERSION}`,
  `./icon-192.png?v=${VERSION}`,
  `./icon-512.png?v=${VERSION}`,
  // Travel documents
  './our_nyc_family_itinerary.md',
  './our_nyc_must_do_list.md',
  './orlando_itinerary.md',
  './boston_itinerary.md',
  './MIT tour.md',
  './boston_to_nyc_roadtrip.md',
  './newhaven_to_logan_roadtrip.md'
];

// Install event - cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache.map(url => new Request(url, {credentials: 'same-origin'})));
      })
      .catch(error => {
        console.log('Cache install error:', error);
        // Don't fail if some files don't exist
        return Promise.resolve();
      })
  );
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // For critical PWA files, always check network first to ensure updates
  const criticalFiles = ['manifest.json', 'index.html'];
  const isCriticalFile = criticalFiles.some(file => url.pathname.includes(file));
  
  if (isCriticalFile) {
    // Network first strategy for critical files
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => cache.put(event.request, responseToCache));
            return response;
          }
          return caches.match(event.request);
        })
        .catch(() => caches.match(event.request))
    );
  } else {
    // Cache first strategy for other resources
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          // Return cached version or fetch from network
          if (response) {
            return response;
          }

          return fetch(event.request).then(response => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          }).catch(() => {
            // If both cache and network fail, show offline page for navigation requests
            if (event.request.destination === 'document') {
            return new Response(`
              <!DOCTYPE html>
              <html>
              <head>
                <title>Offline - US Trip 2025</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                  body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                    color: white;
                  }
                  .container {
                    background: rgba(255,255,255,0.95);
                    color: #333;
                    padding: 40px;
                    border-radius: 12px;
                    max-width: 500px;
                    margin: 0 auto;
                  }
                </style>
              </head>
              <body>
                <div class="container">
                  <h1>🗽 US Trip 2025</h1>
                  <h2>You're Offline</h2>
                  <p>Don't worry! Your travel documents are saved and available offline.</p>
                  <p>Click the back button to return to your cached content.</p>
                  <button onclick="window.location.reload()" style="padding: 10px 20px; border: none; background: #e74c3c; color: white; border-radius: 5px; cursor: pointer;">Try Again</button>
                </div>
              </body>
              </html>
            `, {
              headers: { 'Content-Type': 'text/html' }
            });
            }
          });
        })
    );
  }
});

// Handle background sync for offline actions
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    console.log('Background sync triggered');
  }
});

// Handle push notifications (future feature)
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body,
      icon: 'icon-192.png',
      badge: 'icon-72.png',
      vibrate: [200, 100, 200],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: 1
      },
      actions: [
        {
          action: 'explore',
          title: 'View Details',
          icon: 'icon-192.png'
        },
        {
          action: 'close',
          title: 'Close',
          icon: 'icon-192.png'
        }
      ]
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title, options)
    );
  }
});

console.log('Service Worker loaded for US Trip 2025');
