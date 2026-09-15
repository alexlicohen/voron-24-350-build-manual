/* Two build-data boards (R7 F2 + F3).
 *
 *   .build-progress   on Home — the cumulative CAD render of the last chapter
 *                     whose every step is ticked, plus an N-of-M counter.
 *   .plate-board      on Print › Plate board — the 22 plates in run order with
 *                     printed / sorted toggles.
 *
 * Both read a JSON written at build time by scripts/build_printables.py
 * (docs/assets/build-progress.json, docs/assets/plate-board.json), so no list
 * of chapters, renders, plates or spools is maintained by hand here.
 *
 * Step ticks come from progress.js's stores (`voron-progress:ch:<slug>`), read
 * with the same safeGet/parse guards; plate ticks live under `plate-board:<id>`.
 */
(function () {
  var PROGRESS_PREFIX = 'voron-progress:ch:';
  var PLATE_PREFIX = 'plate-board:';

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }
  function parse(raw) {
    try { return raw ? JSON.parse(raw) : {}; } catch (e) { return {}; }
  }
  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }
  function getJSON(url, then) {
    if (typeof fetch !== 'function') return;
    fetch(url, { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { if (data) then(data); })
      .catch(function () { /* offline or missing — leave the static fallback */ });
  }

  /* --------------------------------------------------- Home: what you've built */

  function mountBuildProgress() {
    var root = document.querySelector('.build-progress[data-build-progress]');
    if (!root || root.dataset.mounted) return;
    root.dataset.mounted = '1';
    getJSON(root.getAttribute('data-build-progress'), function (data) {
      var chapters = data.chapters || [];
      var total = 0, done = 0, next = null, best = null;

      chapters.forEach(function (ch) {
        var state = parse(safeGet(PROGRESS_PREFIX + ch.slug));
        var ticked = 0;
        (ch.steps || []).forEach(function (id) {
          total++;
          if (state[id]) { ticked++; done++; }
          else if (!next) next = id;
        });
        if (ch.steps && ch.steps.length && ticked === ch.steps.length && ch.image) best = ch;
      });

      var img = root.querySelector('.build-progress__img');
      var caption = root.querySelector('.build-progress__caption');
      var counts = root.querySelector('.build-progress__counts');

      if (best) {
        if (img) {
          img.src = best.image;
          img.alt = 'The machine after Chapter ' + best.number + ' — ' + best.title;
          img.hidden = false;
        }
        if (caption) {
          caption.textContent = 'Your build so far: after Ch ' + best.number + ' — ' + best.title;
        }
      } else {
        var start = data.start || null;
        if (img && start && start.image) {
          img.src = start.image;
          img.alt = start.title || 'The machine before the first chapter';
          img.hidden = false;
        } else if (img) {
          img.hidden = true;
        }
        if (caption) caption.textContent = 'Nothing ticked yet — the frame is next.';
      }

      if (counts) {
        counts.textContent = done + ' of ' + total + ' build steps done' +
          (next ? ' · next: Step ' + next : ' · every chapter ticked');
      }
      root.classList.add('build-progress--ready');
    });
  }

  /* ------------------------------------------------------------- plate board */

  function plateState(id) {
    var s = parse(safeGet(PLATE_PREFIX + id));
    return { printed: !!s.printed, sorted: !!s.sorted };
  }
  function savePlate(id, s) { safeSet(PLATE_PREFIX + id, JSON.stringify(s)); }

  function mountPlateBoard() {
    var root = document.querySelector('.plate-board[data-plate-board]');
    if (!root || root.dataset.mounted) return;
    root.dataset.mounted = '1';
    getJSON(root.getAttribute('data-plate-board'), function (data) {
      var plates = data.plates || [];
      if (!plates.length) return;
      root.textContent = '';

      var head = el('div', 'plate-board__head');
      var summary = el('p', 'plate-board__summary');
      head.appendChild(summary);
      root.appendChild(head);

      var grid = el('div', 'plate-board__grid');
      root.appendChild(grid);

      var tiles = [];

      function refresh() {
        var printed = 0, remaining = 0, spool = null;
        plates.forEach(function (plate, i) {
          var s = plateState(plate.id);
          if (s.printed) printed++;
          else {
            remaining += plate.hours;
            if (spool === null) spool = plate.spool;
          }
          var tile = tiles[i];
          tile.node.classList.toggle('plate-tile--printed', s.printed);
          tile.node.classList.toggle('plate-tile--sorted', s.sorted);
          tile.printed.setAttribute('aria-pressed', s.printed ? 'true' : 'false');
          tile.sorted.setAttribute('aria-pressed', s.sorted ? 'true' : 'false');
        });
        var nextIdx = -1;
        for (var i = 0; i < plates.length; i++) {
          if (!plateState(plates[i].id).printed) { nextIdx = i; break; }
        }
        tiles.forEach(function (t, i) {
          t.node.classList.toggle('plate-tile--next', i === nextIdx);
        });
        summary.textContent = printed + ' of ' + plates.length + ' plates printed · ' +
          remaining.toFixed(1) + ' h left · ' +
          (spool ? 'spool ' + spool : 'every plate printed');
      }

      plates.forEach(function (plate) {
        var node = el('div', 'plate-tile');
        node.setAttribute('data-plate', plate.id);

        var thumb = el('a', 'plate-tile__thumb');
        thumb.href = plate.diagram;
        var img = document.createElement('img');
        img.src = plate.diagram;
        img.alt = 'Sorting diagram for plate ' + plate.id;
        img.loading = 'lazy';
        img.decoding = 'async';
        thumb.appendChild(img);
        node.appendChild(thumb);

        var body = el('div', 'plate-tile__body');

        var title = el('div', 'plate-tile__head');
        title.appendChild(el('span', 'plate-tile__id', plate.id));
        var swatch = el('span', 'plate-swatch plate-swatch--' + plate.colour);
        swatch.title = plate.colour === 'blue' ? 'accent blue' : 'Galaxy Black';
        title.appendChild(swatch);
        title.appendChild(el('span', 'plate-tile__slot plate-tile__slot--' + plate.slot,
          plate.slot === 'overnight' ? 'overnight' : 'day'));
        body.appendChild(title);

        var batch = el('a', 'plate-tile__batch', plate.batch + ' — ' + plate.batch_title);
        batch.href = plate.chapter;
        body.appendChild(batch);

        body.appendChild(el('p', 'plate-tile__meta',
          plate.hours.toFixed(1) + ' h · ' + plate.grams + ' g · spool ' + plate.spool +
          ' · ' + plate.remaining + ' g left after'));
        if (plate.note) body.appendChild(el('p', 'plate-tile__note', plate.note));

        var toggles = el('div', 'plate-tile__toggles');
        var printedBtn = el('button', 'plate-tile__toggle', 'Printed');
        printedBtn.type = 'button';
        var sortedBtn = el('button', 'plate-tile__toggle', 'Sorted');
        sortedBtn.type = 'button';
        toggles.appendChild(printedBtn);
        toggles.appendChild(sortedBtn);
        body.appendChild(toggles);

        node.appendChild(body);
        grid.appendChild(node);

        var entry = { node: node, printed: printedBtn, sorted: sortedBtn };
        tiles.push(entry);

        printedBtn.addEventListener('click', function () {
          var s = plateState(plate.id);
          s.printed = !s.printed;
          savePlate(plate.id, s);
          refresh();
        });
        sortedBtn.addEventListener('click', function () {
          var s = plateState(plate.id);
          s.sorted = !s.sorted;
          savePlate(plate.id, s);
          refresh();
        });
      });

      refresh();
    });
  }

  function mount() {
    mountBuildProgress();
    mountPlateBoard();
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
