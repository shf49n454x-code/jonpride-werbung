#!/usr/bin/env python3
"""Baut werbung.jonpride.de nach public/.

    python3 tools/site.py

Inhalte: content/arbeiten.json (Projekte, Kategorien, FAQ, Kunden),
content/ratgeber.json. Bilder: src/img/*.jpg -> public/img/<name>-<breite>.{webp,jpg}
in 640/1000/1600 (kleiner, wenn das Original kleiner ist), ohne Metadaten.
CSS und JS bekommen einen Inhalts-Fingerabdruck (?v=...), damit niemand alte
Dateien aus dem Cache behaelt.
"""
import hashlib, html, json, pathlib, re, shutil
from datetime import date
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SRC_IMG = ROOT / "src/img"
SITE = "https://werbung.jonpride.de"
HEUTE = date.today().isoformat()
STUFEN = (640, 1000, 1600)

D = json.loads((ROOT / "content/arbeiten.json").read_text())
RATGEBER = json.loads((ROOT / "content/ratgeber.json").read_text())
KAT = {k["slug"]: k for k in D["kategorien"]}
ARBEITEN = D["arbeiten"]
BY_SLUG = {a["slug"]: a for a in ARBEITEN}
PROJEKTE = [a for a in ARBEITEN if a.get("seite")]

esc = lambda s: html.escape(str(s), quote=True)


# ---------------------------------------------------------------- Bilder
BILD = {}  # name -> (breiten, w, h)

def bilder_bauen():
    out = PUB / "img"
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted(SRC_IMG.glob("*.jpg")):
        name = f.stem
        im = Image.open(f).convert("RGB")
        w0, h0 = im.size
        breiten = [s for s in STUFEN if s < w0] + [min(w0, STUFEN[-1])]
        breiten = sorted(set(breiten))
        for b in breiten:
            h = round(h0 * b / w0)
            klein = im.resize((b, h), Image.LANCZOS) if b != w0 else im
            for ext, kw in (("jpg", dict(quality=80, optimize=True, progressive=True)),
                            ("webp", dict(quality=78, method=6))):
                ziel = out / f"{name}-{b}.{ext}"
                if not ziel.exists() or ziel.stat().st_mtime < f.stat().st_mtime:
                    klein.save(ziel, **kw)  # PIL schreibt ohne EXIF/XMP
        BILD[name] = (breiten, w0, h0)


def bild(name, alt, sizes, eager=False, cls=""):
    breiten, w0, h0 = BILD[name]
    gross = breiten[-1]
    h = round(h0 * gross / w0)
    webp = ", ".join(f"/img/{name}-{b}.webp {b}w" for b in breiten)
    jpg = ", ".join(f"/img/{name}-{b}.jpg {b}w" for b in breiten)
    laden = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img{c} src="/img/{name}-{breiten[min(1, len(breiten) - 1)]}.jpg" srcset="{jpg}" sizes="{sizes}" '
            f'width="{gross}" height="{h}" alt="{esc(alt)}" {laden}></picture>')


def bild_name(a):
    if a.get("bild"):
        return a["bild"]
    if a.get("yt"):
        return "yt-" + a["yt"]
    if a.get("bilder"):
        return a["bilder"][0]
    return None


# ---------------------------------------------------------------- Rahmen
def fingerabdruck(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:8]


def worte(text):
    """Ueberschrift Wort fuer Wort einblenden: jedes Wort ein eigenes span."""
    teile = text.split(" ")
    return " ".join(f'<span class="w" style="--i:{i}">{t}</span>' for i, t in enumerate(teile))


NAV = [("/#arbeiten", "Arbeiten"), ("/#leistungen", "Leistungen"), ("/ratgeber/", "Ratgeber")]


