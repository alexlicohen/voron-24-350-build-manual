"""Build-time markdown callout conversion for the Voron build manual.

Converts convention-marked lines into Material admonition blocks. Source
markdown files stay untouched — this only runs on the in-memory string
mkdocs passes through on_page_markdown.

Recognized line-starts (see docs/manual/CONVENTIONS.md), each of which may
also be introduced with an optional Markdown blockquote (`> `):
  ⚠ Rev D+ / LDO: <body>     -> !!! warning "Rev D+ / LDO"
  ⚠ **Rev D+ / LDO:** <body> -> !!! warning "Rev D+ / LDO"
  ⚠ <body>                   -> !!! warning
  Tip: <body>                -> !!! tip
  **Tip:** <body>            -> !!! tip
  **Check:** <body>          -> !!! success "Check"

A trigger line's body continues onto every following line — including a
hard-wrapped paragraph continuation, or a list/table that belongs to a
Check — until a blank line, a heading, a thematic break (`---`), or the
start of the next callout. That whole run is indented into the admonition
body so nothing after the first line is silently dropped.
"""

import re

_BLOCKQUOTE_PREFIX_RE = re.compile(r"^>\s?")

_WARNING_RE = re.compile(
    r"^⚠\s*(?:\*{0,2}([^:\n*]+?)\*{0,2}:\*{0,2}\s*)?(.*)$"
)
_TIP_RE = re.compile(r"^\*{0,2}Tip:\*{0,2}\s*(.*)$")
_CHECK_RE = re.compile(r"^\*{0,2}Check:\*{0,2}\s*(.*)$")

_HEADING_RE = re.compile(r"^#{1,6}\s")
_HR_RE = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})\s*$")


def _strip_blockquote(line):
    return _BLOCKQUOTE_PREFIX_RE.sub("", line, count=1)


def _match_trigger(logical_line):
    """Return (kind, title, body) if logical_line opens a callout, else None."""
    m = _WARNING_RE.match(logical_line)
    if m:
        title, body = m.group(1), m.group(2)
        return "warning", (title.strip() if title else None), body
    m = _CHECK_RE.match(logical_line)
    if m:
        return "success", "Check", m.group(1)
    m = _TIP_RE.match(logical_line)
    if m:
        return "tip", None, m.group(1)
    return None


def _is_block_boundary(logical_line):
    """True if this line starts a new block that must not be swallowed
    into a preceding callout's body (a heading, a thematic break, or the
    start of another callout)."""
    if _HEADING_RE.match(logical_line) or _HR_RE.match(logical_line):
        return True
    return _match_trigger(logical_line) is not None


def _admonition(kind, title, body_lines):
    first = body_lines[0].strip()
    indented = ["    " + first] + ["    " + ln for ln in body_lines[1:]]
    header = f'!!! {kind} "{title}"' if title else f"!!! {kind}"
    return header + "\n" + "\n".join(indented)


def _convert_callouts(markdown):
    lines = markdown.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        raw = lines[i]
        logical = _strip_blockquote(raw)
        trigger = _match_trigger(logical)
        if trigger is None:
            out.append(raw)
            i += 1
            continue

        kind, title, first_body = trigger
        body_lines = [first_body]
        i += 1
        while i < n:
            nxt_raw = lines[i]
            if nxt_raw.strip() == "":
                break
            nxt_logical = _strip_blockquote(nxt_raw)
            if _is_block_boundary(nxt_logical):
                break
            body_lines.append(nxt_logical)
            i += 1
        out.append(_admonition(kind, title, body_lines))
    return "\n".join(out)


def on_page_markdown(markdown, page, config, files):
    return _convert_callouts(markdown)


def on_page_content(html, page, config, files):
    """R5 F7 — lazy-load and async-decode every image so a chapter revisit
    doesn't eagerly re-pull every step illustration up front."""
    html = re.sub(
        r"<img(?![^>]*\bloading=)([^>]*)>",
        r'<img loading="lazy"\1>',
        html,
    )
    html = re.sub(
        r"<img(?![^>]*\bdecoding=)([^>]*)>",
        r'<img decoding="async"\1>',
        html,
    )
    return html


