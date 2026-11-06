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

  // Preise: Reiter mit Wechsel-Effekt
  var tabs = document.querySelectorAll('.tabs .tab');
  var strich = document.querySelector('.tab-strich');
  function strichSetzen(t) {
    if (!strich || !t) return;
    strich.style.setProperty('--x', t.offsetLeft + 'px');
    strich.style.setProperty('--w', t.offsetWidth + 'px');
  }
  function zeigen(id, merken) {
    var t = document.querySelector('.tab[data-tab="' + id + '"]');
    if (!t) return;
    tabs.forEach(function (x) { var an = x === t; x.classList.toggle('an', an); x.setAttribute('aria-selected', an ? 'true' : 'false'); x.tabIndex = an ? 0 : -1; });
    document.querySelectorAll('.panel').forEach(function (p) { p.classList.toggle('an', p.id === 'p-' + id); });
    strichSetzen(t);
    if (merken && history.replaceState) history.replaceState(null, '', '#' + id);
  }
  if (tabs.length) {
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { zeigen(t.getAttribute('data-tab'), true); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!n) return;
        var z = tabs[(i + n + tabs.length) % tabs.length]; z.focus(); zeigen(z.getAttribute('data-tab'), true);
      });
    });
    var start = (location.hash || '').slice(1);
    zeigen(document.querySelector('.tab[data-tab="' + start + '"]') ? start : tabs[0].getAttribute('data-tab'), false);
    window.addEventListener('hashchange', function () { zeigen(location.hash.slice(1), false); });
    window.addEventListener('resize', function () { strichSetzen(document.querySelector('.tab.an')); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { strichSetzen(document.querySelector('.tab.an')); });
  }

  // Auswahl: Pakete sammeln und zusammen anfragen (nur fuer diesen Besuch gemerkt)
  var SPEICHER = 'jp-auswahl';
  function lesen() { try { return JSON.parse(sessionStorage.getItem(SPEICHER) || '[]'); } catch (e) { return []; } }
  function schreiben(l) { try { sessionStorage.setItem(SPEICHER, JSON.stringify(l)); } catch (e) {} }
  var auswahl = lesen();
  var korb = document.getElementById('korb');
  function euro(n) { return n.toLocaleString('de-DE') + ' €'; }
  function korbZeigen() {
    document.querySelectorAll('.pk').forEach(function (k) {
      var drin = auswahl.some(function (a) { return a.id === k.getAttribute('data-id'); });
      k.classList.toggle('gew', drin);
      var b = k.querySelector('.wahl'); if (b) b.setAttribute('aria-pressed', drin ? 'true' : 'false');
    });
    if (!korb) return;
    korb.hidden = false;
    if (!auswahl.length) { korb.classList.remove('offen'); document.body.classList.remove('mit-korb'); return; }
    var summe = auswahl.reduce(function (s, a) { return s + (a.ab || 0); }, 0);
    var offen = auswahl.some(function (a) { return !a.ab; });
    korb.querySelector('.korb-t').textContent = auswahl.map(function (a) { return a.name; }).join(' + ') +
      (summe ? ' · ab ' + euro(summe) + (offen ? ' plus Anfrage' : '') : '');
    document.getElementById('korb-los').href = '/kontakt/?pakete=' + encodeURIComponent(auswahl.map(function (a) { return a.id; }).join(','));
    korb.classList.add('offen'); document.body.classList.add('mit-korb');
  }
  document.querySelectorAll('.pk .wahl').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.closest('.pk'), id = k.getAttribute('data-id');
      var i = auswahl.findIndex(function (a) { return a.id === id; });
      if (i > -1) auswahl.splice(i, 1);
      else auswahl.push({ id: id, name: k.getAttribute('data-name'), ab: Number(k.getAttribute('data-ab')) || 0 });
      schreiben(auswahl); korbZeigen();
    });
  });
  korbZeigen();

  // Kontakt: gewaehlte Pakete ins Formular uebernehmen
  var feld = document.getElementById('f-pakete');
  if (feld) {
    var ids = (new URLSearchParams(location.search).get('pakete') || '').split(',').filter(Boolean);
    var namen = ids.map(function (id) { var a = auswahl.find(function (x) { return x.id === id; }); return a ? a.name : null; }).filter(Boolean);
    if (!namen.length) namen = auswahl.map(function (a) { return a.name; });
    if (namen.length) {
      feld.value = namen.join('; ');
      var box = document.getElementById('auswahl');
      namen.forEach(function (n) { var li = document.createElement('li'); li.textContent = n; box.querySelector('ul').appendChild(li); });
      box.hidden = false;
    }
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
