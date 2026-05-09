/* Barbara Spica - main.js
   Comportamenti: nav mobile, scroll effect header, cookie banner, anno footer */
(function () {
  'use strict';

  // ----- Header scrolled state -----
  var header = document.querySelector('.site-header');
  if (header) {
    var setScrolled = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    setScrolled();
    window.addEventListener('scroll', setScrolled, { passive: true });
  }

  // ----- Mobile nav toggle -----
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    // Close on link click
    header.querySelectorAll('.main-nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ----- Year in footer -----
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // ----- Cookie banner (essenziale: solo informativa, niente cookie tecnici di terze parti caricati) -----
  var KEY = 'bspica_cookie_v1';
  var banner = document.getElementById('cookie-banner');
  if (banner && !localStorage.getItem(KEY)) {
    banner.classList.add('is-visible');
    banner.querySelectorAll('button[data-cookie]').forEach(function (b) {
      b.addEventListener('click', function () {
        try { localStorage.setItem(KEY, b.dataset.cookie); } catch (e) {}
        banner.classList.remove('is-visible');
      });
    });
  }

  // ----- Smooth focus on anchor for #content -----
  // (gestito da scroll-behavior smooth in CSS)

  // ----- Form: client-side validation feedback -----
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) { e.preventDefault(); return; } // honeypot
      // Add timestamp for anti-spam
      var ts = form.querySelector('input[name="ts"]');
      if (ts && !ts.value) ts.value = String(Math.floor(Date.now() / 1000));
    });
    // Set start ts on load
    var startTs = form.querySelector('input[name="start_ts"]');
    if (startTs) startTs.value = String(Math.floor(Date.now() / 1000));
  }

  // ----- Reveal on scroll (lightweight) -----
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-visible');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    document.querySelectorAll('[data-reveal]').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ----- YouTube facade (lazy, privacy-friendly) -----
  document.querySelectorAll('.video-facade').forEach(function (el) {
    var load = function () {
      var id = el.dataset.video;
      if (!id) return;
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = el.dataset.title || 'Video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      iframe.loading = 'lazy';
      el.replaceWith(iframe);
    };
    el.addEventListener('click', load);
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); load(); } });
  });

})();
