/* Per-step progress, keyed by chapter + step id (not page path).
 *
 * One store per chapter — `voron-progress:ch:<chapter-slug>` — so a tick made
 * on a generated step page, on the long chapter page and on the chapter
 * overview grid are the same tick. Checkpoint list items live in the same
 * store under `cp:<checkpoint-slug>:<n>`.
 *
 * Mount points:
 *   long chapter page   every `Step NN.M` h2/h3 gets a checkbox + a summary bar
 *   step page           `.step-crumbs[data-step]` -> a big Done toggle
 *   chapter overview    `.step-grid[data-chapter]` -> card ticks + Resume
 *   manual index        chapter links get an "(N / M)" badge
 *
 * No server, no sync; works offline and in standalone mode.
 */
(function () {
  var STATE_PREFIX = 'voron-progress:ch:';
  var META_PREFIX = 'voron-progress-meta:ch:';
  var LEGACY_STATE = 'voron-progress:';
  var LEGACY_META = 'voron-progress-meta:';
  var MIGRATED = 'voron-progress:migrated-v2';
  var STEP_RE = /Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)/;

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }
  function parse(raw) {
    try { return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; }
  }

  function loadState(ch) { return parse(safeGet(STATE_PREFIX + ch)); }
  function saveState(ch, s) { safeSet(STATE_PREFIX + ch, JSON.stringify(s)); }
  function loadMeta(ch) { return parse(safeGet(META_PREFIX + ch)); }
  function saveMeta(ch, m) { safeSet(META_PREFIX + ch, JSON.stringify(m)); }

  function slug(text) {
    return (text || '')
      .replace(/[¶#]+\s*$/, '')
      .trim()
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s-]+/g, '-');
  }

  /* `/manual/04-ab-drives/` -> "04-ab-drives"; `/manual/print/B03-x/` -> "b03-x". */
  function chapterFromPath() {
    var parts = document.location.pathname.split('/').filter(Boolean);
    if (!parts.length) return null;
    var last = parts[parts.length - 1];
    if (/\.html?$/.test(last)) last = last.replace(/\.html?$/, '');
    return last.toLowerCase();
  }

  function currentChapter() {
    var el = document.querySelector('.md-content [data-chapter]');
    if (el) return el.getAttribute('data-chapter');
    return chapterFromPath();
  }

  /* One-time move of v1 path-keyed stores into the chapter-keyed scheme. */
  function migrate() {
    if (safeGet(MIGRATED)) return;
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var key = localStorage.key(i);
        if (!key || key.indexOf(LEGACY_STATE) !== 0) continue;
        if (key.indexOf(STATE_PREFIX) === 0 || key.indexOf(LEGACY_META) === 0) continue;
        var path = key.slice(LEGACY_STATE.length);
        if (path.indexOf('/') !== 0) continue;
        var parts = path.split('/').filter(Boolean);
        var ch = (parts[parts.length - 1] || '').toLowerCase();
        if (!ch) continue;
        var old = parse(localStorage.getItem(key));
        var next = loadState(ch);
        var touched = false;
        Object.keys(old).forEach(function (k) {
          if (!(k in next) && old[k]) { next[k] = true; touched = true; }
        });
        if (touched) saveState(ch, next);
      }
    } catch (e) { /* ignore */ }
    safeSet(MIGRATED, '1');
  }

  function countDone(state) {
    return Object.keys(state).filter(function (k) {
      return state[k] && k.indexOf('cp:') !== 0;
    }).length;
  }

  function updateCounters(ch, state, total) {
    var done = countDone(state);
    document.querySelectorAll('.step-counter__done').forEach(function (el) {
      el.textContent = ' · ' + done + ' done';
    });
    document.querySelectorAll('.progress-summary').forEach(function (el) {
      el.textContent = done + ' / ' + total + ' steps done';
    });
  }

  /* ---------------------------------------------------------------- long page */

  function stepHeadings() {
    var content = document.querySelector('.md-content');
    if (!content) return [];
    return Array.prototype.filter.call(content.querySelectorAll('h2, h3'), function (h) {
      return STEP_RE.test(h.textContent || '');
    });
  }

  function mountLongChapter() {
    var headings = stepHeadings();
    if (!headings.length) return false;
    if (document.querySelector('.step-crumbs')) return false; // a step page

    var ch = currentChapter();
    var state = loadState(ch);
    saveMeta(ch, { total: headings.length });

    headings.forEach(function (h) {
      if (h.querySelector('.step-done-toggle')) return;
      var m = STEP_RE.exec(h.textContent || '');
      if (!m) return;
      var id = m[1];
      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'step-done-toggle';
      cb.setAttribute('aria-label', 'Mark Step ' + id + ' done');
      cb.checked = !!state[id];
      h.classList.toggle('step-done', cb.checked);
      cb.addEventListener('change', function () {
        state[id] = cb.checked;
        saveState(ch, state);
        h.classList.toggle('step-done', cb.checked);
        updateCounters(ch, state, headings.length);
      });
      h.insertBefore(cb, h.firstChild);
    });

    var inner = document.querySelector('.md-content__inner');
    if (inner && !document.querySelector('.progress-bar')) {
      var bar = document.createElement('div');
      bar.className = 'progress-bar';

      var summary = document.createElement('span');
      summary.className = 'progress-summary';

      var resume = document.createElement('button');
      resume.type = 'button';
      resume.className = 'progress-resume';
      resume.textContent = 'Resume';
      resume.addEventListener('click', function () {
        var target = null;
        for (var i = 0; i < headings.length; i++) {
          var m = STEP_RE.exec(headings[i].textContent || '');
          if (m && !state[m[1]]) { target = headings[i]; break; }
        }
        (target || headings[headings.length - 1])
          .scrollIntoView({ behavior: 'smooth', block: 'start' });
      });

      var reset = document.createElement('button');
      reset.type = 'button';
      reset.className = 'progress-reset';
      reset.textContent = 'Reset chapter';
      reset.addEventListener('click', function () {
        if (!window.confirm('Clear step progress for this chapter?')) return;
        Object.keys(state).forEach(function (k) { delete state[k]; });
        saveState(ch, state);
        headings.forEach(function (h) {
          var cb = h.querySelector('.step-done-toggle');
          if (cb) cb.checked = false;
          h.classList.remove('step-done');
        });
        updateCounters(ch, state, headings.length);
      });

      bar.appendChild(summary);
      bar.appendChild(resume);
      bar.appendChild(reset);
      inner.insertBefore(bar, inner.firstChild);
    }

    updateCounters(ch, state, headings.length);
    mountCheckpoints(ch, state);
    return true;
  }

  /* ---------------------------------------------------------------- step page */

  function mountStepPage() {
    var crumbs = document.querySelector('.step-crumbs');
    if (!crumbs) return false;
    var ch = crumbs.getAttribute('data-chapter');
    var id = crumbs.getAttribute('data-step');
    var total = parseInt(crumbs.getAttribute('data-total'), 10) || 0;
    var state = loadState(ch);
    if (total) saveMeta(ch, { total: total });

    if (id && !document.querySelector('.step-done-bar')) {
      var nav = document.querySelector('.step-nav');
      var bar = document.createElement('div');
      bar.className = 'step-done-bar';

      var label = document.createElement('label');
      label.className = 'step-done-label';
      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'step-done-toggle';
      cb.checked = !!state[id];
      var text = document.createElement('span');
      text.textContent = 'Step ' + id + ' done';
      label.appendChild(cb);
      label.appendChild(text);
      bar.appendChild(label);

      cb.addEventListener('change', function () {
        state[id] = cb.checked;
        saveState(ch, state);
        document.body.classList.toggle('step-is-done', cb.checked);
        updateCounters(ch, state, total);
      });
      document.body.classList.toggle('step-is-done', cb.checked);

      if (nav && nav.parentNode) nav.parentNode.insertBefore(bar, nav);
      else {
        var inner = document.querySelector('.md-content__inner');
        if (inner) inner.appendChild(bar);
      }
    }

    updateCounters(ch, state, total);
    mountCheckpoints(ch, state);
    return true;
  }

  /* ---------------------------------------------------------------- overview */

  function mountOverview() {
    var grid = document.querySelector('.step-grid[data-chapter]');
    if (!grid) return false;
    var ch = grid.getAttribute('data-chapter');
    var state = loadState(ch);

    var cards = grid.querySelectorAll('.step-card[data-step]');
    var done = 0;
    var firstOpen = null;
    cards.forEach(function (card) {
      var id = card.getAttribute('data-step');
      var ticked = !!state[id];
      card.classList.toggle('step-card--done', ticked);
      if (ticked) done++;
      else if (!firstOpen) firstOpen = card;
    });
    saveMeta(ch, { total: cards.length });

    var meta = document.querySelector('.chapter-meta');
    if (meta && !meta.querySelector('.chapter-meta__done')) {
      var span = document.createElement('span');
      span.className = 'chapter-meta__done';
      span.textContent = ' · ' + done + ' / ' + cards.length + ' done';
      meta.appendChild(span);
    }

    var resume = document.querySelector('.chapter-resume');
    if (resume) {
      var target = firstOpen || cards[cards.length - 1];
      if (target) resume.setAttribute('href', target.getAttribute('href'));
      resume.textContent = firstOpen ? 'Resume' : 'Chapter complete — review';
    }
    return true;
  }

  /* ------------------------------------------------------------- checkpoints */

  function mountCheckpoints(ch, state) {
    var heads = Array.prototype.filter.call(
      document.querySelectorAll('.md-content h1, .md-content h2'),
      function (h) { return /^\s*Checkpoint\b/i.test(h.textContent || ''); }
    );
    heads.forEach(function (heading) {
      var key = 'cp:' + slug(heading.textContent);
      var list = heading.nextElementSibling;
      while (list && list.tagName !== 'UL' && list.tagName !== 'OL') {
        list = list.nextElementSibling;
      }
      if (!list) return;
      var boxes = list.querySelectorAll('input[type="checkbox"]');
      boxes.forEach(function (cb, idx) {
        if (cb.dataset.cpBound) return;
        cb.dataset.cpBound = '1';
        var k = key + ':' + idx;
        if (state[k]) cb.checked = true;
        cb.disabled = false;
        cb.addEventListener('change', function () {
          state[k] = cb.checked;
          saveState(ch, state);
        });
      });
    });
  }

  /* ----------------------------------------------------------- index badges */

  var CHROME = '.step-crumbs, .step-counter, .step-nav, .step-grid,' +
               ' .chapter-actions, .chapter-nav, .chapter-meta, .step-done-bar';
  var CHROME_SELF = '.step-pages-link, .tonight-seg';

  function mountIndexBadges() {
    document.querySelectorAll('.md-content a[href]').forEach(function (a) {
      if (a.querySelector('.progress-badge')) return;
      if (a.closest(CHROME) || a.matches(CHROME_SELF)) return;  // generated chrome, not an index link
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^[a-z]+:/i.test(href)) return;
      var url;
      try { url = new URL(href, document.location.href); } catch (e) { return; }
      if (url.origin !== document.location.origin) return;
      var parts = url.pathname.split('/').filter(Boolean);
      if (!parts.length) return;
      var ch = parts[parts.length - 1].replace(/\.html?$/, '').toLowerCase();
      var meta = loadMeta(ch);
      if (!meta || !meta.total) return;
      var badge = document.createElement('span');
      badge.className = 'progress-badge';
      badge.textContent = ' (' + countDone(loadState(ch)) + ' / ' + meta.total + ')';
      a.appendChild(badge);
    });
  }

  function mount() {
    migrate();
    var handled = mountStepPage() || mountOverview() || mountLongChapter();
    if (!handled) {
      var ch = currentChapter();
      if (ch) mountCheckpoints(ch, loadState(ch));
    }
    mountIndexBadges();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(mount);
  }
})();
