"""Build-time mascot placement for the Voron build manual (the raven).

Three jobs, all of them here so no other file has to know where the art lives:

1. The ` ```mascot ` fence — a page illustration with a caption:

       ```mascot
       pose: hexkey
       caption: One corner square. Three to go.
       side: right          # optional, default right
       ```

   becomes

       <figure class="mascot-scene mascot-scene--right">
         <img class="mascot-scene__img" src="<page-relative>/mascot-hexkey.svg"
              alt="Revali turning a hex key" width="220" height="220">
         <figcaption>One corner square. Three to go.</figcaption>
       </figure>

   Like `hooks/gatecalc.py` this runs `on_page_markdown` on **every** page, so a
   fence authored in a chapter also renders in the step page
   `scripts/build_steps.py` copies it into (a fence survives that copy untouched:
   `rewrite_links` only rewrites `](…)`, and `_segments` keeps a fence as one
   block).  Validation is a build error with the page name: the pose must be one
   of the files in `docs/manual/assets/mascot/`, the caption is at most 18 words
   with no em-dash and no parenthetical, and `pose: warn` is allowed only on
   `00a-mains-safety` (STYLE.md § "Humour rule": `⚠` boxes carry no bird).

2. `badge_html()` / `panel_html()` / `image_html()` — the markup the other
   generators embed (`hooks/callouts.py` for the Check / Tip / Pause admonition
   titles, `scripts/build_steps.py` for the Gather block and the Helper line,
   `scripts/build_printables.py`, `scripts/build_tonight.py`).  Badges are
   `mascot-badge` sized: 28–32 px, in an admonition **title** row, never inside a
   budgeted Do / Check / Tip / ⚠ text run.

3. The `@mascot/` sentinel.  Everything above emits `src="@mascot/mascot-X.svg"`
   because most of it is written at `on_pre_build`, before any page URL exists —
   and because raw HTML `src` attributes are the one thing mkdocs does *not*
   re-base.  `on_page_content` rewrites the sentinel once per page to the path
   that page needs, so every reference on a page resolves to the same five or six
   URLs and the browser caches them.  Nothing is inlined.

4. The humour rule's step list, `NO_MASCOT_STEPS`: mains, soldering-iron
   (heat-set insert or solder), blade and hot-chamber steps carry no bird at
   all.  `on_page_content` strips every badge inside such a step — the Check /
   Tip / Pause titles `hooks/callouts.py` writes and the Gather / Helper badges
   `scripts/build_steps.py` writes alike — on the step page and on the long
   chapter page, and the fence refuses a scene inside one.  No other file
   classifies steps.  The same list refuses a `**Helper:**` line inside such a
   step (the build fails), with one approved exception, `HELPER_RECORD_ONLY`.

5. `reward_html()` — the Checkpoint reward `scripts/build_steps.py` generates:
   the `pass` scene with its caption, or the caption alone for a Checkpoint in
   `REWARD_TEXT_ONLY`.  The caption obeys the fence's rules.

`scripts/gen_mascot.py` owns the SVGs; this hook never writes one.
"""

from __future__ import annotations

import html
import posixpath
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "docs" / "manual" / "assets" / "mascot"

# Where the art sits relative to the site root, and the token that stands in for
# "the path from this page to there" until `on_page_content` knows the page.
ASSET_ROOT = "manual/assets/mascot"
SENTINEL = "@mascot/"

# STYLE.md: the warn pose is the hard hat, and it belongs to exactly one chapter.
WARN_POSE = "warn"
WARN_PAGE = "00a-mains-safety"

CAPTION_MAX_WORDS = 18

# Sizes, in CSS px, paired with the class that enforces them in extra.css.
SIZES = {"mascot-badge": 30, "mascot-panel": 96, "mascot-scene__img": 220,
         "mascot-hero": 200}

_FENCE_RE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})\s*([A-Za-z0-9_-]*)\s*$")
_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
_DASH_RE = re.compile(r"[—–]")
_PAREN_RE = re.compile(r"[()]")
_SIDES = ("left", "right")


class MascotError(Exception):
    """A bad fence — fails the build with the page name."""


# --------------------------------------------------------------------------
# the humour rule, as data: the steps that get no bird at all
# --------------------------------------------------------------------------

