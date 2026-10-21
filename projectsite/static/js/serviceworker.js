const CACHE = 'hangarin-cache-v3';

const ASSETS = [
  '/static/css/bootstrap.min.css',
  '/static/css/ready.css',
  '/static/css/demo.css',
  '/static/js/core/jquery.3.2.1.min.js',
  '/static/js/plugin/jquery-ui-1.12.1.custom/jquery-ui.min.js',
  '/static/js/core/popper.min.js',
  '/static/js/core/bootstrap.min.js',
  '/static/js/plugin/chartist/chartist.min.js',
  '/static/js/plugin/chartist/plugin/chartist-plugin-tooltip.min.js',
  '/static/js/plugin/bootstrap-notify/bootstrap-notify.min.js',
  '/static/js/plugin/bootstrap-toggle/bootstrap-toggle.min.js',
  '/static/js/plugin/jquery-mapael/jquery.mapael.min.js',
  '/static/js/plugin/jquery-mapael/maps/world_countries.min.js',
  '/static/js/plugin/chart-circle/circles.min.js',
  '/static/js/plugin/jquery-scrollbar/jquery.scrollbar.min.js',
  '/static/js/ready.min.js',
  '/static/img/profile.jpg',
  '/static/img/icon-192.png',
];

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      // add one by one so a single missing file doesn't break the whole install
      return Promise.all(ASSETS.map(function (url) {
        return cache.add(url).catch(function () {});
      }));
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
                             .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  var url = new URL(req.url);
  if (url.origin !== location.origin) return;                 // leave Google Fonts etc. alone
  if (url.pathname.startsWith('/admin/') ||
      url.pathname.startsWith('/accounts/')) return;          // never cache login / admin pages

  // network first, remember the response, fall back to the saved copy when offline
  e.respondWith(
    fetch(req).then(function (res) {
      if (res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match('/');
      });
    })
  );
});