def kopf(title, desc, pfad, ld, og_bild="w10", extra=""):
    css_v = fingerabdruck(PUB / "assets/site.css")
    ci_v = fingerabdruck(PUB / "assets/ci.css")
    breiten = BILD[og_bild][0] if og_bild in BILD else [1000]
    og = f"{SITE}/img/{og_bild}-{breiten[-1]}.jpg"
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{pfad}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{pfad}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/logo.svg?v=2">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
<link rel="preload" href="/assets/fonts/anton-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/ci.css?v={ci_v}">
<link rel="stylesheet" href="/assets/site.css?v={css_v}">
<script>document.documentElement.classList.add('js')</script>
{lds}{extra}
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt</a>
<header class="top">
  <div class="wrap">
    <a href="/" class="marke" aria-label="Jon Pride, zur Startseite"><img src="/assets/logo/jonpride-logo.svg" alt="Jon Pride" width="962" height="592"></a>
    <nav class="haupt" aria-label="Hauptnavigation">{nav}<a class="hz" href="https://jonpride.de/">Hochzeit&nbsp;→</a><a class="cta" href="/kontakt/">Projekt anfragen</a></nav>
    <details class="menu"><summary aria-label="Menü öffnen">Menü</summary><nav aria-label="Menü">{nav}<a href="/kontakt/">Projekt anfragen</a><a href="https://jonpride.de/">Hochzeit&nbsp;→</a></nav></details>
  </div>
</header>
<main id="inhalt">
"""


def fuss():
    js_v = fingerabdruck(PUB / "assets/site.js")
    kats = "".join(f'<a href="/{k["slug"]}/">{esc(k["name"])}</a>' for k in D["kategorien"] if kat_arbeiten(k["slug"]))
    rg = "".join(f'<a href="/ratgeber/{r["slug"]}/">{esc(r["titel"])}</a>' for r in RATGEBER)
    return f"""</main>
<footer class="fuss">
  <div class="wrap">
    <div class="fs">
      <div><p class="mono">Arbeiten</p>{kats}</div>
      <div><p class="mono">Ratgeber</p>{rg}<a href="/ratgeber/">Alle Ratgeber</a></div>
      <div><p class="mono">Kontakt</p><a href="mailto:me@jonpride.de">me@jonpride.de</a><a href="tel:+491623361352">0162 3361352</a><a href="https://www.instagram.com/jonpride" rel="noopener">Instagram @jonpride</a></div>
      <div><p class="mono">Jon Pride</p><a href="https://jonpride.de/">Hochzeitsfotografie</a><a href="https://jonpride.de/impressum">Impressum</a><a href="https://jonpride.de/datenschutz">Datenschutz</a></div>
    </div>
    <p class="copy mono">© {date.today().year} Jon Pride · Tostedt, Hamburg &amp; Lüneburger Heide</p>
  </div>
</footer>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Arbeit im Detail">
  <div class="lb-in"><button class="lb-zu" type="button" aria-label="Schließen">×</button><div class="lb-media"></div><p class="lb-t"></p></div>