# STYLE.md § "Humour rule", CONVENTIONS.md § "Where the bird may and may not
# go": no mascot on mains, soldering-iron, blade or hot-chamber content.  A step
# is listed when its Do puts the reader at that hazard: mains wiring, metering
# or power-on (all of Ch 00a); the iron, for a heat-set insert or a solder
# joint; a blade or cutter as the step's main action; a heater at temperature
# with hands at the open machine.  `A.B-A.C` is a range inside one chapter.
# Step ids never change (CONVENTIONS: never split or renumber): an appended
# step of one of these kinds goes in here, and a step whose hazard is edited
# out of its Do comes out (07.34 keeps its probe lead whole since 2026-09-24).  The
# self-test fails on an id that is not a step heading, and on a `**Helper:**`
# line inside a listed step (the Helper safety rule forbids the same steps).
NO_MASCOT_STEPS: dict[str, str] = {
    "mains": "00a.1-00a.12 09.11-09.18 09.34-09.36 10.1-10.23 10.68 10.69 "
             "10.73 10.77 10.78 10.80 11.67 12.11 13.2 13.3 13.8",
    "iron": "00.13-00.16 02.03-02.04 04.3-04.4 07.6 08.3-08.7 08.36 09.10 09.34 "
            "10.35 10.50 11.2 11.3 11.5 11.28 11.33 11.49 B00.7",
    "blade": "00.1 03.10 06.4 06.21 07.8 08.2 08.32 08.33 08.34 10.59 10.66 11.27 11.29 "
             "11.31 11.45",
    "hot": "13.29-13.33 13.35-13.37 13.39 13.40 13.42 14.3 14.6-14.9 14.17 14.19 14.20 "
           "14.21 14.22",
}

# Alex, 2026-09-24 (WAVE4-PLAN D4): on the unplugged meter sweep the helper may
# RECORD readings while the adult holds the probes, so a Helper line in these
# steps is allowed, listed or not, only if its job says "record".
HELPER_RECORD_ONLY = "10.74-10.78"
_RECORD_RE = re.compile(r"\brecord", re.IGNORECASE)
_HELPER_LINE_RE = re.compile(r"^(?:>\s?)?\*{0,2}Helper:\*{0,2}\s*(.*)$")

# WAVE4-PLAN D5: Checkpoint 00a closes the mains-safety chapter, so its reward
# is the caption alone; every other Checkpoint (10 included) gets the bird.
REWARD_TEXT_ONLY = {"00a"}
REWARD_POSE = "pass"

_STEP_ID_RE = re.compile(r"^([0-9]{2}[a-z]?|B[0-9]{2})\.([0-9]+)$", re.IGNORECASE)


def _step_key(step_id: str) -> tuple[str, int] | None:
    """`10.8` / `02.03` / `00a.2` / `B00.7` -> (`10`, 8) etc.; None if not a step id."""
    m = _STEP_ID_RE.match(step_id.strip())
    return (m.group(1).lower(), int(m.group(2))) if m else None


def _expand(spec: str) -> list[tuple[str, int]]:
    keys = []
    for token in spec.split():
        first, _, last = token.partition("-")
        a = _step_key(first)
        b = _step_key(last) if last else a
        if a is None or b is None or a[0] != b[0] or b[1] < a[1]:
            raise ValueError(f"NO_MASCOT_STEPS: bad step or range {token!r}")
        keys += [(a[0], n) for n in range(a[1], b[1] + 1)]
    return keys


_NO_MASCOT: dict[tuple[str, int], str] = {}


def no_mascot_reason(step_id: str) -> str | None:
    """`mains` / `iron` / `blade` / `hot` if the step carries no bird, else None."""
    if not _NO_MASCOT:
        for reason, spec in NO_MASCOT_STEPS.items():
            for key in _expand(spec):
                _NO_MASCOT.setdefault(key, reason)
    key = _step_key(step_id)
    return _NO_MASCOT.get(key) if key else None


_RECORD_ONLY: set[tuple[str, int]] = set()


def helper_problem(step_id: str, job: str) -> str | None:
    """Why a `**Helper:**` job may not sit in this step, or None if it may."""
    if not _RECORD_ONLY:
        _RECORD_ONLY.update(_expand(HELPER_RECORD_ONLY))
    if _step_key(step_id) in _RECORD_ONLY:
        if _RECORD_RE.search(job):
            return None
        return ("the meter sweep %s allows a helper who records readings only "
                "(the adult holds the probes); say \"records\"" % HELPER_RECORD_ONLY)
    reason = no_mascot_reason(step_id)
    if reason:
        return "%s %s step takes no helper" % ("an" if reason[0] in "aeiou" else "a", reason)
    return None


