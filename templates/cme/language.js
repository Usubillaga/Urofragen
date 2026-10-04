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
  function t(text, values) {
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
      if (node.parentElement && !node.parentElement.closest('script, style')) node.nodeValue = t(node.nodeValue);
    }
    Array.prototype.forEach.call(document.querySelectorAll('[aria-label], [title], [alt]'), function (element) {
      ['aria-label', 'title', 'alt'].forEach(function (name) { if (element.hasAttribute(name)) element.setAttribute(name, t(element.getAttribute(name))); });
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
