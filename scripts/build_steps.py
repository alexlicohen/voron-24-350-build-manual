"""mkdocs hook: generate one page per step from the chapter markdown.

`docs/manual/NN-*.md` and `docs/manual/print/B*.md` stay the single source.
On every build this hook re-derives `docs/manual/steps/<chapter-slug>/`:

    index.md      chapter overview — title, Time/Sessions, a card grid of steps
    start.md      "Before you start Chapter NN" — the chapter header material
    <step>.md     one page per `### Step NN.M` block
    checkpoint-NN.md   the `## Checkpoint NN` list (+ Common mistakes / Next)
    note-<slug>.md     a `##` section that carries body text but no steps

Contract and layout rules: docs/manual/CONVENTIONS.md § "Step pages".

Navigation: docs/.nav.yml owns the whole site nav (five tabs). Its Build and
Print tabs list the generated chapter/batch `index.md` overviews by path; the
step pages themselves stay out of the nav — `steps/.nav.yml`, written by
`build()` below, carries `hide: true`. Prev/next and the breadcrumb are static
markup emitted here, so step navigation never depends on nav order.

Prev/next follow file order, with one exception: when a chapter's `## Next`
section *leads* with a link to a step (`[Step 11.67](11-skirts-panels-door.md#step-1167-…)`),
the Next button on the chapter's last page goes to that step instead of the
next file's first page. That is how a chapter whose bench successor is not
the next file (Ch 12 → Ch 11 Part A, per the 00-index timeline) says so once,
in its own prose, and the button agrees. A lead link to a chapter or a
non-step anchor changes nothing.

The same override is available mid-chapter: a `## Checkpoint` whose own body
carries a `**Next:** [Step 7.1](07-ab-belts.md#step-071-…)` line sends ITS
Next button there instead of the page that follows it in the file (Ch 06's
Checkpoint 06, whose next page in file order is Part B/06b.1 even though the
manual's own text says to go to Ch 07 and come back to 06b from Ch 13). The
line stays visible in the rendered checklist; only its first valid link is
read.

A **step** body can carry the same `**Next:** [..](..)` line (13.34 hands off
to Ch 06b, not to 13.35): it renders visibly after Source and overrides that
step page's Next button the same way.

Panel crops: an image line may declare `{ crop="x0 y0 x1 y1" }` (page
fractions) on a `manual-pages/` or `sb-pages/` PNG. The step page shows the
committed crop from `assets/manual-crops/` (scripts/crop_panels.py owns the box
parse, file name and `--check`) with a "Full page" link to the original; the
long chapter page keeps the whole page. A declared crop whose PNG is missing
fails the build.

Checkpoint rewards: every `## Checkpoint` page ends its own section with a
reward from `mascot.reward_html` — the `pass` scene, captioned "You built <X>.
<N> gummy worms." from the Checkpoint's `**Built:** <X>` line (assembly
chapters; ≤12 words) or "<Checkpoint> passed." without one, and for a print
batch "Batch Bnn printed: plate(s) … of 22, … of 157.0 h." from slicer/plates.py
and slicer/check_docs.py. Worms: one per 30 min of the chapter's
`**Sessions:**` bench time (split across a chapter's Checkpoints by their
Pause segments), one per plate for a batch. The long chapter page gets the same
reward at the end of each Checkpoint section.

The directory is gitignored and rebuilt by `mkdocs build`; never hand-edit it.
Writes are content-compared so `mkdocs serve` does not loop on its own output.
"""

from __future__ import annotations

import html
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from markdown.extensions.toc import slugify

REPO = Path(__file__).resolve().parent.parent

import sys  # noqa: E402

sys.path.insert(0, str(REPO / "hooks"))
import mascot  # noqa: E402  (hooks/mascot.py — the raven's markup and asset paths)

sys.path.insert(0, str(REPO / "scripts"))
import parts  # noqa: E402  (scripts/parts.py — Parts parse, counts, bins, kit-BOM source)
import crop_panels  # noqa: E402  (scripts/crop_panels.py — crop declarations and file names)
# One owner for what a `Pause:` line says: build_tonight.py's parser, whose
# `(pre-kit)` group is what "Before the kit" plans from (build_printables.py
# imports its chapter-title rule the same way).
from build_tonight import _PAUSE_RE as _TONIGHT_PAUSE_RE  # noqa: E402

sys.path.insert(0, str(REPO / "slicer"))
import check_docs  # noqa: E402  (slicer/check_docs.py — per-batch hours, rounded as the docs print them)
from plates import PLATES, run_of  # noqa: E402  (slicer/plates.py — which plates a batch has)


class BuildStepsError(Exception):
    """A chapter declares something the step pages cannot honour — fails the build."""

DOCS = REPO / "docs"
MANUAL = DOCS / "manual"
PRINT = MANUAL / "print"
STEPS = MANUAL / "steps"

# Chapter files that are indexes/generated/meta, never step sources.
_EXCLUDE = {"00-index.md", "00-tonight.md", "CONVENTIONS.md"}

_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*?)\s*$")
_STEP_HEAD_RE = re.compile(r"^Step\s+([A-Za-z]?\d+[A-Za-z]?\.\d+)\s*(?:[—–-]\s*)?(.*)$")
_CHECKPOINT_HEAD_RE = re.compile(r"^Checkpoint\b\s*(\S*)", re.IGNORECASE)
# A checkpoint whose Next button should not just fall through to the next page
# in file order (e.g. a mid-chapter Checkpoint whose text says "stop here and
# go to a different chapter") carries a `**Next:** [text](file.md#anchor)`
# line in its own body; it stays visible and is also read as the override.
_NEXT_OVERRIDE_RE = re.compile(r"^\*\*Next:\*\*\s*(.+)$")
_IMAGE_LINE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]*)\)(?P<attr>\s*\{[^}]*\})?\s*$")
_NOIMAGE_RE = re.compile(r"^\*?\(no image[^\n]*\)\*?\s*$", re.IGNORECASE)
_PARTS_RE = parts.PARTS_RE
_PAUSE_RE = re.compile(r"^>?\s*Pause:\s")
_SOURCE_RE = re.compile(r"^>?\s*Source:\s")
# House markers the step layout reorders around (callouts.py renders them).
_DO_RE = re.compile(r"^\*{0,2}Do:\*{0,2}(?:\s|$)")
_CHECK_RE = re.compile(r"^\*{0,2}Check:\*{0,2}(?:\s|$)")
_TIP_RE = re.compile(r"^\*{0,2}Tip:\*{0,2}(?:\s|$)")
_WARN_RE = re.compile(r"^⚠")
_DESC_RE = re.compile(r"^\*{0,2}What you're looking at:\*{0,2}\s*(.*)$")
# A helper (child) job for this step: rendered right after Check, and counted on
# the overview, the chapter start page and the Tonight view.
_HELPER_RE = re.compile(r"^\*{0,2}Helper:\*{0,2}\s*(.*)$")
# A Checkpoint's authored "what you built" line, the reward's caption.
_BUILT_RE = re.compile(r"^\*\*Built:\*\*\s*(.*?)\s*$")
BUILT_MAX_WORDS = 12
WORM_MINUTES = 30
_SESSIONS_MIN_RE = re.compile(r"(\d+)\s*×\s*~?\s*(\d+)\s*min")
_TIME_HOURS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*h\b")
# `{ crop="x0 y0 x1 y1" }` on an image line, and the page PNG it crops.
_CROP_ATTR_RE = re.compile(r"""\s*\bcrop=(["'])([^"']*)\1""")
_PAGE_PNG_RE = re.compile(r"(manual|sb)-p(\d{3})\.png$")
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_TABLE_ROW_RE = re.compile(r"^\s*\|")
_BQ_PREFIX_RE = re.compile(r"^>\s?")
_TIME_RE = re.compile(r"^\*\*Time:\*\*\s*(.+)$")
_SESSIONS_RE = re.compile(r"^\*\*Sessions:\*\*\s*(.+)$")
_HR_RE = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})\s*$")
# Any markdown link/image destination: ](dest) or ](dest "title")
_LINK_RE = re.compile(r"\]\(\s*([^()\s]+?)\s*(\"[^\"]*\")?\)")
# Images that are the step's primary illustration (a scanned manual page).
_PRIMARY_IMG_DIRS = ("assets/manual-pages/", "assets/sb-pages/")

# Cumulative "state at the end of this chapter" CAD renders, built by
# scripts/cad_render/render_steps.py --chapters into docs/manual/assets/cad/.
# Only chapters that have one get the before/after figure; the rest (wiring,
# software, startup, calibration) simply do not show one.  The words under each
# figure are the `caption` and `note_350` of that chapter's entry in
# assets/cad/steps.yml, so the manifest that decides what the picture shows also
# says what it means; nothing in it is written twice.
_CH_NUM_RE = re.compile(r"^(\d+[a-z]?)-")
CHAPTER_SHOTS: dict[str, tuple[str | None, str]] = {}   # stem -> (before, after)
CHAPTER_CAPTIONS: dict[str, tuple[str, str]] = {}   # "04" -> (title, caption + caveat)
CAD_YML = MANUAL / "assets/cad/steps.yml"
# Fallback when a render exists but steps.yml has no entry for it.
_CAD_PROVENANCE = "Voron 2.4r2 CAD, which is the 250 machine; yours is the 350."