# --------------------------------------------------------------------------
# the twenty files, and the title each one carries
# --------------------------------------------------------------------------

_POSES: dict[str, str] = {}


def poses() -> dict[str, str]:
    """`{pose: <title> of its SVG}`, read once from the asset directory."""
    if not _POSES:
        for path in sorted(ASSETS.glob("mascot-*.svg")):
            head = path.read_text(encoding="utf-8")[:4096]
            m = _TITLE_RE.search(head)
            _POSES[path.stem[len("mascot-"):]] = (m.group(1).strip() if m
                                                  else "Revali, the manual's raven")
    return _POSES


def title_of(pose: str) -> str:
    return poses().get(pose, "Revali, the manual's raven")


# --------------------------------------------------------------------------
# markup
# --------------------------------------------------------------------------


def _img(pose: str, cls: str, alt: str, *, eager: bool) -> str:
    """One `<img>`.

    Attributes are **single**-quoted on purpose: a badge is embedded in an
    admonition title, and Python-Markdown delimits that title with `"` — a
    double quote inside it makes the title regex ambiguous.  `width`/`height`
    are always set (the files are square 512s) so a badge never shifts the line
    it punctuates while it loads.
    """
    size = SIZES[cls.split()[0]]
    # `off-glb` keeps glightbox out: the bird is punctuation, not a figure to
    # open full-screen, and a lightbox on a badge is a tap trap at the bench.
    cls = cls + " off-glb"
    return (
        "<img class='%s' src='%s%s' alt='%s' width='%d' height='%d' "
        "loading='%s' decoding='async'>"
        % (cls, SENTINEL, "mascot-%s.svg" % pose, html.escape(alt, quote=True),
           size, size, "eager" if eager else "lazy")
    )


def badge_html(pose: str, alt: str | None = None) -> str:
    """A 28–32 px inline badge for an admonition title row.

    Eagerly loaded: a badge is beside text that is already on screen, and a
    lazy one flashes in after the line it punctuates has been read.
    """
    return _img(pose, "mascot-badge", alt or pose, eager=True)


def panel_html(pose: str, alt: str | None = None, extra: str = "") -> str:
    """A ~96 px panel — the gate verdicts, the plate board header, printables."""
    cls = "mascot-panel" + ((" " + extra) if extra else "")
    return _img(pose, cls, alt or title_of(pose), eager=False)


def image_html(pose: str, cls: str, alt: str | None = None) -> str:
    return _img(pose, cls, alt or title_of(pose), eager=cls == "mascot-hero")


def asset(pose: str) -> str:
    """The sentinel URL for a pose, for a `data-` attribute the JS reads."""
    return SENTINEL + "mascot-%s.svg" % pose


def scene_html(pose: str, caption: str, side: str = "right") -> str:
    return (
        '<figure class="mascot-scene mascot-scene--%s">%s'
        "<figcaption>%s</figcaption></figure>"
        % (side, image_html(pose, "mascot-scene__img"), html.escape(caption))
    )


# --------------------------------------------------------------------------
# the fence
# --------------------------------------------------------------------------


def check_caption(caption: str, where: str) -> None:
    """The caption rule, for fences and generated captions alike."""
    words = len(caption.split())
    if words > CAPTION_MAX_WORDS:
        raise MascotError(
            f"{where}: caption is {words} words, budget is {CAPTION_MAX_WORDS}"
        )
    if _DASH_RE.search(caption):
        raise MascotError(f"{where}: caption may not use an em-dash — {caption!r}")
    if _PAREN_RE.search(caption):
        raise MascotError(f"{where}: caption may not use a parenthetical — {caption!r}")


def reward_html(checkpoint: str, caption: str, where: str) -> str:
    """A Checkpoint's reward: the `pass` scene, or text only (`REWARD_TEXT_ONLY`).

    One line of raw HTML, so it drops into any markdown body as its own block.
    """
    check_caption(caption, where)
    if checkpoint.lower() in REWARD_TEXT_ONLY:
        return ('<p class="checkpoint-reward checkpoint-reward--text">%s</p>'
                % html.escape(caption))
    return '<div class="checkpoint-reward">%s</div>' % scene_html(REWARD_POSE, caption)


