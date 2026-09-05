# R5 — iPad-at-the-bench usability (LIVE site)

Target: https://alexlicohen.github.io/voron-24-350-build-manual/ (GitHub Pages, checked 2026-09-05).
Viewports: 1180×820 (iPad Air 11 landscape), 820×1180 (portrait), 1024×768. Chromium/Playwright, DPR 1.
All 32 nav pages swept programmatically (home, manual/00-index, 00–14, print/ + 00-slicer-setup + B00–B10, print plan, survey).
Screenshots: `/Users/alex/projects/3d-printing/.playwright-mcp/R5-*.png`.

Counts: 3 BLOCKER · 9 MAJOR · 5 MINOR.

---

### F1 · BLOCKER · docs/voron-build-instructions-survey.md — §3 "Follow / Overlay from / Ignore" table
Claim in doc: `| Phase | Follow | Overlay from | Ignore |` … `| Frame | Manual p.12–21 | … | … |`
Source checked: live `/voron-build-instructions-survey/` at 820×1180 — table renders 1274 px inside an 805 px `.md-typeset__scrollwrap`; `thead th` right edges put **Follow, Overlay from and Ignore all past the wrapper edge**. `box-shadow: none`, no scrollbar → zero visual cue that 469 px of the table exists. Screenshot `R5-portrait-820x1180-survey-table-clipped.png`.
Problem: in portrait the builder sees only `Phase` + a stub of `Follow`, and the `Ignore` column — the one that says which official-manual pages **not** to do — is invisible, so they will follow steps the kit does not use.
Fix: apply the F1–F3 CSS block in the Appendix (drops this table to 995 px, sticky first column, scroll shadow — verified) **and** split this 4-col table in the markdown into two 3-col tables (`Phase | Follow | Overlay from` and `Phase | Ignore`), or move `Ignore` into a bulleted cell.

### F2 · BLOCKER · docs/manual/14-calibration.md — acceptance table (`Measurement | Nominal | … | Accept | If out`)
Claim in doc: `| Measurement | Nominal | Prusa Core One+ (B00) | Voron 2.4 350 (this build) | Accept | If out |`
Source checked: live `/manual/14-calibration/` at 820×1180 — table 900 px in an 805 px wrapper; measured `hidden = ["If out"]`. At 1180×820 it is 900 px in ~891 px usable — clipped by ~9 px, i.e. the column head is cut in both orientations.
Problem: the "If out" remediation column — what to do when a calibration measurement fails — is off-screen at the bench with no scroll affordance, so an out-of-spec result reads as having no defined action.
Fix: Appendix CSS block — verified to bring this table to 789 px / 805 px, **0 hidden columns**, in portrait.

### F3 · BLOCKER · docs/stylesheets/extra.css:6-9 — admonition text is the smallest text on every page
Claim in doc: `.md-typeset { font-size: 1.05rem; line-height: 1.6; }` (body bumped for bench reading; admonitions never touched)
Source checked: live computed styles on `/manual/05-gantry/` — body `<p>` = **21 px**, `.md-typeset .admonition p` = **12.8 px** (Material `main.ec1eaa64.min.css`: `.md-typeset .admonition{font-size:.64rem}`, root 20 px). Screenshots `R5-portrait-820x1180-ch05-step.png`, `R5-landscape-1180x820-home.png`.
Problem: every `**Check:**`, `⚠ Rev D+ / LDO:` and `Tip:` — the whole safety/kit-deviation layer, and the home page's own "Bench mode" instructions — renders at 61 % of body size, the least legible content on the page at arm's length.
Fix: add to extra.css — `.md-typeset .admonition, .md-typeset details { font-size: 0.95rem; }` and `.md-typeset .admonition-title, .md-typeset summary { font-size: 1rem; }`. Verified live: 12.8 px → 19 px body, 20 px title.

---