# Populated by on_pre_build; read by on_page_markdown.
STEP_URLS: dict[str, str] = {}          # "04.2" -> "manual/steps/04-ab-drives/04-2.md"
ANCHOR_URLS: dict[tuple[str, str], str] = {}  # (chapter stem, anchor) -> step page src path
CHAPTER_OVERVIEW: dict[str, str] = {}   # chapter stem -> overview src path
CHAPTER_FIRST: dict[str, str] = {}      # chapter stem -> first page src path
STEP_ANCHORS: dict[str, set[str]] = {}  # chapter stem -> its step headings' anchors


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------


@dataclass
class Block:
    level: int          # 0 = preamble, 1/2/3 = heading depth
    heading: str | None
    body: list[str] = field(default_factory=list)


@dataclass
class Page:
    kind: str           # front | step | checkpoint | note
    slug: str
    title: str          # h1 text, plain markdown
    body: list[str]
    step_id: str | None = None
    section: str | None = None
    ordinal: int | None = None   # 1-based position among the chapter's steps
    images: list[tuple[str, str, str]] = field(default_factory=list)
    next_override: list[str] = field(default_factory=list)  # a `**Next:** [...]` line, if this
                                                              # page (e.g. a mid-chapter Checkpoint)
                                                              # sends the Next button somewhere
                                                              # other than the following page
    own_end: int | None = None   # Checkpoint: where its own section ends in `body` (the
                                 # chapter tail rides after it); the reward goes here
    built: str | None = None     # Checkpoint: its `**Built:**` text, line removed from body


@dataclass
class Chapter:
    path: Path
    stem: str
    slug: str
    title: str          # "Chapter 04 — A/B drive units and front idlers"
    short: str          # "Ch 04"
    time: str | None
    sessions: str | None
    pages: list[Page] = field(default_factory=list)
    n_steps: int = 0
    segments: list["Segment"] = field(default_factory=list)
    gather: dict[str, list[str]] = field(default_factory=dict)
    next_body: list[str] = field(default_factory=list)   # the `## Next` section's lines


def _split_blocks(text: str) -> list[Block]:
    """Split markdown into heading-delimited blocks, ignoring fenced code."""
    blocks = [Block(0, None)]
    fence: str | None = None
    for line in text.split("\n"):
        m = _FENCE_RE.match(line)
        if m:
            token = m.group(1)[0] * 3
            if fence is None:
                fence = token
            elif line.strip().startswith(fence):
                fence = None
            blocks[-1].body.append(line)
            continue
        if fence is None:
            hm = _HEADING_RE.match(line)
            if hm:
                blocks.append(Block(len(hm.group(1)), hm.group(2)))
                continue
        blocks[-1].body.append(line)
    return blocks


def _strip_edges(lines: list[str]) -> list[str]:
    out = list(lines)
    while out and not out[0].strip():
        out.pop(0)
    while out and (not out[-1].strip() or _HR_RE.match(out[-1])):
        out.pop()
    return out


_plain = parts.plain


def _chapter_files() -> list[Path]:
    assembly = sorted(f for f in MANUAL.glob("*.md") if f.name not in _EXCLUDE)
    batches = sorted(PRINT.glob("B*.md")) if PRINT.exists() else []
    return assembly + batches


def _slug_for_step(step_id: str) -> str:
    return step_id.replace(".", "-").lower()


def parse_chapter(path: Path) -> Chapter | None:
    text = path.read_text(encoding="utf-8")
    blocks = _split_blocks(text)

    h1 = next((b for b in blocks if b.level == 1), None)
    if h1 is None:
        return None
    start = blocks.index(h1)

    steps_present = any(
        b.level in (2, 3) and b.heading and _STEP_HEAD_RE.match(b.heading)
        for b in blocks
    )
    if not steps_present:
        return None

    title = h1.heading or path.stem
    m = re.match(r"^(?:Chapter|Batch)\s+(\S+)", title)
    short = f"Ch {m.group(1)}" if m and title.startswith("Chapter") else (
        f"Batch {m.group(1)}" if m else title
    )

    front = _strip_edges(h1.body)
    time = sessions = None
    for line in front:
        tm = _TIME_RE.match(line)
        if tm and time is None:
            time = tm.group(1).strip()
        sm = _SESSIONS_RE.match(line)
        if sm and sessions is None:
            sessions = sm.group(1).strip()

    slug = path.stem.lower()
    chapter = Chapter(path=path, stem=path.stem, slug=slug, title=title,
                      short=short, time=time, sessions=sessions)

    pages: list[Page] = []
    if front:
        pages.append(Page(kind="front", slug="start",
                          title=f"Before you start {short_title(short)}",
                          body=front))

    pending_title: str | None = None
    pending_body: list[str] = []
    current_section: str | None = None
    ordinal = 0
    trailing: list[str] = []   # Common mistakes / Next, appended to the last page

    def flush_pending_note() -> None:
        nonlocal pending_title, pending_body
        body = _strip_edges(pending_body)
        if pending_title and body:
            pages.append(Page(kind="note",
                              slug="note-" + (slugify(pending_title, "-") or "section"),
                              title=pending_title, body=body))
        pending_title, pending_body = None, []

    for block in blocks[start + 1:]:
        head = block.heading or ""
        body = _strip_edges(block.body)

        step_m = _STEP_HEAD_RE.match(head) if block.level in (2, 3) else None
        if step_m:
            ordinal += 1
            step_id, step_title = step_m.group(1), step_m.group(2).strip()
            intro = _strip_edges(pending_body)
            if pending_title:
                section = _plain(pending_title)
                current_section = None if section.lower() == "steps" else section
            pending_title, pending_body = None, []
            step_body = (intro + ["", ""] if intro else []) + body
            pages.append(Page(kind="step", slug=_slug_for_step(step_id),
                              title=head, step_id=step_id, section=current_section,
                              ordinal=ordinal, body=step_body,
                              next_override=[seg.lines[0] for seg in _segments(step_body)
                                             if seg.kind == "next"]))
            continue

        if block.level == 2:
            cp = _CHECKPOINT_HEAD_RE.match(head)
            if cp:
                flush_pending_note()
                tag = cp.group(1).strip() or ""
                override = [l for l in body if _NEXT_OVERRIDE_RE.match(l.strip())]
                built = [l for l in body if _BUILT_RE.match(l.strip())]
                if len(built) > 1:
                    raise BuildStepsError("%s: %s has %d **Built:** lines; one per Checkpoint"
                                          % (path.name, head, len(built)))
                body = _strip_edges([l for l in body if l not in built])
                pages.append(Page(kind="checkpoint",
                                  slug="checkpoint-" + (tag.lower() or "end"),
                                  title=head, body=body, next_override=override,
                                  own_end=len(body),
                                  built=_BUILT_RE.match(built[0].strip()).group(1) if built else None))
                continue
            if re.match(r"^Common mistakes", head, re.IGNORECASE) or head.strip() == "Next":
                trailing += ["", f"## {head}", ""] + body
                if head.strip() == "Next":
                    chapter.next_body = body
                continue
            flush_pending_note()
            pending_title, pending_body = head, body
            continue

        # Anything else (a stray h3, or preamble text) rides with the last page.
        if pages:
            pages[-1].body += ["", ""] + ([f"### {head}"] if head else []) + body
        else:
            pending_body += ["", ""] + ([f"## {head}"] if head else []) + body

    flush_pending_note()
    tail = _strip_edges(trailing)
    if tail and pages:
        pages[-1].body += ["", ""] + tail

    chapter.pages = pages
    chapter.n_steps = ordinal
    return chapter


def short_title(short: str) -> str:
    return short.replace("Ch ", "Chapter ")


def _short_meta(value: str) -> str:
    """Keep only the quantity from a `**Time:**` / `**Sessions:**` line."""
    value = _plain(value)
    value = re.split(r"\s+[—–]\s+|\s*\(", value, maxsplit=1)[0]
    return value.strip().rstrip(".,")


# --------------------------------------------------------------------------
# link rewriting
# --------------------------------------------------------------------------


def _rel(src_dir: Path, dest_dir: Path, target: str) -> str:
    """Re-express a link relative to src_dir so it resolves from dest_dir."""
    import os

    resolved = os.path.normpath(str(src_dir / target))
    return os.path.relpath(resolved, str(dest_dir)).replace("\\", "/")