def _scene_from_fence(body: list[str], where: str) -> str:
    try:
        spec = yaml.safe_load("\n".join(body))
    except yaml.YAMLError as exc:
        raise MascotError(f"{where}: mascot fence YAML did not parse — {exc}")
    if not isinstance(spec, dict):
        raise MascotError(f"{where}: a mascot fence must be a YAML mapping")

    unknown = set(spec) - {"pose", "caption", "side"}
    if unknown:
        raise MascotError(
            f"{where}: unknown key(s) {sorted(unknown)} — a mascot fence takes "
            "`pose:`, `caption:` and an optional `side:`"
        )

    pose = str(spec.get("pose") or "").strip()
    if not pose:
        raise MascotError(f"{where}: a mascot fence needs a `pose:`")
    if pose not in poses():
        raise MascotError(
            f"{where}: unknown pose {pose!r} — the poses are "
            + ", ".join(sorted(poses()))
        )
    if pose == WARN_POSE and WARN_PAGE not in where:
        raise MascotError(
            f"{where}: `pose: warn` is the hard hat and belongs only to "
            f"{WARN_PAGE}; every other ⚠ box stays free of the bird "
            "(assets/mascot/STYLE.md § Humour rule)"
        )

    caption = str(spec.get("caption") or "").strip()
    if not caption:
        raise MascotError(f"{where}: a mascot fence needs a `caption:`")
    check_caption(caption, where)

    side = str(spec.get("side") or "right").strip().lower()
    if side not in _SIDES:
        raise MascotError(f"{where}: `side:` must be `left` or `right`, got {side!r}")

    return scene_html(pose, caption, side)


_MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_STEP_TITLE_RE = re.compile(r"^\s*Step\s+(\S+?)\s+[—–-]")


class _StepScope:
    """Which listed step, if any, the text after the last heading belongs to.

    A `Step <id> — …` heading opens a scope when the step is in
    `NO_MASCOT_STEPS`; the next heading at the same or a higher level (the
    next step, `## Checkpoint`, …) closes it, a deeper one (a `####` inside the
    step) does not.  Shared by the fence check and the badge strip, so the
    markdown and the HTML agree on where a step ends.
    """

    def __init__(self) -> None:
        self.level: int | None = None
        self.step: str | None = None     # a listed step only
        self.sid: str | None = None      # any step

    def heading(self, level: int, text: str) -> None:
        if self.level is not None and level > self.level:
            return
        self.level = self.step = self.sid = None
        m = _STEP_TITLE_RE.match(text)
        if m:
            self.level, self.sid = level, m.group(1)
            if no_mascot_reason(self.sid):
                self.step = self.sid