### F4 · MAJOR · docs/manual/07-ab-belts.md:119, 437, 481, 145, 203, 449 — six callouts never become admonitions
Claim in doc: `> ⚠ **Rev D+ / LDO:** *"PAGE 145 SKIP — The kit does not use hall effect endstops."* … Do not insert a 3×6 magnet.` and `**Tip:** If the probe barrel measures 9 mm rather than 8 mm, use \`probe_retainer_bracket_9mm.stl\``
Source checked: `hooks/callouts.py` anchors on `^⚠` and `^Tip:` (MULTILINE). Lines 119/437/481 start with `> ` (blockquote) and 145/203/449 start with `**Tip:**` (bolded) — neither form matches. Live `/manual/07-ab-belts/` renders all six as plain `<p>`; repo-wide scan found these six and no others.
Problem: three LDO deviations (wrong X-carriage, insulate the probe, skip p.145 hall endstops) and three tips render as ordinary body text with no warning styling — exactly the lines a builder skims past.
Fix: in `07-ab-belts.md` strip the leading `> ` on lines 119/437/481 and change `**Tip:**` → `Tip:` on 145/203/449. Optionally harden the hook: `re.compile(r"^(?:>\s*)?⚠\s*…")` and `r"^\*{0,2}Tip:\*{0,2}\s*(.*)$"`.

### F5 · MAJOR · docs/manual/print/B07-electronics-bay-and-lighting.md:6 — pause-point warning buried mid-paragraph
Claim in doc: `mechanical gantry). ⚠ **This is the Gen 2 belt-upgrade pause point** — if the Gen 1→Gen 2 upgrade kit arrives mid-run, finish this batch, then pause before starting B08.`
Source checked: live `/manual/print/B07-electronics-bay-and-lighting/` — renders inside the Prerequisites paragraph as inline text; `hooks/callouts.py` only converts line-initial `⚠`.
Problem: the one instruction that stops the print run at the right moment is inline body text inside a prerequisites sentence, not a warning block.
Fix: move it to its own line as `⚠ **Gen 2 belt-upgrade pause point:** if the Gen 1→Gen 2 upgrade kit arrives mid-run, finish this batch, then pause before starting B08.` so the hook converts it.

### F6 · MAJOR · docs/manual/print/00-slicer-setup.md + docs/voron-print-plan.md — "Source"/"Why" columns off-screen in the tables you slice from
Claim in doc: `| Setting | STRUCTURAL default | Set to | Why | Source |` (25 rows of PrusaSlicer overrides)
Source checked: live `/manual/print/00-slicer-setup/` — table is 1297 px. At 1180×820: cols end at 195/371/532/922/1312 px in a 923 px window → **`Source` fully hidden** (screenshot `R5-landscape-1180x820-slicer-table-clipped.png`). At 820×1180: `Why` and `Source` both hidden. Second table on the page has cells wrapping to **21 lines**. Same two tables duplicated in `voron-print-plan.md`; its `batch_id … unlocks_chapter | hard_prereq_batches` table (1173 px) hides the last two columns.
Problem: `Set to` (the value you type) stays visible, but justification and provenance vanish silently, and 21-line cells make the second table near-unusable in portrait.
Fix: Appendix CSS (verified: second slicer table 907/923 → 0 hidden; first drops 1297 → 992). For the first table also drop the `Source` column into a footnote row or merge `Why`+`Source`.

### F7 · MAJOR · site-wide — no lazy loading; 9.7–13.3 MB per chapter, re-downloaded every 10 minutes
Claim in doc: `![Voron manual p.82](assets/manual-pages/manual-p082.png)` ×414 refs; `![LDO S4 mapping](https://raw.githubusercontent.com/MotorDynamicsLab/…)` ×29 on Ch 10
Source checked: cold-cache loads — `11-skirts-panels-door` **9.68 MB / 51 image requests**; `10-wiring` 16 distinct raw.githubusercontent images = **10.4 MB** plus 2.3 MB local ≈ **13.3 MB**. `loading="lazy"` count = **0** on every page. `curl -I`: GitHub Pages `cache-control: max-age=600`, raw.githubusercontent `max-age=300`.
Problem: every chapter revisit after a 10-minute break re-pulls the whole page; Ch 10 (read crouched behind the printer) additionally hard-depends on GitHub's raw CDN with no fallback.
Fix: add a hook — `def on_page_content(html, page, config, files): return html.replace('<img ', '<img loading="lazy" decoding="async" ')` in `hooks/callouts.py`; then the SW in F12. Vendoring the LDO images locally would fix Ch 10 outright but `docs/manual/CONVENTIONS.md:10` forbids it pending a licence check.

