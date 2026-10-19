// Real desktop/mobile navigation; use isolated browser storage only.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');
const local = name => pathToFileURL(path.join(root, name)).href;
const languages = [
  { lang: 'es', label: 'Español', suffix: '-es', title: 'Estudios y actualizaciones urológicas' },
  { lang: 'en', label: 'English', suffix: '', title: 'Urological studies and updates' },
  { lang: 'de', label: 'Deutsch', suffix: '-de', title: 'Urologische Studien und Updates' }
];

(async () => {
  const channel = process.env.CME_BROWSER_CHANNEL ?? 'msedge';
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    for (const width of [1280, 390]) {
      await page.setViewportSize({ width, height: 844 });
      for (const language of languages) {
        await page.goto(local('index.html'), { waitUntil: 'domcontentloaded' });
        await page.getByRole('button', { name: language.label, exact: true }).click();
        await page.locator(`a[href="reports${language.suffix}.html"]`).waitFor();
        await page.evaluate(() => {
          localStorage.setItem('urofragen.progress.v1', '{"reportTest":"unchanged"}');
          localStorage.setItem('urofragen-clinical-review-v1', '{"reportTest":"unchanged"}');
        });
        const link = page.locator(`a[href="reports${language.suffix}.html"]`);
        assert.equal(await link.getAttribute('target'), null);
        await link.click();
        assert.equal(await page.locator('html').getAttribute('lang'), language.lang);
        assert.equal(await page.locator('nav.languages a').count(), 3);
        assert.equal(await page.locator('main .edition').count() >= 2, true);
        // Exercise the preserved reference edition, even when newer reports exist.
        const research = page.locator(`section[aria-labelledby="research"] a[href="reports/research/2026-10-17${language.suffix}.html"]`);
        await research.click();
        assert.match(await page.locator('article h1').innerText(), new RegExp(language.title));
        const report = await page.locator('article').innerText();
        for (const finding of ['LUNAR', 'SABR', 'Truqap', '71,4', '108,6']) {
          // English uses decimal dots; preserve each report's original convention.
          assert.ok(report.includes(language.lang === 'en' ? finding.replace(',', '.') : finding), finding);
        }
        assert.ok(report.includes('[Sicher]'));
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        if (width === 390 && language.lang === 'de') {
          await page.screenshot({ path: path.join(__dirname, 'reports-research-mobile.png'), fullPage: true });
        }
        for (const other of languages) {
          await page.locator(`nav.languages a[lang="${other.lang}"]`).click();
          assert.equal(await page.locator('html').getAttribute('lang'), other.lang);
          assert.match(await page.locator('article h1').innerText(), new RegExp(other.title));
        }
        await page.goto(local(`reports/maintenance/2026-10-17${language.suffix}.html`));
        assert.equal(await page.locator('article table').count() >= 3, true);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
        if (language.lang !== 'de') {
          await page.locator('article a[href$="#monitoring_state"]').click();
          assert.equal(await page.locator('html').getAttribute('lang'), 'de');
        }
        const state = JSON.parse(await page.locator('pre code.language-json').innerText());
        assert.ok(state.checked_default_sha);
        const saved = await page.evaluate(() => [localStorage.getItem('urofragen.progress.v1'), localStorage.getItem('urofragen-clinical-review-v1')]);
        assert.deepEqual(saved, ['{"reportTest":"unchanged"}', '{"reportTest":"unchanged"}']);
        if (width === 1280 && language.lang === 'de') {
          await page.goto(local('reports-de.html'));
          await page.screenshot({ path: path.join(__dirname, 'reports-archive-desktop.png'), fullPage: true });
        }
      }
    }
    assert.deepEqual(errors, []);
    await context.close();
    console.log('Native reports: homepage, ES/EN/DE, full reports, source data, audit links, desktop/mobile and stored progress passed.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