def rewrite_links(lines: list[str], src_dir: Path, dest_dir: Path,
                  chapter_stem: str) -> list[str]:
    """Rewrite relative links/images for a page moved to dest_dir.

    `<chapter>.md#step-…` retargets the generated step page; a bare
    `<chapter>.md` retargets that chapter's overview; everything else is
    re-based path-wise so it still resolves.
    """

    def one(m: re.Match) -> str:
        dest, title = m.group(1), m.group(2) or ""
        if re.match(r"^[a-z][a-z0-9+.-]*:", dest, re.IGNORECASE) or dest.startswith(("#", "/", "<")):
            if dest.startswith("#"):
                anchor = dest[1:]
                page = ANCHOR_URLS.get((chapter_stem, anchor))
                if page:
                    return "](%s%s)" % (_rel(DOCS, dest_dir, page), (" " + title) if title else "")
            return m.group(0)

        path, _, frag = dest.partition("#")
        if path.endswith(".md"):
            import os
            stem = Path(path).stem
            target_stem = stem
            if frag and (target_stem, frag) in ANCHOR_URLS:
                page = ANCHOR_URLS[(target_stem, frag)]
                return "](%s%s)" % (_rel(DOCS, dest_dir, page), (" " + title) if title else "")
            if not frag and target_stem in CHAPTER_OVERVIEW:
                page = CHAPTER_OVERVIEW[target_stem]
                return "](%s%s)" % (_rel(DOCS, dest_dir, page), (" " + title) if title else "")

        new = _rel(src_dir, dest_dir, path)
        return "](%s%s%s)" % (new, ("#" + frag) if frag else "", (" " + title) if title else "")

    return [_LINK_RE.sub(one, line) for line in lines]


# --------------------------------------------------------------------------
# step body layout
# --------------------------------------------------------------------------


_split_top_level = parts.split_top_level
_CODE_SPAN_RE = parts.CODE_SPAN_RE
_load_part_thumbs = parts.load_part_thumbs
_thumb_for = parts.thumb_for


_parts_items = parts.parts_items


def _parts_block(line: str, dest_dir: Path) -> list[str]:
    body = _PARTS_RE.match(line).group(1).strip()
    plain = _plain(body).strip().rstrip(".").lower()
    if not body or plain in {"none", "—", "-", "n/a"}:
        return ["**Parts:** " + (body or "none")]
    items = _split_top_level(body, ";")
    if len(items) == 1:
        items = _split_top_level(body, "·")
    items = [i.strip().rstrip(".").strip() for i in items if i.strip()]
    if not items:
        return ["**Parts:** " + body]
    out = ['<div class="step-parts" markdown="1">', "", "**Parts:**", ""]
    for item in items:
        thumb = _thumb_for(item, dest_dir)
        out.append("- " + (("![](%s){ .step-parts__thumb } " % thumb) if thumb else "") + item)
    out += ["", "</div>"]
    return out


def _parts_list_block(fld: "parts.Field", dest_dir: Path) -> list[str]:
    """A list-form Parts field: one bullet per item, thumb for printed parts,
    and a muted source (kit box, bin, hand-set source, tool, on the bench)."""
    out = ['<div class="step-parts" markdown="1">', "", "**Parts:**", ""]
    for it in fld.items:
        thumb = _thumb_for(it.text, dest_dir)
        out.append("- " + (("![](%s){ .step-parts__thumb } " % thumb) if thumb else "")
                   + it.body + _src(it.note))
    if fld.stray:
        out += [""] + fld.stray
    out += ["", "</div>"]
    return out


def _logical(line: str) -> str:
    """The line with one optional `> ` blockquote marker off (as callouts.py)."""
    return _BQ_PREFIX_RE.sub("", line, count=1)


def _marker(line: str) -> str | None:
    """Which house marker this line opens, if any."""
    if _IMAGE_LINE_RE.match(line):
        return "image"
    if _NOIMAGE_RE.match(line.strip()):
        return "noimage"
    if _PAUSE_RE.match(line):
        return "pause"
    if _SOURCE_RE.match(line):
        return "source"
    s = _logical(line)
    if _PARTS_RE.match(s):
        return "parts"
    if _DO_RE.match(s):
        return "do"
    if _CHECK_RE.match(s):
        return "check"
    if _TIP_RE.match(s):
        return "tip"
    if _WARN_RE.match(s):
        return "warn"
    if _DESC_RE.match(s):
        return "desc"
    if _HELPER_RE.match(s):
        return "helper"
    if _NEXT_OVERRIDE_RE.match(s):
        return "next"
    return None


def _is_boundary(line: str) -> bool:
    """True where a marker's logical body must stop (callouts.py's own rule)."""
    s = _logical(line)
    if _HEADING_RE.match(s) or _HR_RE.match(s) or _FENCE_RE.match(s):
        return True
    return _marker(line) is not None


def _run(lines: list[str], i: int) -> int:
    """End index (exclusive) of a marker line's logical body."""
    j = i + 1
    while j < len(lines) and lines[j].strip() and not _is_boundary(lines[j]):
        j += 1
    return j


def _absorb_lead(lines: list[str], end: int) -> int:
    """Pull a list or code block sitting directly under a Do line into the Do.

    The house form for a multi-action step is a numbered list of ≤3
    imperatives, and a command a Do line ends by introducing has to stay with
    it — both are part of the lead, not loose body text.
    """
    while True:
        k = end
        while k < len(lines) and not lines[k].strip():
            k += 1
        if k >= len(lines) or k - end > 1:
            return end
        fence = _FENCE_RE.match(lines[k])
        if fence:
            token = fence.group(1)[0] * 3
            j = k + 1
            while j < len(lines) and not lines[j].strip().startswith(token):
                j += 1
            end = min(j + 1, len(lines))
            continue
        if not _LIST_ITEM_RE.match(lines[k]):
            return end
        last = k
        while k < len(lines):
            if not lines[k].strip():
                nxt = k + 1
                while nxt < len(lines) and not lines[nxt].strip():
                    nxt += 1
                if (nxt < len(lines) and not _is_boundary(lines[nxt])
                        and (_LIST_ITEM_RE.match(lines[nxt]) or lines[nxt].startswith("  "))):
                    k = nxt
                    continue
                break
            if _is_boundary(lines[k]):
                break
            k += 1
            last = k
        end = last


@dataclass
class _Seg:
    kind: str
    lines: list[str]


def _segments(lines: list[str]) -> list[_Seg]:
    """Split a step body into marker/prose/block segments, in source order."""
    segs: list[_Seg] = []
    i, n = 0, len(lines)
    tail = False
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        s = _logical(line)
        if tail:
            # Common mistakes / Next ride on the chapter's last page; from the
            # first heading down everything stays visible, in source order.
            segs.append(_Seg("block", [line]))
            i += 1
            continue
        fence = _FENCE_RE.match(line)
        if fence:
            token = fence.group(1)[0] * 3
            j = i + 1
            while j < n and not lines[j].strip().startswith(token):
                j += 1
            j = min(j + 1, n)
            segs.append(_Seg("block", lines[i:j]))
            i = j
            continue
        if _HEADING_RE.match(s):
            tail = True
            segs.append(_Seg("block", [line]))
            i += 1
            continue
        if _HR_RE.match(s):
            i += 1
            continue
        kind = _marker(line)
        if kind == "image":
            segs.append(_Seg("image", [line.strip()]))
            i += 1
            continue
        if kind == "noimage":
            segs.append(_Seg("noimage", [line.strip().strip("*")]))
            i += 1
            continue
        if kind:
            j = _run(lines, i)
            if kind == "do":
                j = _absorb_lead(lines, j)
            elif kind == "parts" and not _PARTS_RE.match(_logical(line)).group(1).strip():
                # List form: `**Parts:**`, a blank line, one bullet per item.
                j = parts.absorb_list(lines, j, _is_boundary)
            segs.append(_Seg(kind, lines[i:j]))
            i = j
            continue
        if _TABLE_ROW_RE.match(s) or _LIST_ITEM_RE.match(line) or line.lstrip().startswith(("<", ">")):
            kind = "block"
        else:
            kind = "prose"
        j = _run(lines, i)
        segs.append(_Seg(kind, lines[i:j]))
        i = j

    # A paragraph that introduces or reads out a table/list/code block belongs
    # with it, so it stays visible instead of being collapsed away from what it
    # explains. Judged on the original kinds, so promotion never cascades.
    kinds = [s.kind for s in segs]
    for n, seg in enumerate(segs):
        if seg.kind != "prose":
            continue
        if (n and kinds[n - 1] == "block") or (n + 1 < len(kinds) and kinds[n + 1] == "block"):
            seg.kind = "block"
    return segs


def _describe(seg: _Seg) -> list[str]:
    """Prose for the collapsed block; the description keeps its text, not its label."""
    if seg.kind != "desc":
        return list(seg.lines)
    head = _DESC_RE.match(_logical(seg.lines[0]))
    return [head.group(1).strip()] + list(seg.lines[1:])