if __name__ == "__main__":
    fixtures = {
        "basic warning (plain title)": (
            "⚠ Rev D+ / LDO: kit ships with a longer bolt than the manual calls for.\n"
        ),
        "basic warning (bold title)": (
            "⚠ **Rev D+ / LDO:** the kit ships with an M4x6 BHCS already fitted.\n"
        ),
        "untitled warning": ("⚠ Double-check orientation before tightening.\n"),
        "plain Tip": (
            "Tip: chamfer the printed part edge first for a cleaner fit. [src](https://example.com)\n"
        ),
        "bold Tip (07-ab-belts.md style)": (
            "**Tip:** Mark one belt \"A\" with a dot of marker on the smooth back near each end.\n"
        ),
        "single-line blockquoted warning (07-ab-belts.md style)": (
            "> ⚠ **Rev D+ / LDO:** *\"PAGE 145 SKIP — The kit does not use hall effect "
            "endstops.\"* Do not insert a 3×6 magnet. [src](https://docs.ldomotors.com/voron/voron2/build-faq)\n"
        ),
        "Ch 08 ESD box — hard-wrapped warning body, no blank line": (
            "**Check:** Continuity from the toolboard `GND` pad to the motor can, and the "
            "wire cannot reach any moving part.\n\n"
            "⚠ Rev D+ / LDO: **use the supplied grounding cable** — LDO warns that larger "
            "ring-lug connectors can short\n"
            "the PCB. **If your kit did not include the grounding cables**, stop and ask in "
            "`#ldo_motors` before\n"
            "improvising a ground connection; this scheme was undocumented prose until LDO's "
            "board doc was updated\n"
            "2026-07-10 (survey §4.1 ⑤).\n\n"
            "---\n"
        ),
        "Ch 10 mains check — Check followed by a list, then an unrelated paragraph": (
            "**Check:** Meter on continuity, nothing plugged in.\n"
            "- C14 **E** pin → outgoing green/yellow: **beeps, switch in either position.**\n"
            "- C14 **L** pin → outgoing brown: **beeps only with the rocker ON.**\n"
            "- C14 **N** pin → outgoing blue: **beeps only with the rocker ON.**\n"
            "- Pull the fuse: C14 L → outgoing brown now **open** even with the rocker on. "
            "Put the fuse back.\n\n"
            "Any deviation from that pattern means the inlet is miswired — stop and fix it "
            "before anything else. [src](https://docs.ldomotors.com/en/voron/voron2/wiring_guide_rev_d)\n"
        ),
        "two adjacent callouts must not merge": (
            "⚠ First warning body.\n"
            "⚠ Second warning starts immediately after, no blank line.\n"
        ),
        "callout stops at a heading with no blank line": (
            "**Check:** last check line.\n"
            "### Step 3.3 — Next step\n"
        ),
    }

    fail = False
    for name, fixture in fixtures.items():
        rendered = on_page_markdown(fixture, None, None, None)
        print(f"--- {name} ---")
        print(rendered)
        print()
        if "⚠" in rendered or re.search(r"\*\*Check:\*\*|(?<!\w)Tip:", rendered):
            print(f"FAIL: raw marker leaked through in {name!r}")
            fail = True

    # Adjacent-callout regression: must produce two separate `!!!` blocks, not one merged body.
    adjacent = on_page_markdown(fixtures["two adjacent callouts must not merge"], None, None, None)
    if adjacent.count("!!! warning") != 2:
        print("FAIL: adjacent callouts merged into one admonition")
        fail = True

    # Heading-boundary regression: the heading must survive, unindented, outside the admonition.
    heading_case = on_page_markdown(
        fixtures["callout stops at a heading with no blank line"], None, None, None
    )
    if "\n### Step 3.3 — Next step" not in heading_case:
        print("FAIL: heading was swallowed into the preceding callout's body")
        fail = True

    # on_page_content: lazy-load / async-decode injection, idempotent on already-attributed tags.
    html_in = '<img src="a.png" alt=""><img src="b.png" loading="eager" decoding="sync">'
    html_out = on_page_content(html_in, None, None, None)
    print("--- on_page_content ---")
    print(html_out)
    if 'loading="lazy"' not in html_out or 'decoding="async"' not in html_out:
        print("FAIL: lazy-loading not injected")
        fail = True
    if 'loading="eager"' not in html_out or 'decoding="sync"' not in html_out:
        print("FAIL: on_page_content overwrote an existing loading/decoding attribute")
        fail = True

    if fail:
        raise SystemExit(1)
    print("All self-tests passed.")
