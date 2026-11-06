#!/usr/bin/env python3
"""Baut jonandjoystudios.com nach public/. Aufruf: python3 tools/build.py"""
import json, os, pathlib, html
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = "https://jonandjoystudios.com"
STAND = "06.11.2026"
MAIL = "hello@jonandjoystudios.com"
TEL = "0162 3361352"
TEL_INT = "+491623361352"

PLAYFAIR = (ROOT / "tools/playfair.css").read_text()

# ---------- Bilder ----------
BILDER = {
    "w04": ("Executive-Porträt am Empfang einer Bank", "Executive-Porträt", "Corporate"),
    "w08": ("Studioporträt einer Frau mit kurzen blonden Haaren vor warmem Hintergrund", "Studioporträt", "Porträt"),
    "w03": ("Rennfahrer im Phoenix-Racing-Overall, freigestellt für die Pressemappe", "Fahrerporträt", "Motorsport · Phoenix Racing"),
    "w01": ("Beauty-Porträt in Schwarz-Weiß im Gegenlicht", "Beauty-Porträt", "Editorial"),
    "w09": ("Vier Geschäftsreisende mit Koffern auf dem Weg zum Privatjet", "Business Travel", "Kampagne"),
    "w07": ("Verpackung und Skizzen auf gelbem Grund, von oben fotografiert", "Verpackung & Konzept", "Produkt"),
    "w05": ("Dessert mit Feigen und Heidelbeeren, Food-Styling für ein Restaurant", "Fine Dining", "Food"),
    "w11": ("Himbeer-Dessert auf Steingutteller", "Dessert", "Food"),
    "w10": ("Model im orangen Kleid in der blühenden Heide bei Gegenlicht", "Fashion in der Heide", "Editorial"),
    "w06": ("Band auf einem Dach vor der Skyline, Scheinwerfer im Hintergrund", "Bandfoto", "Künstler"),
    "w12": ("Festzelt-Tafeln vor einem Fußballstadion, Eventaufbau von oben", "Event-Aufbau", "Corporate Event"),
}

def groessen(n):
    w = Image.open(ROOT / f"src/img/{n}.jpg").width
    return [s for s in (640, 1000, 1600) if s <= w or s == 640]

def img(n, sizes="(min-width: 900px) 50vw, 100vw", eager=False, cls=""):
    alt = BILDER[n][0]
    gs = groessen(n)
    im = Image.open(PUB / f"img/{n}-{gs[-1]}.jpg")
    w, h = im.size
    webp = ", ".join(f"/img/{n}-{g}.webp {g}w" for g in gs)
    jpg = ", ".join(f"/img/{n}-{g}.jpg {g}w" for g in gs)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="/img/{n}-{gs[-1]}.jpg" srcset="{jpg}" sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}" {load} class="{cls}"></picture>')