</div>
<script defer src="/assets/site.js?v={js_v}"></script>
</body>
</html>
"""


def krumen(items):
    """items: [(name, pfad)] ab der Startseite."""
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}
    teile = [f'<a href="{p}">{esc(n)}</a>' for n, p in items[:-1]] + [f'<span aria-current="page">{esc(items[-1][0])}</span>']
    return ld, f'<nav class="krumen mono" aria-label="Brotkrumen">{" / ".join(teile)}</nav>'


def faq_block(paare, titel="Häufige Fragen", h="h2"):
    ds = "".join(
        f'<details id="frage-{re.sub(r"[^a-z0-9]+", "-", q.lower().replace("ü","ue").replace("ä","ae").replace("ö","oe").replace("ß","ss")).strip("-")}">'
        f'<summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in paare)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in paare]}
    return ld, f'<div class="faq"><{h} class="rv">{titel}</{h}><div class="faq-l">{ds}</div></div>'


def kat_arbeiten(slug):
    return [a for a in ARBEITEN if slug in a["kat"]]


# ---------------------------------------------------------------- Karten
def karte(a, i, sizes):
    name = bild_name(a)
    alt = D["bilder"].get(name, a["titel"]) if name else ""
    if a.get("logo") == "mcdonalds":
        media = '<div class="media logo-rot"><img src="/assets/mcdonalds.svg" alt="McDonald\'s Logo" width="273" height="239" loading="lazy"></div>'
    elif name:
        play = '<span class="play" aria-hidden="true"></span>' if a.get("yt") else ""
        hoch = " hoch" if BILD[name][2] > BILD[name][1] else ""  # Hochformat: Ausschnitt oben
        media = f'<div class="media{hoch}">{bild(name, alt, sizes)}{play}</div>'
    else:
        media = f'<div class="media leer" style="view-transition-name:p-{a["slug"]}"><span>{esc(a.get("kunde") or a["titel"])}</span></div>'
    kopfzeile = f'<span class="kt">{esc(a["titel"])}</span><span class="km mono">{esc(a["meta"])}</span>'
    inhalt = f'{media}<span class="kz">{kopfzeile}</span><span class="kd">{esc(a["zeile"])}</span>'
    cats = " ".join(a["kat"])
    attr = f'class="karte rv" data-kat="{cats}" style="--d:{i % 3}"'
    if a.get("seite"):
        return f'<a {attr} href="/projekte/{a["slug"]}/">{inhalt}<span class="mehr mono">Projekt ansehen →</span></a>'
    if a.get("link"):
        return f'<a {attr} href="{a["link"]}" target="_blank" rel="noopener">{inhalt}<span class="mehr mono">Reel auf Instagram ↗</span></a>'
    if a.get("yt"):
        return f'<button type="button" {attr} data-yt="{a["yt"]}" data-t="{esc(a["titel"] + " · " + a["zeile"])}">{inhalt}<span class="mehr mono">Video abspielen ▶</span></button>'
    breiten = BILD[name][0]
    return f'<button type="button" {attr} data-img="/img/{name}-{breiten[-1]}.jpg" data-alt="{esc(alt)}" data-t="{esc(a["titel"] + " · " + a["zeile"])}">{inhalt}<span class="mehr mono">Ansehen +</span></button>'


# Raster: gleich hohe Kacheln (3:2), drei Spalten, kein Versatz
def raster(liste):
    teile = [f'<div class="zelle">{karte(a, i, "(min-width: 1100px) 31vw, (min-width: 640px) 48vw, 100vw")}</div>' for i, a in enumerate(liste)]
    return f'<div class="raster">{"".join(teile)}</div>'


# ---------------------------------------------------------------- Seiten
def business_ld():
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "name": "Jon Pride – Werbung & Business", "url": f"{SITE}/",
         "inLanguage": "de", "publisher": {"@id": f"{SITE}/#business"}},
        {"@type": "ProfessionalService", "@id": f"{SITE}/#business", "name": "Jon Pride – Werbung & Business",
         "url": f"{SITE}/", "image": f"{SITE}/img/w10-1600.jpg",
         "description": "Werbe- und Businessfotografie, Film und Content für Marken und Unternehmen in Hamburg, im Landkreis Harburg und in der Lüneburger Heide.",
         "telephone": "+49 162 3361352", "email": "me@jonpride.de", "priceRange": "€€",
         "address": {"@type": "PostalAddress", "streetAddress": "Schützenstraße 10", "postalCode": "21255",
                     "addressLocality": "Tostedt", "addressRegion": "Niedersachsen", "addressCountry": "DE"},
         "areaServed": ["Hamburg", "Landkreis Harburg", "Lüneburger Heide", "Lüneburg", "Buchholz in der Nordheide", "Deutschland"],
         "knowsAbout": ["Werbefotografie", "Businessfotografie", "Business-Porträts", "Foodfotografie", "Musikvideo", "Social-Media-Content"],
         "founder": {"@id": "https://jonpride.de/#person"}, "sameAs": ["https://jonpride.de/", "https://www.instagram.com/jonpride"]}]}


def kontakt():
    return """<section class="kontakt" id="kontakt">
  <div class="wrap kg">
    <div class="kl">
      <h1 class="rv">Projekt anfragen</h1>
      <p class="rv">Erzählt mir kurz von eurem Projekt. Ich melde mich innerhalb von zwei Werktagen.</p>
      <p class="rv kd2"><a href="mailto:me@jonpride.de">me@jonpride.de</a><br><a href="tel:+491623361352">0162 3361352</a></p>
    </div>
    <form class="form rv" action="https://jonpride.de/api/formular/anfrage" method="POST">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="seite" value="werbung">
      <div class="row"><div><label for="f-name">Name *</label><input id="f-name" type="text" name="name" required autocomplete="name"></div>
      <div><label for="f-firma">Firma</label><input id="f-firma" type="text" name="firma" autocomplete="organization"></div></div>
      <div class="row"><div><label for="f-mail">E-Mail *</label><input id="f-mail" type="email" name="email" required autocomplete="email"></div>
      <div><label for="f-tel">Telefon</label><input id="f-tel" type="tel" name="telefon" autocomplete="tel"></div></div>
      <div class="row"><div><label for="f-leistung">Worum geht es?</label><select id="f-leistung" name="leistung">
        <option value="">Bitte wählen</option><option>Werbe- / Produktfotografie</option><option>Markenauftritt / Unternehmen</option><option>Mitarbeiterporträts</option><option>Food / Restaurant</option><option>Content / Social Media</option><option>Video / Musikvideo</option><option>Sonstiges</option></select></div>
      <div><label for="f-zeit">Zeitraum</label><input id="f-zeit" type="text" name="zeitraum" placeholder="z. B. März 2027 oder offen"></div></div>
      <div><label for="f-msg">Nachricht</label><textarea id="f-msg" name="nachricht" placeholder="Was soll entstehen, wofür und wo?"></textarea></div>
      <p class="hinweis">Mit dem Absenden stimmt ihr zu, dass ich eure Angaben zur Beantwortung der Anfrage verarbeite. Details in der <a href="https://jonpride.de/datenschutz">Datenschutzerklärung</a>.</p>
      <button type="submit">Anfrage senden</button>
    </form>
  </div>
