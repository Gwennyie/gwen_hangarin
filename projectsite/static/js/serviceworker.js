self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('hangarin-cache-v1').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/css/bootstrap.min.css',
        '/static/css/ready.css',
        '/static/css/demo.css',
        '/static/js/ready.min.js',
      ]);
    })
  );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});