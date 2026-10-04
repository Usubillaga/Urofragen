'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets', 'cme.js'), 'utf8');
execFileSync(process.execPath, ['--check', path.join(root, 'assets', 'cme.js')]);

const questions = [
  {n: 1, correct: 'A', axis: 'A', diff: 1, opts: {A: 'a', B: 'b'}, vignette: 'Fall 1', lead: 'Frage 1'},
  {n: 2, correct: 'B', axis: 'A', diff: 2, opts: {A: 'a', B: 'b'}, vignette: 'Fall 2', lead: 'Frage 2'},
  {n: 3, correct: 'A', axis: 'B', diff: 3, opts: {A: 'a', B: 'b'}, vignette: 'Fall 3', lead: 'Frage 3'}
];
function engine() {
  const context = {window: {}};
  vm.runInNewContext(source, context);
  return context.window.UroCme;
}
const api = engine();
const session = api.createSession(questions);
session.start();
assert.equal(session.next(), false, 'An unanswered question cannot be skipped.');
assert.equal(session.answer('Z'), false, 'Unknown options are rejected.');
assert.equal(session.answer('B'), true);
assert.equal(session.answer('A'), false, 'A shown solution cannot replace the first answer.');
session.next(); session.answer('B'); session.next(); session.answer('A'); session.next();
assert.equal(session.summary('first').right, 2);
const initialAnswers = JSON.stringify(session.snapshot().first);
assert.equal(session.retry(), true);
assert.equal(session.state().order.length, 1);
session.answer('B'); session.next();
assert.equal(session.summary('round').right, 0);
assert.equal(JSON.stringify(session.snapshot().first), initialAnswers);
assert.equal(session.retry(), true);
session.answer('A'); session.next();
assert.equal(session.summary('round').right, 1);
assert.equal(session.summary('latest').right, 3);
assert.equal(session.summary('first').right, 2, 'Repeating mistakes never raises the initial score.');
assert.equal(JSON.stringify(session.snapshot().first), initialAnswers);
assert.equal(session.retry(), false, 'No empty retry round.');
const restored = api.createSession(questions);
assert.equal(restored.restore(session.snapshot()), true);
assert.equal(restored.summary('first').right, 2);
const invalid = restored.snapshot(); invalid.order = [0, 0];
assert.equal(restored.restore(invalid), false, 'Corrupt saved state is rejected.');
const invalidAnswer = restored.snapshot(); invalidAnswer.first['999'] = 'A';
assert.equal(restored.restore(invalidAnswer), false);
const incomplete = restored.snapshot(); incomplete.round = {};
assert.equal(restored.restore(incomplete), false, 'An incomplete round cannot be restored as a result.');
restored.start();
assert.equal(restored.summary('first').answered, 0, 'An explicit new run resets the initial score.');

