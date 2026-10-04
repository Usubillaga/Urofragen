(function (global) {
  'use strict';

  var commonDictionary = {"Urofragen und Lernmodule": {"en": "Urofragen and learning modules", "es": "Urofragen y módulos de aprendizaje"}, "← Urofragen": {"en": "← Urofragen", "es": "← Urofragen"}, "Fragen fachlich prüfen": {"en": "Clinical question review", "es": "Revisión clínica de preguntas"}, "Seminom IIA/B": {"en": "Stage IIA/B seminoma", "es": "Seminoma IIA/B"}, "Hodentumor, Teil 3": {"en": "Testicular cancer, part 3", "es": "Cáncer testicular, parte 3"}, "Peniskarzinom": {"en": "Penile cancer", "es": "Cáncer de pene"}, "Salvage-Operationen": {"en": "Salvage surgery", "es": "Cirugía de rescate"}, "Importiertes Lernmodul auf Deutsch. Quellenhinweise stammen aus der bereitgestellten Datei; eine fachärztliche Freigabe dieses Moduls ist hier noch nicht dokumentiert.": {"en": "Translated learning module. Source annotations come from the supplied file; clinical approval of this module has not yet been documented here.", "es": "Módulo de aprendizaje traducido. Las indicaciones sobre las fuentes proceden del archivo proporcionado; aún no se ha documentado aquí la aprobación clínica de este módulo."}, "Der Browser kann diesen Lernstand nicht speichern. Du kannst weiter üben; beim Schließen geht der aktuelle Stand verloren.": {"en": "The browser cannot save this progress. You can keep practising; the current progress will be lost when you close the page.", "es": "El navegador no puede guardar este progreso. Puedes seguir practicando; el progreso actual se perderá al cerrar la página."}, "Der gespeicherte Stand passt nicht mehr zu diesem Modul. Bitte beginne einen neuen Durchgang. ": {"en": "The saved progress no longer matches this module. Please start a new run. ", "es": "El progreso guardado ya no corresponde a este módulo. Inicia una nueva sesión. "}, "Der Lernstand wird nur in diesem Browser gespeichert. Die CME-Auswertung ist vom allgemeinen Lernprofil getrennt.": {"en": "Progress is saved only in this browser. CME results are separate from the main learning profile.", "es": "El progreso se guarda únicamente en este navegador. Los resultados CME son independientes del perfil de aprendizaje principal."}, "Ein neuer Durchgang löscht die bisherigen Antworten und die Erstquote dieses CME-Moduls. Neu beginnen?": {"en": "A new run deletes the previous answers and the first-attempt score for this CME module. Start again?", "es": "Una nueva sesión borra las respuestas anteriores y la puntuación del primer intento de este módulo CME. ¿Volver a empezar?"}, " von ": {"en": " of ", "es": " de "}, "scoreOne": {"de": "{right} von {total} richtig ({percent} %)", "en": "{right} of {total} correct ({percent} %)", "es": "{right} de {total} correcta ({percent} %)"}, "scoreMany": {"de": "{right} von {total} richtig ({percent} %)", "en": "{right} of {total} correct ({percent} %)", "es": "{right} de {total} correctas ({percent} %)"}, "weakOne": {"de": "Übungsbedarf: {n} falsch", "en": "Needs practice: {n} incorrect", "es": "Necesita práctica: {n} incorrecta"}, "weakMany": {"de": "Übungsbedarf: {n} falsch", "en": "Needs practice: {n} incorrect", "es": "Necesita práctica: {n} incorrectas"}, " richtig (": {"en": " correct (", "es": " correctas ("}, "Auswertung": {"en": "Results", "es": "Resultados"}, "Erster Versuch": {"en": "First attempt", "es": "Primer intento"}, "Die Erstquote bleibt bei Fehlerwiederholungen erhalten. Ein neuer Durchgang setzt sie zurück.": {"en": "The first-attempt score is preserved when you retry mistakes. Starting a new run resets it.", "es": "La puntuación del primer intento se conserva al repetir los errores. Una nueva sesión la reinicia."}, "Aktuelle Übungsrunde ": {"en": "Current practice round ", "es": "Ronda de práctica actual "}, "Stärken und Übungsbedarf im ersten Versuch": {"en": "Strengths and practice needs on the first attempt", "es": "Fortalezas y necesidades de práctica en el primer intento"}, "Je Thema gibt es nur wenige Fragen, häufig ein oder zwei. Die Rückmeldung beschreibt diese Beispiele und erlaubt noch keine belastbare Aussage über deine gesamte Kompetenz.": {"en": "Each topic contains only a few questions, often one or two. This feedback describes these examples and cannot reliably assess your overall competence.", "es": "Cada tema contiene pocas preguntas, a menudo una o dos. Esta valoración describe estos ejemplos y no permite evaluar de forma fiable tu competencia global."}, "Noch nicht vollständig beantwortet": {"en": "Not yet fully answered", "es": "Aún no se ha completado"}, "Stärke in diesen Beispielen": {"en": "Strength in these examples", "es": "Fortaleza en estos ejemplos"}, "Übungsbedarf: ": {"en": "Needs practice: ", "es": "Necesita práctica: "}, " falsch": {"en": " incorrect", "es": " incorrectas"}, "Gelungen:": {"en": "Well answered:", "es": "Respuestas acertadas:"}, "Weiter üben:": {"en": "Keep practising:", "es": "Sigue practicando:"}, ". Die Merkkästen stehen nach der letzten Frage des jeweiligen Themas.": {"en": ". Key-point summaries appear after the last question in each topic.", "es": ". Los cuadros de puntos clave aparecen después de la última pregunta de cada tema."}, "Erster Versuch nach Schwierigkeit": {"en": "First attempt by difficulty", "es": "Primer intento según dificultad"}, "Schwierigkeit ": {"en": "Difficulty ", "es": "Dificultad "}, "currentWrong": {"de": "Aktueller Lernstand: {n} zuletzt falsch beantwortete Fragen.", "en": "Current progress: {n} questions most recently answered incorrectly.", "es": "Progreso actual: {n} preguntas cuya última respuesta fue incorrecta."}, "currentWrongOne": {"de": "Aktueller Lernstand: 1 zuletzt falsch beantwortete Frage.", "en": "Current progress: 1 question most recently answered incorrectly.", "es": "Progreso actual: 1 pregunta cuya última respuesta fue incorrecta."}, "Fehler üben (": {"en": "Practise mistakes (", "es": "Practicar los errores ("}, "Neuen Durchgang beginnen": {"en": "Start a new run", "es": "Iniciar una nueva sesión"}, "Druckfassung": {"en": "Print version", "es": "Versión para imprimir"}, " Fallvignetten, je fünf Antwortoptionen, eine beste Antwort. Nach jeder Antwort folgen Kernaussage, Evidenz mit Herkunftsmarkern, Analyse aller Distraktoren und Praxiskonsequenz.": {"en": " clinical scenarios, each with five options and one best answer. Every answer is followed by the key message, evidence with source markers, analysis of all distractors and clinical implications.", "es": " casos clínicos, cada uno con cinco opciones y una mejor respuesta. Después de cada respuesta se presentan el mensaje clave, la evidencia con marcadores de origen, el análisis de todos los distractores y las implicaciones prácticas."}, "Gespeicherter Durchgang: ": {"en": "Saved run: ", "es": "Sesión guardada: "}, " Fragen im ersten Versuch beantwortet, davon ": {"en": " questions answered on the first attempt; ", "es": " preguntas respondidas en el primer intento; "}, " richtig.": {"en": " correct.", "es": " correctas."}, "Fortsetzen": {"en": "Continue", "es": "Continuar"}, "Neu beginnen": {"en": "Start again", "es": "Volver a empezar"}, "Fragen beginnen": {"en": "Start questions", "es": "Empezar las preguntas"}, "Erster Durchgang": {"en": "First run", "es": "Primera sesión"}, "Übungsrunde ": {"en": "Practice round ", "es": "Ronda de práctica "}, " · Frage ": {"en": " · Question ", "es": " · Pregunta "}, " von 3": {"en": " of 3", "es": " de 3"}, "⚠ Evidenz begrenzt": {"en": "⚠ Limited evidence", "es": "⚠ Evidencia limitada"}, "Zurück": {"en": "Back", "es": "Atrás"}, "Auswertung ansehen": {"en": "View results", "es": "Ver resultados"}, "Nächste Frage": {"en": "Next question", "es": "Siguiente pregunta"}, "Richtig.": {"en": "Correct.", "es": "Correcto."}, "Nicht richtig. Richtig ist ": {"en": "Incorrect. The correct answer is ", "es": "Incorrecto. La respuesta correcta es "}, "Kernaussage": {"en": "Key message", "es": "Mensaje clave"}, "Evidenz": {"en": "Evidence", "es": "Evidencia"}, "Distraktoren": {"en": "Distractors", "es": "Distractores"}, "Praxiskonsequenz": {"en": "Clinical implications", "es": "Implicaciones prácticas"}, "Lernziel: ": {"en": "Learning objective: ", "es": "Objetivo de aprendizaje: "}, "Referenz: ": {"en": "Reference: ", "es": "Referencia: "}, "Merkkasten ": {"en": "Key points ", "es": "Puntos clave "}, "Alle Fragen mit Lösung und Begründung": {"en": "All questions with answers and explanations", "es": "Todas las preguntas con respuestas y explicaciones"}, "Frage ": {"en": "Question ", "es": "Pregunta "}, ", Schwierigkeit ": {"en": ", difficulty ", "es": ", dificultad "}, " (richtig)": {"en": " (correct)", "es": " (correcta)"}, "Steht so im Quellartikel": {"en": "As stated in the source article", "es": "Tal como figura en el artículo original"}, "Eigene Einordnung ohne direkten Beleg": {"en": "Interpretation without direct supporting evidence", "es": "Interpretación sin respaldo directo"}, "Leitlinie im Volltext geprüft": {"en": "Full guideline text checked in the supplied source", "es": "Texto completo de la guía comprobado según la fuente proporcionada"}, "Standard": {"en": "Standard", "es": "Estándar"}, "Standard, nachrangig": {"en": "Standard, lower priority", "es": "Estándar, segunda opción"}, "Option mit Bedingungen": {"en": "Conditional option", "es": "Opción condicionada"}, "Abwarten": {"en": "Observe", "es": "Observación"}, "Nicht indiziert": {"en": "Not indicated", "es": "No indicado"}};
  var LANGUAGE_KEY = 'urofragen.lang.v1';
  function readLanguage() {
    var preferred = null;
    try { preferred = new URLSearchParams(global.location.search).get('lang'); } catch (_) {}
    if (['de', 'en', 'es'].indexOf(preferred) >= 0) return preferred;
    try { preferred = global.localStorage.getItem(LANGUAGE_KEY); } catch (_) {}
    if (['de', 'en', 'es'].indexOf(preferred) >= 0) return preferred;
    preferred = ((global.navigator && global.navigator.language) || 'de').slice(0, 2);
    return ['de', 'en', 'es'].indexOf(preferred) >= 0 ? preferred : 'de';
  }
  var language = readLanguage(), dictionary = Object.assign({}, commonDictionary, (global.CME_I18N || {}).ui || {});
  var terms = Object.keys(dictionary).filter(function (key) { return key.length; }).sort(function (a, b) { return b.length - a.length; });
  var pattern = terms.length ? new RegExp(terms.map(function (key) { return key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|'), 'g') : null;
  function cmeText(text, values) {
    var entry = dictionary[text];
    var output = entry ? (entry[language] || text) : language === 'de' || !pattern ? text :
      text.replace(pattern, function (key) { return dictionary[key][language] || key; });
    if (values) Object.keys(values).forEach(function (key) { output = output.split('{' + key + '}').join(String(values[key])); });
    return output;
  }
  function initialize(german) {
    var translated = language === 'de' ? german : ((global.CME_I18N || {}).data || {})[language];
    if (!translated) throw new Error('Missing CME translation: ' + language);
    document.documentElement.lang = language;
    var walker = document.createTreeWalker(document.documentElement, 4), node;
    while ((node = walker.nextNode())) {
      if (node.parentElement && !node.parentElement.closest('script, style')) node.nodeValue = cmeText(node.nodeValue);
    }
    Array.prototype.forEach.call(document.querySelectorAll('[aria-label], [title], [alt]'), function (element) {
      ['aria-label', 'title', 'alt'].forEach(function (name) { if (element.hasAttribute(name)) element.setAttribute(name, cmeText(element.getAttribute(name))); });
    });
    var nav = document.querySelector('.cme-nav');
    if (nav) {
      var switcher = document.createElement('div'); switcher.className = 'cme-language';
      switcher.setAttribute('role', 'group'); switcher.setAttribute('aria-label', {de:'Sprache',en:'Language',es:'Idioma'}[language]);
      ['de', 'en', 'es'].forEach(function (code) {
        var button = document.createElement('button'); button.type = 'button'; button.textContent = code.toUpperCase();
        button.dataset.language = code; button.setAttribute('aria-label', {de:'Deutsch',en:'English',es:'Español'}[code]);
        button.setAttribute('aria-pressed', String(code === language));
        button.onclick = function () {
          if (code === language) return;
          try { global.localStorage.setItem(LANGUAGE_KEY, code); } catch (_) {}
          var destination = new URL(global.location.href); destination.searchParams.set('lang', code); destination.searchParams.set('continue', '1');
          global.location.assign(destination.href);
        };
        switcher.appendChild(button);
      });
      nav.insertBefore(switcher, nav.firstChild);
      Array.prototype.forEach.call(nav.querySelectorAll('a'), function (link) {
        var href = link.getAttribute('href');
        if (/^(cme-[^?]+|index\.html)$/.test(href)) link.setAttribute('href', href + '?lang=' + language);
      });
    }
    return translated;
  }
  function number(value, digits) { return Number(value).toLocaleString(language, {minimumFractionDigits: digits, maximumFractionDigits: digits}); }

  function own(object, key) { return Object.prototype.hasOwnProperty.call(object, key); }
  function copy(value) { return JSON.parse(JSON.stringify(value)); }

  function createSession(questions) {
    var byNumber = Object.create(null);
    questions.forEach(function (q) { byNumber[String(q.n)] = q; });
    function fresh() {
      return {schema: 2, order: questions.map(function (_, i) { return i; }), pos: 0,
        ans: {}, first: {}, round: {}, roundType: 'first', roundNumber: 1, mode: 'start'};
    }
    var state = fresh();
    function validAnswers(answers) {
      return answers && typeof answers === 'object' && !Array.isArray(answers) &&
        Object.keys(answers).every(function (number) {
          return own(byNumber, number) && typeof answers[number] === 'string' &&
            own(byNumber[number].opts, answers[number]);
        });
    }
    function validate(candidate) {
      if (!candidate || candidate.schema !== 2 || !Array.isArray(candidate.order) || !candidate.order.length ||
          candidate.order.some(function (i) { return !Number.isInteger(i) || i < 0 || i >= questions.length; }) ||
          new Set(candidate.order).size !== candidate.order.length ||
          !Number.isInteger(candidate.pos) || candidate.pos < 0 || candidate.pos >= candidate.order.length ||
          ['start', 'q', 'result'].indexOf(candidate.mode) < 0 ||
          ['first', 'retry'].indexOf(candidate.roundType) < 0 ||
          !Number.isInteger(candidate.roundNumber) || candidate.roundNumber < 1 ||
          !validAnswers(candidate.ans) || !validAnswers(candidate.first) || !validAnswers(candidate.round)) return false;
      if (candidate.roundType === 'first' && (candidate.roundNumber !== 1 || candidate.order.length !== questions.length)) return false;
      if (candidate.roundType === 'retry' && candidate.roundNumber < 2) return false;
      var roundNumbers = candidate.order.map(function (i) { return String(questions[i].n); });
      if (Object.keys(candidate.first).some(function (n) { return !own(candidate.ans, n); }) ||
          Object.keys(candidate.ans).some(function (n) { return !own(candidate.first, n); }) ||
          Object.keys(candidate.round).some(function (n) { return roundNumbers.indexOf(n) < 0 || candidate.ans[n] !== candidate.round[n]; })) return false;
      if (candidate.roundType === 'first' && Object.keys(candidate.first).some(function (n) {
        return candidate.first[n] !== candidate.round[n] || candidate.ans[n] !== candidate.first[n];
      })) return false;
      if (candidate.mode === 'result' && roundNumbers.some(function (n) { return !own(candidate.round, n); })) return false;
      return true;
    }
    function tally(answers, subset) {
      return {right: subset.filter(function (q) { return answers[q.n] === q.correct; }).length,
        answered: subset.filter(function (q) { return own(answers, q.n); }).length, total: subset.length};
    }
    return {
      state: function () { return state; },
      snapshot: function () { return copy(state); },
      restore: function (candidate) { if (!validate(candidate)) return false; state = copy(candidate); return true; },
      start: function () { state = fresh(); state.mode = 'q'; },
      answer: function (option) {
        if (state.mode !== 'q') return false;
        var q = questions[state.order[state.pos]];
        if (own(state.round, q.n) || !own(q.opts, option)) return false;
        state.round[q.n] = option; state.ans[q.n] = option;
        if (!own(state.first, q.n)) state.first[q.n] = option;
        return true;
      },
      back: function () { if (state.mode === 'q' && state.pos > 0) state.pos--; },
      next: function () {
        if (state.mode !== 'q' || !own(state.round, questions[state.order[state.pos]].n)) return false;
        if (state.pos === state.order.length - 1) state.mode = 'result'; else state.pos++;
        return true;
      },
      retry: function () {
        if (state.mode !== 'result') return false;
        var order = questions.map(function (_, i) { return i; }).filter(function (i) {
          return own(state.ans, questions[i].n) && state.ans[questions[i].n] !== questions[i].correct;
        });
        if (!order.length) return false;
        state.order = order; state.pos = 0; state.round = {}; state.roundType = 'retry'; state.roundNumber++; state.mode = 'q';
        return true;
      },
      summary: function (kind, predicate) {
        var subset = kind === 'round' ? state.order.map(function (i) { return questions[i]; }) : questions;
        if (predicate) subset = subset.filter(predicate);
        return tally(kind === 'first' ? state.first : kind === 'round' ? state.round : state.ans, subset);
      },
      wrong: function () { return questions.filter(function (q) { return own(state.ans, q.n) && state.ans[q.n] !== q.correct; }); }
    };
  }

  function sourceHtml(source, esc) {
    var escaped = esc(source);
    return escaped.replace(/https?:\/\/[^\s<>]+/g, function (url) {
      var tail = '', href = url;
      while (/[.,;)]$/.test(href)) { tail = href.slice(-1) + tail; href = href.slice(0, -1); }
      return '<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + href + '</a>' + tail;
    }).replace(/\bDOI (10\.\d{4,9}\/[-._;()/:A-Z0-9]+)/gi, function (whole, doi) {
      return '<a href="https://doi.org/' + doi + '" target="_blank" rel="noopener noreferrer">' + whole + '</a>';
    });
  }

  function mount(config) {
    var Q = config.questions, AX = config.axes, esc = config.esc;
    var session = createSession(Q), saved = null, storageFailed = false, invalidSaved = false;
    var quiz = document.getElementById('quiz');
    var notice = document.createElement('p'); notice.className = 'cme-storage'; notice.setAttribute('role', 'status');
    quiz.parentNode.insertBefore(notice, quiz);
    function storageNotice() {
      notice.textContent = storageFailed ? cmeText('Der Browser kann diesen Lernstand nicht speichern. Du kannst weiter üben; beim Schließen geht der aktuelle Stand verloren.') :
        (invalidSaved ? cmeText('Der gespeicherte Stand passt nicht mehr zu diesem Modul. Bitte beginne einen neuen Durchgang. ') : '') +
        cmeText('Der Lernstand wird nur in diesem Browser gespeichert. Die CME-Auswertung ist vom allgemeinen Lernprofil getrennt.');
    }
    try {
      var raw = global.localStorage.getItem(config.key);
      if (raw) {
        var candidate;
        try { candidate = JSON.parse(raw); } catch (_) { invalidSaved = true; }
        var probe = createSession(Q);
        if (!invalidSaved && probe.restore(candidate)) saved = candidate;
        else invalidSaved = true;
      }
    } catch (_) { storageFailed = true; }
    storageNotice();
    function persist() {
      try { global.localStorage.setItem(config.key, JSON.stringify(session.snapshot())); invalidSaved = false; }
      catch (_) { storageFailed = true; }
      storageNotice();
    }
    function update(focusTarget) { persist(); render(focusTarget); }
    function focus(selector) {
      var target = quiz.querySelector(selector);
      if (!target) return;
      target.setAttribute('tabindex', '-1');
      if (target.focus) target.focus({preventScroll: true});
      if (target.scrollIntoView) target.scrollIntoView({block: 'nearest'});
    }
    function button(id, handler) { var node = document.getElementById(id); if (node) node.onclick = handler; }
    function percent(t) { return t.total ? Math.round(100 * t.right / t.total) : 0; }
    function score(t) { return cmeText(t.right === 1 ? 'scoreOne' : 'scoreMany', {right:t.right, total:t.total, percent:percent(t)}); }
    function restart() {
      if ((saved || Object.keys(session.state().first).length) && !global.confirm(cmeText('Ein neuer Durchgang löscht die bisherigen Antworten und die Erstquote dieses CME-Moduls. Neu beginnen?'))) return;
      saved = null; session.start(); update('.lead');
    }
    function progressBar(S) {
      return '<div class="progress" aria-hidden="true">' + S.order.map(function (qi, i) {
        var q = Q[qi], a = S.round[q.n];
        return '<span class="' + (a ? (a === q.correct ? 'ok' : 'bad') : (i === S.pos ? 'here' : '')) + '"></span>';
      }).join('') + '</div>';
    }
    function row(label, t, verdict) {
      return '<div class="row"><span>' + esc(label) + (verdict ? '<small class="cme-verdict">' + esc(verdict) + '</small>' : '') +
        '</span><span class="bar"><i style="width:' + percent(t) + '%"></i></span><span>' + t.right + cmeText(' von ') + t.total + '</span></div>';
    }
    function renderResult() {
      var S = session.state(), first = session.summary('first'), current = session.summary('round');
      var h = cmeText('<h3 class="cme-result-title" tabindex="-1">Auswertung</h3><p class="cme-score-label">Erster Versuch</p><p class="score">') + score(first) + '</p>';
      h += cmeText('<p class="note">Die Erstquote bleibt bei Fehlerwiederholungen erhalten. Ein neuer Durchgang setzt sie zurück.</p>');
      if (S.roundType === 'retry') h += cmeText('<p class="cme-score-label">Aktuelle Übungsrunde ') + S.roundNumber + '</p><p class="score">' + score(current) + '</p>';
      var strong = [], weak = [];
      h += cmeText('<h3 class="slot">Stärken und Übungsbedarf im ersten Versuch</h3><p class="note">Je Thema gibt es nur wenige Fragen, häufig ein oder zwei. Die Rückmeldung beschreibt diese Beispiele und erlaubt noch keine belastbare Aussage über deine gesamte Kompetenz.</p><div class="rows">');
      Object.keys(AX).forEach(function (axis) {
        var t = session.summary('first', function (q) { return q.axis === axis; });
        if (!t.total) return;
        var label = axis + ': ' + AX[axis], verdict;
        if (t.answered < t.total) verdict = cmeText('Noch nicht vollständig beantwortet');
        else if (t.right === t.total) { verdict = cmeText('Stärke in diesen Beispielen'); strong.push(label); }
        else { var missing = t.total - t.right; verdict = cmeText(missing === 1 ? 'weakOne' : 'weakMany', {n:missing}); weak.push(label); }
        h += row(label, t, verdict);
      });
      h += '</div>';
      if (strong.length) h += cmeText('<p class="hint cme-positive"><b>Gelungen:</b> ') + esc(strong.join('; ')) + '.</p>';
      if (weak.length) h += cmeText('<p class="hint"><b>Weiter üben:</b> ') + esc(weak.join('; ')) + cmeText('. Die Merkkästen stehen nach der letzten Frage des jeweiligen Themas.</p>');
      h += cmeText('<h3 class="slot">Erster Versuch nach Schwierigkeit</h3><div class="rows">');
      [1, 2, 3].forEach(function (diff) { var t = session.summary('first', function (q) { return q.diff === diff; }); if (t.total) h += row(cmeText('Schwierigkeit ') + diff, t); });
      h += '</div>';
      var wrong = session.wrong();
      h += '<p class="note">' + cmeText(wrong.length === 1 ? 'currentWrongOne' : 'currentWrong', {n: wrong.length}) + '</p><div class="actions">';
      if (wrong.length) h += cmeText('<button class="btn" id="retry">Fehler üben (') + wrong.length + ')</button>';
      h += cmeText('<button class="btn ghost" id="restart">Neuen Durchgang beginnen</button><button class="btn ghost" id="print">Druckfassung</button></div>');
      quiz.innerHTML = h;
      button('retry', function () { if (session.retry()) update('.lead'); });
      button('restart', restart); button('print', function () { global.print(); });
    }
    function render(focusTarget) {
      var S = session.state();
      if (S.mode === 'start') {
        var h = '<p class="lede">' + Q.length + cmeText(' Fallvignetten, je fünf Antwortoptionen, eine beste Antwort. Nach jeder Antwort folgen Kernaussage, Evidenz mit Herkunftsmarkern, Analyse aller Distraktoren und Praxiskonsequenz.</p>');
        if (saved) {
          var probe = createSession(Q); probe.restore(saved); var old = probe.summary('first');
          h += cmeText('<p>Gespeicherter Durchgang: ') + old.answered + cmeText(' von ') + old.total + cmeText(' Fragen im ersten Versuch beantwortet, davon ') + old.right + cmeText(' richtig.</p>');
        }
        h += '<div class="actions">' + (saved ? cmeText('<button class="btn" id="resume">Fortsetzen</button><button class="btn ghost" id="go">Neu beginnen</button>') : cmeText('<button class="btn" id="go">Fragen beginnen</button>')) + '</div>';
        quiz.innerHTML = h;
        button('go', restart); button('resume', function () { if (session.restore(saved)) { saved = null; update(session.state().mode === 'result' ? '.cme-result-title' : '.lead'); } });
        return;
      }
      if (S.mode === 'result') renderResult();
      else {
        var q = Q[S.order[S.pos]], chosen = S.round[q.n];
        var title = S.roundType === 'first' ? cmeText('Erster Durchgang') : cmeText('Übungsrunde ') + S.roundNumber;
        var html = '<div class="qhead"><span>' + title + cmeText(' · Frage ') + (S.pos + 1) + cmeText(' von ') + S.order.length + '</span><span class="ax">' + esc(q.axis + ': ' + AX[q.axis]) + cmeText('</span><span>Schwierigkeit ') + q.diff + cmeText(' von 3</span>') + (q.flag ? cmeText('<span class="fl">⚠ Evidenz begrenzt</span>') : '') + '</div>';
        html += progressBar(S) + '<p class="vignette">' + esc(q.vignette) + '</p><p class="lead">' + esc(q.lead) + '</p><div class="opts">';
        Object.keys(q.opts).forEach(function (option) {
          var cls = chosen ? (option === q.correct ? ' is-ok' : option === chosen ? ' is-bad' : '') : '';
          html += '<button class="opt' + cls + '" data-k="' + esc(option) + '"' + (chosen ? ' disabled' : '') + '><span class="k">' + esc(option) + '</span><span>' + esc(q.opts[option]) + '</span></button>';
        });
        html += '</div>' + (chosen ? config.feedback(q, chosen) : '') + '<div class="actions">';
        if (S.pos > 0) html += cmeText('<button class="btn ghost" id="back">Zurück</button>');
        if (chosen) html += '<button class="btn" id="next">' + (S.pos === S.order.length - 1 ? cmeText('Auswertung ansehen') : cmeText('Nächste Frage')) + '</button>';
        html += cmeText('<button class="btn ghost" id="restart">Neuen Durchgang beginnen</button></div>');
        quiz.innerHTML = html;
        Array.prototype.forEach.call(quiz.querySelectorAll('.opt'), function (node) {
          node.onclick = function () { if (session.answer(node.getAttribute('data-k'))) update('.verdictline'); };
        });
        button('back', function () { session.back(); update('.lead'); });
        button('next', function () { if (session.next()) update(session.state().mode === 'result' ? '.cme-result-title' : '.lead'); });
        button('restart', restart);
      }
      if (focusTarget) focus(focusTarget);
    }
    try { if (new URLSearchParams(global.location.search).get('continue') === '1' && saved && session.restore(saved)) saved = null; } catch (_) {}
    render();
    return session;
  }
  global.UroCme = {t: cmeText, initialize: initialize, language: language, number: number, mount: mount, createSession: createSession, sourceHtml: sourceHtml};
})(typeof window === 'undefined' ? globalThis : window);
