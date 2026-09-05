/* R6 B2 — Per-step progress + resume, and index-page completion badges.
 * Every "Step NN.M" h3 gets a done checkbox; state is kept in localStorage
 * keyed by page path + step id. A "Resume" pill scrolls to the first
 * unchecked step; "Reset chapter" clears this page's state. The index page
 * reads the same storage to show "N / M" next to each chapter link.
 * No server, no sync, works offline and in standalone mode.
 */
(function () {
  var STATE_PREFIX = 'voron-progress:';
  var META_PREFIX = 'voron-progress-meta:';
  var STEP_RE = /Step\s+([A-Za-z]?\d+\.\d+)/;

  function safeGet(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function safeSet(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      /* private mode / quota — degrade silently */
    }
  }

  function loadState(path) {
    var raw = safeGet(STATE_PREFIX + path);
    try {
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveState(path, state) {
    safeSet(STATE_PREFIX + path, JSON.stringify(state));
  }

  function loadMeta(path) {
    var raw = safeGet(META_PREFIX + path);
    try {
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function saveMeta(path, meta) {
    safeSet(META_PREFIX + path, JSON.stringify(meta));
  }

  function stepId(heading) {
    var m = STEP_RE.exec(heading.textContent || '');
    return m ? m[1] : null;
  }

  function findStepHeadings() {
    var content = document.querySelector('.md-content');
    if (!content) return [];
    return Array.prototype.filter.call(content.querySelectorAll('h3'), function (h) {
      return STEP_RE.test(h.textContent || '');
    });
  }

  function mountChapter() {
    var headings = findStepHeadings();
    if (!headings.length) return;

    var path = document.location.pathname;
    var state = loadState(path);
    saveMeta(path, { total: headings.length });

    var summaryEl, resumeBtn;

    function updateSummary() {
      var done = headings.filter(function (h) {
        var id = stepId(h);
        return id && state[id];
      }).length;
      if (summaryEl) summaryEl.textContent = done + ' / ' + headings.length + ' steps done';
    }

    headings.forEach(function (h) {
      if (h.querySelector('.step-done-toggle')) return;
      var id = stepId(h);
      if (!id) return;

      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'step-done-toggle';
      cb.setAttribute('aria-label', 'Mark Step ' + id + ' done');
      cb.checked = !!state[id];
      h.classList.toggle('step-done', cb.checked);

      cb.addEventListener('change', function () {
        state[id] = cb.checked;
        saveState(path, state);
        h.classList.toggle('step-done', cb.checked);
        updateSummary();
      });

      h.insertBefore(cb, h.firstChild);
    });

    var content = document.querySelector('.md-content__inner');
    if (content && !document.querySelector('.progress-bar')) {
      var bar = document.createElement('div');
      bar.className = 'progress-bar';

      summaryEl = document.createElement('span');
      summaryEl.className = 'progress-summary';

      resumeBtn = document.createElement('button');
      resumeBtn.type = 'button';
      resumeBtn.className = 'progress-resume';
      resumeBtn.textContent = 'Resume';
      resumeBtn.addEventListener('click', function () {
        var target = null;
        for (var i = 0; i < headings.length; i++) {
          var id = stepId(headings[i]);
          if (id && !state[id]) {
            target = headings[i];
            break;
          }
        }
        (target || headings[headings.length - 1]).scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      });

      var resetBtn = document.createElement('button');
      resetBtn.type = 'button';
      resetBtn.className = 'progress-reset';
      resetBtn.textContent = 'Reset chapter';
      resetBtn.addEventListener('click', function () {
        if (!window.confirm('Clear step progress for this chapter?')) return;
        Object.keys(state).forEach(function (k) {
          delete state[k];
        });
        saveState(path, state);
        headings.forEach(function (h) {
          var cb = h.querySelector('.step-done-toggle');
          if (cb) cb.checked = false;
          h.classList.remove('step-done');
        });
        updateSummary();
      });

      bar.appendChild(summaryEl);
      bar.appendChild(resumeBtn);
      bar.appendChild(resetBtn);
      content.insertBefore(bar, content.firstChild);
    }

    updateSummary();
    mountCheckpoint(path);
  }

  // Wire Checkpoint task-list checkboxes (pymdownx.tasklist, clickable) into
  // the same per-page store, keyed by their position in the list, so a
  // Checkpoint is a real, persisted gate too.
  function mountCheckpoint(path) {
    var heading = Array.prototype.find.call(
      document.querySelectorAll('.md-content h2'),
      function (h) {
        return /^Checkpoint\b/i.test(h.textContent || '');
      }
    );
    if (!heading) return;
    var list = heading.nextElementSibling;
    while (list && list.tagName !== 'UL' && list.tagName !== 'OL') {
      list = list.nextElementSibling;
    }
    if (!list) return;

    var boxes = list.querySelectorAll('input[type="checkbox"]');
    if (!boxes.length) return;
    var state = loadState(path);

    boxes.forEach(function (cb, idx) {
      var key = 'checkpoint-' + idx;
      if (state[key]) cb.checked = true;
      cb.disabled = false;
      cb.addEventListener('change', function () {
        state[key] = cb.checked;
        saveState(path, state);
      });
    });
  }

  function mountIndexBadges() {
    var links = document.querySelectorAll('.md-content a[href]');
    links.forEach(function (a) {
      if (a.querySelector('.progress-badge')) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^[a-z]+:/i.test(href)) return;
      var url;
      try {
        url = new URL(href, document.location.href);
      } catch (e) {
        return;
      }
      if (url.origin !== document.location.origin) return;
      var meta = loadMeta(url.pathname);
      if (!meta || !meta.total) return;
      var state = loadState(url.pathname);
      var done = Object.keys(state).filter(function (k) {
        return state[k] && k.indexOf('checkpoint-') !== 0;
      }).length;
      var badge = document.createElement('span');
      badge.className = 'progress-badge';
      badge.textContent = ' (' + done + ' / ' + meta.total + ')';
      a.appendChild(badge);
    });
  }

  function mount() {
    mountChapter();
    mountIndexBadges();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  // Material instant-navigation swaps .md-content on page change; re-mount.
  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(mount);
  }
})();
