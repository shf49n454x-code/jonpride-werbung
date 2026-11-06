// Baut die Checkliste als PDF: node tools/pdf.mjs
// Quelle: src/pdf/checkliste.html  Ziel: public/downloads/checkliste-mitarbeiterfotos.pdf
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
// require findet playwright auch, wenn es global installiert ist
const { chromium } = require('playwright');
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const quelle = resolve('src/pdf/checkliste.html');
const ziel = resolve('public/downloads/checkliste-mitarbeiterfotos.pdf');
mkdirSync(resolve('public/downloads'), { recursive: true });
const browser = await chromium.launch();
const seite = await browser.newPage();
await seite.goto('file://' + quelle, { waitUntil: 'networkidle' });
await seite.evaluate(() => document.fonts.ready);
await seite.pdf({ path: ziel, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log('PDF:', ziel);