# ---------- Rahmen ----------
CSS = """
@font-face{font-family:'Archivo';src:url(/fonts/archivo-variable.woff2) format('woff2');font-weight:100 900;font-stretch:62% 125%;font-display:swap}
@font-face{font-family:'JetBrains Mono';src:url(/fonts/jetbrains-mono-variable.woff2) format('woff2');font-weight:100 800;font-display:swap}
""" + PLAYFAIR + """
:root{--paper:#F3EFE8;--paper-2:#E9E3D9;--ink:#141413;--ink-2:#55524C;--line:#D6CFC3;--deep:#1C2B27;--deep-2:#24372F;--on-deep:#EDE8DF;--on-deep-2:#A9B3AC;--accent:#B5734A;
--sans:'Archivo','Helvetica Neue',Arial,sans-serif;--serif:'Playfair Display',Georgia,serif;--mono:'JetBrains Mono',ui-monospace,monospace;--pad:clamp(16px,4vw,48px);--max:1280px}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 18px/1.6 var(--sans);font-stretch:100%}
img{max-width:100%;height:auto;display:block}picture{display:block}
a{color:inherit}a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
.mono{font:500 12.5px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;background:var(--ink);color:var(--paper);padding:10px 14px;z-index:9}
header.top{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
.logo{text-decoration:none;font:700 15px/1 var(--sans);font-stretch:112%;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
.logo em{font:italic 400 22px/1 var(--serif);letter-spacing:0;text-transform:none;margin:0 .18em;color:var(--accent)}
nav.main{display:flex;gap:28px;align-items:center}
nav.main a{text-decoration:none;font-size:15px;font-weight:500}
nav.main a:hover{text-decoration:underline;text-underline-offset:5px}
nav.main a.cta{background:var(--ink);color:var(--paper);padding:10px 16px}
nav.main a.cta:hover{background:var(--deep);text-decoration:none}
@media(max-width:820px){nav.main a:not(.cta){display:none}}
h1,h2,h3{text-wrap:balance;overflow-wrap:break-word;font-family:var(--sans);font-weight:700;line-height:1.04;letter-spacing:-.015em;margin:0}
h1{font-size:clamp(38px,5.6vw,80px);font-stretch:96%}
h2{font-size:clamp(32px,4.2vw,56px);font-stretch:96%}
h3{font-size:22px;line-height:1.2;hyphens:auto;-webkit-hyphens:auto}
.ser{font-family:var(--serif);font-style:italic;font-weight:400;letter-spacing:-.01em}
section{padding:clamp(72px,10vw,140px) 0}
.lead{font-size:clamp(19px,1.6vw,22px);line-height:1.55;color:var(--ink-2);max-width:34em}
.btn{display:inline-block;text-decoration:none;font-weight:600;font-size:16px;padding:16px 24px;border:1.5px solid var(--ink)}
.btn.solid{background:var(--ink);color:var(--paper)}.btn.solid:hover{background:var(--deep);border-color:var(--deep)}
.btn.ghost:hover{background:var(--ink);color:var(--paper)}
/* Hero */
.hero{padding:clamp(40px,6vw,80px) 0 clamp(56px,8vw,110px)}
.hero .grid{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(28px,5vw,72px);align-items:center}
.hero picture{aspect-ratio:4/5;overflow:hidden}.hero img{width:100%;height:100%;object-fit:cover;object-position:30% 30%}
.hero .eyebrow{margin-bottom:16px;color:var(--ink-2)}
.hero p.lead{margin:28px 0 36px}
.hero .actions{display:flex;flex-wrap:wrap;gap:12px}
.hero figure{margin:0;position:relative}
.hero figcaption{margin-top:12px;color:var(--ink-2)}
@media(max-width:900px){.hero .grid{grid-template-columns:1fr}.hero picture{aspect-ratio:3/2;max-height:46vh}}
/* Leistungen */
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(20px,3vw,40px);margin-top:56px}
.card{display:flex;flex-direction:column;text-decoration:none;background:var(--paper-2)}
.card .txt{padding:28px 28px 32px;display:flex;flex-direction:column;gap:12px;flex:1}
.card p{margin:0;color:var(--ink-2)}
.card .more{margin-top:auto;padding-top:12px;font-weight:600}
.card:hover .more{text-decoration:underline;text-underline-offset:5px}
.card picture{aspect-ratio:3/2;overflow:hidden}.card img{width:100%;height:100%;object-fit:cover;object-position:50% 25%;transition:transform .6s ease}.card img.top{object-position:50% 12%}
.card:hover img{transform:scale(1.015)}
@media(max-width:760px){.two{grid-template-columns:1fr}}
/* Arbeiten (dunkel) */
.dark{background:var(--deep);color:var(--on-deep)}
.dark .lead{color:var(--on-deep-2)}
.works{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:32px 16px;margin-top:56px}
.works figure{margin:0}.works picture{overflow:hidden}.works img{width:100%;height:100%;object-fit:cover}
.works .xl{grid-column:span 7}.works .xl picture{aspect-ratio:7/5}.works .m{grid-column:span 5}.works .m picture{aspect-ratio:1/1}.works .s{grid-column:span 4}.works .s picture{aspect-ratio:4/3}.works img[src*=w03],.works img[src*=w08]{object-position:50% 15%}
@media(max-width:760px){.works figure{grid-column:1/-1!important}.works picture{aspect-ratio:3/2!important}}
.works figcaption{display:flex;justify-content:space-between;gap:12px;padding:12px 0 0;color:var(--on-deep-2)}
.works figcaption b{color:var(--on-deep);font-weight:500;letter-spacing:.08em}
/* Kunden */
.clients{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));column-gap:24px;margin-top:40px;border-top:1px solid var(--line)}
.clients span{padding:22px 0;border-bottom:1px solid var(--line);font:600 clamp(16px,1.4vw,19px)/1.3 var(--sans);font-stretch:118%;letter-spacing:.02em;text-transform:uppercase}
.quote{margin:96px 0 0 auto;max-width:28em;border-left:2px solid var(--accent);padding-left:32px}
.quote p{font:italic 400 clamp(24px,2.6vw,34px)/1.35 var(--serif);margin:0 0 16px}
.quote cite{font-style:normal;color:var(--ink)}
/* Ablauf */
.steps{list-style:none;padding:0;margin:56px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;counter-reset:s}
.steps li{border-top:2px solid var(--ink);padding-top:24px;counter-increment:s}
.steps li::before{content:"0" counter(s);display:block;font:500 12px var(--mono);letter-spacing:.12em;margin-bottom:14px;color:var(--accent)}
.steps h3{font-size:26px}.steps p{margin:10px 0 0;color:var(--ink-2);font-size:16px}
@media(max-width:900px){.steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:520px){.steps{grid-template-columns:1fr}}
/* FAQ */
.faq{max-width:860px;margin-top:40px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;padding:22px 40px 22px 0;font-weight:600;font-size:19px;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:4px;top:18px;font:300 28px/1 var(--sans)}
.faq details[open] summary::after{content:"–"}
.faq details p{margin:0 0 24px;color:var(--ink-2);max-width:42em}
/* Kontakt */
.contact .grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:48px;align-items:end}
.contact .big{font:700 clamp(22px,2.6vw,34px)/1.2 var(--sans);text-decoration:none;display:inline-block;border-bottom:2px solid var(--accent);padding-bottom:4px;word-break:normal}
@media(max-width:420px){.contact .big{font-size:19px}}
.contact dl{margin:0;display:grid;gap:18px}.contact dt{color:var(--on-deep-2)}.contact dd{margin:4px 0 0;font-size:20px}
.contact dd a{text-decoration:none;border-bottom:1px solid currentColor}
@media(max-width:820px){.contact .grid{grid-template-columns:1fr}}
/* Unterseite */
.page-hero{padding:clamp(48px,7vw,96px) 0 0}
.crumbs{margin-bottom:28px;color:var(--ink-2)}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.answer{margin-top:32px;max-width:40em}
.answer p{margin:0}
.prose{max-width:44em}.prose p,.prose li{color:var(--ink-2)}.prose h2{margin:0 0 20px}.prose ul{padding-left:1.2em}
.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:start}
@media(max-width:860px){.split{grid-template-columns:1fr}}
.gallery{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;margin-top:40px}
.gallery picture{aspect-ratio:4/5;overflow:hidden}.gallery img{width:100%;height:100%;object-fit:cover}
@media(max-width:760px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}.gallery picture:first-child{grid-column:1/-1;aspect-ratio:3/2}}
.stand{margin-top:16px;color:var(--ink-2)}
.legal{max-width:760px}.legal h2{font-size:24px;margin:40px 0 12px}.legal p{color:var(--ink-2)}
footer{border-top:1px solid var(--line);padding:40px 0 56px;font-size:15px;color:var(--ink-2)}
footer .wrap{display:flex;flex-wrap:wrap;gap:16px 32px;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:8px 24px}footer a{text-decoration:none}footer a:hover{text-decoration:underline}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

def logo():
    return '<a class="logo" href="/" aria-label="Jon &amp; Joy Studios, zur Startseite">Jon<em>&amp;</em>Joy Studios</a>'

def head(title, desc, path, ld, extra=""):
    url = SITE + path
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/img/w04-1600.jpg"><meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#F3EFE8"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/archivo-variable.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>{extra}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body>
<a class="skip" href="#inhalt">Zum Inhalt</a>
<header class="top"><div class="wrap">{logo()}<nav class="main" aria-label="Hauptnavigation"><a href="/business-portraets/">Business-Porträts</a><a href="/werbefotografie/">Werbefotografie</a><a href="/#arbeiten">Arbeiten</a><a href="/#kontakt" class="cta">Anfragen</a></nav></div></header>
<main id="inhalt">"""