// Minimal DOM fixture exercises buttons, persistence, rendering and failure handling.
class Node {
  constructor(document, attrs = {}) { this.document = document; this.attrs = attrs; this.children = []; this.textContent = ''; }
  set innerHTML(html) {
    this.html = html; this.children = [];
    for (const match of html.matchAll(/<([a-z0-9]+)\b([^>]*)>/gi)) {
      const attrs = {};
      for (const attr of match[2].matchAll(/([a-z0-9-]+)="([^"]*)"/gi)) attrs[attr[1]] = attr[2];
      this.children.push(new Node(this.document, attrs));
    }
  }
  get innerHTML() { return this.html || ''; }
  getAttribute(name) { return this.attrs[name]; }
  setAttribute(name, value) { this.attrs[name] = value; }
  querySelectorAll(selector) { return this.children.filter(n => (n.attrs.class || '').split(' ').includes(selector.slice(1))); }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  focus() { this.focused = true; }
  scrollIntoView() {}
}
function environment(data, failRead = false, failWrite = false) {
  const document = {roots: []};
  document.createElement = () => new Node(document);
  document.getElementById = id => {
    for (const node of document.roots) {
      if (node.attrs.id === id) return node;
      const child = node.children.find(n => n.attrs.id === id);
      if (child) return child;
    }
    return null;
  };
  const quiz = new Node(document, {id: 'quiz'});
  quiz.parentNode = {insertBefore: node => document.roots.push(node)};
  document.roots.push(quiz);
  const writes = [];
  const window = {confirm: () => true, print: () => {}, localStorage: {
    getItem(key) { if (failRead) throw Error('denied'); return data[key] || null; },
    setItem(key, value) { if (failWrite) throw Error('quota'); data[key] = value; writes.push(key); }
  }};
  const context = {window, document};
  vm.runInNewContext(source, context);
  const config = {questions, axes: {A: 'Thema A', B: 'Thema B'}, esc: s => String(s),
    feedback: () => '<div class="fb"><p class="verdictline">Antwort</p></div>', key: 'urofragen-cme-v2:test:revision1'};
  return {document, quiz, window, writes, config, api: window.UroCme};
}
const storage = {'urofragen-clinical-review-v1': 'UNCHANGED', 'urofragen-progress': 'UNCHANGED'};
let env = environment(storage);
env.api.mount(env.config);
assert.match(env.quiz.innerHTML, /3 Fallvignetten/);
env.document.getElementById('go').onclick();
env.quiz.querySelectorAll('.opt')[1].onclick();
assert.match(env.quiz.innerHTML, /disabled/);
assert.ok(env.quiz.querySelector('.verdictline').focused, 'Feedback receives keyboard focus.');
assert.deepEqual(env.writes, [env.config.key, env.config.key]);
assert.equal(storage['urofragen-clinical-review-v1'], 'UNCHANGED');
assert.equal(storage['urofragen-progress'], 'UNCHANGED');
env = environment(storage);
env.api.mount(env.config);
assert.ok(env.document.getElementById('resume'), 'Reload offers to resume the saved run.');
env.document.getElementById('resume').onclick();
env.document.getElementById('next').onclick();
env.quiz.querySelectorAll('.opt')[1].onclick();
env.document.getElementById('next').onclick();
env.quiz.querySelectorAll('.opt')[0].onclick();
env.document.getElementById('next').onclick();
assert.match(env.quiz.innerHTML, /Erster Versuch/);
assert.match(env.quiz.innerHTML, /2 von 3 richtig \(67 %\)/);
assert.match(env.quiz.innerHTML, /Stärke in diesen Beispielen/);
assert.match(env.quiz.innerHTML, /Übungsbedarf: 1 falsch/);
env.document.getElementById('retry').onclick();
env.quiz.querySelectorAll('.opt')[0].onclick();
env.document.getElementById('next').onclick();
assert.match(env.quiz.innerHTML, /2 von 3 richtig \(67 %\)/);
assert.match(env.quiz.innerHTML, /Aktuelle Übungsrunde 2/);
assert.match(env.quiz.innerHTML, /1 von 1 richtig \(100 %\)/);
env.window.confirm = () => false;
const beforeCancel = storage[env.config.key];
env.document.getElementById('restart').onclick();
assert.equal(storage[env.config.key], beforeCancel, 'Canceling a new run preserves the saved run.');
const corrupt = environment({[env.config.key]: '{not json'});
corrupt.api.mount(corrupt.config);
assert.match(corrupt.document.roots[1].textContent, /passt nicht mehr/);
const unavailable = environment({}, true, true);
unavailable.api.mount(unavailable.config);
unavailable.document.getElementById('go').onclick();
unavailable.quiz.querySelectorAll('.opt')[0].onclick();
assert.match(unavailable.quiz.innerHTML, /disabled/);
assert.match(unavailable.document.roots[1].textContent, /kann diesen Lernstand nicht speichern/);

const names = ['cme-seminom-IIAB.html', 'cme-hodentumor-heft-teil3.html', 'cme-peniskarzinom.html', 'cme-salvage-operationen.html'];
const keys = [];
for (const name of names) {
  const html = fs.readFileSync(path.join(root, name), 'utf8');
  const original = fs.readFileSync(path.join(root, 'updates', '2026-10-04', 'cme-originals', name), 'utf8');
  const dataMatch = /var DATA = (.*?);\s*\n/s;
  assert.equal(html.match(dataMatch)[1], original.match(dataMatch)[1], name + ': source DATA is unchanged.');
  const inlineScript = html.match(/<script>([\s\S]*?)<\/script>/)[1];
  execFileSync(process.execPath, ['--check'], {input: inlineScript});
  keys.push(html.match(/key: "([^"]+)"/)[1]);
  assert.match(html, /<script src="assets\/cme\.js"><\/script>/);
  assert.match(html, /href="assets\/cme\.css"/);
  for (const target of ['index.html', 'pruefung.html', ...names]) {
    assert.ok(html.includes('href="' + target + '"'), name + ': navigation to ' + target);
  }
  assert.equal((html.match(/aria-current="page"/g) || []).length, 1);
}
assert.equal(new Set(keys).size, 4, 'Every module uses a distinct revision-specific storage key.');
console.log('CME-Prüfungen bestanden: Erstquote, Wiederholungen, Fortsetzen, Speicherfehler, Navigation, unveränderte Inhalte und JavaScript-Syntax.');