### F8 · MAJOR · docs/index.md:5-6 — "Bench mode" tip is wrong for the published site
Claim in doc: `Open this on the iPad at \`http://<hostname>.local:8000\` (printed by \`scripts/serve.sh\`) while the Mac is on the LAN. Add the page to the Home Screen … for a full-screen, app-like view`
Source checked: live home page — the site is served from `https://alexlicohen.github.io/voron-24-350-build-manual/`; probing the DOM returns `manifest: false`, `apple-touch-icon: false`, `apple-mobile-web-app-capable: absent`. Screenshot `R5-landscape-1180x820-home.png`.
Problem: the first instruction the builder reads points at a LAN URL that only works while the Mac is serving, and the "full-screen, app-like view" it promises cannot happen without a manifest.
Fix: replace with — `Open https://alexlicohen.github.io/voron-24-350-build-manual/ on the iPad (or the LAN URL from \`scripts/serve.sh\` when editing offline). Share → Add to Home Screen for a full-screen view.` — and land F9 so the second sentence is true.

### F9 · MAJOR · mkdocs.yml (no `theme.custom_dir`) — no manifest / touch icon / apple meta
Claim in doc: mkdocs.yml `theme: { name: material, features: [...] }` — no `custom_dir`, no `extra_javascript`.
Source checked: live head has `theme-color: #4051b5` and `viewport` only; `link[rel=manifest]`, `link[rel=apple-touch-icon]`, `meta[name=apple-mobile-web-app-capable]`, `meta[name=apple-mobile-web-app-title]` all absent. `serviceWorker` API available, none registered.
Problem: Add-to-Home-Screen gives a Safari-chrome bookmark with a screenshot icon rather than a standalone app, and there is no offline capability at all.
Fix: Appendix "PWA minimum" — `theme.custom_dir: overrides`, `overrides/main.html` with an `extrahead` block, `docs/manifest.webmanifest`, `docs/assets/icon-180.png` / `-192` / `-512`.

### F10 · MAJOR · site-wide — no screen-wake-lock control; current advice is a manual workaround
Claim in doc: `docs/index.md:6` — "enable Guided Access or turn up Auto-Lock so the screen doesn't sleep mid-step"
Source checked: MDN browser-compat-data `api/WakeLock.json` — `safari: 16.4`; `safari_ios: 18.4` (16.4–18.3 present but **"Does not work in standalone Home Screen Web Apps", WebKit bug 254545**). `'wakeLock' in navigator` is the only gate needed; HTTPS is satisfied by GitHub Pages.
Problem: the builder has to reconfigure iPadOS settings instead of tapping a toggle, and the setting then persists after the build.
Fix: Appendix "Wake lock" — `extra_javascript: [javascripts/wakelock.js]` plus the ~20-line script; it re-acquires on `visibilitychange` (the lock is dropped whenever the tab is backgrounded). Works in Safari on any current iPadOS; on iPadOS 16.4–18.3 it silently no-ops **inside a Home Screen web app** only, so keep the Guided Access sentence as a one-line fallback.

### F11 · MAJOR · dark mode — manual-page renders are white rectangles, unfiltered
Claim in doc: mkdocs.yml `palette: [... scheme: slate ...]` (auto-follows `prefers-color-scheme`)
Source checked: live `/manual/05-gantry/` with `data-md-color-scheme="slate"` — body bg `rgb(30,33,41)`, `.md-content img` computed `filter: none`, PNG background measured at ≈ `#f7f7f7`. Screenshot `R5-dark-portrait-ch05.png`.
Problem: in a dim garage each step image is a full-width ~630 px-tall white panel on a near-black page — a glare source every time you scroll a step.
Fix: `[data-md-color-scheme="slate"] .md-typeset a.glightbox img { filter: brightness(.82) contrast(1.06); }` — verified applied live; add `:hover/:focus { filter: none }` if you want full brightness on demand.

