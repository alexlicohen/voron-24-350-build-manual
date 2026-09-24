/* Tonight: re-plan the 30/60/90-minute buckets from this device's ticks.
 *
 * scripts/build_tonight.py writes the static plan into manual/00-tonight.md
 * (as if nothing were ticked) and the same timeline into
 * docs/assets/tonight.json. This script reads progress.js's tick stores
 * (`voron-progress:ch:<chapter-slug>`, `{stepId: true}`) and the plate
 * board's (`plate-board:<plate id>`, `{printed: true}`), drops the segments
 * that are done, and re-runs the planner over what is left:
 *
 *   build segment   done when every step it spans is ticked (so B00.8's four
 *                   review sessions stay until B00.8 itself is ticked)
 *   print segment   done when its Load step is ticked, or the plate board
 *                   marks the plate printed
 *   row 1's gate    closed once any step after B00's "Before B00" section is
 *                   ticked (B00.8 on) or B00-P1 is printed
 *
 * The planner below is a line-for-line port of build_tonight.py's
 * (_plan_for_budget, _next_segment, _live_rows, _pre_kit_rows,
 * plan_sections, done_segments, gate_is_closed, plan_state). The JSON
 * carries the Python planner's own answers for seeded states (`cases`);
 * scripts/check_tonight.mjs replays them through this file and fails on any
 * difference. Without JS, or without the JSON, the static plan stays.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  } else {
    root.TonightPlanner = api;
    api.mountWhenReady();
  }
})(this, function () {
  'use strict';

  /* ---------------------------------------------------------------- planner */

  function planForBudget(rows, budget, stopAtKit, benchFirst, psm) {
    var picked = [], total = 0, plateStarted = false;
    var i, j, row, seg;
    if (benchFirst) {
      for (i = 0; i < rows.length; i++) {
        row = rows[i];
        if (stopAtKit && row.kit) break;
        if (row.kind === 'Print' || row.kind === 'Both') continue;
        for (j = 0; j < row.segments.length; j++) {
          seg = row.segments[j];
          if (total + seg.minutes > budget) break;
          picked.push([row, seg]);
          total += seg.minutes;
        }
      }
      var firstPrint = null;
      for (i = 0; i < rows.length; i++) {
        if (rows[i].kind === 'Print' && rows[i].segments.length) { firstPrint = rows[i]; break; }
      }
      if (firstPrint !== null && budget - total >= psm) {
        var rest = planForBudget([firstPrint], budget - total, stopAtKit, false, psm);
        picked = picked.concat(rest[0]);
        total += rest[1];
      }
      return [picked, total];
    }
    var printsBlocked = false;
    for (i = 0; i < rows.length; i++) {
      row = rows[i];
      if (stopAtKit && row.kit) break;
      if (!row.segments.length) continue;
      if (row.kind === 'Print' && printsBlocked) continue;
      var finished = true;
      for (j = 0; j < row.segments.length; j++) {
        seg = row.segments[j];
        if (seg.kind === 'print') {
          finished = false;
          if (!plateStarted && total + seg.minutes <= budget) {
            picked.push([row, seg]);
            total += seg.minutes;
            plateStarted = true;
          }
          break;
        }
        if (total + seg.minutes > budget) { finished = false; break; }
        picked.push([row, seg]);
        total += seg.minutes;
      }
      if (row.kind === 'Print' && !finished) printsBlocked = true;
      if (budget - total < psm) break;
    }
    return [picked, total];
  }

  function nextSegment(rows) {
    for (var i = 0; i < rows.length; i++) {
      if (rows[i].segments.length) return [rows[i], rows[i].segments[0]];
    }
    return [null, null];
  }

  function withSegments(row, segs) {
    var out = {};
    Object.keys(row).forEach(function (k) { out[k] = row[k]; });
    out.segments = segs;
    return out;
  }

  function liveRows(rows, done) {
    return rows.map(function (r) {
      return withSegments(r, r.segments.filter(function (s) { return !done[s.id]; }));
    });
  }

  function preKitRows(rows) {
    var out = [];
    rows.forEach(function (r) {
      var segs = !r.kit ? r.segments : r.segments.filter(function (s) { return s.pre_kit; });
      if (segs.length) out.push(withSegments(r, segs));
    });
    return out;
  }

  function planSections(data, kitArrived, done, gateClosed) {
    var live = liveRows(data.rows, done);
    var pre = preKitRows(live);
    var gateOpen = !!data.gate && !gateClosed;
    var specs = [];
    if (kitArrived) specs.push(['tonight', live, !kitArrived, false]);
    specs.push(['before-kit', pre, false, gateOpen]);
    var sections = specs.map(function (sp) {
      var srows = sp[1];
      return {
        id: sp[0], rows: srows, gate: gateOpen, bench_first: sp[3],
        buckets: data.budgets.map(function (budget) {
          var r = planForBudget(srows, budget, sp[2], sp[3], data.plate_start_min);
          return { budget: budget, picked: r[0], total: r[1],
                   next: r[0].length ? null : nextSegment(srows) };
        })
      };
    });
    var helpers = [];
    (kitArrived ? live : pre).forEach(function (row) {
      row.segments.forEach(function (seg) {
        if (seg.helpers && seg.helpers.length) helpers.push([row, seg]);
      });
    });
    return { sections: sections, helpers: helpers };
  }

  /* ticks: {slug: {stepId: true}}; printed: {plateId: true} */
  function doneSegments(rows, ticks, printed) {
    var done = {}, n = 0;
    rows.forEach(function (row) {
      row.segments.forEach(function (seg) {
        var have = ticks[seg.chapter] || {};
        var ok;
        if (seg.kind === 'print') {
          ok = !!have[seg.first_step] || (seg.plate != null && !!printed[seg.plate]);
        } else {
          ok = seg.steps.length > 0 && seg.steps.every(function (s) { return !!have[s]; });
        }
        if (ok && !done[seg.id]) { done[seg.id] = true; n++; }
      });
    });
    return { ids: done, count: n };
  }

  function gateIsClosed(gate, ticks, printed) {
    if (!gate) return false;
    var have = ticks[gate.chapter || ''] || {};
    return (gate.closed_by || []).some(function (s) { return !!have[s]; }) ||
           (gate.plates || []).some(function (p) { return !!printed[p]; });
  }

  function summary(plan, doneCount, gateClosed) {
    var head = plan.sections[0].buckets[plan.sections[0].buckets.length - 1];
    var start = null;
    if (head.picked.length) start = head.picked[0][1].first_step;
    else if (head.next && head.next[1]) start = head.next[1].first_step;
    return {
      done: doneCount, gate_closed: gateClosed, start: start,
      sections: plan.sections.map(function (sec) {
        return {
          id: sec.id, gate: sec.gate, bench_first: sec.bench_first,
          buckets: sec.buckets.map(function (b) {
            return {
              budget: b.budget, total: b.total,
              items: b.picked.map(function (p) { return p[1].id; }),
              next: b.next && b.next[1] ? b.next[1].id : null
            };
          })
        };
      }),
      helpers: plan.helpers.map(function (p) { return p[1].id; })
    };
  }

  function asSet(list) {
    var out = {};
    (list || []).forEach(function (x) { out[x] = true; });
    return out;
  }

  /* The whole overlay for one device state. `ticks` may hold arrays (the
   * JSON cases) or progress.js's own {id: true} objects. */
  function planState(data, ticks, printed, kitArrived) {
    var t = {};
    Object.keys(ticks || {}).forEach(function (ch) {
      var v = ticks[ch];
      if (Array.isArray(v)) t[ch] = asSet(v);
      else {
        t[ch] = {};
        Object.keys(v || {}).forEach(function (k) { if (v[k]) t[ch][k] = true; });
      }
    });
    var p = Array.isArray(printed) ? asSet(printed) : (printed || {});
    var done = doneSegments(data.rows, t, p);
    var closed = gateIsClosed(data.gate, t, p);
    var plan = planSections(data, kitArrived, done.ids, closed);
    plan.summary = summary(plan, done.count, closed);
    return plan;
  }

  /* ---------------------------------------------------------------- overlay */

  var PROGRESS_PREFIX = 'voron-progress:ch:';
  var PLATE_PREFIX = 'plate-board:';

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function parse(raw) {
    try { return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; }
  }

  function deviceState(data) {
    var ticks = {}, printed = {}, seen = {};
    data.rows.forEach(function (row) {
      row.segments.forEach(function (seg) {
        if (!seen[seg.chapter]) {
          seen[seg.chapter] = true;
          ticks[seg.chapter] = parse(safeGet(PROGRESS_PREFIX + seg.chapter));
        }
        if (seg.plate && parse(safeGet(PLATE_PREFIX + seg.plate)).printed) printed[seg.plate] = true;
      });
    });
    if (data.gate && data.gate.chapter && !seen[data.gate.chapter]) {
      ticks[data.gate.chapter] = parse(safeGet(PROGRESS_PREFIX + data.gate.chapter));
    }
    return { ticks: ticks, printed: printed };
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function segLink(seg, base) {
    var node;
    if (seg.href) {
      node = el('a', 'tonight-seg', seg.text);
      try { node.href = new URL(seg.href, base).href; } catch (e) { node.href = seg.href; }
    } else {
      node = el('span', 'tonight-seg', seg.text);
    }
    node.setAttribute('data-first-step', seg.first_step);
    return node;
  }

  function helperSuffix(seg) {
    var jobs = seg.helpers || [];
    if (!jobs.length) return '';
    return ' · helper: ' + jobs[0][1] + (jobs.length > 1 ? ' (+' + (jobs.length - 1) + ' more)' : '');
  }

  function strongLi(strong, rest) {
    var li = el('li');
    li.appendChild(el('strong', null, strong));
    li.appendChild(document.createTextNode(' ' + rest));
    return li;
  }

  /* Mirrors build_tonight._emit_section, line for line. */
  function renderSection(box, sec, gate, base) {
    var frag = document.createDocumentFragment();
    sec.buckets.forEach(function (b) {
      var label = b.budget + ' min';
      var head = el('p');
      head.appendChild(el('strong', null, 'If you have ' + label + ':'));
      frag.appendChild(head);
      var ul = el('ul');
      if (sec.gate && gate) {
        ul.appendChild(sec.bench_first
          ? strongLi('First, before B00 (not tonight):',
                     gate.label + '. The print rows below wait on it; the bench items do not.')
          : strongLi('first, and not tonight:', gate.label + ' — every row below waits on it'));
      }
      if (!b.picked.length) {
        var nx = b.next;
        ul.appendChild(el('li', null, (nx && nx[1])
          ? 'nothing fits in ' + label + ' — the next segment is ' + nx[0].label + ' — ' + nx[1].text
          : 'nothing to plan — no segments on this timeline yet'));
      } else {
        b.picked.forEach(function (p) {
          var row = p[0], seg = p[1];
          var li = el('li');
          var after = sec.bench_first && row.kind === 'Print' ? 'after the checks: ' : '';
          li.appendChild(document.createTextNode(row.label + ' — ' + after));
          li.appendChild(segLink(seg, base));
          var suffix = helperSuffix(seg);
          if (suffix) li.appendChild(document.createTextNode(suffix));
          ul.appendChild(li);
        });
      }
      var last = ul.lastElementChild;
      last.appendChild(document.createTextNode('\n'));
      last.appendChild(el('small', null, '~' + b.total + ' min hands-on planned'));
      frag.appendChild(ul);
    });
    box.textContent = '';
    box.appendChild(frag);
  }

  function renderHelpers(box, helpers, base) {
    var ul = el('ul');
    helpers.forEach(function (p) {
      var row = p[0], seg = p[1];
      var li = el('li');
      li.appendChild(el('strong', null, row.label));
      li.appendChild(document.createTextNode(' — '));
      li.appendChild(segLink(seg, base));
      var sub = el('ul');
      seg.helpers.forEach(function (h) { sub.appendChild(el('li', null, 'Step ' + h[0] + ' — ' + h[1])); });
      li.appendChild(sub);
      ul.appendChild(li);
    });
    if (!helpers.length) ul.appendChild(el('li', null, 'no helper jobs marked on this timeline yet'));
    box.textContent = '';
    box.appendChild(ul);
  }

  function stepHref(data, stepId) {
    for (var i = 0; i < data.rows.length; i++) {
      var segs = data.rows[i].segments;
      for (var j = 0; j < segs.length; j++) {
        if (segs[j].first_step === stepId && segs[j].href) return segs[j].href;
      }
    }
    return null;
  }

  function render(note, data, base) {
    var state = deviceState(data);
    var plan = planState(data, state.ticks, state.printed, !!data.kit_arrived);
    var s = plan.summary;

    plan.sections.forEach(function (sec) {
      var box = document.querySelector('.tonight-plan[data-tonight-section="' + sec.id + '"]');
      if (box) renderSection(box, sec, data.gate, base);
    });
    var hbox = document.querySelector('.tonight-helpers');
    if (hbox) renderHelpers(hbox, plan.helpers, base);

    note.textContent = '';
    note.appendChild(document.createTextNode(
      s.done + (s.done === 1 ? ' segment' : ' segments') + ' done on this device; '));
    if (s.start) {
      note.appendChild(document.createTextNode('plans start at '));
      var href = stepHref(data, s.start);
      var target = href ? el('a', 'tonight-live__start', 'Step ' + s.start) : el('strong', null, 'Step ' + s.start);
      if (href) { try { target.href = new URL(href, base).href; } catch (e) { target.href = href; } }
      note.appendChild(target);
      note.appendChild(document.createTextNode('.'));
    } else {
      note.appendChild(document.createTextNode('nothing left to plan.'));
    }
    note.hidden = false;
    document.body.classList.add('tonight--live');
  }

  function mount() {
    var note = document.querySelector('.tonight-live[data-tonight]');
    if (!note || note.dataset.mounted || typeof fetch !== 'function') return;
    note.dataset.mounted = '1';
    var url;
    try { url = new URL(note.getAttribute('data-tonight'), document.location.href).href; }
    catch (e) { return; }
    fetch(url, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data || !data.rows || !data.budgets) return;  // keep the static plan
        render(note, data, url);
        /* A tick made in another tab of the bench iPad re-plans this one. */
        window.addEventListener('storage', function (ev) {
          if (!ev.key || ev.key.indexOf(PROGRESS_PREFIX) === 0 || ev.key.indexOf(PLATE_PREFIX) === 0) {
            render(note, data, url);
          }
        });
        window.addEventListener('pageshow', function (ev) {
          if (ev.persisted) render(note, data, url);  // back from a step page (bfcache)
        });
      })
      .catch(function () { /* offline or missing: the static plan stays */ });
  }

  function mountWhenReady() {
    if (typeof document === 'undefined') return;
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
    else mount();
    if (typeof document$ !== 'undefined' && document$.subscribe) document$.subscribe(mount);
  }

  return {
    planForBudget: planForBudget,
    planState: planState,
    mountWhenReady: mountWhenReady
  };
});
