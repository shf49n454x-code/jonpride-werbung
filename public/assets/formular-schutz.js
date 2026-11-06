/* Spamschutz fuer die eigenen Formulare (functions/api/formular).
   Schreibt beim Absenden die Zeit seit Seitenaufruf in _dauer. Menschen
   brauchen fuer ein Formular Sekunden bis Minuten, Bots Millisekunden —
   der Server verwirft alles unter 3 Sekunden still.
   Zusaetzlich: Hochzeitsdatum nicht in der Vergangenheit waehlbar. */
(function () {
  var start = Date.now();
  var FORMULARE = 'form[action^="/api/formular/"]';

  function feld(form) {
    var d = form.querySelector('input[name="_dauer"]');
    if (!d) {
      d = document.createElement('input');
      d.type = 'hidden';
      d.name = '_dauer';
      form.appendChild(d);
    }
    return d;
  }

  function zwei(n) { return (n < 10 ? '0' : '') + n; }
  var heute = new Date();
  var min = heute.getFullYear() + '-' + zwei(heute.getMonth() + 1) + '-' + zwei(heute.getDate());

  var liste = document.querySelectorAll(FORMULARE);
  for (var i = 0; i < liste.length; i++) {
    var form = liste[i];
    feld(form);
    var datum = form.querySelector('input[type="date"][name="hochzeitsdatum"]');
    if (datum && !datum.min) datum.min = min;
  }

  // Capture auf document: laeuft vor jedem Submit-Handler am Formular selbst
  // (ablauf.html liest die Felder per FormData in seinem eigenen Handler).
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form && form.matches && form.matches(FORMULARE)) feld(form).value = String(Date.now() - start);
  }, true);
})();
