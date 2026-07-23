/* Landing page only — footer Supabase reads + sticky nav. */
(function () {
  'use strict';

  var nav = document.getElementById('nav');
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 12);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function loadSupabaseData() {
    try {
      if (!window.solstice || typeof window.solstice.sb !== 'function') return;
      var client = window.solstice.sb();
      client.from('landing_links').select('label,url').order('sort_order').then(function (res) {
        var data = res && res.data ? res.data : [];
        var host = document.getElementById('home-links');
        if (host) {
          host.innerHTML = data.map(function (l) {
            return '<a href="' + l.url + '" target="_blank" rel="noopener">' + l.label + '</a>';
          }).join('');
        }
      });
      client.from('logs').select('created_at').order('created_at', { ascending: false }).limit(1).then(function (res) {
        var logs = res && res.data ? res.data : [];
        if (logs[0]) {
          var min = Math.floor((Date.now() - new Date(logs[0].created_at).getTime()) / 60000);
          var el = document.getElementById('stat-latency');
          if (el) el.textContent = min < 1 ? '<1m' : (min < 60 ? min + 'm' : Math.floor(min / 60) + 'h');
        }
      });
    } catch (_) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadSupabaseData);
  } else {
    loadSupabaseData();
  }
})();
