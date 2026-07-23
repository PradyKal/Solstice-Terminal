/* ============================================================
   SOLSTICE TERMINAL — Landing page (public) animations + data.
   Loaded ONLY by index.html. Uses window.solstice from config.js
   (shared, unchanged) purely to READ landing_links + last log time.
   No auth, routing, or write logic here.
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Nav shadow on scroll ---------- */
  var nav = document.getElementById('nav');
  function onScroll() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 12); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Helpers ---------- */
  function dpi(canvas) {
    var r = window.devicePixelRatio || 1;
    var w = canvas.width, h = canvas.height;
    canvas.width = w * r; canvas.height = h * r;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    var ctx = canvas.getContext('2d'); ctx.scale(r, r);
    return { ctx: ctx, w: w, h: h };
  }
  function bell(x, mu, sig) {
    return Math.exp(-0.5 * Math.pow((x - mu) / sig, 2)) / (sig * Math.sqrt(2 * Math.PI));
  }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  /* ---------- Hero Monte Carlo distribution (looping) ---------- */
  function heroDist() {
    var c = document.getElementById('mcDist'); if (!c) return;
    var d = dpi(c), ctx = d.ctx, W = d.w, H = d.h;
    var t0 = performance.now();
    function frame(now) {
      var phase = ((now - t0) / 5200) % 1;
      var shift = Math.sin((now - t0) / 2600) * 0.6;
      ctx.clearRect(0, 0, W, H);
      var mu = W * 0.5 + shift * 22, sig = W * 0.13;
      var peak = bell(mu, mu, sig);
      var pts = [];
      for (var x = 0; x <= W; x += 4) {
        var y = H - (bell(x, mu, sig) / peak) * (H * 0.82) - 8;
        pts.push([x, y]);
      }
      // area fill
      var g = ctx.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, 'rgba(56,230,255,0.34)');
      g.addColorStop(1, 'rgba(56,230,255,0.02)');
      ctx.beginPath(); ctx.moveTo(0, H);
      pts.forEach(function (p) { ctx.lineTo(p[0], p[1]); });
      ctx.lineTo(W, H); ctx.closePath(); ctx.fillStyle = g; ctx.fill();
      // line
      ctx.beginPath();
      pts.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.strokeStyle = 'rgba(120,240,255,0.95)'; ctx.lineWidth = 2; ctx.stroke();
      // sweeping confidence marker
      var mx = phase * W;
      ctx.strokeStyle = 'rgba(59,130,246,0.6)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(mx, 6); ctx.lineTo(mx, H); ctx.stroke();
      if (!reduce) requestAnimationFrame(frame); 
    }
    if (reduce) { frame(performance.now()); } else { requestAnimationFrame(frame); }
  }

  /* ---------- Hero portfolio growth paths ---------- */
  function heroPaths() {
    var c = document.getElementById('mcPaths'); if (!c) return;
    var d = dpi(c), ctx = d.ctx, W = d.w, H = d.h;
    var N = 22, steps = 60, seeds = [];
    for (var i = 0; i < N; i++) seeds.push(Math.random() * 1000);
    var t0 = performance.now();
    function frame(now) {
      ctx.clearRect(0, 0, W, H);
      var prog = Math.min(1, (now - t0) / 2400);
      var shown = Math.floor(easeOut(prog) * steps);
      for (var k = 0; k < N; k++) {
        var s = seeds[k], val = H * 0.72, drift = 0.15 + (k % 5) * 0.03;
        ctx.beginPath();
        for (var j = 0; j <= shown; j++) {
          var noise = Math.sin(s + j * 0.55) * 3.2 + (Math.sin(s * 2 + j) * 1.8);
          val -= drift + noise * 0.16;
          var x = (j / steps) * W, y = Math.max(6, Math.min(H - 4, val));
          j ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
        }
        var hi = k < 3;
        ctx.strokeStyle = hi ? 'rgba(56,230,255,0.9)' : 'rgba(120,150,190,0.22)';
        ctx.lineWidth = hi ? 1.8 : 1; ctx.stroke();
      }
      if (prog < 1 && !reduce) requestAnimationFrame(frame);
    }
    if (reduce) { frame(t0 + 3000); } else { requestAnimationFrame(frame); }
  }

  /* ---------- Hero sparklines ---------- */
  function spark(id, color, up) {
    var c = document.getElementById(id); if (!c) return;
    var d = dpi(c), ctx = d.ctx, W = d.w, H = d.h, pts = 26;
    ctx.clearRect(0, 0, W, H);
    ctx.beginPath();
    for (var i = 0; i < pts; i++) {
      var x = (i / (pts - 1)) * W;
      var base = up ? (H - 6 - (i / pts) * (H - 12)) : (6 + (i / pts) * (H - 12));
      var y = base + Math.sin(i * 0.9) * 4;
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.strokeStyle = color; ctx.lineWidth = 1.6; ctx.stroke();
  }

  /* ---------- Risk heatmap ---------- */
  function heatmap() {
    var el = document.getElementById('heat'); if (!el) return;
    for (var i = 0; i < 48; i++) {
      var s = document.createElement('span');
      var v = Math.random();
      var col = v > 0.72 ? '248,113,113' : (v > 0.45 ? '56,230,255' : '59,130,246');
      s.style.background = 'rgba(' + col + ',' + (0.12 + v * 0.55).toFixed(2) + ')';
      el.appendChild(s);
    }
  }

  /* ---------- Big self-drawing distribution (interactive section) ---------- */
  function bigDist(trigger) {
    var c = document.getElementById('bigDist'); if (!c) return;
    var d = dpi(c), ctx = d.ctx, W = d.w, H = d.h;
    var mu = W * 0.5, sig = W * 0.14, peak = bell(mu, mu, sig);
    function yOf(x) { return H - (bell(x, mu, sig) / peak) * (H * 0.8) - 20; }
    var t0 = null;
    function frame(now) {
      if (t0 === null) t0 = now;
      var prog = Math.min(1, (now - t0) / 1600), e = easeOut(prog), drawn = e * W;
      ctx.clearRect(0, 0, W, H);
      // 90% band
      shade(mu - 1.65 * sig, mu + 1.65 * sig, 'rgba(59,130,246,0.18)', drawn);
      // 50% band
      shade(mu - 0.67 * sig, mu + 0.67 * sig, 'rgba(56,230,255,0.22)', drawn);
      // curve
      ctx.beginPath();
      for (var x = 0; x <= drawn; x += 3) { var y = yOf(x); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.strokeStyle = 'rgba(140,245,255,0.98)'; ctx.lineWidth = 2.4; ctx.stroke();
      // mean line
      if (drawn >= mu) {
        ctx.strokeStyle = 'rgba(56,230,255,0.9)'; ctx.lineWidth = 1.4;
        ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(mu, yOf(mu)); ctx.lineTo(mu, H); ctx.stroke();
        ctx.setLineDash([]);
      }
      // baseline
      ctx.strokeStyle = 'rgba(255,255,255,0.12)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(0, H - 1); ctx.lineTo(W, H - 1); ctx.stroke();
      if (prog < 1 && !reduce) requestAnimationFrame(frame);
    }
    function shade(a, b, fill, drawn) {
      ctx.beginPath(); ctx.moveTo(a, H);
      for (var x = a; x <= Math.min(b, drawn); x += 3) ctx.lineTo(x, yOf(x));
      ctx.lineTo(Math.min(b, drawn), H); ctx.closePath(); ctx.fillStyle = fill; ctx.fill();
    }
    if (reduce) { frame(0); frame(3000); } else { requestAnimationFrame(frame); }
  }

  /* ---------- Number counters ---------- */
  function runCounter(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var decimals = (String(target).split('.')[1] || '').length;
    var big = Math.abs(target) >= 1000;
    var t0 = null, dur = 1400;
    function step(now) {
      if (t0 === null) t0 = now;
      var p = Math.min(1, (now - t0) / dur), v = target * easeOut(p);
      var txt = big ? Math.round(v).toLocaleString() : v.toFixed(decimals);
      el.textContent = txt + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    if (reduce) { el.textContent = (big ? Math.round(target).toLocaleString() : target.toFixed(decimals)) + suffix; }
    else requestAnimationFrame(step);
  }

  /* ---------- Reveal + trigger observers ---------- */
  function initObservers() {
    var revEls = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
      revEls.forEach(function (el) { el.classList.add('in'); });
      document.querySelectorAll('[data-count]').forEach(runCounter);
      bigDist(); return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, delay = parseInt(el.getAttribute('data-delay') || '0', 10);
        setTimeout(function () { el.classList.add('in'); }, delay);
        el.querySelectorAll && el.querySelectorAll('[data-count]').forEach(runCounter);
        if (el.hasAttribute && el.hasAttribute('data-count')) runCounter(el);
        io.unobserve(el);
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });
    revEls.forEach(function (el) { io.observe(el); });

    document.querySelectorAll('[data-count]').forEach(function (el) { io.observe(el); });

    var viz = document.getElementById('bigDist');
    if (viz) {
      var io2 = new IntersectionObserver(function (e) {
        if (e[0].isIntersecting) { bigDist(true); io2.disconnect(); }
      }, { threshold: 0.3 });
      io2.observe(viz);
    }
  }

  /* ---------- Supabase footer data (preserves original integration) ---------- */
  function loadSupabaseData() {
    try {
      if (!window.solstice || typeof window.solstice.sb !== 'function') return;
      var client = window.solstice.sb();
      client.from('landing_links').select('label,url').order('sort_order').then(function (res) {
        var data = res && res.data ? res.data : [];
        var host = document.getElementById('home-links');
        if (host) host.innerHTML = data.map(function (l) {
          return '<a href="' + l.url + '" target="_blank" rel="noopener">' + l.label + '</a>';
        }).join('');
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

  /* ---------- Init ---------- */
  function init() {
    heroDist(); heroPaths(); heatmap();
    spark('sparkA', 'rgba(56,230,255,0.9)', true);
    spark('sparkB', 'rgba(248,113,113,0.9)', false);
    initObservers();
    loadSupabaseData();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
