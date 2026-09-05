"""Build-time markdown callout conversion for the Voron build manual.

Converts convention-marked lines into Material admonition blocks. Source
markdown files stay untouched — this only runs on the in-memory string
mkdocs passes through on_page_markdown.

Recognized lines (see docs/manual/CONVENTIONS.md):
  ⚠ Rev D+ / LDO: <body>   -> !!! warning "Rev D+ / LDO"
  ⚠ <body>                 -> !!! warning
  Tip: <body>               -> !!! tip
  **Check:** <body>         -> !!! success "Check"
"""

import re

_WARNING_RE = re.compile(
    r"^⚠\s*(?:\*{0,2}([^:\n*]+?)\*{0,2}:\*{0,2}\s*)?(.*)$", re.MULTILINE
)
_TIP_RE = re.compile(r"^Tip:\s*(.*)$", re.MULTILINE)
_CHECK_RE = re.compile(r"^\*\*Check:\*\*\s*(.*)$", re.MULTILINE)


def _admonition(kind, title, body):
    body = body.strip()
    if title:
        return f'!!! {kind} "{title}"\n    {body}'
    return f"!!! {kind}\n    {body}"


def _warning_sub(match):
    title, body = match.group(1), match.group(2)
    title = title.strip() if title else None
    return _admonition("warning", title, body)


def _tip_sub(match):
    return _admonition("tip", None, match.group(1))


def _check_sub(match):
    return _admonition("success", "Check", match.group(1))


def on_page_markdown(markdown, page, config, files):
    markdown = _WARNING_RE.sub(_warning_sub, markdown)
    markdown = _TIP_RE.sub(_tip_sub, markdown)
    markdown = _CHECK_RE.sub(_check_sub, markdown)
    return markdown


if __name__ == "__main__":
    fixture = (
        "### Step 3.2 — Install idler\n\n"
        "**Parts:** M3x8 BHCS, qty 4\n\n"
        "**Do:** Seat the idler in the corner bracket, snug the bolts.\n\n"
        "**Check:** Idler spins freely with no side play.\n\n"
        "⚠ Rev D+ / LDO: kit ships with a longer bolt than the manual calls for.\n\n"
        "⚠ **Rev D+ / LDO:** the kit ships with an M4x6 BHCS already fitted.\n\n"
        "⚠ Double-check orientation before tightening.\n\n"
        "Tip: chamfer the printed part edge first for a cleaner fit. [src](https://example.com)\n"
    )
    print(on_page_markdown(fixture, None, None, None))
