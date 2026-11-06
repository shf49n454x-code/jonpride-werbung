#!/usr/bin/env python3
"""Übernimmt die fertige Markenseite (jonpride.de/werbung, dunkles System) 1:1 als
Startseite von werbung.jonpride.de. Geändert werden nur Adressen und Links.
Quelle: src/werbung.html (Stand aus jonpride.de main, 06.11.2026)."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://werbung.jonpride.de"
s = (ROOT / "src/werbung.html").read_text()

# --- JSON-LD ---------------------------------------------------------------
def ld_fix(m):
    d = json.loads(m.group(1))
    t = json.dumps(d, ensure_ascii=False)
    t = (t.replace("https://jonpride.de/werbung#service", SITE + "/#service")
          .replace("https://jonpride.de/werbung", SITE + "/")
          .replace("https://jonpride.de/assets/", SITE + "/assets/")
          .replace("https://jonpride.de/kontakt", SITE + "/#kontakt")
          .replace("https://jonpride.de/#website", SITE + "/#website")
          .replace("https://jonpride.de/#business", SITE + "/#business"))
    d = json.loads(t)
    if "@graph" in d:
        for n in d["@graph"]:
            if n.get("@type") == "WebSite":
                n.update({"url": SITE + "/"})
            if n.get("@id") == SITE + "/#business":
                n.update({"name": "Jon Pride – Werbung & Business", "url": SITE + "/", "image": SITE + "/assets/werbung/w04.jpg",
                          "description": "Firmen- und Werbefotografie, Business-Porträts und Content für Marken und Unternehmen in Hamburg und der Lüneburger Heide.",
                          "email": "me@jonpride.de", "sameAs": ["https://jonpride.de/"]})
    if d.get("@type") == "BreadcrumbList":
        d["itemListElement"] = [{"@type": "ListItem", "position": 1, "name": "Jon Pride Werbung", "item": SITE + "/"}]
    if d.get("@type") == "WebPage":
        pass
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

s = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', ld_fix, s, flags=re.S)

# --- Kopf ------------------------------------------------------------------
s = s.replace('content="https://jonpride.de/werbung"', f'content="{SITE}/"')
s = s.replace('href="https://jonpride.de/werbung"', f'href="{SITE}/"')
s = s.replace("https://jonpride.de/assets/og-image.jpg", f"{SITE}/assets/werbung/w04.jpg")


# --- Navigation und Fuß ------------------------------------------------------
s = s.replace('<a class="dim" href="/">Hochzeit &rarr;</a>', '<a class="dim" href="https://jonpride.de/">Hochzeit &rarr;</a>')
s = s.replace('<a class="dim" href="/news">News</a>', '<a class="dim" href="https://jonpride.de/news">News</a>')
s = s.replace('<a href="/impressum">Impressum</a> · <a href="/datenschutz">Datenschutz</a>', '<a href="https://jonpride.de/impressum">Impressum</a> · <a href="https://jonpride.de/datenschutz">Datenschutz</a>')

# --- Formular: landet im selben Posteingang wie jonpride.de -----------------
s = s.replace('action="/api/formular/anfrage"', 'action="https://jonpride.de/api/formular/anfrage"')

# --- Dateien: absolute Pfade -------------------------------------------------
s = re.sub(r'(["(\s])assets/', r'\1/assets/', s)


(ROOT / "public/index.html").write_text(s)
print("index.html übernommen,", len(s), "Zeichen")