</section>"""


def startseite():
    hero_alt = D["bilder"]["w10"]
    kunden = "".join(f"<li>{esc(k)}</li>" for k in D["kunden"])
    auswahl = [BY_SLUG[x] for x in D["startseite"]]
    kats = [k for k in D["kategorien"] if kat_arbeiten(k["slug"])]
    kacheln = "".join(
        f'<a class="kat-k rv" style="--d:{i % 3}" href="/{k["slug"]}/"><div class="media">{bild(k["cover"], D["bilder"].get(k["cover"], k["name"]), "(min-width: 1100px) 31vw, (min-width: 640px) 48vw, 100vw")}</div>'
        f'<span class="kz"><span class="kt">{esc(k["name"])}</span><span class="km mono">{len(kat_arbeiten(k["slug"]))} {"Arbeit" if len(kat_arbeiten(k["slug"])) == 1 else "Arbeiten"}</span></span>'
        f'<span class="kd">{esc(k["leistung"])}</span><span class="mehr mono">Ansehen →</span></a>' for i, k in enumerate(kats))
    kacheln += '<a class="kat-k cta-k rv" style="--d:2" href="/kontakt/"><span class="kt">Euer Projekt?</span><span class="kd">Erzählt mir in zwei Minuten, was entstehen soll. Antwort innerhalb von zwei Werktagen.</span><span class="btn schwarz">Projekt anfragen</span></a>'
    rg = "".join(f'<a class="rgk rv" href="/ratgeber/{r["slug"]}/"><span class="mono">{esc(r["thema"])}</span><span class="rgt">{esc(r["titel"])}</span><span class="mehr mono">Lesen →</span></a>' for r in RATGEBER)
    h = kopf("Werbefotograf & Content Creator Hamburg – Jon Pride",
             "Werbe- und Businessfotografie, Film und Content für Marken: Swarovski, Procter & Gamble, Volkswagen, McDonald's, Sky Sport. Jon Pride aus Hamburg und der Lüneburger Heide.",
             "/", [business_ld()])
    h += f"""<section class="hero">
  <div class="wrap hg">
    <div class="ht">
      <p class="mono eyebrow rv">Werbe- und Businessfotografie · Hamburg &amp; international</p>
      <h1>{worte("Länger im Kopf als auf dem Bildschirm.")}</h1>
      <p class="lead rv">Kampagnen für Swarovski und Procter &amp; Gamble, ein TV-Format für Sky Sport und Musikvideos mit Millionen Views. Seit 2009 hinter der Kamera.</p>
      <div class="btns rv"><a class="btn voll" href="#arbeiten">Arbeiten ansehen</a><a class="btn rand" href="/kontakt/">Projekt anfragen</a></div>
    </div>
    <figure class="hb rv">{bild("w10", hero_alt, "(min-width: 900px) 48vw, 100vw", eager=True)}<figcaption class="mono">Fashion-Editorial · Lüneburger Heide</figcaption></figure>
  </div>