def _helper_text(lines: list[str]) -> str:
    """The job in a `**Helper:**` run, label stripped, wrapped onto one line."""
    m = _HELPER_RE.match(_logical(lines[0]))
    parts = [m.group(1).strip()] + [_logical(l).strip() for l in lines[1:]]
    return " ".join(p for p in parts if p).strip()


def helper_jobs(body: list[str]) -> list[str]:
    """Every helper job in a step body, in source order (usually one)."""
    return [_helper_text(seg.lines) for seg in _segments(body) if seg.kind == "helper"]


def helper_steps(chapter: Chapter) -> list[Page]:
    return [p for p in chapter.pages
            if p.kind == "step" and p.step_id and helper_jobs(p.body)]


# A code block this long (or this long and this wide) cannot be read in the
# half-width text column of the landscape split: the step page stacks instead
# (picture on top, text and code full width). Widget fences are not code.
WIDE_CODE_LINES = 12
WIDE_CODE_MIN_LINES, WIDE_CODE_COLS = 5, 72
_WIDGET_FENCES = ("gate-calc", "tap-tree", "mascot")


def _has_wide_code(lines: list[str]) -> bool:
    i, n = 0, len(lines)
    while i < n:
        m = _FENCE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        token = m.group(1)[0] * 3
        lang = lines[i].strip()[len(m.group(1)):].strip().split(" ")[0].lstrip("{.")
        j = i + 1
        while j < n and not lines[j].strip().startswith(token):
            j += 1
        code = lines[i + 1:j]
        if lang not in _WIDGET_FENCES and (
                len(code) >= WIDE_CODE_LINES
                or (len(code) >= WIDE_CODE_MIN_LINES
                    and max(len(l) for l in code) > WIDE_CODE_COLS)):
            return True
        i = j + 1
    return False


# Under the step's scanned manual page or panel crop: glightbox makes every
# figure image tappable, and nothing else says so. Kept out of search.
_ENLARGE_HINT = '<p class="step-figure__hint" data-search-exclude>Tap to enlarge</p>'


def layout_step(page: Page, chapter: Chapter) -> list[str]:
    """Action-first step page: Do, Check, the helper's job, then the segment's
    Gather block and Parts, the collapsed description, then ⚠/Tip, Pause and
    Source (CONVENTIONS.md § "Action-first steps" and § "Helper steps")."""
    dest_dir = STEPS / chapter.slug
    segs = _segments(page.body)

    images = [s.lines[0] for s in segs if s.kind == "image"]
    noimage = [s.lines[0] for s in segs if s.kind == "noimage"]
    do: list[str] = []
    parts_md: list[str] = []
    check: list[str] = []
    helper: list[str] = []
    desc: list[str] = []
    other: list[str] = []
    pause: list[str] = []
    source: list[str] = []
    nxt: list[str] = []
    for seg in segs:
        if seg.kind == "do":
            do += seg.lines + [""]
        elif seg.kind == "parts":
            fld = parts.parse_field(seg.lines)
            if fld.form == "list":
                parts_md += _parts_list_block(fld, dest_dir) + [""]
            else:
                parts_md += _parts_block(" ".join(l.strip() for l in seg.lines), dest_dir) + [""]
        elif seg.kind == "check":
            check += seg.lines + [""]
        elif seg.kind == "helper":
            helper.append(_helper_text(seg.lines))
        elif seg.kind in ("desc", "prose"):
            desc += _describe(seg) + [""]
        elif seg.kind in ("warn", "tip", "block"):
            other += seg.lines + [""]
        elif seg.kind == "pause":
            pause += seg.lines + [""]
        elif seg.kind == "source":
            source += seg.lines + [""]
        elif seg.kind == "next":
            nxt += seg.lines + [""]

    def key(img: str) -> int:
        src = _IMAGE_LINE_RE.match(img).group("src")
        return 0 if any(d in src for d in _PRIMARY_IMG_DIRS) else 1

    images.sort(key=key)

    wide = " step-body--wide" if _has_wide_code(page.body) else ""
    out: list[str] = ['<div class="step-body%s" markdown="1">' % wide, ""]
    out += ['<div class="step-figure" markdown="1">', ""]
    if images:
        for n, img in enumerate(images):
            m = _IMAGE_LINE_RE.match(img)
            cls = "step-figure__main" if n == 0 else "step-figure__extra"
            attr = (m.group("attr") or "").strip()
            if attr:
                attr = attr[1:-1].strip()
            hint = (n == 0 and key(img) == 0 and "off-glb" not in attr)
            crop = _crop_file(m.group("src"), attr)
            if crop:
                # The committed crop, larger in the column; the page it came
                # from one tap away (glightbox opens it zoomable).
                attr = _CROP_ATTR_RE.sub("", attr).strip()
                rel = Path(os.path.relpath(crop_panels.CROPS_DIR / crop, dest_dir)).as_posix()
                img = "![%s](%s){ %s.%s .step-figure__crop }\n[Full page](%s){ .glightbox .step-figure__full data-type=\"image\" }" % (
                    m.group("alt"), rel, (attr + " ") if attr else "", cls, m.group("src"))
            elif attr:
                img = "![%s](%s){ %s .%s }" % (m.group("alt"), m.group("src"), attr, cls)
            else:
                img = "![%s](%s){ .%s }" % (m.group("alt"), m.group("src"), cls)
            out += [img, ""]
            if hint:
                out += [_ENLARGE_HINT, ""]
        # A step can carry both renders and a "(no image — …)" note that says
        # where the missing view lives; keep the note rather than dropping it.
        for caption in noimage:
            out += ['<p class="step-figure__note" markdown="span">%s</p>' % caption, ""]
    else:
        caption = noimage[0] if noimage else "(no image — see text)"
        out += ['<p class="step-figure__none" markdown="span">%s</p>' % caption, ""]
    out += ["</div>", ""]

    out += ['<div class="step-text" markdown="1">', ""]
    if do:
        out += ['<div class="step-do" markdown="1">', ""] + _strip_edges(do) + ["", "</div>", ""]
    # Check right under Do, so the pass criterion is on the first screen at
    # 1024×768 (G2-26); the helper's job stays with it.
    if check:
        out += _strip_edges(check) + [""]
    for job in helper:
        out += ['<p class="step-helper" markdown="span">%s'
                '<span class="step-helper__label">Helper</span> %s</p>'
                % (mascot.badge_html("helper", "helper"), job), ""]
    gather = chapter.gather.get(page.step_id or "")
    if gather:
        # Parts items may carry chapter-relative links; re-base them as the
        # rest of the page's links already were.
        out += rewrite_links(gather, chapter.path.parent, dest_dir, chapter.stem) + [""]
    if parts_md:
        out += _strip_edges(parts_md) + [""]
    if desc:
        out += ['??? note "What you\'re looking at"', ""]
        out += ["    " + l if l.strip() else "" for l in _strip_edges(desc)]
        out += [""]
    if other:
        out += _strip_edges(other) + [""]
    if pause:
        out += _strip_edges(pause) + [""]
    if source:
        out += _strip_edges(source)
    if nxt:
        out += [""] + _strip_edges(nxt)
    out += ["", "</div>", "", "</div>"]
    return out


# --------------------------------------------------------------------------
# "Gather for this segment" — staging list per bench session
# --------------------------------------------------------------------------
#
# A *segment* is the run of steps from the step after a `Pause:` line (or the
# chapter's first step) through the next step that carries one.  Prusa's kit
# guide spends ~39 % of its steps on staging parts; we get the same effect for
# free by summing each segment's `**Parts:**` lines.  Nothing here is
# hand-maintained: the chapters stay the single source.

_PAUSE_MIN_RE = re.compile(r"^>?\s*Pause:\s*~?\s*(\d+)\s*min", re.IGNORECASE)

# Parse, counts, merge and bins live in scripts/parts.py; the names below are
# the ones this module has always used.
PARSE_WARNINGS = parts.PARSE_WARNINGS
_count_of = parts.count_of
_printed_info = parts.printed_info
_merge_key = parts.merge_key
_Item = parts.Tally
_collect = parts.collect


@dataclass
class Segment:
    ids: list[str]                       # step ids, in order
    minutes: int | None                  # from the closing Pause line
    hardware: list[_Item] = field(default_factory=list)
    printed: list[_Item] = field(default_factory=list)
    # Any list-form Parts field in the segment switches its Gather block to the
    # grouped-by-source layout (parts.groups); single-line-only segments keep
    # the Hardware / Printed parts layout above, unchanged.
    grouped: bool = False
    tallies: list[_Item] = field(default_factory=list)
    # Its closing Pause carries `(pre-kit)`: bench work that needs no Voron part
    # (build_tonight.py's "Before the kit" planner offers exactly these).
    pre_kit: bool = False

    @property
    def first(self) -> str:
        return self.ids[0]

    @property
    def label(self) -> str:
        if len(self.ids) == 1:
            return "step %s" % self.ids[0]
        return "steps %s–%s" % (self.ids[0], self.ids[-1])

    @property
    def title(self) -> str:
        mins = " (~%d min)" % self.minutes if self.minutes else ""
        return "Gather for this segment — %s%s" % (self.label, mins)

    def items(self) -> list[_Item]:
        return self.tallies if self.grouped else self.hardware + self.printed