def _convert(markdown: str, where: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    scope = _StepScope()
    i, n = 0, len(lines)
    while i < n:
        m = _FENCE_RE.match(lines[i])
        if not m:
            h = _MD_HEADING_RE.match(lines[i])
            if h:
                scope.heading(len(h.group(1)), h.group(2))
            hl = _HELPER_LINE_RE.match(lines[i]) if scope.sid else None
            problem = hl and helper_problem(scope.sid, hl.group(1))
            if problem:
                raise MascotError(
                    f"{where}: a **Helper:** line inside Step {scope.sid} — {problem} "
                    "(hooks/mascot.py NO_MASCOT_STEPS, CONVENTIONS.md § Helper steps)"
                )
            out.append(lines[i])
            i += 1
            continue
        token, info = m.group(2)[0] * 3, m.group(3)
        j = i + 1
        while j < n and not lines[j].strip().startswith(token):
            j += 1
        close = min(j + 1, n)
        if info != "mascot":
            out.extend(lines[i:close])          # somebody else's fence, untouched
        elif scope.step:
            raise MascotError(
                f"{where}: a mascot fence inside Step {scope.step}, a "
                f"{no_mascot_reason(scope.step)} step — no mascot at all there "
                "(hooks/mascot.py NO_MASCOT_STEPS, STYLE.md § Humour rule)"
            )
        else:
            out += ["", _scene_from_fence(lines[i + 1:j], where), ""]
        i = close
    return "\n".join(out)


# --------------------------------------------------------------------------
# the badge strip: no bird inside a listed step, whoever put it there
# --------------------------------------------------------------------------

_HTML_HEADING_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_BADGE_IMG_RE = re.compile(r"<img\b[^>]*\bclass=(['\"])mascot-badge\b[^>]*>[ \t]?")


def strip_badges(html_text: str) -> str:
    """Remove every `mascot-badge` <img> inside a `NO_MASCOT_STEPS` step.

    Works on the rendered page, after every markdown hook has run, so it does
    not matter which generator wrote the badge.  A step page is one `<h1>Step
    …` scope; a long chapter page has one `<h3>` scope per step.
    """
    if "mascot-badge" not in html_text:
        return html_text
    scope = _StepScope()
    out: list[str] = []
    pos = 0
    for m in _HTML_HEADING_RE.finditer(html_text):
        chunk = html_text[pos:m.start()]
        out.append(_BADGE_IMG_RE.sub("", chunk) if scope.step else chunk)
        out.append(m.group(0))
        scope.heading(int(m.group(1)), html.unescape(_TAG_RE.sub("", m.group(2))))
        pos = m.end()
    tail = html_text[pos:]
    out.append(_BADGE_IMG_RE.sub("", tail) if scope.step else tail)
    return "".join(out)


# --------------------------------------------------------------------------
# the sentinel -> a page-relative path
# --------------------------------------------------------------------------


def prefix_for(url: str) -> str:
    """Path from a rendered page's own directory to the asset directory."""
    url = (url or "").strip("/")
    base = posixpath.dirname(url) if url.endswith(".html") else url
    return posixpath.relpath(ASSET_ROOT, base or ".")


def resolve(html_text: str, url: str) -> str:
    if SENTINEL not in html_text:
        return html_text
    return html_text.replace(SENTINEL, prefix_for(url) + "/")


# --------------------------------------------------------------------------
# mkdocs hooks
# --------------------------------------------------------------------------


def on_page_markdown(markdown, page, config, files, **kwargs):
    if ("```mascot" not in markdown and "~~~mascot" not in markdown
            and "Helper:" not in markdown):
        return markdown
    where = getattr(getattr(page, "file", None), "src_uri", None) or "page"
    return _convert(markdown, where)


def on_page_content(html_text, page, config, files, **kwargs):
    return resolve(strip_badges(html_text), getattr(page, "url", "") or "")


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------

if __name__ == "__main__":
    fail = False

    def _ok(fn) -> bool:
        try:
            fn()
            return True
        except MascotError:
            return False

    def check(name, cond, detail=""):
        global fail
        if not cond:
            print(f"FAIL: {name}{(' — ' + detail) if detail else ''}")
            fail = True

    found = poses()
    print("--- poses ---")
    print(len(found), "files:", ", ".join(sorted(found)))
    check("twenty poses on disk", len(found) == 20, f"found {len(found)}")
    for pose in ("check", "tip", "pause", "gather", "helper", "pass", "fail",
                 "print", "carry", "kitday", "base-front", "badge", "warn"):
        check(f"pose {pose!r} exists", pose in found)
    check("titles are read from the SVG",
          found.get("hexkey") == "Revali turning a hex key",
          repr(found.get("hexkey")))
    check("every title names Revali",
          all(t.startswith("Revali") for t in found.values()),
          repr(sorted(t for t in found.values() if not t.startswith("Revali"))))

    # ---- the fence, happy path -------------------------------------------
    good = ("```mascot\n"
            "pose: hexkey\n"
            "caption: One corner square. Three to go.\n"
            "```\n")
    out = _convert(good, "manual/01-frame.md")
    print("\n--- fence ---")
    print(out.strip())
    check("figure emitted", '<figure class="mascot-scene mascot-scene--right">' in out)
    check("references the SVG, not the preview PNG",
          '@mascot/mascot-hexkey.svg' in out and ".png" not in out)
    check("alt comes from the SVG <title>", "alt='Revali turning a hex key'" in out)
    check("caption rendered", "<figcaption>One corner square. Three to go.</figcaption>" in out)
    check("size attributes present (no layout shift)", "width='220' height='220'" in out)
    check("img attributes are single-quoted (admonition titles use \")",
          '"' not in re.search(r"<img[^>]*>", out).group(0))

    left = _convert("```mascot\npose: point\ncaption: This one.\nside: left\n```\n", "p.md")
    check("side: left honoured", "mascot-scene--left" in left)

    # ---- the fence survives a step-page copy ------------------------------
    # build_steps pulls in Python-Markdown, which the venv has and a bare
    # interpreter may not; a missing third-party module SKIPs rather than fails,
    # so `python3 hooks/mascot.py` still runs everything this file owns.
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import build_steps
    except ModuleNotFoundError as exc:                  # pragma: no cover
        print(f"\n--- build_steps interop: SKIPPED ({exc.name} not installed; "
              "run .venv/bin/python for this one) ---")
    else:
        segs = build_steps._segments(good.rstrip("\n").split("\n"))
        check("build_steps keeps a mascot fence as one block",
              len(segs) == 1 and segs[0].kind == "block" and len(segs[0].lines) == 4,
              repr(segs))
        check("build_steps.rewrite_links leaves the fence alone",
              build_steps.rewrite_links(good.split("\n"), REPO / "docs/manual",
                                        REPO / "docs/manual/steps/01-frame",
                                        "01-frame") == good.split("\n"))

    # ---- validation -------------------------------------------------------
    bad = {
        "unknown pose": "```mascot\npose: dancing\ncaption: Nope.\n```\n",
        "missing pose": "```mascot\ncaption: Nope.\n```\n",
        "missing caption": "```mascot\npose: tip\n```\n",
        "caption too long": "```mascot\npose: tip\ncaption: %s\n```\n" % " ".join(
            ["word"] * (CAPTION_MAX_WORDS + 1)),
        "caption em-dash": "```mascot\npose: tip\ncaption: One thing — then another.\n```\n",
        "caption parenthetical": "```mascot\npose: tip\ncaption: One thing (maybe).\n```\n",
        "bad side": "```mascot\npose: tip\ncaption: Fine.\nside: middle\n```\n",
        "unknown key": "```mascot\npose: tip\ncaption: Fine.\nsize: big\n```\n",
        "warn off its page": "```mascot\npose: warn\ncaption: Mains is live.\n```\n",
    }
    print("\n--- rejections ---")
    for name, fixture in bad.items():
        try:
            _convert(fixture, "manual/04-ab-drives.md")
        except MascotError as exc:
            print(f"  {name}: {exc}")
            check(f"{name} names the page", "04-ab-drives" in str(exc))
            continue
        check(f"{name} rejected", False)

    try:
        ok = _convert(bad["warn off its page"], "manual/00a-mains-safety.md")
        check("warn allowed on 00a-mains-safety", "mascot-warn.svg" in ok)
    except MascotError as exc:
        check("warn allowed on 00a-mains-safety", False, str(exc))

    check("a foreign fence is untouched",
          _convert("```gate-calc\nid: x\n```\n", "p.md") == "```gate-calc\nid: x\n```\n")

    # ---- the sentinel -----------------------------------------------------
    print("\n--- paths ---")
    cases = {
        "": "manual/assets/mascot",
        "manual/steps/04-ab-drives/04-2/": "../../../assets/mascot",
        "manual/04-ab-drives/": "../assets/mascot",
        "manual/print/B00-calibration-and-jigs/": "../../assets/mascot",
        "print/plate-board/": "../../manual/assets/mascot",
        "manual/steps/b00-calibration-and-jigs/b00-5/": "../../../assets/mascot",
        "print/plate-board.html": "../manual/assets/mascot",
    }
    for url, want in cases.items():
        got = prefix_for(url)
        print(f"  {url or '(home)':52s} -> {got}")
        check(f"prefix for {url!r}", got == want, f"got {got!r}, want {want!r}")

    resolved = resolve(badge_html("check", "check"), "manual/steps/04-ab-drives/04-2/")
    print("\n--- badge ---")
    print(" ", resolved)
    check("sentinel resolved",
          "src='../../../assets/mascot/mascot-check.svg'" in resolved)
    check("badge is 28-32 px", "width='30' height='30'" in resolved)
    check("badge alt is the plain word", "alt='check'" in resolved)
    check("badge loads eagerly (no flash beside read text)", "loading='eager'" in resolved)
    check("glightbox opts out (a badge is not a figure)", "off-glb" in resolved)
    check("no sentinel survives", SENTINEL not in resolved)

    print("\n--- panel ---")
    print(" ", panel_html("pass"))
    check("panel is ~96 px", "width='96' height='96'" in panel_html("pass"))
    check("panel alt from title", "alt='Revali passing a gate'" in panel_html("pass"))

    # Everything a page emits must resolve to one of a handful of URLs.
    page_html = (badge_html("check", "check") + badge_html("tip", "tip")
                 + badge_html("check", "check") + scene_html("point", "Look here."))
    urls = set(re.findall(r"src='([^']+)'", resolve(page_html, "manual/04-x/")))
    check("repeated badges share one URL", len(urls) == 3, repr(sorted(urls)))

    # ---- the humour rule's step list --------------------------------------
    print("\n--- no-mascot steps ---")
    for reason, spec in NO_MASCOT_STEPS.items():
        print(f"  {reason:6s} {len(_expand(spec)):3d}  {spec}")
    listed = {k for spec in NO_MASCOT_STEPS.values() for k in _expand(spec)}
    print(f"  {'total':6s} {len(listed):3d} distinct steps")

    # Every listed id is a real step heading, and no listed step carries a
    # **Helper:** line (CONVENTIONS § Helper steps forbids the same steps).
    heading_re = re.compile(r"^(#{2,4})\s+Step\s+(\S+?)\s+[—–-]")
    sections: dict[tuple[str, int], list[str]] = {}
    for src in sorted((REPO / "docs/manual").glob("*.md")) + sorted(
            (REPO / "docs/manual/print").glob("*.md")):
        if src.name == "CONVENTIONS.md":
            continue
        cur, in_fence = None, False
        for line in src.read_text(encoding="utf-8").split("\n"):
            if _FENCE_RE.match(line):
                in_fence = not in_fence
            if in_fence:                       # a `# comment` in a code block
                if cur:
                    sections[cur].append(line)
                continue
            hm = heading_re.match(line)
            if hm:
                cur = _step_key(hm.group(2))
                if cur:
                    sections.setdefault(cur, [])
                continue
            if line.startswith("#") and _MD_HEADING_RE.match(line) and len(
                    line) - len(line.lstrip("#")) <= 3:
                cur = None
            elif cur:
                sections[cur].append(line)
    missing = sorted(k for k in listed if k not in sections)
    check("every NO_MASCOT_STEPS id is a step heading", not missing,
          ", ".join("%s.%d" % k for k in missing))
    bad_helpers = sorted(
        "%s.%d" % k for k, body in sections.items() for ln in body
        if (hm := _HELPER_LINE_RE.match(ln)) and helper_problem("%s.%d" % k, hm.group(1)))
    check("no **Helper:** line where the humour rule forbids one", not bad_helpers,
          ", ".join(bad_helpers))

    for sid in ("00.1", "00.14", "00a.2", "00a.4", "08.3", "08.7", "09.10", "09.11",
                "09.13", "09.34", "10.5", "10.23", "10.35", "10.50", "10.80", "08.34", "11.2", "11.3",
                "11.28", "11.33", "02.03", "B00.7", "b00.7"):
        check(f"{sid} carries no mascot", no_mascot_reason(sid) is not None)
    for sid in ("01.1", "01.14", "05.2", "10.4x", "10.24", "10.81", "11.1", "B00.5", "Ch"):
        check(f"{sid} keeps its mascot", no_mascot_reason(sid) is None)
    check("reason is reported", no_mascot_reason("10.8") == "mains"
          and no_mascot_reason("11.33") == "iron" and no_mascot_reason("06.4") == "blade"
          and no_mascot_reason("14.6") == "hot")

    b = badge_html("check", "check")
    chapter = ("<h1>Chapter 10</h1><p>%s intro</p>"
               "<h3 id='a'>Step 10.8 — Inlet<a class='headerlink'>¶</a></h3>"
               "<p class='admonition-title'>%s Check</p><h4>Detail</h4><p>%s Tip</p>"
               "<h3 id='b'>Step 10.24 — PSU</h3><p class='admonition-title'>%s Check</p>"
               "<h2>Checkpoint 10</h2><p>%s Check</p>") % (b, b, b, b, b)
    stripped = strip_badges(chapter)
    check("chapter page: badges gone inside the mains step",
          "<p class='admonition-title'>Check</p>" in stripped
          and "<p>Tip</p>" in stripped, stripped)
    check("chapter page: badges kept outside it", stripped.count("mascot-badge") == 3,
          str(stripped.count("mascot-badge")))
    step_page = ('<h1 id="step-1133">Step 11.33 — Solder the fans</h1>'
                 '<details class="note"><summary>%s Gather</summary></details>'
                 '<p class="admonition-title">%s Check</p>'
                 '<p class="step-helper">%s Holds it</p>') % (b, b, b.replace("'", '"'))
    check("step page: every badge gone, either quote style",
          "mascot-badge" not in strip_badges(step_page), strip_badges(step_page))
    ordinary = '<h1 id="s">Step 01.1 — Lay out</h1><p>%s Check</p>' % b
    check("step page: an ordinary step keeps its badge", strip_badges(ordinary) == ordinary)

    fence = "```mascot\npose: tip\ncaption: Fine.\n```\n"
    try:
        _convert("### Step 10.8 — Inlet\n\n" + fence, "manual/10-wiring.md")
        check("a fence inside a mains step is rejected", False)
    except MascotError as exc:
        print(f"  fence in 10.8: {exc}")
        check("the rejection names the page and step",
              "10-wiring" in str(exc) and "10.8" in str(exc))
    check("a fence after the listed step closes is allowed",
          "mascot-scene" in _convert("### Step 10.8 — Inlet\n\n## Checkpoint 10\n\n"
                                     + fence, "manual/10-wiring.md"))
    check("a fence inside an ordinary step is allowed",
          "mascot-scene" in _convert("### Step 10.24 — PSU\n\n" + fence, "p.md"))

    # ---- Helper lines: forbidden in a listed step, the D4 exception -------
    print("\n--- helper lines ---")
    helper_cases = {
        # (step heading, helper job) -> allowed?
        ("Step 10.8 — Inlet", "Holds the cord out of the way."): False,
        ("Step 11.33 — Solder the fans", "Hands over the solder."): False,
        ("Step 10.77 — Meter the PE path", "Records each reading on the sheet while the adult holds the probes."): True,
        ("Step 10.78 — Meter the heater", "Reads the meter aloud."): False,
        ("Step 10.75 — Meter the frame", "Holds the black probe on the lug."): False,
        ("Step 10.75 — Meter the frame", "Records the reading."): True,
        ("Step 10.24 — PSU", "Holds the PSU square while you start the screws."): True,
    }
    for (head, job), allowed in helper_cases.items():
        md = "### %s\n\n**Do:** Something.\n\n**Check:** Fine.\n\n**Helper:** %s\n" % (head, job)
        try:
            _convert(md, "manual/10-wiring.md")
            got = True
        except MascotError as exc:
            got = False
            print(f"  refused: {exc}")
        check(f"helper in {head.split(' —')[0]} ({job[:28]}…) "
              f"{'allowed' if allowed else 'refused'}", got == allowed)
    check("a quoted **Helper:** line is caught too",
          not _ok(lambda: _convert("### Step 10.8 — Inlet\n\n> **Helper:** Holds it.\n",
                                   "manual/10-wiring.md")))
    check("a Helper line after the listed step closes is allowed",
          _ok(lambda: _convert("### Step 10.8 — Inlet\n\n## Checkpoint 10\n\n"
                               "**Helper:** Ticks the list.\n", "manual/10-wiring.md")))
    check("a Helper line in a code fence is not a Helper line",
          _ok(lambda: _convert("### Step 10.8 — Inlet\n\n```text\n**Helper:** x\n```\n",
                               "manual/10-wiring.md")))

    # ---- the Checkpoint reward -------------------------------------------
    print("\n--- reward ---")
    bird = reward_html("02", "You built the four Z drives. 11 gummy worms.", "cp")
    print(" ", bird)
    check("reward: pass scene", "mascot-pass.svg" in bird and "checkpoint-reward" in bird)
    text = reward_html("00a", "You built a safe mains plan. 2 gummy worms.", "cp")
    check("reward: 00a is text only", "mascot-" not in text
          and "checkpoint-reward--text" in text, text)
    check("reward: Checkpoint 10 gets the bird",
          "mascot-pass.svg" in reward_html("10", "Wired. 14 gummy worms.", "cp"))
    check("reward: caption cap enforced",
          not _ok(lambda: reward_html("02", " ".join(["w"] * 19), "cp")))
    check("reward: no en/em dash in a caption",
          not _ok(lambda: reward_html("B03", "Plates 7–9 printed.", "cp")))

    if fail:
        raise SystemExit(1)
    print("\nAll self-tests passed.")
