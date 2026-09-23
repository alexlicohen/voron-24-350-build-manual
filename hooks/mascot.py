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
    words = len(caption.split())
    if words > CAPTION_MAX_WORDS:
        raise MascotError(
            f"{where}: caption is {words} words, budget is {CAPTION_MAX_WORDS}"
        )
    if _DASH_RE.search(caption):
        raise MascotError(f"{where}: caption may not use an em-dash — {caption!r}")
    if _PAREN_RE.search(caption):
        raise MascotError(f"{where}: caption may not use a parenthetical — {caption!r}")

    side = str(spec.get("side") or "right").strip().lower()
    if side not in _SIDES:
        raise MascotError(f"{where}: `side:` must be `left` or `right`, got {side!r}")

    return scene_html(pose, caption, side)


def _convert(markdown: str, where: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        m = _FENCE_RE.match(lines[i])
        if not m:
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
        else:
            out += ["", _scene_from_fence(lines[i + 1:j], where), ""]
        i = close
    return "\n".join(out)


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
    if "```mascot" not in markdown and "~~~mascot" not in markdown:
        return markdown
    where = getattr(getattr(page, "file", None), "src_uri", None) or "page"
    return _convert(markdown, where)


def on_page_content(html_text, page, config, files, **kwargs):
    return resolve(html_text, getattr(page, "url", "") or "")


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------

if __name__ == "__main__":
    fail = False

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

    if fail:
        raise SystemExit(1)
    print("\nAll self-tests passed.")