def build_segments(chapter: Chapter) -> list[Segment]:
    """Split the chapter's steps into Pause-delimited segments and sum their
    Parts lines. Hardware keeps source order, printed parts follow."""
    segments: list[Segment] = []
    current: Segment | None = None
    for page in chapter.pages:
        if page.kind != "step" or not page.step_id:
            continue
        if current is None:
            current = Segment(ids=[], minutes=None)
        current.ids.append(page.step_id)
        closing = None
        for seg in _segments(page.body):
            if seg.kind == "parts":
                fld = parts.parse_field(seg.lines)
                if fld.form == "list":
                    current.grouped = True
                else:
                    line = " ".join(l.strip() for l in seg.lines)
                    where = "%s Step %s" % (chapter.stem, page.step_id)
                    for item in _parts_items(line):
                        printed, _ = _printed_info(item)
                        _collect(current.printed if printed else current.hardware, item, where)
                for it in fld.items:
                    parts.grouped_tally(current.tallies, it)
            elif seg.kind == "pause":
                closing = seg.lines[0]
        if closing is not None:
            m = _PAUSE_MIN_RE.match(closing)
            current.minutes = int(m.group(1)) if m else None
            tm = _TONIGHT_PAUSE_RE.match(closing.strip())
            current.pre_kit = bool(tm and tm.group(2))
            segments.append(current)
            current = None
    if current is not None:
        segments.append(current)
    return segments


def pre_kit_steps(chapter: Chapter) -> set[str]:
    """Step ids inside a `(pre-kit)` segment: the overview tile and the step
    counter badge them, so a pair working before the kit skips the rest."""
    return {sid for seg in chapter.segments if seg.pre_kit for sid in seg.ids}


def _item_line(item: _Item) -> str:
    bins = ", ".join(item.bins)
    count = " ×%d" % item.count if (item.explicit or item.count > 1) else ""
    return "%s%s%s" % (item.display, count, (" — from bin %s" % bins) if bins else "")


def _src(note: str | None) -> str:
    """The muted source suffix: kit box, bin, hand-set source, tool, on the bench."""
    return (' <span class="step-parts__src">· %s</span>' % html.escape(note)) if note else ""


def gather_admonition(segment: Segment) -> list[str]:
    """The collapsed block that opens a segment's first step page."""
    if not segment.items():
        return []
    out = ['??? note "%s %s"' % (mascot.badge_html("gather", "gather"),
                                 segment.title), ""]
    if segment.grouped:
        for heading, items in parts.groups(segment.tallies):
            out += ["    **%s**" % heading, ""]
            out += ["    - " + parts.tally_line(i) + _src(i.note) for i in items]
            out += [""]
        return out[:-1] if out[-1] == "" else out
    for label, items in (("Hardware", segment.hardware), ("Printed parts", segment.printed)):
        if not items:
            continue
        out += ["    **%s**" % label, ""]
        out += ["    - " + _item_line(i) for i in items]
        out += [""]
    return out[:-1] if out[-1] == "" else out


def _overview_body(segment: Segment) -> str:
    if not segment.items():
        return "nothing to lay out"
    if not segment.grouped:
        return " · ".join(_item_line(i) for i in segment.items())
    return " · ".join(
        "*%s:* %s" % (heading, "; ".join(
            parts.tally_line(i) + ((" (%s)" % i.note) if i.note else "") for i in items))
        for heading, items in parts.groups(segment.tallies))


def gather_overview(chapter: Chapter) -> list[str]:
    """One line per segment for the chapter overview, under the step grid."""
    if not chapter.segments:
        return []
    out = ['<div class="chapter-gather" markdown="1">', "",
           "**Gather per session** — what to lay out before each bench segment.", ""]
    for segment in chapter.segments:
        mins = " · ~%d min" % segment.minutes if segment.minutes else ""
        body = _overview_body(segment)
        label = segment.label[0].upper() + segment.label[1:]   # step ids keep their case
        out.append("- **%s**%s — %s" % (label, mins, body))
    out += ["", "</div>", ""]
    return out


# --------------------------------------------------------------------------
# panel crops (scripts/crop_panels.py owns the box, the file name and --check)
# --------------------------------------------------------------------------


def _crop_file(src: str, attr: str) -> str | None:
    """The crop PNG's file name for an image `{ crop="…" }` attr, else None."""
    cm = _CROP_ATTR_RE.search(attr or "")
    if not cm:
        return None
    pm = _PAGE_PNG_RE.search(src)
    try:
        box = tuple(float(v) for v in cm.group(2).split())
    except ValueError:
        box = ()
    if not pm or len(box) != 4:
        raise BuildStepsError("crop=%r on %s: needs four numbers on a manual-pages/ or "
                              "sb-pages/ PNG" % (cm.group(2), src))
    page_id = ("p" if pm.group(1) == "manual" else "sb") + pm.group(2)
    return crop_panels.crop_filename(page_id, box)


def check_crops(chapters: list["Chapter"]) -> None:
    """Fail the build on a crop the step pages cannot show.

    Every `crop=` image line must be one `crop_panels.py --check` sees (same
    regex), and every declared crop's PNG must be committed.
    """
    problems = []
    for chapter in chapters:
        for n, line in enumerate(chapter.path.read_text(encoding="utf-8").split("\n"), 1):
            m = _IMAGE_LINE_RE.match(line.strip())
            if not m or not _CROP_ATTR_RE.search(m.group("attr") or ""):
                continue
            where = "%s:%d" % (chapter.path.relative_to(REPO), n)
            if chapter.path.parent != crop_panels.CHAPTERS_DIR \
                    or not crop_panels.CROP_ATTR_RE.search(line):
                problems.append("%s: crop declared where crop_panels.py --check cannot see "
                                "it (write `](assets/…png){ crop=\"x0 y0 x1 y1\" }` in "
                                "docs/manual/*.md)" % where)
                continue
            try:
                fname = _crop_file(m.group("src"), m.group("attr")[1:-1])
            except BuildStepsError as exc:
                problems.append("%s: %s" % (where, exc))
                continue
            if not (crop_panels.CROPS_DIR / fname).exists():
                problems.append("%s: crop PNG missing: assets/manual-crops/%s — render it with "
                                "`python3 scripts/crop_panels.py --render …`" % (where, fname))
    if problems:
        raise BuildStepsError("panel crops:\n  " + "\n  ".join(problems))


# --------------------------------------------------------------------------
# Checkpoint rewards
# --------------------------------------------------------------------------

REWARDS: dict[tuple[str, str], str] = {}   # (chapter stem, checkpoint slug) -> reward HTML


def _bench_minutes(chapter: "Chapter") -> int | None:
    """The chapter's bench time: `**Sessions:** N × ~M min`, else the Time midpoint."""
    m = _SESSIONS_MIN_RE.search(chapter.sessions or "")
    if m:
        return int(m.group(1)) * int(m.group(2))
    m = _TIME_HOURS_RE.search(_plain(chapter.time or ""))
    if m:
        lo = float(m.group(1))
        hi = float(m.group(2) or lo)
        return round((lo + hi) / 2 * 60)
    return None


def _worms(n: int) -> str:
    return "%d gummy worm%s." % (n, "" if n == 1 else "s")


def _checkpoint_worms(chapter: "Chapter") -> dict[str, int]:
    """checkpoint slug -> worms: one per 30 min of bench time, split across a
    chapter's Checkpoints by how many Pause segments lead up to each."""
    cps = [p for p in chapter.pages if p.kind == "checkpoint"]
    minutes = _bench_minutes(chapter)
    if not cps or minutes is None:
        return {}
    total = max(1, int(minutes / WORM_MINUTES + 0.5))
    if len(cps) == 1:
        return {cps[0].slug: total}
    index = {p.step_id: i for i, p in enumerate(chapter.pages) if p.step_id}
    cp_at = [i for i, p in enumerate(chapter.pages) if p.kind == "checkpoint"]
    weight = [0] * len(cps)
    for seg in chapter.segments:
        last = index.get(seg.ids[-1], 0)
        k = next((j for j, at in enumerate(cp_at) if at > last), len(cps) - 1)
        weight[k] += 1
    whole = sum(weight) or 1
    return {cp.slug: max(1, int(total * w / whole + 0.5)) for cp, w in zip(cps, weight)}