def foot():
    return f"""</main><footer><div class="wrap"><div>© 2026 Jon &amp; Joy Studios</div>
<nav aria-label="Fußnavigation"><a href="/business-portraets/">Business-Porträts</a><a href="/werbefotografie/">Werbefotografie</a><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a><a href="https://jonpride.de">Hochzeiten: jonpride.de</a></nav></div></footer></body></html>"""

ORG = {"@type": "ProfessionalService", "@id": SITE + "/#org", "name": "Jon & Joy Studios", "url": SITE + "/",
       "description": "Business-Porträts, Werbe- und Produktfotografie für Unternehmen in Hamburg, im Landkreis Harburg und in der Lüneburger Heide.",
       "email": MAIL, "telephone": TEL_INT, "image": SITE + "/img/w04-1600.jpg",
       "address": {"@type": "PostalAddress", "addressLocality": "Tostedt", "postalCode": "21255", "addressCountry": "DE"},
       "areaServed": ["Hamburg", "Landkreis Harburg", "Lüneburger Heide", "Lüneburg", "Buchholz in der Nordheide", "Norddeutschland"],
       "founder": {"@id": SITE + "/#jan"}, "sameAs": ["https://jonpride.de"]}
PERSON = {"@type": "Person", "@id": SITE + "/#jan", "name": "Jan Stolz", "alternateName": "Jon Pride", "jobTitle": "Fotograf", "worksFor": {"@id": SITE + "/#org"}, "url": "https://jonpride.de"}