</section>
<section class="zahlen" aria-label="In Zahlen"><div class="wrap zg">{"".join(f'<div class="rv" style="--d:{i}"><span class="zz">{esc(z)}</span><span class="zt">{esc(t)}</span></div>' for i, (z, t) in enumerate(D["zahlen"]))}</div></section>
<section class="kunden" aria-label="Kunden"><div class="wrap"><ul>{kunden}</ul></div></section>
<section class="arbeiten" id="arbeiten">
  <div class="wrap">
    <div class="ah"><h2 class="rv">Ausgewählte<br>Arbeiten</h2><p class="lead rv">Sechs Projekte aus Kampagne, Film und Social.</p></div>
    {raster(auswahl)}
  </div>
</section>
<section class="leistungen" id="leistungen">
  <div class="wrap"><div class="ah"><h2 class="rv">Was ich <em>mache</em></h2><p class="lead rv">Jeder Bereich hat eigene Arbeiten und Antworten auf die häufigsten Fragen. Ansprechpartner bin immer ich.</p></div><div class="raster">{kacheln}</div></div>
</section>
<section class="ratgeber-teaser liste-start"><div class="wrap"><h2 class="rv">Ratgeber für Unternehmen</h2><div class="rgl">{rg}</div></div></section>
<section class="band"><div class="wrap bg"><h2>Eigenes Projekt im Kopf?</h2><a class="btn schwarz" href="/kontakt/">Projekt anfragen</a></div></section>
"""
    return h + fuss()


def kontakt_seite():
    ld_k, nav_k = krumen([("Start", "/"), ("Projekt anfragen", "/kontakt/")])
    paare = [D["faq"][k] for k in D["startseite_faq"]]
    faq_ld, faq_html = faq_block(paare)
    h = kopf("Projekt anfragen – Jon Pride, Werbe- und Businessfotografie",
             "Anfrage für Werbe- und Businessfotografie, Film oder Content. Antwort innerhalb von zwei Werktagen. Jon Pride, Hamburg und Lüneburger Heide.",
             "/kontakt/", [ld_k, faq_ld])
    h += f"""<section class="seitenkopf"><div class="wrap">{nav_k}</div></section>
{kontakt()}
<section class="faq-s"><div class="wrap">{faq_html}<p><a class="weiter mono" href="/#arbeiten">Arbeiten ansehen →</a><a class="weiter mono" href="/ratgeber/">Ratgeber →</a></p></div></section>
"""
    return h + fuss()


def kategorie(k):
    liste = kat_arbeiten(k["slug"])
    ld_k, nav_k = krumen([("Start", "/"), ("Arbeiten", "/#arbeiten"), (k["name"], f'/{k["slug"]}/')])
    paare = [D["faq"][x] for x in k["faq"]]
    faq_ld, faq_html = faq_block(paare, f"Häufige Fragen zu {k['name']}")
    chips = "".join(
        f'<a class="chip{" an" if kk["slug"] == k["slug"] else ""}" href="/{kk["slug"]}/"{" aria-current=page" if kk["slug"] == k["slug"] else ""}>{esc(kk["name"])}</a>'
        for kk in D["kategorien"] if kat_arbeiten(kk["slug"]))
    rg = [r for r in RATGEBER if r.get("kategorie") == k["slug"]]
    rg_html = "".join(f'<a class="weiter mono" href="/ratgeber/{r["slug"]}/">Ratgeber: {esc(r["titel"])} →</a>' for r in rg)
    coll = {"@context": "https://schema.org", "@type": "CollectionPage", "name": k["name"], "url": f'{SITE}/{k["slug"]}/',
            "isPartOf": {"@id": f"{SITE}/#website"}, "description": k["desc"]}
    og = next((bild_name(a) for a in liste if bild_name(a)), "w10")
    h = kopf(k["title"], k["desc"], f'/{k["slug"]}/', [coll, ld_k, faq_ld], og_bild=og)
    h += f"""<section class="seitenkopf"><div class="wrap">
  {nav_k}
  <div class="skg"><h1>{worte(k["name"])}</h1><p class="lead rv">{esc(k["intro"])}</p></div>
  {f'<div class="preis rv"><p class="pz">{esc(k["preis"][0])}</p><p>{esc(k["preis"][1])}</p><a class="btn voll" href="/kontakt/">Angebot anfragen</a></div>' if k.get("preis") else ""}
  {('<div class="stufen rv">' + "".join(f'<div class="stufe{" top" if i == 1 else ""}"><p class="mono">{esc(n)}{" · Empfehlung" if i == 1 else ""}</p><p class="sp">{esc(pr)}</p><p>{esc(t)}</p></div>' for i, (n, pr, t) in enumerate(k["stufen"])) + '</div>') if k.get("stufen") else ""}
  <div class="chips rv">{chips}</div>