### F12 · MAJOR · site-wide — nothing works without a live connection
Claim in doc: `CLAUDE.md` — "Delivery: MkDocs Material site from docs/ … read on an iPad at the bench"
Source checked: no service worker registered (`navigator.serviceWorker` available, zero registrations); GitHub Pages `max-age=600` on HTML, CSS, JS and PNGs.
Problem: a garage/basement wifi dropout leaves the builder with a blank page mid-chapter, and every revisit re-downloads the chapter.
Fix: Appendix "Service worker" — `docs/sw.js` (cache-first for `assets/manual-pages/*.png` and `assets/stylesheets|javascripts/*`, stale-while-revalidate for HTML) registered from `docs/javascripts/wakelock.js`; do **not** precache all 263 PNGs (40 MB) — cache on first view.

---

### F13 · MINOR · docs/stylesheets/extra.css:2-4 and :20-25 — two dead rules
Claim in doc: `:root { --md-typeset-font-size: 0.9rem; }` and `.bench-mode { border-left: 4px solid …; }`
Source checked: `grep -c -- "--md-typeset-font-size"` in the served `main.ec1eaa64.min.css` = **0** (Material hard-codes `.md-typeset{font-size:.8rem}`, no such variable). `grep -rn "bench-mode" docs --include="*.md"` = **0** (the home page uses `!!! tip "Bench mode"`).
Problem: two rules that look load-bearing but change nothing — the `0.9rem` is silently overridden by the `1.05rem` two lines below, and the class is never applied.
Fix: delete both blocks, or point `.bench-mode` at the real element with `.md-typeset .admonition.tip { … }`.

### F14 · MINOR · header/footer chrome — tap targets under 44 pt
Claim in doc: n/a (Material defaults)
Source checked: measured at 820×1180 — drawer button **40×40**, search button **40×40**, palette toggle **40×40**, back-to-top **130×40**. Footer prev/next 171×56 and drawer nav links 44–120 px are fine.
Problem: the three most-used controls sit under Apple HIG's 44×44 pt minimum — a real miss rate with gloves or greasy fingers.
Fix: `.md-header__button, .md-top { min-width: 44px; min-height: 44px; padding: .55rem; }`

### F15 · MINOR · docs/manual/10-wiring.md:897, 918, 932, 946 — raw `⚠` inside four h3 titles
Claim in doc: `### Step 10.58 — ⚠ Fit the ESD grounding path`
Source checked: live `/manual/10-wiring/` — renders as `<h3>Step 10.58 — ⚠ Fit the ESD grounding path</h3>`; the glyph propagates into the right-hand TOC, the drawer TOC and the search index (`search_index.json` title: `"Step 10.58 — ⚠ Fit the ESD grounding path"`). These are the only 4 of ~640 step headings that do this.
Problem: inconsistent with `CONVENTIONS.md` ("`⚠ Rev D+ / LDO:` callout … inline at the step") and clutters the 79-entry Ch 10 TOC.
Fix: drop the glyph from the four headings; the `⚠` callout inside each step already carries the warning.

### F16 · MINOR · search — "Step 10.58" returns all 32 pages
Claim in doc: n/a
Source checked: driven through the real UI on `/manual/10-wiring/` — `Nitehawk` → 14 docs (top: 08-toolhead ✓); `625-2RS` → 6 docs (top: print plan, then 02-z-drives ✓); `Step 10.58` → **32 matching documents**, correct page ranked first. `search_index.json`: `separator: "[\\s\\-]+"`, 1017 records, 984 with heading anchors, `Step 10.58` has its own `#step-1058-fit-the-esd-grounding-path` record.
Problem: `Step` is a term on all 32 pages, so a step-number search returns the whole site; ranking is correct but the list is long to thumb through on an iPad.
Fix: none needed in config — add a line to `docs/index.md`: `Searching a bare step number ("10.58") is faster than "Step 10.58".`

