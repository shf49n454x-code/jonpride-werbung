/* werbung.jonpride.de – Einblenden, Filter, Lightbox, Formularschutz */
(function () {
  'use strict';

  // Einblenden beim Scrollen
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  // Filter auf der Startseite (ohne JS fuehren die Chips auf die Kategorieseiten)
  var chips = document.querySelectorAll('.arbeiten .chip[data-f]');
  var karten = document.querySelectorAll('.arbeiten .zelle');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function (ev) {
      ev.preventDefault();
      var f = chip.getAttribute('data-f');
      chips.forEach(function (c) { c.classList.toggle('an', c === chip); c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      karten.forEach(function (z) {
        var k = z.querySelector('.karte');
        var passt = f === 'alle' || (k.getAttribute('data-kat') || '').split(' ').indexOf(f) > -1;
        z.style.display = passt ? '' : 'none';
        if (passt) k.classList.add('in');
      });
    });
  });

  // Lightbox fuer Fotos und Videos
  var lb = document.getElementById('lb');
  if (lb) {
    var media = lb.querySelector('.lb-media');
    var titel = lb.querySelector('.lb-t');
    var zuletzt = null;
    var oeffnen = function (k) {
      media.innerHTML = '';
      var yt = k.getAttribute('data-yt');
      if (yt) {
        if (!/^[A-Za-z0-9_-]{6,20}$/.test(yt)) return;
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + yt + '?autoplay=1&rel=0';
        f.title = k.getAttribute('data-t') || 'Video';
        f.allow = 'autoplay; encrypted-media; fullscreen; picture-in-picture';
        f.allowFullscreen = true;
        media.appendChild(f);
      } else {
        var img = document.createElement('img');
        img.src = k.getAttribute('data-img');
        img.alt = k.getAttribute('data-alt') || '';
        media.appendChild(img);
      }
      titel.textContent = k.getAttribute('data-t') || '';
      zuletzt = k;
      lb.hidden = false;
      document.body.style.overflow = 'hidden';
      lb.querySelector('.lb-zu').focus();
    };
    var schliessen = function () {
      lb.hidden = true;
      media.innerHTML = '';
      document.body.style.overflow = '';
      if (zuletzt) zuletzt.focus();
    };
    document.querySelectorAll('button.karte[data-yt], button.karte[data-img]').forEach(function (k) {
      k.addEventListener('click', function () { oeffnen(k); });
    });
    lb.querySelector('.lb-zu').addEventListener('click', schliessen);
    lb.addEventListener('click', function (e) { if (e.target === lb) schliessen(); });
    document.addEventListener('keydown', function (e) { if (!lb.hidden && e.key === 'Escape') schliessen(); });
  }

  // Formularschutz: Zeit seit Seitenaufruf (der Server verwirft alles unter 3 s)
  var start = Date.now();
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.matches || !form.matches('form[action*="/api/formular/"]')) return;
    var d = form.querySelector('input[name="_dauer"]');
    if (!d) { d = document.createElement('input'); d.type = 'hidden'; d.name = '_dauer'; form.appendChild(d); }
    d.value = String(Date.now() - start);
  }, true);
})();