</div></section>
<section class="arbeiten kat"><div class="wrap">{raster(liste)}</div></section>
<section class="faq-s"><div class="wrap">{faq_html}{rg_html}</div></section>
<section class="band"><div class="wrap bg"><h2>Eigenes Projekt im Kopf?</h2><a class="btn schwarz" href="/kontakt/">Projekt anfragen</a></div></section>
"""
    return h + fuss()


def projekt(a):
    i = PROJEKTE.index(a)
    vor, nach = PROJEKTE[i - 1], PROJEKTE[(i + 1) % len(PROJEKTE)]
    k = KAT[a["kat"][0]]
    ld_k, nav_k = krumen([("Start", "/"), (k["name"], f'/{k["slug"]}/'), (a["titel"], f'/projekte/{a["slug"]}/')])
    dl = "".join(f"<dt class=\"mono\">{esc(x)}</dt><dd>{esc(y)}</dd>" for x, y in a["steckbrief"])
    txt = []
    for t in a["text"]:
        if isinstance(t, list):
            txt.append(f'<h2 class="rv">{esc(t[0])}</h2><p class="rv">{esc(t[1])}</p>')
        else:
            txt.append(f'<p class="rv erster">{esc(t)}</p>')
    quellen = ""
    if a.get("quellen"):
        quellen = '<p class="quellen mono">Quellen: ' + " · ".join(f'<a href="{u}" rel="noopener">{esc(n)}</a>' for n, u in a["quellen"]) + "</p>"
    if a.get("bilder"):
        n0 = a["bilder"][0]
        hero = f'<figure class="ph rv" style="view-transition-name:p-{a["slug"]}">{bild(n0, D["bilder"].get(n0, a["titel"]), "100vw", eager=True)}</figure>'
        galerie = '<div class="gal">' + "".join(f'<figure class="rv">{bild(n, D["bilder"].get(n, a["titel"]), "(min-width: 900px) 50vw, 100vw")}</figure>' for n in a["bilder"][1:]) + "</div>"
    else:
        hero = f'<div class="ph leer" style="view-transition-name:p-{a["slug"]}"><span>{esc(a.get("kunde") or a["titel"])}</span></div>'
        galerie = ""
    cw = {"@context": "https://schema.org", "@type": "CreativeWork", "name": a["titel"], "url": f'{SITE}/projekte/{a["slug"]}/',
          "description": a["kurz"], "creator": {"@id": "https://jonpride.de/#person"}, "publisher": {"@id": f"{SITE}/#business"},
          "about": a.get("kunde", a["titel"])}
    passend = [r for r in RATGEBER if a["slug"] in r.get("projekte", [])]
    rg = "".join(f'<a class="weiter mono" href="/ratgeber/{r["slug"]}/">Ratgeber: {esc(r["titel"])} →</a>' for r in passend)
    h = kopf(f'{a["titel"]}: {a["zeile"]} – Jon Pride', a["kurz"], f'/projekte/{a["slug"]}/', [cw, ld_k],
             og_bild=bild_name(a) or "w10")
    h += f"""<article class="projekt">
<section class="seitenkopf"><div class="wrap">
  {nav_k}
  <h1 class="riesig">{worte(a["titel"])}</h1>
  <p class="lead rv">{esc(a["kurz"])}</p>
