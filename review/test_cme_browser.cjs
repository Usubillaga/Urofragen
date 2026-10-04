// Uses a fresh browser context; does not touch the user's real browser data.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');
const modules = ['cme-seminom-IIAB.html', 'cme-hodentumor-heft-teil3.html', 'cme-peniskarzinom.html', 'cme-salvage-operationen.html'];
const local = name => pathToFileURL(path.join(root, name)).href;

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    await page.route('https://fonts.googleapis.com/**', route => route.abort());
    await page.route('https://fonts.gstatic.com/**', route => route.abort());
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(local('index.html'), { waitUntil: 'domcontentloaded' });
    await page.locator('.cme-card').first().waitFor();
    assert.equal(await page.locator('.cme-card').count(), 4);
    await page.getByRole('button', { name: 'Español', exact: true }).click();
    await page.getByText('Alemán, inglés y español', { exact: false }).waitFor();
    for (const filename of modules) {
      await page.goto(local(filename) + '?lang=de', { waitUntil: 'domcontentloaded' });
      await page.locator('#go').waitFor();
      assert.equal(await page.locator('.cme-nav a').count(), 6);
      assert.equal(await page.locator('.cme-nav a[aria-current="page"]').count(), 1);
      const questions = await page.evaluate(() => DATA.questions.map(q => ({ n: q.n, correct: q.correct, opts: Object.keys(q.opts) })));
      const count = questions.length;
      assert.match(await page.locator('#quiz').innerText(), new RegExp(`${count} Fallvignetten`));
      await page.setViewportSize({ width: 390, height: 844 });
      await page.screenshot({ path: path.join(__dirname, filename.replace('.html', '-header-mobile.png')), fullPage: false });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.setViewportSize({ width: 1280, height: 900 });
      await page.evaluate(() => {
        localStorage.setItem('urofragen.progress.v1', '{"test":"unchanged"}');
        localStorage.setItem('urofragen-clinical-review-v1', '{"test":"unchanged"}');
      });
      await page.locator('#go').click();
      const wrong = questions[0].opts.find(x => x !== questions[0].correct);
      await page.locator(`.opt[data-k="${wrong}"]`).click();
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.locator('#resume').click();
      assert.equal(await page.locator('.opt:disabled').count(), 5);
      await page.locator('#next').click();
      for (let i = 1; i < count; i++) {
        await page.locator(`.opt[data-k="${questions[i].correct}"]`).click();
        await page.locator('#next').click();
      }
      await page.locator('.cme-result-title').waitFor();
      const firstScore = await page.locator('.score').first().innerText();
      assert.match(firstScore, new RegExp(`${count - 1} von ${count} richtig`));
      assert.match(await page.locator('#quiz').innerText(), /Übungsbedarf: 1 falsch/);
      assert.match(await page.locator('#quiz').innerText(), /Stärke in diesen Beispielen/);
      await page.locator('#retry').click();
      await page.locator(`.opt[data-k="${questions[0].correct}"]`).click();
      await page.locator('#next').click();
      assert.equal(await page.locator('.score').first().innerText(), firstScore);
      assert.equal(await page.locator('.score').nth(1).innerText(), '1 von 1 richtig (100 %)');
      assert.equal(await page.locator('#retry').count(), 0);
      assert.match(await page.locator('#quiz').innerText(), /Aktueller Lernstand: 0/);
      assert.deepEqual(await page.evaluate(() => ['urofragen.progress.v1', 'urofragen-clinical-review-v1'].map(k => localStorage.getItem(k))), ['{"test":"unchanged"}', '{"test":"unchanged"}']);
      await page.screenshot({ path: path.join(__dirname, filename.replace('.html', '-result-desktop.png')), fullPage: false });
      await page.setViewportSize({ width: 390, height: 844 });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.locator('#quiz').screenshot({ path: path.join(__dirname, filename.replace('.html', '-result-mobile.png')) });
      page.once('dialog', d => d.dismiss());
      await page.locator('#restart').click();
      assert.equal(await page.locator('.score').first().innerText(), firstScore);
      page.once('dialog', d => d.accept());
      await page.locator('#restart').click();
      assert.match(await page.locator('.qhead').innerText(), /Erster Durchgang · Frage 1/);
      assert.equal(await page.locator('.opt:not(:disabled)').count(), 5);
      await page.setViewportSize({ width: 1280, height: 900 });
      console.log(`${filename}: start, resume, first score, retry, topic feedback, storage isolation, restart and mobile layout passed`);
    }
    assert.deepEqual(errors, []);
    const blocked = await browser.newContext();
    await blocked.addInitScript(() => { Storage.prototype.setItem = function () { throw new Error('TEST: storage unavailable'); }; });
    const blockedPage = await blocked.newPage();
    await blockedPage.goto(local(modules[0]), { waitUntil: 'domcontentloaded' });
    await blockedPage.locator('#go').click();
    assert.match(await blockedPage.locator('.cme-storage').innerText(), /kann diesen Lernstand nicht speichern/);
    await blockedPage.locator('.opt').first().click();
    assert.equal(await blockedPage.locator('#next').count(), 1);
    console.log('Storage failure: warning displayed and quiz remains usable; no browser JavaScript errors');
    await blocked.close();
    await context.close();
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
