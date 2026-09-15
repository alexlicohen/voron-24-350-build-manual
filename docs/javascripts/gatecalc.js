/* Gate calculators (R7 F1).
 *
 * `hooks/gatecalc.py` turns a ```gate-calc fence into
 *   <div class="gate-calc" data-gate-calc="<the whole spec, as JSON>">
 * and this file fills it in. The spec carries the semantics — a band
 * (`min` + `max`), a one-sided limit (`min` or `max` alone) or a yes/no row
 * (`fail_on` + `advice`) — so nothing here knows which gate it is drawing. A
 * row's `why` is one sentence behind a collapsed `why?` disclosure; it never
 * touches the verdict. A fence's `derive` is an arithmetic expression over its
 * own number keys, shown beside the badge — the hook has already whitelisted
 * it to keys, digits and `+ - * / ( ) .`, which is why `new Function` is safe
 * on it here.
 *
 * Values and the last verdict persist per gate id under `gate-calc:<id>`, the
 * same safeGet/safeSet/parse pattern progress.js uses, so a gate measured on
 * the chapter page is already filled in on the generated step page.
 */
(function () {
  var PREFIX = 'gate-calc:';

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }
  function safeRemove(key) {
    try { localStorage.removeItem(key); } catch (e) { /* private mode */ }
  }
  function parse(raw) {
    try { return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; }
  }

  function load(id) {
    var s = parse(safeGet(PREFIX + id));
    if (!s || typeof s !== 'object') s = {};
    if (!s.values || typeof s.values !== 'object') s.values = {};
    return s;
  }
  function save(id, state) { safeSet(PREFIX + id, JSON.stringify(state)); }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  /* ---------------------------------------------------------------- verdict */

  /* -> { verdict: 'pass' | 'fail' | 'incomplete', fails: [{row, advice}] } */
  function evaluate(spec, values) {
    var fails = [];
    var incomplete = false;
    spec.inputs.forEach(function (row) {
      var raw = values[row.key];
      if (row.kind === 'yesno') {
        if (raw !== 'yes' && raw !== 'no') {
          if (!row.optional) incomplete = true;
          return;
        }
        if (raw === row.fail_on) fails.push({ row: row, advice: row.advice });
        return;
      }
      var n = parseFloat(raw);
      if (raw === '' || raw == null || !isFinite(n)) {
        if (!row.optional) incomplete = true;
        return;
      }
      if (row.min != null && n < row.min) fails.push({ row: row, advice: row.low });
      else if (row.max != null && n > row.max) fails.push({ row: row, advice: row.high });
    });
    if (fails.length) return { verdict: 'fail', fails: fails };
    if (incomplete) return { verdict: 'incomplete', fails: [] };
    return { verdict: 'pass', fails: [] };
  }

  /* ------------------------------------------------------------- derivation */

  /* -> function(values) -> formatted string, or null while a key is unfilled */
  function compile(spec) {
    var d = spec.derive;
    if (!d || !d.keys || !d.keys.length) return null;
    var fn;
    try { fn = new Function(d.keys.join(','), 'return (' + d.expr + ');'); } catch (e) { return null; }
    return function (values) {
      var args = [];
      for (var i = 0; i < d.keys.length; i++) {
        var n = parseFloat(values[d.keys[i]]);
        if (!isFinite(n)) return null;
        args.push(n);
      }
      var out;
      try { out = fn.apply(null, args); } catch (e) { return null; }
      if (typeof out !== 'number' || !isFinite(out)) return null;
      return out.toFixed(d.digits);
    };
  }

  /* ------------------------------------------------------------------ build */

  function build(root) {
    var spec;
    try { spec = JSON.parse(root.getAttribute('data-gate-calc') || 'null'); } catch (e) { return; }
    if (!spec || !spec.inputs || !spec.inputs.length) return;
    if (root.dataset.gateCalcMounted) return;
    root.dataset.gateCalcMounted = '1';

    var state = load(spec.id);
    var values = state.values;
    root.textContent = '';

    var head = el('div', 'gate-calc__head');
    head.appendChild(el('span', 'gate-calc__title', spec.title));
    var badge = el('span', 'gate-calc__badge');
    badge.hidden = true;
    head.appendChild(badge);
    /* The verdict bird. Its two URLs come from data- attributes the hook set
     * page-relative, so nothing here knows where the art lives; it stays
     * hidden until there is a verdict to stand beside. */
    var bird = document.createElement('img');
    bird.className = 'mascot-panel gate-calc__mascot';
    bird.width = 96;
    bird.height = 96;
    bird.decoding = 'async';
    bird.hidden = true;
    head.appendChild(bird);
    function showBird(which) {
      var src = root.getAttribute('data-mascot-' + which);
      if (!src) { bird.hidden = true; return; }
      bird.src = src;
      bird.alt = root.getAttribute('data-mascot-' + which + '-alt') || '';
      bird.hidden = false;
    }
    var derived = el('span', 'gate-calc__derived');
    derived.hidden = true;
    head.appendChild(derived);
    root.appendChild(head);

    var derive = compile(spec);
    function paintDerived() {
      var value = derive && derive(values);
      derived.hidden = value == null;
      derived.textContent = value == null ? '' : spec.derive.label + ' ' + value;
    }

    var rows = el('div', 'gate-calc__rows');
    var fields = {};

    spec.inputs.forEach(function (row) {
      var wrap = el('div', 'gate-calc__row');
      wrap.setAttribute('data-key', row.key);

      var name = el('span', 'gate-calc__label', row.label + (row.optional ? ' (optional)' : ''));
      var hint = el('span', 'gate-calc__hint', row.hint || '');
      var label = el('span', 'gate-calc__labels');
      label.appendChild(name);
      label.appendChild(hint);
      wrap.appendChild(label);

      if (row.kind === 'yesno') {
        var group = el('span', 'gate-calc__yesno');
        group.setAttribute('role', 'group');
        group.setAttribute('aria-label', row.label);
        ['yes', 'no'].forEach(function (answer) {
          var b = el('button', 'gate-calc__yn', answer === 'yes' ? 'Yes' : 'No');
          b.type = 'button';
          b.setAttribute('data-answer', answer);
          b.setAttribute('aria-pressed', values[row.key] === answer ? 'true' : 'false');
          b.addEventListener('click', function () {
            values[row.key] = values[row.key] === answer ? '' : answer;
            Array.prototype.forEach.call(group.children, function (other) {
              other.setAttribute('aria-pressed',
                other.getAttribute('data-answer') === values[row.key] ? 'true' : 'false');
            });
            state.values = values;
            save(spec.id, state);
          });
          group.appendChild(b);
        });
        wrap.appendChild(group);
        fields[row.key] = group;
      } else {
        var input = document.createElement('input');
        input.type = 'number';
        input.step = '0.01';
        input.className = 'gate-calc__input';
        input.setAttribute('inputmode', 'decimal');
        input.setAttribute('aria-label', row.label);
        if (values[row.key] != null) input.value = values[row.key];
        input.addEventListener('input', function () {
          values[row.key] = input.value;
          state.values = values;
          save(spec.id, state);
          paintDerived();
        });
        wrap.appendChild(input);
        fields[row.key] = input;
      }

      if (row.why) {
        var why = el('details', 'gate-calc__why');
        why.appendChild(el('summary', 'gate-calc__why-toggle', 'why?'));
        why.appendChild(el('p', 'gate-calc__why-text', row.why));
        wrap.appendChild(why);
      }

      wrap.appendChild(el('p', 'gate-calc__advice'));
      rows.appendChild(wrap);
    });
    root.appendChild(rows);

    var actions = el('div', 'gate-calc__actions');
    var check = el('button', 'gate-calc__check', 'Check');
    check.type = 'button';
    var clear = el('button', 'gate-calc__clear', 'Clear');
    clear.type = 'button';
    actions.appendChild(check);
    actions.appendChild(clear);
    root.appendChild(actions);

    var note = el('p', 'gate-calc__note');
    root.appendChild(note);

    function paint(result, announce) {
      root.classList.remove('gate-calc--pass', 'gate-calc--fail');
      badge.hidden = result.verdict === 'incomplete';
      if (result.verdict === 'pass') {
        badge.textContent = 'PASS';
        badge.className = 'gate-calc__badge gate-calc__badge--pass';
        root.classList.add('gate-calc--pass');
        note.textContent = spec.pass;
        showBird('pass');
      } else if (result.verdict === 'fail') {
        badge.textContent = 'FAIL';
        badge.className = 'gate-calc__badge gate-calc__badge--fail';
        root.classList.add('gate-calc--fail');
        note.textContent = '';
        showBird('fail');
      } else {
        note.textContent = announce ? 'Fill in every row, then press Check.' : '';
        bird.hidden = true;
      }
      var failed = {};
      result.fails.forEach(function (f) { failed[f.row.key] = f.advice; });
      Array.prototype.forEach.call(rows.children, function (wrap) {
        var key = wrap.getAttribute('data-key');
        var advice = wrap.querySelector('.gate-calc__advice');
        wrap.classList.toggle('gate-calc__row--fail', key in failed);
        advice.textContent = key in failed ? failed[key] : '';
      });
      paintDerived();
    }

    check.addEventListener('click', function () {
      var result = evaluate(spec, values);
      state.values = values;
      state.verdict = result.verdict === 'incomplete' ? null : result.verdict;
      state.at = new Date().toISOString().slice(0, 10);
      save(spec.id, state);
      paint(result, true);
    });

    clear.addEventListener('click', function () {
      Object.keys(values).forEach(function (k) { delete values[k]; });
      state.verdict = null;
      safeRemove(PREFIX + spec.id);
      spec.inputs.forEach(function (row) {
        var field = fields[row.key];
        if (row.kind === 'yesno') {
          Array.prototype.forEach.call(field.children, function (b) {
            b.setAttribute('aria-pressed', 'false');
          });
        } else {
          field.value = '';
        }
      });
      paint({ verdict: 'incomplete', fails: [] }, false);
    });

    /* Re-render what was stored: a verdict only shows again if one was saved. */
    if (state.verdict === 'pass' || state.verdict === 'fail') paint(evaluate(spec, values), false);
    else paint({ verdict: 'incomplete', fails: [] }, false);
    paintDerived();
  }

  function mount() {
    document.querySelectorAll('.gate-calc[data-gate-calc]').forEach(build);
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