</div></section>
<div class="wrap">{hero}</div>
<section class="pinfo"><div class="wrap pg">
  <dl class="steck rv">{dl}</dl>
  <div class="ptext">{"".join(txt)}{quellen}<p class="rv"><a class="weiter mono" href="/{k["slug"]}/">Mehr aus {esc(k["name"])} →</a></p>{rg}</div>
</div></section>
{f'<div class="wrap">{galerie}</div>' if galerie else ""}
<nav class="pnav" aria-label="Weitere Projekte"><div class="wrap pnv">
  <a href="/projekte/{vor["slug"]}/" class="mono">← {esc(vor["titel"])}</a>
  <a class="btn voll" href="/kontakt/">Ähnliches Projekt anfragen</a>
  <a href="/projekte/{nach["slug"]}/" class="mono">Nächstes Projekt: {esc(nach["titel"])} →</a>
</div></nav>
</article>
"""
    return h + fuss()


def ratgeber_seite(r):
    ld_k, nav_k = krumen([("Start", "/"), ("Ratgeber", "/ratgeber/"), (r["titel"], f'/ratgeber/{r["slug"]}/')])
    faq_ld, faq_html = faq_block(r["faq"])
    stand = date.fromisoformat(r["stand"]).strftime("%d.%m.%Y")
    schritte = "".join(f'<li class="rv"><span class="nr">{i + 1:02d}</span><div><h3>{esc(t)}</h3><p>{esc(p)}</p></div></li>' for i, (t, p) in enumerate(r["schritte"]))
    bt, bp, bslug = r["beispiel"]
    proj = "".join(f'<a href="/projekte/{s}/">{esc(BY_SLUG[s]["titel"])}: {esc(BY_SLUG[s]["zeile"])} →</a>' for s in r["projekte"])
    quellen = "".join(f'<li><a href="{u}" rel="noopener">{esc(n)}</a></li>' for n, u in r["quellen"])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": r["titel"], "description": r["desc"],
           "datePublished": r["stand"], "dateModified": r["stand"], "inLanguage": "de",
           "author": {"@id": "https://jonpride.de/#person"}, "publisher": {"@id": f"{SITE}/#business"},
           "mainEntityOfPage": f'{SITE}/ratgeber/{r["slug"]}/'}
    h = kopf(r["title"], r["desc"], f'/ratgeber/{r["slug"]}/', [art, ld_k, faq_ld])
    h += f"""<article class="ratgeber"><div class="wrap schmal">
  {nav_k}
  <p class="mono meta">Ratgeber · Stand {stand} · von Jon Pride</p>
  <h1>{worte(r["titel"])}</h1>
  <div class="kurz rv"><p class="mono">Kurzantwort</p><p>{esc(r["kurzantwort"])}</p></div>
  <h2 class="rv">In fünf Schritten</h2>
  <ol class="schritte">{schritte}</ol>
  <div class="bsp rv"><h2>{esc(bt)}</h2><p>{esc(bp)}</p><a class="weiter mono" href="/projekte/{bslug}/">Zum Projekt {esc(BY_SLUG[bslug]["titel"])} →</a></div>
  <h2 class="rv">{esc(r["recht"][0])}</h2><p class="rv">{esc(r["recht"][1])}</p>
  {faq_html}
  <div class="proj rv"><p class="mono">So sah das in echt aus</p>{proj}</div>
  <div class="quellen-l rv"><p class="mono">Quellen · Stand {stand}</p><ul>{quellen}</ul></div>
</div></article>
<section class="band"><div class="wrap bg"><h2>Eigenes Projekt im Kopf?</h2><a class="btn schwarz" href="/kontakt/">Projekt anfragen</a></div></section>
"""
    return h + fuss()


def ratgeber_index():
    ld_k, nav_k = krumen([("Start", "/"), ("Ratgeber", "/ratgeber/")])
    liste = "".join(f'<a class="rgk rv" href="/ratgeber/{r["slug"]}/"><span class="mono">{esc(r["thema"])}</span><span class="rgt">{esc(r["titel"])}</span><span class="kd">{esc(r["kurzantwort"].split(". ")[0])}.</span><span class="mehr mono">Lesen →</span></a>' for r in RATGEBER)
    h = kopf("Ratgeber Werbe- und Businessfotografie – Jon Pride",
             "Ratgeber für Unternehmen: wie Werbefotos entstehen, was sie kosten und wie Nutzungsrechte funktionieren. Von Jon Pride, Werbefotograf aus Hamburg.",
             "/ratgeber/", [ld_k])
    h += f"""<section class="seitenkopf"><div class="wrap">{nav_k}<div class="skg"><h1>{worte("Ratgeber")}</h1>