### F17 · MINOR · docs/manual/12-software.md — 18 of 34 code blocks scroll horizontally in portrait
Claim in doc: Klipper `printer.cfg` blocks, e.g. `# CHANGED — Leviathan; stm32h743xx if V1`
Source checked: live `/manual/12-software/` at 820×1180 — 18 `pre > code` with `scrollWidth > clientWidth`, widest **1360 px** in a 773 px column; `14-calibration` 6 blocks, `13-initial-startup` 2. No document-level overflow (`scrollWidth === clientWidth` on all 32 pages, both orientations).
Problem: config comments and G-code lines are cut mid-line; you can two-finger scroll, but not while reading a line into a terminal.
Fix: `@media (max-width: 76.1875em) { .md-typeset pre > code { font-size: .72rem; } }` — keeps scroll behaviour, fits ~1.3× more per line. Do **not** use `white-space: pre-wrap` on config blocks (wrapped lines read as separate directives).

### F18 · MINOR · docs/manual/assets/manual-pages/*.png — 54 % of each image is page chrome and whitespace
Claim in doc: `![Voron manual p.82](assets/manual-pages/manual-p082.png)` (414 refs, 263 files, 40 MB)
Source checked: PIL ink-bbox over a 14-page sample — every PNG is 1287×910; the drawing occupies a mean of **46 % of image height** (union bbox across the sample: y 170–796, x 90–1206). The rest is the "GANTRY / WWW.VORONDESIGN.COM" band, the page-number rule and margin. Rendered at 891 px (landscape) / 773 px (portrait), one step's image eats a full portrait screen. Lightbox opens on tap (verified: `.glightbox-container` visible, `zoomable: true, draggable: true`) but shows the image at 820 px vs 773 px inline — ~6 % larger until you double-tap to zoom.
Problem: scrolling cost per step is roughly double what the drawings need, and the lightbox's first frame adds nothing without a second gesture.
Fix: build-time crop to the union bbox — `sips -c 650 1140 --cropOffset 160 75 <in> --out <out>` over the 263 files reclaims ~29 % of vertical screen and ~30 % of bytes. CSS-only stopgap: `.md-typeset a.glightbox img { max-height: 62vh; width: auto; }`.

---

## Appendix — verified patches

**F1/F2/F3/F6 — `docs/stylesheets/extra.css`** (injected live and re-measured; results quoted in each finding)

```css
/* Callouts carry the safety + kit-deviation content — never smaller than body. */
.md-typeset .admonition,
.md-typeset details            { font-size: 0.95rem; }
.md-typeset .admonition-title,
.md-typeset summary            { font-size: 1rem; }

/* Wide tables: fit more, keep the row label, show that there is more to the right. */
.md-typeset__table                              { padding: 0 .4rem; }
.md-typeset table:not([class])                  { font-size: 0.85rem; }
.md-typeset table:not([class]) th,
.md-typeset table:not([class]) td               { padding: .5em .6em; }
.md-typeset table:not([class]) tbody td:first-child { position: sticky; left: 0; z-index: 1;
                                                      background: var(--md-default-bg-color); }
.md-typeset table:not([class]) thead th:first-child { position: sticky; left: 0; z-index: 2;
                                                      background: var(--md-default-bg-color); }
.md-typeset__scrollwrap {
  background:
    linear-gradient(to right, var(--md-default-bg-color) 30%, transparent) left  / 40px 100% no-repeat local,
    linear-gradient(to left,  var(--md-default-bg-color) 30%, transparent) right / 40px 100% no-repeat local,
    radial-gradient(farthest-side at 0 50%,   rgba(0,0,0,.28), transparent) left  / 14px 100% no-repeat scroll,
    radial-gradient(farthest-side at 100% 50%, rgba(0,0,0,.28), transparent) right / 14px 100% no-repeat scroll;
}

/* F11 — page renders are white; stop them glaring in slate. */
[data-md-color-scheme="slate"] .md-typeset a.glightbox img { filter: brightness(.82) contrast(1.06); }

/* F14 — 44 pt tap targets. */
.md-header__button, .md-top { min-width: 44px; min-height: 44px; padding: .55rem; }

/* F17 — fit more config per line in portrait. */
@media (max-width: 76.1875em) { .md-typeset pre > code { font-size: .72rem; } }
```

