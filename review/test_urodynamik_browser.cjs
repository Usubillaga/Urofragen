// Urodynamik: the tracings in the learning page and the review page (all 19 questions, DE/EN/ES, desktop and phone).
// Uses a fresh browser context; does not touch the user's real browser data. URODYNAMIK_SHOTS=<folder> saves screenshots.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');
const local = name => pathToFileURL(path.join(root, name)).href;
const shots = process.env.URODYNAMIK_SHOTS;
const shot = async (page, name) => { if (shots) await page.screenshot({ path: path.join(shots, name), fullPage: true }); };
// Mirrors limitOf() of the renderer: parts that answer a later step stay hidden until it is answered.
const limitOf = (tr, reveal) => Math.min(Infinity, ...(tr.conceal || []).filter(c => !reveal.includes(c.until)).map(c => c.from));
const findingsAfter = (tr, q) => tr.annotations.filter(a => q.tracing.after.includes(a.step));
const noSidewaysScroll = page => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);

(async () => {
  // Edge by default; CME_BROWSER_CHANNEL= (empty) uses Playwright's bundled Chromium, e.g. in CI.
  const channel = process.env.CME_BROWSER_CHANNEL ?? 'msedge';
  const browser = await chromium.launch({ ...(channel ? { channel } : {}), headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, acceptDownloads: true });
    await context.route('https://fonts.googleapis.com/**', route => route.abort());
    await context.route('https://fonts.gstatic.com/**', route => route.abort());
    // The adaptive selection is replaced by all questions of the section in a fixed order.
    await context.addInitScript(() => {
      const all = qs => qs.filter(q => q.taxonomy.domain === 'urodynamik').sort((a, b) => (a.id < b.id ? -1 : 1));
      Object.defineProperty(window, 'selectLearningQuestions', { configurable: true, get: () => all, set: () => {} });
    });
    const errors = [];
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    page.on('pageerror', e => errors.push('index.html: ' + e.message));
    await page.goto(local('index.html') + '?lang=de', { waitUntil: 'domcontentloaded' });
    const { questions, tracings } = await page.evaluate(() => ({
      questions: window.QUESTION_BANK.questions.filter(q => q.taxonomy.domain === 'urodynamik'),
      tracings: window.QUESTION_BANK.tracings
    }));
    assert.equal(questions.length, 19);
    assert.equal(Object.keys(tracings).length, 19);
    assert.ok(questions.every(q => tracings[q.tracing.case]), 'every question has its tracing');
    assert.ok(Object.values(tracings).every(tr => !('readings' in tr)), 'the page carries no pinned readings');
    // The learning page names granted approvals only: no counter and no "pending" line.
    assert.equal(await page.getByText(/Fachärztlich freigegeben|Freigabe ausstehend/).count(), 0);
    const start = async () => page.locator('button.domain', { has: page.locator('.domain-name', { hasText: /^(Urodynamik|Urodynamics|Urodinámica)$/ }) }).click();
    await start();

    for (const [i, q] of questions.entries()) {
      const tr = tracings[q.tracing.case], before = page.locator('.card .case-tracing .udy');
      await before.waitFor();
      assert.equal(await before.getAttribute('data-view'), q.tracing.view, q.id + ' opens on its section');
      assert.equal(await page.locator('.card .udy-findings').count(), 0, q.id + ': no findings before the answer');
      const end = Number(await before.locator('svg').getAttribute('data-t1'));
      assert.ok(end <= limitOf(tr, []), q.id + ': a part that gives the answer away is hidden');
      assert.equal(await before.locator('svg').getAttribute('viewBox').then(v => v.split(' ')[2]), '760', q.id + ' uses the medium layout');
      // Order: vignette, tracing, lead-in, options.
      assert.deepEqual(await page.locator('.card > *').evaluateAll(n => n.slice(0, 4).map(e => e.className)), ['vignette', 'case-tracing', 'lead-in', 'options']);
      // The cursor reads every channel at the clicked moment.
      const box = await before.locator('.udy-svg').boundingBox();
      await page.mouse.click(box.x + box.width * 0.62, box.y + box.height * 0.45);
      assert.match(await before.locator('.udy-readout').innerText(), /^Zeit \d+:\d\d/);
      if (i === 0) await shot(page, 'urodynamik-frage-vorher.png');
      const correct = q.options.find(o => o.correct).key;
      await page.locator('.card button.option', { hasText: q.content.de.options[correct].text }).click();
      const after = page.locator('.card .case-tracing .udy');
      await after.locator('.udy-findings li').first().waitFor();
      const expected = findingsAfter(tr, q);
      assert.equal(await after.locator('.udy-findings li').count(), expected.length, q.id + ': findings after the answer');
      assert.deepEqual(await after.locator('.udy-findings li').allInnerTexts(), expected.map(a => a.label.de));
      assert.equal(await after.getAttribute('data-view'), q.tracing.view_after || q.tracing.view);
      if (q.tracing.view_after) assert.ok(Number(await after.locator('svg').getAttribute('data-t1')) > end, q.id + ': the hidden part appears after the answer');
      assert.equal(await page.locator('.option.is-correct').count(), 1);
      assert.doesNotMatch(await page.locator('.explain').innerText(), /Freigabe ausstehend/);
      // Section buttons redraw the plot in place and keep the findings.
      const views = after.locator('.udy-view');
      if (await views.count() > 1) {
        const last = views.last();
        await last.click();
        assert.equal(await last.getAttribute('aria-pressed'), 'true');
        assert.equal(await after.locator('.udy-findings li').count(), expected.length);
      }
      if (i === 0) await shot(page, 'urodynamik-frage-nachher.png');
      await page.locator('.explain .actions .btn').filter({ hasText: i === questions.length - 1 ? 'Auswertung ansehen' : 'Nächste Frage' }).click();
    }

    // The result sheet carries every tracing with its findings, without controls.
    await page.locator('.score').waitFor();
    const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Als Datei speichern' }).click()]);
    const sheet = fs.readFileSync(await download.path(), 'utf8');
    assert.equal((sheet.match(/<figure class="trace">/g) || []).length, 19);
    assert.equal((sheet.match(/class="q has-trace"/g) || []).length, 19);
    assert.ok(!/udy-views|udy-readout/.test(sheet), 'the sheet has no buttons or readout');
    assert.ok(!/Freigabe ausstehend/.test(sheet), 'the sheet names no pending approval');
    for (const q of questions) for (const a of findingsAfter(tracings[q.tracing.case], q)) {
      const label = a.label.de.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      assert.ok(sheet.includes('<li>' + label + '</li>'), q.id + ': the sheet lists ' + a.label.de);
    }

    // Phone: the narrow layout, no sideways scrolling; back to desktop redraws the medium layout.
    await page.getByRole('button', { name: 'Zur Übersicht' }).click();
    await page.setViewportSize({ width: 390, height: 844 });
    await start();
    const phone = page.locator('.card .case-tracing .udy');
    await phone.waitFor();
    assert.equal((await phone.locator('svg').getAttribute('viewBox')).split(' ')[2], '560');
    assert.equal(await noSidewaysScroll(page), true, 'no sideways scrolling at 390 px');
    await shot(page, 'urodynamik-frage-telefon.png');
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.waitForFunction(() => document.querySelector('.udy-svg').getAttribute('viewBox').split(' ')[2] === '760');

    // English and Spanish: captions, markers and hints follow the language switch.
    for (const [name, lc, hint] of [['English', 'en', /^Tap or drag/], ['Español', 'es', /^Toca o arrastra/]]) {
      await page.getByRole('button', { name, exact: true }).click();
      const fig = page.locator('.card .case-tracing .udy');
      await fig.waitFor();
      assert.match(await fig.locator('.udy-hint').innerText(), hint);
      const q = questions[0];
      assert.equal(await page.locator('.card .vignette').innerText(), q.content[lc].vignette);
    }

    // Review page: the tracing as before the answer, then with its findings.
    const review = await context.newPage();
    review.setDefaultTimeout(10000);
    review.on('pageerror', e => errors.push('pruefung.html: ' + e.message));
    await review.goto(local('pruefung.html'), { waitUntil: 'domcontentloaded' });
    await review.selectOption('#domain', 'urodynamik');
    for (const [i, q] of questions.entries()) {
      const tr = tracings[q.tracing.case];
      await review.locator('#question p.muted', { hasText: q.id }).waitFor();
      const fig = review.locator('#question .case-tracing .udy');
      assert.equal(await fig.getAttribute('data-view'), q.tracing.view);
      assert.equal(await review.locator('#question .udy-findings').count(), 0, q.id + ': review page opens as before the answer');
      await review.getByRole('button', { name: 'Nach der Antwort, mit Befunden' }).click();
      assert.equal(await review.locator('#question .udy-findings li').count(), findingsAfter(tr, q).length);
      assert.equal(await review.getByRole('button', { name: 'Nach der Antwort, mit Befunden' }).getAttribute('aria-pressed'), 'true');
      if (i === 15) await shot(review, 'urodynamik-pruefung.png');
      await review.getByRole('button', { name: 'Wie vor der Antwort' }).click();
      assert.equal(await review.locator('#question .udy-findings').count(), 0);
      if (i < questions.length - 1) await review.click('#next');
    }
    await review.setViewportSize({ width: 390, height: 844 });
    assert.equal(await noSidewaysScroll(review), true, 'review page: no sideways scrolling at 390 px');

    assert.deepEqual(errors, []);
    console.log('Urodynamik-Kurven: 19 Fragen im Lernmodus (DE, EN, ES, Desktop und Telefon), im Ergebnisblatt und im Prüfmodus geprüft.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