def _batch_caption(batch: str, where: str) -> str:
    """"Batch B05 printed: plate 9 of 22, 72.2 of 157.0 h. 1 gummy worm." — plates
    from slicer/plates.py, hours as slicer/check_docs.py rounds them for the docs."""
    ids = sorted(PLATES)
    mine = [pid for pid in ids if PLATES[pid]["batch"] == batch]
    if not mine:
        raise BuildStepsError("%s: Checkpoint %s names no batch in slicer/plates.py"
                              % (where, batch))
    run_of_batch = {PLATES[pid]["batch"]: run_of(pid) for pid in ids}
    _plate, batches = check_docs.load()
    run = [pid for pid in ids if run_of(pid) == "asa"]
    done = total = 0.0
    for b, d in batches.items():            # additive, as check_docs sums the run
        if run_of_batch.get(b) == "asa":
            total = round(total + d["h"], 1)
            if b <= batch:
                done = round(done + d["h"], 1)
    worms = _worms(len(mine))
    if run_of(mine[0]) != "asa":
        return "Batch %s printed: %d plate%s, %.1f h, outside the %.1f h run. %s" % (
            batch, len(mine), "" if len(mine) == 1 else "s", batches[batch]["h"], total, worms)
    first, last = run.index(mine[0]) + 1, run.index(mine[-1]) + 1
    plates = ("plate %d" % first) if first == last else ("plates %d to %d" % (first, last))
    return "Batch %s printed: %s of %d, %.1f of %.1f h. %s" % (
        batch, plates, len(run), done, total, worms)


def build_rewards(chapters: list["Chapter"]) -> None:
    """Fill REWARDS for every Checkpoint (mascot.reward_html owns the markup,
    the humour rule and the caption cap)."""
    REWARDS.clear()
    for chapter in chapters:
        is_batch = chapter.path.parent == PRINT
        worms = {} if is_batch else _checkpoint_worms(chapter)
        for page in chapter.pages:
            if page.kind != "checkpoint":
                continue
            tag = _CHECKPOINT_HEAD_RE.match(page.title).group(1).strip()
            where = "%s § %s" % (chapter.path.name, _plain(page.title))
            if is_batch:
                if page.built:
                    raise BuildStepsError("%s: **Built:** is for assembly Checkpoints; a batch "
                                          "reward is generated from slicer/plates.py" % where)
                caption = _batch_caption(tag, where)
            else:
                n = worms.get(page.slug)
                tail = (" " + _worms(n)) if n else ""
                if page.built:
                    built = _plain(page.built).rstrip(".").strip()
                    if len(built.split()) > BUILT_MAX_WORDS:
                        raise BuildStepsError("%s: **Built:** is %d words, budget is %d"
                                              % (where, len(built.split()), BUILT_MAX_WORDS))
                    caption = "You built %s.%s" % (built, tail)
                else:
                    caption = "Checkpoint %s passed.%s" % (tag, tail)
            REWARDS[(chapter.stem, page.slug)] = mascot.reward_html(tag, caption, where)


def _long_page_rewards(markdown: str, stem: str) -> str:
    """The long chapter page: each Checkpoint section ends with its reward, and
    its `**Built:**` line (the reward's source) is not shown raw."""
    if not any(k[0] == stem for k in REWARDS):
        return markdown
    out: list[str] = []
    pending: str | None = None
    fence: str | None = None
    for line in markdown.split("\n"):
        fm = _FENCE_RE.match(line)
        if fm:
            token = fm.group(1)[0] * 3
            fence = token if fence is None else (None if line.strip().startswith(fence) else fence)
            out.append(line)
            continue
        if fence is None:
            hm = _HEADING_RE.match(line)
            if hm and len(hm.group(1)) <= 2:
                if pending:
                    out += ["", pending, ""]
                    pending = None
                cp = _CHECKPOINT_HEAD_RE.match(hm.group(2)) if len(hm.group(1)) == 2 else None
                if cp:
                    slug = "checkpoint-" + (cp.group(1).strip().lower() or "end")
                    pending = REWARDS.get((stem, slug))
            elif pending and _BUILT_RE.match(line.strip()):
                continue
        out.append(line)
    if pending:
        out += ["", pending, ""]
    return "\n".join(out)


# --------------------------------------------------------------------------
# emission
# --------------------------------------------------------------------------


def _nav_bar(prev: tuple[str, str] | None, nxt: tuple[str, str] | None) -> list[str]:
    out = ['<div class="step-nav" markdown="1">', ""]
    if prev:
        out += ["[<span class=\"step-nav__dir\">← Previous</span>"
                "<span class=\"step-nav__label\">%s</span>](%s){ .step-nav__link .step-nav__prev }"
                % (html.escape(prev[0]), prev[1]), ""]
    else:
        out += ['<span class="step-nav__link step-nav__prev step-nav__link--off"></span>', ""]
    if nxt:
        out += ["[<span class=\"step-nav__dir\">Next →</span>"
                "<span class=\"step-nav__label\">%s</span>](%s){ .step-nav__link .step-nav__next }"
                % (html.escape(nxt[0]), nxt[1]), ""]
    else:
        out += ['<span class="step-nav__link step-nav__next step-nav__link--off"></span>', ""]
    out += ["</div>"]
    return out


def _page_label(chapter: Chapter, page: Page) -> str:
    if page.kind == "step":
        return _plain(page.title)
    if page.kind == "front":
        return f"{chapter.short} — before you start"
    if page.kind == "checkpoint":
        return _plain(page.title)
    return _plain(page.title)


# A markdown link that is not an image: `[text](target)`.
_TEXT_LINK_RE = re.compile(r"(?<!!)\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*([^()\s]+?)\s*(?:\"[^\"]*\")?\)")


def _resolve_link_step(lines: list[str], chapters: list[Chapter]) -> tuple[Chapter, Page] | None:
    """The step a `<chapter>.md#<anchor>` link in `lines` leads to, if any.

    Only the first line carrying a link counts, and only a link whose anchor
    is a `Step` heading (see the module docstring) resolves.
    """
    for line in lines:
        m = _TEXT_LINK_RE.search(line)
        if not m:
            continue
        path, _, frag = m.group(1).partition("#")
        if not (path.endswith(".md") and frag):
            return None
        stem = Path(path).stem
        for target in chapters:
            if target.stem != stem:
                continue
            for page in target.pages:
                if page.kind == "step" and slugify(page.title, "-") == frag:
                    return target, page
        return None
    return None


def _next_section_step(chapter: Chapter, chapters: list[Chapter]) -> tuple[Chapter, Page] | None:
    """The step the chapter's `## Next` section leads with, if it leads with one."""
    return _resolve_link_step(chapter.next_body, chapters)


def _front_matter(title: str, hide_toc: bool = False) -> str:
    """`hide_toc`: a step page has no heading below its h1, so Material's
    table-of-contents sidebar is empty, yet it still takes a quarter of the
    iPad's 1024 px; hiding it gives the picture, the text and a long config
    block (G7-21) the whole width."""
    import yaml

    meta = {"title": title}
    if hide_toc:
        meta["hide"] = ["toc"]
    return "---\n%s---" % yaml.safe_dump(meta, allow_unicode=True,
                                          default_flow_style=False, width=10 ** 6)


def render_page(chapter: Chapter, page: Page, idx: int,
                prev_ref: tuple[str, str] | None,
                next_ref: tuple[str, str] | None) -> str:
    dest_dir = STEPS / chapter.slug
    src_dir = chapter.path.parent
    body = rewrite_links(page.body, src_dir, dest_dir, chapter.stem)
    page = Page(**{**page.__dict__, "body": body})

    crumb_section = html.escape(page.section) if page.section else ""
    if page.kind == "step":
        counter = "Step %d of %d" % (page.ordinal, chapter.n_steps)
        short_counter = "%d / %d" % (page.ordinal, chapter.n_steps)
    elif page.kind == "front":
        counter = short_counter = "Before you start"
    elif page.kind == "checkpoint":
        counter = short_counter = "Checkpoint"
    else:
        counter = short_counter = "Note"

    badge = ''
    if page.kind == "step" and page.step_id in pre_kit_steps(chapter):
        badge += ' <span class="step-prekit-badge">pre-kit</span>'
    if page.kind == "step" and helper_jobs(page.body):
        badge += ' <span class="step-helper-badge">with a helper</span>'

    out = [
        _front_matter(_plain(page.title),
                      hide_toc=page.kind == "step" and len(_split_blocks("\n".join(page.body))) == 1),
        '<div class="step-crumbs" data-chapter="%s"%s data-index="%s" data-total="%d" markdown="span">'
        '[%s](index.md)%s<span class="step-crumbs__counter">%s</span></div>'
        % (
            chapter.slug,
            ' data-step="%s"' % page.step_id if page.step_id else "",
            page.ordinal if page.ordinal else 0,
            chapter.n_steps,
            html.escape(chapter.short),
            (' <span class="step-crumbs__section">› %s</span>' % crumb_section) if crumb_section else "",
            short_counter,
        ),
        "",
        "# %s" % page.title,
        "",
        '<p class="step-counter" markdown="span">%s%s · [%s](index.md)'
        '<span class="step-counter__done"></span></p>'
        % (counter, badge, html.escape(chapter.title)),
        "",
    ]

    if page.kind == "step":
        out += layout_step(page, chapter)
    else:
        m = _CH_NUM_RE.match(chapter.stem)
        # The chapter's own Checkpoint, not Ch 06's second one (06b).
        if page.kind == "checkpoint" and chapter.stem in CHAPTER_SHOTS \
                and m and page.slug == "checkpoint-%s" % m.group(1):
            shot = CHAPTER_SHOTS[chapter.stem][1]
            out += ['<figure class="chapter-progress chapter-progress--single" markdown="1">',
                    "", _shot_img(shot, src_dir, dest_dir), "",
                    "<figcaption>What you should have now — %s</figcaption>"
                    % html.escape(_shot_caption(shot)), "", "</figure>", ""]
        out += ['<div class="step-text step-text--wide" markdown="1">', ""]
        reward = REWARDS.get((chapter.stem, page.slug)) if page.kind == "checkpoint" else None
        if reward:
            end = page.own_end if page.own_end is not None else len(page.body)
            out += page.body[:end] + ["", reward, ""] + page.body[end:]
        else:
            out += page.body
        if page.kind == "front":
            out += helper_list_line(chapter)
        out += ["", "</div>"]

    out += [""] + _nav_bar(prev_ref, next_ref) + [""]
    return "\n".join(out).rstrip() + "\n"