def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faqs) + "</div>"

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

KONTAKT = f"""<section class="dark contact" id="kontakt" aria-labelledby="kontakt-t"><div class="wrap"><div class="grid">
<div><p class="mono" style="color:var(--on-deep-2);margin:0 0 24px">Kontakt</p><h2 id="kontakt-t">Erzählen Sie kurz, <span class="ser">was Sie brauchen.</span></h2>
<p class="lead" style="margin:24px 0 32px">Wofür sind die Bilder, wie viele Personen oder Motive, bis wann? Sie bekommen innerhalb von zwei Werktagen ein Angebot mit Preis und Nutzungsrechten.</p>
<a class="big" href="mailto:{MAIL}?subject=Anfrage%20Fotoproduktion">{MAIL}</a><p style="margin:28px 0 0"><a class="btn" style="background:var(--on-deep);border-color:var(--on-deep);color:var(--deep);font-weight:700" href="mailto:{MAIL}?subject=Anfrage%20Fotoproduktion">Anfrage per Mail</a></p></div>
<dl><div><dt class="mono">Telefon</dt><dd><a href="tel:{TEL_INT}">{TEL}</a></dd></div><div><dt class="mono">Studio</dt><dd>Tostedt, zwischen Hamburg und der Lüneburger Heide</dd></div><div><dt class="mono">Einsatz</dt><dd>Bei Ihnen vor Ort, in ganz Norddeutschland</dd></div></dl>
</div></div></section>"""

# ---------- Startseite ----------
FAQ_START = [
    ("Was fotografiert Jon & Joy Studios?", "Business-Porträts für Team, Führung und Website sowie Werbe- und Produktfotos für Kampagnen, Verpackungen, Speisekarten und Social Media. Hochzeiten fotografiert Jan Stolz unter dem Namen JON PRIDE auf jonpride.de."),
    ("Kommen Sie zu uns ins Unternehmen?", "Ja. Für Porträts bringe ich ein mobiles Studio mit Licht und Hintergrund mit. Ein freier Raum von etwa vier mal vier Metern reicht. Produkte fotografiere ich vor Ort oder im Studio in Tostedt."),
    ("Was kostet ein Shooting?", "Das hängt von Dauer, Anzahl der Personen oder Motive und den Nutzungsrechten ab. Nach einem kurzen Briefing bekommen Sie ein schriftliches Angebot mit Festpreis, ohne nachträgliche Posten."),
    ("Wie sind die Nutzungsrechte geregelt?", "Kanäle, Laufzeit und Umfang stehen im Angebot. Für Website, Pressemappe und Social Media ist die Nutzung in der Regel zeitlich unbegrenzt enthalten. Anzeigen und Kampagnen werden gesondert vereinbart."),
    ("Arbeiten Sie mit Agenturen zusammen?", "Ja. Ich fotografiere nach Ihrem Briefing, arbeite mit Ihrem Art Director und stimme mich auf Wunsch direkt mit dem Endkunden ab."),
    ("Wie schnell sind die Bilder fertig?", "Eine Vorauswahl gibt es meist am Folgetag. Die bearbeiteten Bilder liefere ich innerhalb von fünf Werktagen in einer Online-Galerie, in Druck- und Webgröße."),
]

