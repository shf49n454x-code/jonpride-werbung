#!/usr/bin/env python3
"""Übernimmt die fertige Markenseite (jonpride.de/werbung, dunkles System) 1:1 als
Startseite von jonandjoystudios.com. Geändert werden nur Marke, Adressen und Links.
Quelle: src/werbung.html (Stand aus jonpride.de main, 06.11.2026)."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://jonandjoystudios.com"
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
                n.update({"name": "Jon & Joy Studios", "url": SITE + "/"})
            if n.get("@id") == SITE + "/#business":
                n.update({"name": "Jon & Joy Studios", "url": SITE + "/", "image": SITE + "/assets/werbung/w04.jpg",
                          "description": "Firmen- und Werbefotografie, Business-Porträts und Content für Marken und Unternehmen in Hamburg und der Lüneburger Heide.",
                          "email": "me@jonpride.de", "sameAs": ["https://jonpride.de/"]})
    if d.get("@type") == "BreadcrumbList":
        d["itemListElement"] = [{"@type": "ListItem", "position": 1, "name": "Jon & Joy Studios", "item": SITE + "/"}]
    if d.get("@type") == "WebPage":
        d["name"] = d["name"].replace("Jon Pride", "Jon & Joy Studios")
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"

s = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', ld_fix, s, flags=re.S)

# --- Kopf ------------------------------------------------------------------
s = s.replace("<title>Firmen- &amp; Werbefotograf Hamburg, Content Creator – Jon Pride</title>",
              "<title>Jon &amp; Joy Studios – Firmen- &amp; Werbefotograf Hamburg, Content Creator</title>")
s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")Jon Pride — ', r'\1Jon & Joy Studios — ', s)
s = s.replace('content="Jon Pride – Firmen-', 'content="Jon &amp; Joy Studios – Firmen-')
s = s.replace('content="https://jonpride.de/werbung"', f'content="{SITE}/"')
s = s.replace('href="https://jonpride.de/werbung"', f'href="{SITE}/"')
s = s.replace("https://jonpride.de/assets/og-image.jpg", f"{SITE}/assets/werbung/w04.jpg")
s = s.replace('href="assets/logo.svg?v=2"', 'href="/favicon.svg"')

# --- Logo: Wortmarke statt JON-PRIDE-Logo -----------------------------------
s = re.sub(r'<a href="#work" class="marklogo" aria-label="Jon Pride">.*?</a>',
           '<a href="#work" class="marklogo wordmark" aria-label="Jon &amp; Joy Studios">Jon <span style="color:#F4571B">&amp;</span> Joy<small>Studios</small></a>', s, flags=re.S)
s = s.replace(".marklogo img{width:100%;height:auto}",
              ".marklogo img{width:100%;height:auto}\n.wordmark{width:auto;text-decoration:none;color:#fff;font-family:'Anton',sans-serif;font-size:44px;line-height:.95;text-transform:uppercase;letter-spacing:.01em}\n.wordmark small{display:block;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.32em;margin-top:8px;color:#9a9a9a}")
s = s.replace("  .marklogo{width:100px}", "  .marklogo{width:100px}\n  .wordmark{width:auto;font-size:32px}")

# --- Navigation und Fuß ------------------------------------------------------
s = s.replace('<a class="dim" href="/">Hochzeit &rarr;</a>', '<a class="dim" href="https://jonpride.de/">Hochzeit &rarr;</a>')
s = s.replace('<a class="dim" href="/news">News</a>', '<a class="dim" href="https://jonpride.de/news">News</a>')
s = s.replace("<span>© <span id=\"year\"></span> Jon Pride</span>", "<span>© <span id=\"year\"></span> Jon &amp; Joy Studios</span>")
s = s.replace('<a href="/impressum">Impressum</a> · <a href="/datenschutz">Datenschutz</a>', '<a href="/impressum/">Impressum</a> · <a href="/datenschutz/">Datenschutz</a>')

# --- Formular: landet im selben Posteingang wie jonpride.de -----------------
s = s.replace('action="/api/formular/anfrage"', 'action="https://jonpride.de/api/formular/anfrage"')

# --- Dateien: absolute Pfade -------------------------------------------------
s = re.sub(r'(["(\s])assets/', r'\1/assets/', s)

assert "jonpride-logo" not in s
(ROOT / "public/index.html").write_text(s)
print("index.html übernommen,", len(s), "Zeichen")
