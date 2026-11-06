# CLAUDE.md – werbung.jonpride.de

Werbe- und Business-Portfolio von Jon Pride (Jan Stolz). Statisches HTML auf Cloudflare Pages
(Projekt `jonpride-werbung`, Ausgabeordner `public/`, kein Build-Befehl bei Cloudflare).
Hochzeiten, Impressum, Datenschutz und das Anfrageformular (`/api/formular/anfrage`) liegen auf jonpride.de.

## Ablauf (Pflicht)

Branch → PR → Prüfung → Klartext-Zusammenfassung aus dem echten Diff → Jon sagt „go“ → **Jon merged**.
Die KI merged nie selbst. Jede Branch hat eine Vorschau unter `<branch>.jonpride-werbung.pages.dev`.

## Bauen und prüfen

```bash
python3 tools/site.py                    # Seiten, Bilder, Sitemap, llms.txt → public/
python3 -m http.server 8765 -d public    # lokal ansehen
```

`public/` wird erzeugt und mit eingecheckt. HTML in `public/` nie von Hand ändern.
Nach jeder Änderung bei 375 px und 1440 px ansehen: kein horizontales Scrollen, keine Konsolenfehler,
Lightbox und Formular durchklicken.

## Wo was liegt

| Was | Datei |
|---|---|
| Projekte, Kategorien, FAQ, Kunden, Zahlen, Bild-Alt-Texte | `content/arbeiten.json` |
| Ratgeber-Artikel | `content/ratgeber.json` |
| Generator (Seiten, Bilder, Sitemap, llms.txt, JSON-LD) | `tools/site.py` |
| Stil / Skript | `public/assets/site.css`, `public/assets/site.js` (Fingerabdruck `?v=` automatisch) |
| CI-Tokens und Schriften | `public/assets/ci.css`, `public/assets/fonts/` |
| Bild-Originale | `src/img/*.jpg` (aktiv), `src/archiv/` (ungenutzt) |
| Bestätigte Projektfakten | `docs/projekte.md` |

## Regeln

- **Nur bestätigte Fakten.** Projekttexte entstehen ausschließlich aus `docs/projekte.md`. Keine erfundenen
  Kunden, Zahlen, Zitate oder Rollen. Was fehlt, wird erfragt, nicht geraten.
- **Bilder immer performant.** Original nach `src/img/`, `tools/site.py` erzeugt 640/1000/1600 als WebP und
  JPG ohne Metadaten, mit `srcset`, `width`/`height` und Lazy Loading. Ziel: unter ~200 KB bei 1000 px.
  Videos als kurze stumme MP4-Loops unter 2 MB mit Posterbild, selbst gehostet.
- **Gleichmäßiges Raster:** alle Karten 3:2, drei Spalten, gleiche Höhen (Jon: unterschiedliche Höhen wirken
  unharmonisch). Hochformate mit Ausschnitt oben (`object-position`). Nach jeder Bildänderung bei 375 px nachsehen.
- **Kein langer Onepager:** Startseite zeigt nur eine Auswahl (sechs Arbeiten) und die Bereiche; alles Weitere
  auf Unterseiten, Anfrage auf `/kontakt/`. Jeder Klick auf eine Unterseite ist gut für die Statistik.
- **Überschriften:** Anton in Versalien, Zeilenabstand mindestens 1.04, sonst stoßen Ä/Ö/Ü an die Zeile darüber.
- **Design:** dunkel, Orange `#F4571B` als einziger Akzent, schräge Ecken aus der CI. Animationen dezent
  (Einblenden beim Scrollen, Überschrift Wort für Wort, View Transitions), `prefers-reduced-motion` respektieren.
- **Selbst hosten vor anbinden.** Keine CDNs, keine fremden Einbettungen außer YouTube-nocookie im Klick.
- **Neue Seite:** Eintrag in `content/*.json`, Sitemap und llms.txt entstehen automatisch. Jede Inhaltsseite
  mit Kurztext oben, FAQ und mindestens drei internen Links; Ratgeber zusätzlich mit Stand-Datum und Quellen.
- Nie Kleinunternehmer/§ 19 erwähnen. Private Adresse nur in Impressum/Datenschutz und im LocalBusiness-JSON-LD.