Measured effect at 820×1180: `14-calibration` acceptance table 900 → **789 px, 0 hidden**; survey `Doc|URL|Created|Last updated|Images` 949 → **789 px, 0 hidden**; survey `Phase|Follow|Overlay from|Ignore` 1274 → 995 px (hidden 3 → 2, first column sticky); survey `Phase|Hands-on…` 1085 → 844 px (hidden 3 → 1). At 1180×820: slicer table 2 907 / 923 → **0 hidden**; slicer table 1 1297 → 992 px. Admonition body 12.8 → 19 px, title → 20 px. Screenshot `R5-AFTER-portrait-survey-table-fixed.png`.

**F9 — PWA minimum**

`mkdocs.yml`: add `theme.custom_dir: overrides` and `extra_javascript: [javascripts/wakelock.js]`.

`overrides/main.html`
```html
{% extends "base.html" %}
{% block extrahead %}
  <link rel="manifest" href="{{ 'manifest.webmanifest' | url }}">
  <link rel="apple-touch-icon" href="{{ 'assets/icon-180.png' | url }}">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="Voron Build">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
{% endblock %}
```
`docs/manifest.webmanifest`
```json
{ "name": "Voron 2.4 350 — Build Manual", "short_name": "Voron Build",
  "start_url": "/voron-24-350-build-manual/", "scope": "/voron-24-350-build-manual/",
  "display": "standalone", "background_color": "#ffffff", "theme_color": "#4051b5",
  "icons": [ {"src":"assets/icon-192.png","sizes":"192x192","type":"image/png"},
             {"src":"assets/icon-512.png","sizes":"512x512","type":"image/png"} ] }
```

**F10 — `docs/javascripts/wakelock.js`** (also registers the F12 service worker)

```js
(function () {
  if (!('wakeLock' in navigator)) return;
  let lock = null, want = false;
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'md-header__button md-icon';
  btn.style.cssText = 'min-width:44px;min-height:44px;font:inherit;background:none;border:0;color:inherit;cursor:pointer';
  btn.title = 'Keep screen awake';
  const paint = () => { btn.textContent = want ? '☀' : '☼'; btn.setAttribute('aria-pressed', String(want)); };
  const acquire = async () => {
    try { lock = await navigator.wakeLock.request('screen'); lock.addEventListener('release', () => { lock = null; }); }
    catch (e) { want = false; }          // denied / low battery / unsupported context
    paint();
  };
  btn.addEventListener('click', async () => {
    want = !want;
    if (want) await acquire(); else { if (lock) await lock.release(); lock = null; paint(); }
  });
  document.addEventListener('visibilitychange', () => {
    if (want && !lock && document.visibilityState === 'visible') acquire();   // lock is dropped on background
  });
  const host = document.querySelector('.md-header__inner .md-header__option') || document.querySelector('.md-header__inner');
  if (host) { host.parentNode.insertBefore(btn, host); paint(); }
  if ('serviceWorker' in navigator)
    navigator.serviceWorker.register('/voron-24-350-build-manual/sw.js').catch(() => {});
})();
```
Caveat (MDN BCD `api/WakeLock`): iPadOS Safari **16.4+** in a normal tab; inside a **standalone Home Screen web app** it only works from **iPadOS 18.4**. Keep one fallback line in `index.md` for older iPads.

**F12 — `docs/sw.js`** (sketch; cache on view, never precache the 40 MB of PNGs)

