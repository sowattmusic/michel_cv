// Régénère les captures du site et le journal de bord en PDF.
// Usage, depuis la racine du dépôt :  node docs/build_pdf.js
// Prérequis : Node et Playwright avec Chromium (require('playwright')).
const { chromium } = require('playwright');
const path = require('path');

const racine = path.resolve(__dirname, '..');
const site = path.join(racine, 'site/fr/index.html');
const journal = path.join(__dirname, 'journal');

(async () => {
  const navigateur = await chromium.launch();

  // 1. Captures d'écran du site (bureau et mobile)
  for (const [nom, vp] of [['bureau', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const page = await navigateur.newPage({ viewport: vp });
    await page.goto('file://' + site, { waitUntil: 'load' });
    await page.addStyleTag({ content: '.apparait{transition:none!important}' });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(journal, `ecran_${nom}_hero.png`) });
    await page.evaluate(() => document.querySelectorAll('.apparait').forEach(e => e.classList.add('vu')));
    await page.screenshot({ path: path.join(journal, `ecran_${nom}_complet.png`), fullPage: true });
    if (nom === 'bureau') {
      await page.locator('#prestations').scrollIntoViewIfNeeded();
      await page.evaluate(() => window.scrollTo(0, document.getElementById('prestations').offsetTop + 60));
      await page.waitForTimeout(500);
      await page.screenshot({ path: path.join(journal, 'ecran_bureau_prestations.png') });
    }
    await page.close();
  }

  // 2. Journal de bord en PDF
  const page = await navigateur.newPage();
  await page.goto('file://' + path.join(journal, 'journal_de_bord.html'), { waitUntil: 'load' });
  await page.waitForTimeout(1000);
  await page.pdf({
    path: path.join(__dirname, 'Journal_de_bord_site_Michel_Gallone.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: '16mm', bottom: '18mm', left: '16mm', right: '16mm' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font:8px Arial;color:#888;width:100%;text-align:center">Journal de bord · site de Michel Gallone · page <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  });
  await navigateur.close();
  console.log('Journal généré : docs/Journal_de_bord_site_Michel_Gallone.pdf');
})();