<p class="lead rv">Antworten für Unternehmen, die Fotos oder Videos planen: Ablauf, Kosten, Rechte. Aus der Praxis mit Marken wie Swarovski und Procter &amp; Gamble.</p></div></div></section>
<section class="ratgeber-teaser liste"><div class="wrap"><div class="rgl">{liste}</div><p><a class="weiter mono" href="/#arbeiten">Arbeiten ansehen →</a></p></div></section>
<section class="band"><div class="wrap bg"><h2>Eigenes Projekt im Kopf?</h2><a class="btn schwarz" href="/kontakt/">Projekt anfragen</a></div></section>
"""
    return h + fuss()


def seite_404():
    h = kopf("Seite nicht gefunden – Jon Pride", "Diese Seite gibt es nicht.", "/404", [], extra='<meta name="robots" content="noindex">')
    h += """<section class="seitenkopf"><div class="wrap"><h1>Hier ist nichts.</h1><p class="lead">Die Seite gibt es nicht oder nicht mehr.</p>
<p><a class="btn voll" href="/">Zur Startseite</a> <a class="btn rand" href="/#arbeiten">Arbeiten ansehen</a></p></div></section>"""
    return h + fuss()


# ---------------------------------------------------------------- Ausgabe
def schreiben(pfad, inhalt):
    p = PUB / pfad.strip("/") / "index.html" if pfad != "/404" else PUB / "404.html"
    if pfad == "/":
        p = PUB / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(inhalt)
    return pfad


def main():
    bilder_bauen()
    urls = []
    urls.append(schreiben("/", startseite()))
    for k in D["kategorien"]:
        if kat_arbeiten(k["slug"]):
            urls.append(schreiben(f'/{k["slug"]}/', kategorie(k)))
    for a in PROJEKTE:
        urls.append(schreiben(f'/projekte/{a["slug"]}/', projekt(a)))
    urls.append(schreiben("/kontakt/", kontakt_seite()))
    urls.append(schreiben("/ratgeber/", ratgeber_index()))
    for r in RATGEBER:
        urls.append(schreiben(f'/ratgeber/{r["slug"]}/', ratgeber_seite(r)))
    schreiben("/404", seite_404())

    (PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{HEUTE}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = ["# Jon Pride – Werbung & Business", "",
            "> Werbe- und Businessfotografie, Film und Content für Marken und Unternehmen. Fotograf und Filmemacher Jon Pride (Jan Stolz), Tostedt bei Hamburg, seit 2009. Kunden u. a. Swarovski, Procter & Gamble, Volkswagen, McDonald's, Sky Sport. Hochzeiten: https://jonpride.de",
            "", "## Arbeiten"]
    llms += [f'- [{k["name"]}]({SITE}/{k["slug"]}/): {k["intro"]}' for k in D["kategorien"] if kat_arbeiten(k["slug"])]
    llms += ["", "## Projekte"] + [f'- [{a["titel"]}]({SITE}/projekte/{a["slug"]}/): {a["kurz"]}' for a in PROJEKTE]
    llms += ["", "## Ratgeber"] + [f'- [{r["titel"]}]({SITE}/ratgeber/{r["slug"]}/): {r["kurzantwort"]}' for r in RATGEBER]
    llms += ["", "## Kontakt", "- E-Mail: me@jonpride.de", "- Telefon: 0162 3361352", f"- Anfrage: {SITE}/kontakt/", ""]
    (PUB / "llms.txt").write_text("\n".join(llms))
    print(f"{len(urls)} Seiten, {len(BILD)} Bilder")


if __name__ == "__main__":
    main()