```js
const V = 'voron-v1';
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(k =>
  Promise.all(k.filter(x => x !== V).map(x => caches.delete(x))))));
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  const immutable = /\/assets\/(manual-pages|stylesheets|javascripts|images)\//.test(u.pathname)
                 || u.host === 'raw.githubusercontent.com';
  e.respondWith(caches.open(V).then(async c => {
    const hit = await c.match(e.request);
    if (immutable && hit) return hit;                                  // cache-first
    const net = fetch(e.request).then(r => { if (r.ok || r.type === 'opaque') c.put(e.request, r.clone()); return r; })
                                .catch(() => hit);
    return hit || net;                                                 // stale-while-revalidate
  }));
});
```

---

## Verified OK
- No horizontal document overflow on any of the 32 pages at 1180×820, 820×1180 or 1024×768 (`documentElement.scrollWidth === clientWidth` everywhere). Long URLs in prose wrap (Material `overflow-wrap: break-word`).
- Every `### Step NN.M` renders as `h3` — 0 mis-levelled headings across ~640 steps (checked h1–h6 on all chapter pages).
- Step TOC present in both modes: right-hand sidebar in landscape (e.g. Ch 05 = 48 step links) and the drawer nav in portrait (same 48). `toc.follow` highlights the active step.
- glightbox opens on tap on all 414 images (`a.glightbox` wraps 100 % of `.md-content img`), `zoomable: true, draggable: true`, close/prev/next buttons present.
- Search returns correct top hits for `Nitehawk` (08-toolhead), `625-2RS` (print plan → 02-z-drives), `Step 10.58` (10-wiring); index is section-level (984 of 1017 records carry heading anchors), 995 KB.
- `hooks/callouts.py` converts 731 `**Check:**` → `success`, 193 `⚠` → `warning`, 33 `Tip:` → `tip` correctly; only the 6 in F4 + 1 in F5 escape. No stray `!!! ` literals in rendered HTML.
- Table horizontal scroll does function on touch (`.md-typeset__scrollwrap { overflow-x: auto; touch-action: auto }`, 406 px scrollable on the slicer table) — the defect is discoverability, not mechanics.
- Footer prev/next 171–482 × 56 px and drawer nav links 44–120 px tall are comfortable tap targets; drawer TOC links 48 px minimum.
- Dark-mode admonitions keep their coloured borders and tinted title bands (success `#00c853`, warning `#ff9100`, tip `#00bfa5`) and remain legible; only the images glare (F11).
- No JS console errors on the live site; one Material/glightbox `aria-hidden` warning after opening the lightbox (a11y nit, no functional effect).
- 11-skirts-panels-door is the heaviest page at **9.68 MB** — under the 15 MB flag. Ch 10 reaches ~13.3 MB only because of the external LDO images (F7).
- `mkdocs.yml` `navigation.indexes` / `awesome-nav` produce a working `manual/print/` section index; all 32 nav entries resolve (no 404s).

## Not checkable
- Real iPadOS Safari behaviour (pinch-zoom inside glightbox, momentum scrolling in `.md-typeset__scrollwrap`, Home-Screen standalone launch, actual wake-lock acquisition). All measurements are Chromium at DPR 1; the Safari-specific claims in F10 come from MDN browser-compat-data, not from a device.
- Physical legibility at bench viewing distance — 12.8 px vs 21 px is reported as measured CSS pixels; whether 12.8 px is "unreadable" at ~600 mm depends on the specific iPad and eyesight.
- Licence status of the 60 external LDO / VoronDesign images (blocks the "vendor them locally" fix in F7); `CONVENTIONS.md:10` defers to survey §7.4, which I did not audit.
- Service-worker cache quota on iPadOS for a 40 MB image set — the F12 sketch is cache-on-view precisely because I could not measure the real quota.
- Whether the 4 `⚠`-in-heading cases (F15) were a deliberate choice; treated as an inconsistency with `CONVENTIONS.md`.

## Note
`home.png` (74 KB, untracked, 2026-09-05 15:24) and a modified `CLAUDE.md` were already in the working tree when this pass started — not mine. My artefacts are confined to `.playwright-mcp/` (gitignored): `R5-*.png` screenshots plus `audit*.js`, `search*.js`, `testfix.js`, `shot-after.js`, `audit-L.txt`.