def helper_list_line(chapter: Chapter) -> list[str]:
    """`Helper steps: N` plus the ids, for the chapter's start page."""
    pages = helper_steps(chapter)
    if not pages:
        return []
    ids = ", ".join("[%s](%s.md)" % (p.step_id, p.slug) for p in pages)
    return ["", '<p class="step-helper-list" markdown="span">%s'
            '<span class="step-helper__label">Helper steps:</span> %d · %s</p>'
            % (mascot.badge_html("helper", "helper"), len(pages), ids)]


def _load_chapter_captions() -> None:
    """`title`, `caption` and `note_350` per chapter from assets/cad/steps.yml."""
    CHAPTER_CAPTIONS.clear()
    if not CAD_YML.exists():
        return
    import yaml
    doc = yaml.safe_load(CAD_YML.read_text(encoding="utf-8")) or {}
    for e in doc.get("chapters") or []:
        if not e.get("out"):
            continue
        text = " ".join(x for x in (e.get("caption"), e.get("note_350")) if x)
        if text:
            CHAPTER_CAPTIONS[str(e["chapter"])] = (e.get("title") or "", text)


def _chapter_shot(chapter: Chapter) -> str | None:
    """This chapter's end-state render, as a path relative to docs/manual."""
    m = _CH_NUM_RE.match(chapter.stem)
    if not m:
        return None
    rel = "assets/cad/ch-%s-after.png" % m.group(1)
    return rel if (MANUAL / rel).exists() else None


def _shot_num(rel: str) -> str:
    return re.search(r"ch-([0-9a-z]+)-after", rel).group(1)


def _shot_img(rel: str, src_dir: Path, dest_dir: Path) -> str:
    title = CHAPTER_CAPTIONS.get(_shot_num(rel), ("", ""))[0]
    what = title or "the machine at the end of Chapter %s" % _shot_num(rel)
    return "![Voron 2.4r2 CAD — %s](%s)" % (what, _rel(src_dir, dest_dir, rel))


def _shot_caption(rel: str) -> str:
    """What the after-image shows, from steps.yml — including its 350 caveat."""
    return CHAPTER_CAPTIONS.get(_shot_num(rel), ("", _CAD_PROVENANCE))[1]


def _shot_label(rel: str, side: str) -> str:
    """Side label: `After — end of Ch 05: the gantry, on the bench`.

    The tail comes from the render's own title, so a chapter that ends with a
    subassembly on the bench is not read as a changed machine.
    """
    num = _shot_num(rel)
    tail = CHAPTER_CAPTIONS.get(num, ("", ""))[0].split(" - ", 1)
    return "%s — end of Ch %s%s" % (side, num, (": " + tail[1]) if len(tail) > 1 else "")


def _progress_figure(chapter: Chapter, src_dir: Path, dest_dir: Path) -> list[str]:
    """The overview's "What this chapter builds" figure: the previous chapter's
    end-state render beside this one's, or this one alone where there is no
    earlier render."""
    before, after = CHAPTER_SHOTS[chapter.stem]
    out = ['<figure class="chapter-progress" markdown="1">', ""]
    if before:
        for rel, side in ((before, _shot_label(before, "Before")),
                          (after, _shot_label(after, "After"))):
            out += ['<div class="chapter-progress__shot" markdown="1">', "",
                    _shot_img(rel, src_dir, dest_dir), "",
                    '<span class="chapter-progress__cap">%s</span>' % html.escape(side),
                    "", "</div>", ""]
        lead = "What this chapter builds — orange is new, grey is what you already built."
    else:
        out += [_shot_img(after, src_dir, dest_dir), ""]
        lead = "What this chapter builds — everything orange is new."
    out += ["<figcaption>%s %s</figcaption>" % (lead, html.escape(_shot_caption(after))),
            "", "</figure>", ""]
    return out


def render_overview(chapter: Chapter, prev_ch: Chapter | None, next_ch: Chapter | None) -> str:
    dest_dir = STEPS / chapter.slug
    src_dir = chapter.path.parent
    long_page = _rel(src_dir, dest_dir, chapter.path.name)

    out = ["# %s" % chapter.title, ""]
    meta = []
    if chapter.time:
        meta.append("**Time:** %s" % _short_meta(chapter.time))
    if chapter.sessions:
        meta.append("**Sessions:** %s" % _short_meta(chapter.sessions))
    meta.append("**Steps:** %d" % chapter.n_steps)
    out += ['<p class="chapter-meta" markdown="span">%s</p>' % " · ".join(meta), ""]

    first = next((p for p in chapter.pages), None)
    first_step = next((p for p in chapter.pages if p.kind == "step"), None)
    links = []
    if first:
        links.append("[Start the chapter](%s.md)" % first.slug)
    if first_step:
        links.append('<a class="chapter-resume" href="%s/" data-chapter="%s">Resume</a>'
                     % (first_step.slug, chapter.slug))
    links.append("[Read the whole chapter on one page](%s)" % long_page)
    out += ['<p class="chapter-actions" markdown="span">%s</p>' % " · ".join(links), ""]

    if chapter.stem in CHAPTER_SHOTS:
        out += _progress_figure(chapter, src_dir, dest_dir)

    out += ['<div class="step-grid" data-chapter="%s" markdown="1">' % chapter.slug, ""]
    pre_kit = pre_kit_steps(chapter)
    for page in chapter.pages:
        helper = page.kind == "step" and bool(helper_jobs(page.body))
        early = page.kind == "step" and page.step_id in pre_kit
        if page.kind == "step":
            label = "Step %s" % page.step_id
            title = _plain(_STEP_HEAD_RE.match(page.title).group(2))
            data = ' data-step="%s"' % page.step_id
            mod = " .step-card--helper" if helper else ""
        elif page.kind == "front":
            label, title, data, mod = "Start", "Before you start", "", " .step-card--meta"
        elif page.kind == "checkpoint":
            label, title, data, mod = _plain(page.title), "Tick before moving on", "", " .step-card--meta"
        else:
            label, title, data, mod = "Note", _plain(page.title), "", " .step-card--meta"

        thumb = None
        for line in page.body:
            m = _IMAGE_LINE_RE.match(line)
            if m:
                thumb = rewrite_links([line], src_dir, dest_dir, chapter.stem)[0]
                thumb = _IMAGE_LINE_RE.match(thumb).group("src")
                break

        inner = ""
        if thumb:
            inner += "![](%s){ .step-card__thumb }" % thumb
        else:
            inner += '<span class="step-card__thumb step-card__thumb--none"></span>'
        inner += '<span class="step-card__id">%s</span>' % html.escape(label)
        inner += '<span class="step-card__title">%s</span>' % html.escape(title)
        if helper or early:
            inner += '<span class="step-card__badges">%s%s</span>' % (
                '<span class="step-card__prekit" title="Before the kit arrives">pre-kit</span>'
                if early else "",
                '<span class="step-card__helper" title="With a helper">with a helper</span>'
                if helper else "")
        inner += '<span class="step-card__tick"></span>'
        out += ["[%s](%s.md){ .step-card%s%s }" % (inner, page.slug, mod, data), ""]
    out += ["</div>", ""]

    out += rewrite_links(gather_overview(chapter), src_dir, dest_dir, chapter.stem)

    nav = []
    if prev_ch:
        nav.append("[← %s](../%s/index.md)" % (html.escape(prev_ch.short), prev_ch.slug))
    nav.append("[Manual index](../../00-index.md)")
    if next_ch:
        nav.append("[%s →](../%s/index.md)" % (html.escape(next_ch.short), next_ch.slug))
    out += ['<p class="chapter-nav" markdown="span">%s</p>' % " · ".join(nav), ""]
    return "\n".join(out).rstrip() + "\n"


