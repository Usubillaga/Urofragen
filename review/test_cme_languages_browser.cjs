// Fresh contexts only: no real learner data or clinical decisions are modified.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const modules = ['cme-seminom-IIAB', 'cme-hodentumor-heft-teil3', 'cme-peniskarzinom', 'cme-salvage-operationen'];
const local = name => pathToFileURL(path.join(root, name)).href;
const dictionary = (module, lc) => JSON.parse(fs.readFileSync(path.join(root, 'translations', `${module}.${lc}.json`), 'utf8'));

async function switchTo(page, lc) {
  await Promise.all([page.waitForURL(url => url.searchParams.get('lang') === lc), page.locator(`.cme-language button[data-language="${lc}"]`).click()]);
  await page.locator(`.cme-language button[data-language="${lc}"][aria-pressed="true"]`).waitFor();
  assert.equal(await page.locator('html').getAttribute('lang'), lc);
}

(async () => {
  // Edge by default; CME_BROWSER_CHANNEL= (empty) uses Playwright's bundled Chromium, e.g. in CI.
  const channel = process.env.CME_BROWSER_CHANNEL ?? 'msedge';
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    await page.route('https://fonts.googleapis.com/**', route => route.abort());
    await page.route('https://fonts.gstatic.com/**', route => route.abort());
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(local('index.html') + '?lang=es', { waitUntil: 'domcontentloaded' });
    await page.locator('.cme-card').first().waitFor();
    assert.match(await page.locator('.cme-card').first().getAttribute('href'), /\?lang=es$/);
    for (const module of modules) {
      const en = dictionary(module, 'en'), es = dictionary(module, 'es');
      await page.goto(local(module + '.html') + '?lang=de', { waitUntil: 'domcontentloaded' });
      await page.locator('#go').waitFor();
      const german = await page.evaluate(() => CME_BASE_DATA);
      const count = german.questions.length;
      await page.locator('#go').click();
      const wrong = Object.keys(german.questions[0].opts).find(k => k !== german.questions[0].correct);
      await page.locator(`.opt[data-k="${wrong}"]`).click();
      const before = await page.evaluate(() => Object.fromEntries(Object.keys(localStorage).filter(k => k.startsWith('urofragen-cme-v2:')).map(k => [k, JSON.parse(localStorage.getItem(k)).first])));
      await switchTo(page, 'en');
      assert.equal(await page.locator('#quiz .lead').innerText(), en.questions[0].lead);
      assert.equal(await page.locator('.opt:disabled').count(), 5);
      assert.match(await page.locator('#quiz .verdictline').innerText(), /Incorrect/);
      assert.equal(await page.locator('#printall .verdictline').count(), 0);
      assert.equal(await page.locator('#next').innerText(), 'Next question');
      for (let i = 0; i < count; i++) {
        assert.equal(await page.locator('#printall .pq .vignette').nth(i).innerText(), en.questions[i].vignette);
        assert.equal(await page.locator('#printall .pq .lead').nth(i).innerText(), en.questions[i].lead);
      }
      await page.setViewportSize({ width: 390, height: 844 });
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({ path: path.join(__dirname, `${module}-en-header-mobile.png`), fullPage: false });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.setViewportSize({ width: 1280, height: 900 });
      await page.locator('#next').click();
      await page.locator(`.opt[data-k="${en.questions[1].correct}"]`).click();
      await switchTo(page, 'es');
      assert.equal(await page.locator('#quiz .lead').innerText(), es.questions[1].lead);
      assert.equal(await page.locator('.opt:disabled').count(), 5);
      assert.equal(await page.locator('#quiz .verdictline').innerText(), 'Correcto.');
      const after = await page.evaluate(() => Object.fromEntries(Object.keys(localStorage).filter(k => k.startsWith('urofragen-cme-v2:')).map(k => [k, JSON.parse(localStorage.getItem(k)).first])));
      for (const [key, attempts] of Object.entries(before)) for (const [n, option] of Object.entries(attempts)) assert.equal(after[key][n], option);
      assert.equal(Object.keys(after).length, Object.keys(before).length, 'Switching language does not create a separate scored run.');
      for (let i = 0; i < count; i++) {
        assert.equal(await page.locator('#printall .pq .vignette').nth(i).innerText(), es.questions[i].vignette);
        assert.equal(await page.locator('#printall .pq .lead').nth(i).innerText(), es.questions[i].lead);
      }
      // Interactive helpers must use the selected language, including after an input event.
      if (await page.locator('#hcCauses .seg').count()) {
        for (let i = 0; i < es.hcg.length; i++) {
          assert.equal(await page.locator('#hcCauses .seg').nth(i).innerText(), es.hcg[i].label);
          await page.locator('#hcCauses .seg').nth(i).click();
          const helperText = await page.locator('#hcOut li p').first().evaluate(node => { const copy = node.cloneNode(true); copy.querySelectorAll('.pv').forEach(span => span.remove()); return copy.textContent.replace(/\s+/g, ' ').trim(); });
          assert.equal(helperText, es.hcg[i].mech.replace(/\[(?:Q|X|LL [^\]]+)\]/g, '').replace(/\s+/g, ' ').trim());
        }
        await page.locator('#rpCrit input').first().check();
        assert.ok((await page.locator('#rpOut').innerText()).includes(es.rplnd.verdicts.open.title));
      } else {
        await page.locator('#size').evaluate(input => { input.value = '4.1'; input.dispatchEvent(new Event('input', { bubbles: true })); });
        assert.match(await page.locator('#verdict').innerText(), /Estadio|estadio/);
        await page.locator('#supra').check();
        assert.doesNotMatch(await page.locator('#verdict').innerText(), /Kein Stadium|Chemotherapie nach/);
      }
      await page.locator('#next').click();
      for (let i = 2; i < count; i++) {
        await page.locator(`.opt[data-k="${es.questions[i].correct}"]`).click();
        await page.locator('#next').click();
      }
      await page.locator('.cme-result-title').waitFor();
      assert.equal(await page.locator('.cme-score-label').first().innerText(), 'Primer intento');
      const first = await page.locator('.score').first().innerText();
      assert.match(first, new RegExp(`${count - 1} de ${count} correctas`));
      await page.locator('#retry').click();
      await page.locator(`.opt[data-k="${es.questions[0].correct}"]`).click();
      await page.locator('#next').click();
      assert.equal(await page.locator('.score').first().innerText(), first);
      assert.equal(await page.locator('.score').nth(1).innerText(), '1 de 1 correcta (100 %)');
      await page.setViewportSize({ width: 390, height: 844 });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.locator('#quiz').screenshot({ path: path.join(__dirname, `${module}-es-result-mobile.png`) });
      await switchTo(page, 'en');
      assert.equal(await page.locator('.cme-score-label').first().innerText(), 'First attempt');
      assert.match(await page.locator('.score').first().innerText(), new RegExp(`${count - 1} of ${count} correct`));
      assert.equal(await page.locator('.score').nth(1).innerText(), '1 of 1 correct (100 %)');
      await page.setViewportSize({ width: 1280, height: 900 });
      console.log(`${module}: complete EN/ES print content, DE→EN→ES continuation, first-score preservation, translated helpers/results and mobile layout passed`);
    }
    assert.deepEqual(errors, []);
    await context.close();
    console.log('All multilingual CME browser checks passed; no JavaScript runtime errors.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