def startseite():
    ld = {"@context": "https://schema.org", "@graph": [ORG, PERSON, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Jon & Joy Studios", "inLanguage": "de", "publisher": {"@id": SITE + "/#org"}}, faq_ld(FAQ_START)]}
    LAYOUT = [("w06","xl"),("w01","m"),("w09","s"),("w08","s"),("w10","s"),("w07","m"),("w12","xl"),("w05","s"),("w11","s"),("w03","s")]
    SZ = {"xl":"(min-width:760px) 58vw, 100vw","m":"(min-width:760px) 42vw, 100vw","s":"(min-width:760px) 33vw, 100vw"}
    works = "".join(f'<figure class="{c}">{img(n, SZ[c])}<figcaption><b class="mono">{BILDER[n][1]}</b><span class="mono">{BILDER[n][2]}</span></figcaption></figure>' for n, c in LAYOUT)
    kunden = "".join(f"<span>{k}</span>" for k in ["Swarovski", "Volkswagen", "Levi’s", "P&amp;G", "McDonald’s", "Sky Sport", "UBS", "FC St. Pauli", "Wella", "LBS", "DVAG", "Phoenix Racing"])
    body = f"""
<section class="hero"><div class="wrap"><div class="grid">
<div><p class="mono eyebrow">Business- &amp; Werbefotografie · Hamburg</p>
<h1>Bilder, die aussehen wie <span class="ser">Ihr Unternehmen.</span></h1>
<p class="lead">Business-Porträts für Team und Führung, Werbe- und Produktfotos für Kampagnen. Fotografiert von Jan Stolz, Fotograf seit 2009, für Unternehmen von der Praxis bis zum Konzern.</p>
<div class="actions"><a class="btn solid" href="#kontakt">Shooting anfragen</a><a class="btn ghost" href="#arbeiten">Arbeiten ansehen</a></div></div>
<figure>{img("w04", "(min-width:900px) 45vw, 100vw", eager=True)}<figcaption class="mono">Executive-Porträt · Corporate</figcaption></figure>
</div></div></section>

<section style="padding-top:0" aria-labelledby="leistungen-t"><div class="wrap">
<p class="mono" style="color:var(--ink-2);margin:0 0 20px">Leistungen</p>
<h2 id="leistungen-t">Zwei Dinge, <span class="ser">richtig gemacht.</span></h2>
<div class="two">
<a class="card" href="/business-portraets/">{img("w08", "(min-width:760px) 50vw, 100vw", cls="top")}<div class="txt"><h3>Business-Porträts</h3><p>Mitarbeiter-, Team- und Vorstandsfotos in einheitlichem Look. Mit mobilem Studio bei Ihnen im Unternehmen, für Website, LinkedIn und Pressemappe.</p><span class="more">Mehr zu Business-Porträts →</span></div></a>
<a class="card" href="/werbefotografie/">{img("w09", "(min-width:760px) 50vw, 100vw")}<div class="txt"><h3>Werbe- &amp; Produktfotografie</h3><p>Kampagnen, Produkte, Food und Imagebilder. Vom Konzept über Location und Styling bis zum fertigen Motiv für Anzeige, Verpackung und Social Media.</p><span class="more">Mehr zur Werbefotografie →</span></div></a>
</div></div></section>

<section class="dark" id="arbeiten" aria-labelledby="arbeiten-t"><div class="wrap">
<p class="mono" style="color:var(--on-deep-2);margin:0 0 20px">Arbeiten</p>
<h2 id="arbeiten-t">Ausgewählte <span class="ser">Arbeiten.</span></h2>
<div class="works">{works}</div></div></section>

<section aria-labelledby="kunden-t"><div class="wrap">
<p class="mono" style="color:var(--ink-2);margin:0 0 20px">Kunden</p>
<h2 id="kunden-t">Für wen ich <span class="ser">fotografiert habe.</span></h2>
<div class="clients" role="list">{kunden.replace('<span>', '<span role="listitem">')}</div>
<blockquote class="quote"><p>„Sehr netter Kontakt, super Bilder für den geschäftlichen Bereich! Tolle Beratung und viele Möglichkeiten, was wir zusätzlich noch realisieren könnten.“</p><cite class="mono">Philipp Timm · Google-Rezension</cite></blockquote>
</div></section>

<section style="background:var(--paper-2)" aria-labelledby="ablauf-t"><div class="wrap">
<p class="mono" style="color:var(--ink-2);margin:0 0 20px">Ablauf</p>
<h2 id="ablauf-t">Vom Briefing <span class="ser">zum fertigen Bild.</span></h2>
<ol class="steps"><li><h3>Briefing</h3><p>15 Minuten am Telefon: wofür, wie viele, bis wann.</p></li><li><h3>Angebot</h3><p>Schriftlich, mit Festpreis und Nutzungsrechten.</p></li><li><h3>Shooting</h3><p>Bei Ihnen vor Ort oder im Studio, ohne Leerlauf für Ihr Team.</p></li><li><h3>Lieferung</h3><p>Bearbeitete Bilder in fünf Werktagen, in Web- und Druckgröße.</p></li></ol>
</div></section>

<section style="padding-top:0" aria-labelledby="faq-t"><div class="wrap">
<p class="mono" style="color:var(--ink-2);margin:0 0 20px">Fragen</p>
<h2 id="faq-t">Häufige <span class="ser">Fragen.</span></h2>{faq_html(FAQ_START)}</div></section>
{KONTAKT}"""
    return head("Jon & Joy Studios · Business-Porträts & Werbefotografie Hamburg", "Business-Porträts, Werbe- und Produktfotografie für Unternehmen in Hamburg, im Landkreis Harburg und in der Lüneburger Heide. Festpreis nach kurzem Briefing.", "/", ld) + body + foot()

# ---------- Unterseiten ----------
def unterseite(path, title, desc, h1, kurz, sections_html, faqs, galerie, name):
    ld = {"@context": "https://schema.org", "@graph": [ORG, PERSON,
          {"@type": "Service", "name": name, "provider": {"@id": SITE + "/#org"}, "areaServed": ORG["areaServed"], "url": SITE + path},
          crumbs_ld([("Startseite", "/"), (name, path)]), faq_ld(faqs)]}
    gal = "".join(img(n, "(min-width:760px) 33vw, 50vw") for n in galerie)
    body = f"""
<section class="page-hero"><div class="wrap">
<nav class="crumbs mono" aria-label="Brotkrumen"><a href="/">Startseite</a> / {name}</nav>
<h1>{h1}</h1>
<div class="answer"><p class="lead" style="color:var(--ink)">{kurz}</p></div>
<div class="gallery">{gal}</div>
<p class="mono stand">Stand: {STAND} · Jan Stolz, Fotograf seit 2009</p>
</div></section>
{sections_html}
<section style="padding-top:0" aria-labelledby="faq-t"><div class="wrap"><h2 id="faq-t">Häufige <span class="ser">Fragen.</span></h2>{faq_html(faqs)}</div></section>
{KONTAKT}"""
    return head(title, desc, path, ld) + body + foot()

FAQ_PORTRAET = [
    ("Wie lange dauert ein Porträt pro Person?", "Etwa zehn Minuten. Mit Aufbau und Abbau rechne ich bei 20 Personen mit einem halben Tag, ohne dass jemand lange warten muss."),
    ("Brauchen wir einen Raum mit besonderem Licht?", "Nein. Ich bringe Licht und Hintergrund mit. Ein freier Raum von etwa vier mal vier Metern genügt, Tageslicht ist nicht nötig."),
    ("Können neue Mitarbeiter später im gleichen Look fotografiert werden?", "Ja. Licht, Abstand und Hintergrund dokumentiere ich beim ersten Termin. So passen spätere Porträts genau zu den bisherigen."),
    ("Wer sucht die Bilder aus?", "Jede Person wählt in einer Online-Galerie ihr Lieblingsbild selbst aus. Auf Wunsch übernehme ich die Vorauswahl."),
    ("Wird retuschiert?", "Ja, natürlich und zurückhaltend: Hautunreinheiten, Fusseln, Haarsträhnen. Die Person bleibt erkennbar, Gesichtsformen verändere ich nicht."),
]
PORTRAET_SECTIONS = """
<section aria-labelledby="was-t"><div class="wrap split">
<div class="prose"><h2 id="was-t">Was Sie <span class="ser">bekommen.</span></h2>
<ul><li>Einheitlicher Look für das ganze Team, auf Wunsch passend zu Ihrem Corporate Design</li><li>Mobiles Studio mit Licht und Hintergrund bei Ihnen im Unternehmen</li><li>Auswahl in einer Online-Galerie, jede Person wählt selbst</li><li>Natürliche Retusche, Lieferung in fünf Werktagen</li><li>Formate für Website, LinkedIn, Pressemappe und Druck</li></ul></div>
<div class="prose"><h2>Für wen <span class="ser">es passt.</span></h2>
<p>Für Unternehmen, Kanzleien, Praxen und Agenturen, die auf Website und LinkedIn ein einheitliches Bild abgeben wollen. Ebenso für Geschäftsführung und Vorstand, die für Presse, Geschäftsbericht oder Vortrag ein Porträt brauchen.</p>
<p>Für größere Bildwelten mit Arbeitssituationen, Räumen und Produkten gibt es die <a href="/werbefotografie/">Werbe- und Imagefotografie</a>. Hochzeiten fotografiere ich auf <a href="https://jonpride.de">jonpride.de</a>.</p></div>
</div></section>"""

FAQ_WERBUNG = [
    ("Übernehmen Sie auch Konzept, Location und Styling?", "Ja. Auf Wunsch entwickle ich die Bildidee, suche Location und Models und organisiere Styling und Requisiten. Alternativ arbeite ich nach dem Briefing Ihrer Agentur."),
    ("Fotografieren Sie Produkte freigestellt?", "Ja, sowohl freigestellt auf Weiß für Shop und Katalog als auch inszeniert für Anzeigen und Social Media."),
    ("Machen Sie Food-Fotografie für Restaurants?", "Ja. Für Speisekarten, Website und Social Media fotografiere ich direkt in Ihrer Küche, wenn die Gerichte frisch angerichtet sind."),
    ("Was kostet eine Produktion?", "Das richtet sich nach Shooting-Tagen, Anzahl der Motive, Aufwand für Location und Styling sowie den Nutzungsrechten. Nach dem Briefing bekommen Sie ein schriftliches Angebot mit Festpreis."),
]
WERBUNG_SECTIONS = """
<section aria-labelledby="was-t"><div class="wrap split">
<div class="prose"><h2 id="was-t">Was ich <span class="ser">fotografiere.</span></h2>
<ul><li>Kampagnen und Imagebilder mit Models, Team oder Kunden</li><li>Produkte freigestellt und inszeniert, Verpackung und Packshots</li><li>Food und Getränke für Gastronomie und Hersteller</li><li>Events und Firmenfeiern als Bildstrecke für Presse und Social Media</li><li>Künstler und Bands für Presse und Streaming-Dienste</li></ul></div>
<div class="prose"><h2>Wie <span class="ser">gearbeitet wird.</span></h2>
<p>Am Anfang steht die Frage, wo das Bild laufen soll. Eine Anzeige braucht anderes Format und andere Freiflächen als ein Instagram-Post. Daraus folgen Motive, Licht und Location.</p>
<p>Fotografiert wird mit Profi-Licht und Tethering, damit Sie die Bilder am Set direkt am Bildschirm sehen und freigeben. Für Porträts Ihres Teams gibt es die <a href="/business-portraets/">Business-Porträts</a>, die <a href="/#arbeiten">Arbeiten</a> zeigen weitere Beispiele.</p></div>
</div></section>"""

def recht(path, title, inner):
    ld = {"@context": "https://schema.org", "@graph": [ORG]}
    return head(title + " · Jon & Joy Studios", title + " von Jon & Joy Studios.", path, ld, '<meta name="robots" content="noindex">') + f'<section class="page-hero"><div class="wrap legal"><h1 style="font-size:clamp(36px,5vw,56px)">{title}</h1>{inner}</div></section>' + foot()

IMPRESSUM = f"""<h2>Angaben gemäß § 5 DDG</h2><p>Jon &amp; Joy Studios<br>Jan Stolz<br>Schützenstraße 10<br>21255 Tostedt<br>Deutschland</p>
<h2>Kontakt</h2><p>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a><br>Telefon: {TEL}</p>
<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2><p>Jan Stolz, Anschrift wie oben.</p>
<h2>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>"""

DATENSCHUTZ = f"""<p class="mono stand">Stand: {STAND}</p>
<h2>1. Verantwortlicher</h2><p>Jon &amp; Joy Studios, Inhaber Jan Stolz, Schützenstraße 10, 21255 Tostedt. E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>2. Hosting</h2><p>Diese Website wird über Cloudflare Pages der Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, USA) ausgeliefert. Beim Aufruf verarbeitet Cloudflare technisch notwendige Daten, darunter Ihre IP-Adresse. Eine Verarbeitung in den USA ist nicht ausgeschlossen. Cloudflare ist unter dem EU-US Data Privacy Framework zertifiziert, ergänzend gelten die EU-Standardvertragsklauseln. Rechtsgrundlage ist unser berechtigtes Interesse an einer sicheren und schnellen Bereitstellung (Art. 6 Abs. 1 lit. f DSGVO). Mit Cloudflare besteht ein Vertrag zur Auftragsverarbeitung.</p>
<h2>3. Server-Logfiles</h2><p>Erhoben werden Browsertyp und -version, Betriebssystem, Referrer-URL, Uhrzeit der Anfrage und IP-Adresse. Die Daten dienen der technischen Sicherheit und werden nicht mit anderen Daten zusammengeführt.</p>
<h2>4. Keine Cookies, kein Tracking</h2><p>Diese Website setzt keine Cookies und lädt keine Analyse-, Werbe- oder Social-Media-Dienste. Schriften und Bilder liegen auf unserem eigenen Server.</p>
<h2>5. Kontakt per E-Mail oder Telefon</h2><p>Wenn Sie uns schreiben oder anrufen, verarbeiten wir Ihre Angaben, um Ihre Anfrage zu beantworten und ein Angebot zu erstellen (Art. 6 Abs. 1 lit. b DSGVO). Wir löschen die Daten, wenn sie dafür nicht mehr nötig sind und keine gesetzlichen Aufbewahrungsfristen bestehen.</p>
<h2>6. Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren, zum Beispiel bei der Landesbeauftragten für den Datenschutz Niedersachsen.</p>"""

PAGES = {
    "/": startseite(),
    "/business-portraets/": unterseite("/business-portraets/", "Business-Porträts Hamburg & Landkreis Harburg · Jon & Joy Studios",
        "Mitarbeiter-, Team- und Vorstandsporträts mit mobilem Studio bei Ihnen im Unternehmen. Einheitlicher Look, Auswahl online, Lieferung in fünf Werktagen.",
        'Business-Porträts, <span class="ser">bei Ihnen im Haus.</span>',
        "Ich komme mit Licht und Hintergrund zu Ihnen ins Unternehmen und fotografiere Team, Führung und neue Mitarbeiter in einem einheitlichen Look. Etwa zehn Minuten pro Person, Auswahl in einer Online-Galerie, fertige Bilder in fünf Werktagen.",
        PORTRAET_SECTIONS, FAQ_PORTRAET, ["w04", "w08", "w03"], "Business-Porträts"),
    "/werbefotografie/": unterseite("/werbefotografie/", "Werbe- & Produktfotografie Hamburg · Jon & Joy Studios",
        "Kampagnen, Produkte, Food und Imagebilder für Unternehmen in Hamburg und Norddeutschland. Konzept, Location, Styling und Shooting aus einer Hand.",
        'Werbe- &amp; Produktfotografie <span class="ser">mit Konzept.</span>',
        "Kampagnen, Produkte, Food und Imagebilder für Anzeige, Verpackung, Website und Social Media. Auf Wunsch mit Bildidee, Location, Models und Styling. Sie sehen die Bilder am Set und geben direkt frei.",
        WERBUNG_SECTIONS, FAQ_WERBUNG, ["w09", "w07", "w05"], "Werbefotografie"),
    "/impressum/": recht("/impressum/", "Impressum", IMPRESSUM),
    "/datenschutz/": recht("/datenschutz/", "Datenschutzerklärung", DATENSCHUTZ),
}

for path, content in PAGES.items():
    out = PUB / path.strip("/") / "index.html" if path != "/" else PUB / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)

nf = head("Seite nicht gefunden · Jon & Joy Studios", "Diese Seite gibt es nicht.", "/404", {"@context": "https://schema.org", "@graph": [ORG]}, '<meta name="robots" content="noindex">')
(PUB / "404.html").write_text(nf + '<section class="page-hero"><div class="wrap"><h1>Diese Seite <span class="ser">gibt es nicht.</span></h1><p class="lead" style="margin:24px 0 32px">Vielleicht hilft einer dieser Wege weiter.</p><a class="btn solid" href="/">Zur Startseite</a></div></section>' + foot())

indexiert = ["/", "/business-portraets/", "/werbefotografie/"]
(PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{p}</loc><lastmod>2026-11-06</lastmod></url>\n" for p in indexiert) + "</urlset>\n")
(PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(PUB / "llms.txt").write_text(f"""# Jon & Joy Studios

> Business-Porträts sowie Werbe- und Produktfotografie für Unternehmen in Hamburg, im Landkreis Harburg und in der Lüneburger Heide. Fotograf: Jan Stolz (Jon Pride), Tostedt, seit 2009. Hochzeiten: https://jonpride.de

## Seiten
- [Startseite]({SITE}/): Leistungen, Arbeiten, Kunden, Ablauf, FAQ, Kontakt
- [Business-Porträts]({SITE}/business-portraets/): Mitarbeiter-, Team- und Vorstandsporträts mit mobilem Studio
- [Werbefotografie]({SITE}/werbefotografie/): Kampagnen, Produkte, Food, Events

## Kontakt
- E-Mail: {MAIL}
- Telefon: {TEL}
""")
(PUB / "_headers").write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; script-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=2592000
""")
(PUB / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1C2B27"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="40" fill="#EDE8DF">&amp;</text></svg>')
print("ok", len(PAGES), "Seiten")