def _write(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def build() -> dict:
    _load_part_thumbs()
    chapters: list[Chapter] = []
    for path in _chapter_files():
        chapter = parse_chapter(path)
        if chapter:
            chapters.append(chapter)

    check_crops(chapters)

    PARSE_WARNINGS.clear()
    for chapter in chapters:
        chapter.segments = build_segments(chapter)
        chapter.gather = {}
        for segment in chapter.segments:
            block = gather_admonition(segment)
            if block:
                chapter.gather[segment.first] = block

    build_rewards(chapters)

    _load_chapter_captions()
    CHAPTER_SHOTS.clear()
    before: str | None = None
    for chapter in chapters:
        shot = _chapter_shot(chapter)
        if shot:
            CHAPTER_SHOTS[chapter.stem] = (before, shot)
            before = shot

    STEP_URLS.clear()
    ANCHOR_URLS.clear()
    CHAPTER_OVERVIEW.clear()
    CHAPTER_FIRST.clear()
    STEP_ANCHORS.clear()
    for chapter in chapters:
        rel = "manual/steps/%s" % chapter.slug
        CHAPTER_OVERVIEW[chapter.stem] = "%s/index.md" % rel
        if chapter.pages:
            CHAPTER_FIRST[chapter.stem] = "%s/%s.md" % (rel, chapter.pages[0].slug)
        for page in chapter.pages:
            src = "%s/%s.md" % (rel, page.slug)
            ANCHOR_URLS[(chapter.stem, slugify(page.title, "-"))] = src
            if page.step_id:
                STEP_URLS[page.step_id] = src
                STEP_ANCHORS.setdefault(chapter.stem, set()).add(slugify(page.title, "-"))

    written = 0
    keep: set[Path] = set()
    for n, chapter in enumerate(chapters):
        dest_dir = STEPS / chapter.slug
        prev_ch = chapters[n - 1] if n else None
        next_ch = chapters[n + 1] if n + 1 < len(chapters) else None

        index = dest_dir / "index.md"
        keep.add(index)
        written += _write(index, render_overview(chapter, prev_ch, next_ch))

        for i, page in enumerate(chapter.pages):
            if i:
                p = chapter.pages[i - 1]
                prev_ref = (_page_label(chapter, p), "%s.md" % p.slug)
            else:
                prev_ref = ("%s — chapter overview" % chapter.short, "index.md")
            bench = _next_section_step(chapter, chapters) if i + 1 == len(chapter.pages) else None
            own = _resolve_link_step(page.next_override, chapters) if page.next_override else None
            if own:
                tch, tp = own
                next_ref = (_page_label(tch, tp), "%s%s.md" % (
                    "" if tch is chapter else "../%s/" % tch.slug, tp.slug))
            elif i + 1 < len(chapter.pages):
                nx = chapter.pages[i + 1]
                next_ref = (_page_label(chapter, nx), "%s.md" % nx.slug)
            elif bench:
                tch, tp = bench
                next_ref = (_page_label(tch, tp), "%s%s.md" % (
                    "" if tch is chapter else "../%s/" % tch.slug, tp.slug))
            elif next_ch and next_ch.pages:
                next_ref = (_page_label(next_ch, next_ch.pages[0]),
                            "../%s/%s.md" % (next_ch.slug, next_ch.pages[0].slug))
            else:
                next_ref = ("Manual index", "../../00-index.md")

            out = dest_dir / ("%s.md" % page.slug)
            keep.add(out)
            written += _write(out, render_page(chapter, page, i, prev_ref, next_ref))

    # Keep the whole generated tree out of the sidebar; the Build/Print tabs in
    # docs/.nav.yml name the chapter overviews individually instead.
    nav = STEPS / ".nav.yml"
    keep.add(nav)
    written += _write(nav, "hide: true\n")

    # Drop pages whose source step disappeared, so the tree is a pure function
    # of the chapters (and `mkdocs build --strict` never sees a stale orphan).
    if STEPS.exists():
        for stale in STEPS.rglob("*"):
            if stale.is_file() and stale not in keep:
                stale.unlink()
        for d in sorted((p for p in STEPS.rglob("*") if p.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()

    return {"chapters": len(chapters), "pages": len(keep) - 1, "written": written,
            "steps": sum(c.n_steps for c in chapters),
            "segments": sum(len(c.segments) for c in chapters),
            "unparsed_parts": len(PARSE_WARNINGS)}


# --------------------------------------------------------------------------
# mkdocs hooks
# --------------------------------------------------------------------------

_BANNER = ('!!! tip "One page per step"\n'
           '    Read this chapter [one step per page](%s){ .step-pages-link } — big pictures, prev/next, '
           'and the same tick marks. This page is the whole chapter in one scroll.\n')

_TONIGHT_SPAN_RE = re.compile(r'<span data-first-step="([^"]+)">(.*?)</span>')


def on_pre_build(config, **kwargs):
    import logging

    stats = build()
    log = logging.getLogger("mkdocs.hooks.build_steps")
    for warning in PARSE_WARNINGS:
        log.info("build_steps: %s", warning)
    if PARSE_WARNINGS:
        log.info("build_steps: %d Parts item(s) listed verbatim in gather blocks",
                 len(PARSE_WARNINGS))
    log.info("build_steps: %(segments)d gather segment(s) across %(chapters)d chapters", stats)


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_uri
    if src.startswith("manual/steps/"):
        return markdown

    import os

    def to(dest: str) -> str:
        """Markdown-link path: mkdocs re-bases these from the source file."""
        return os.path.relpath(dest, os.path.dirname(src)).replace("\\", "/")

    def href(dest: str) -> str:
        """Browser href for raw HTML, which mkdocs does NOT re-base. With
        use_directory_urls a page at `a/b.md` is served from `a/b/`, so the
        base is one level deeper than the source file."""
        base = os.path.dirname(src)
        if Path(src).name not in ("index.md", "README.md"):
            base = os.path.join(base, Path(src).stem)
        target = os.path.dirname(dest) if Path(dest).name in ("index.md", "README.md") \
            else os.path.join(os.path.dirname(dest), Path(dest).stem)
        rel = os.path.relpath(target, base).replace("\\", "/")
        return "./" if rel == "." else rel + "/"

    # Long chapter pages: point at their step-page overview.
    stem = Path(src).stem
    if stem in CHAPTER_OVERVIEW and src.startswith("manual/"):
        banner = _BANNER % to(CHAPTER_OVERVIEW[stem])
        lines = markdown.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# "):
                lines[i] = line + "\n\n" + banner
                break
        markdown = "\n".join(lines)
        return _long_page_rewards(markdown, stem)

    # The manual index: chapter links become chapter-overview links.
    if src == "manual/00-index.md":
        def one(m):
            dest, title = m.group(1), m.group(2) or ""
            path, _, frag = dest.partition("#")
            target = Path(path).stem
            if not frag and target in CHAPTER_OVERVIEW:
                return "](%s%s)" % (to(CHAPTER_OVERVIEW[target]), (" " + title) if title else "")
            return m.group(0)
        return _LINK_RE.sub(one, markdown)

    # Tonight: each segment links to the first step page of that segment.
    if src == "manual/00-tonight.md":
        def one(m):
            step_id, label = m.group(1), m.group(2)
            dest = STEP_URLS.get(step_id)
            if not dest:
                return m.group(0)
            return '<a class="tonight-seg" data-first-step="%s" href="%s">%s</a>' % (
                step_id, href(dest), label)
        return _TONIGHT_SPAN_RE.sub(one, markdown)

    return markdown


_HEADING_ID_RE = re.compile(r'<h([23]) id="([^"]+)"')


def on_page_content(html_text, page, config, files, **kwargs):
    """Search: a step is indexed on its own page only (G1-33). The long
    chapter page's step sections carry `data-search-exclude`, which Material's
    search plugin honours per section; the chapter's intro, section headings,
    Checkpoint and Common mistakes stay searchable there."""
    src = page.file.src_uri
    if src.startswith("manual/steps/") or not src.startswith("manual/"):
        return html_text
    anchors = STEP_ANCHORS.get(Path(src).stem)
    if not anchors:
        return html_text

    def one(m: re.Match) -> str:
        if m.group(2) in anchors:
            return '<h%s data-search-exclude id="%s"' % (m.group(1), m.group(2))
        return m.group(0)

    return _HEADING_ID_RE.sub(one, html_text)


if __name__ == "__main__":
    print(build())
    for warning in PARSE_WARNINGS:
        print("  warn:", warning)
