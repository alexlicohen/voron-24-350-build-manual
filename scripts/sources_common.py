"""Shared helpers for scripts/sources_build.py and scripts/sources_verify.py.

sources.yml is the pinned-source inventory for the manual (R6 V2/V3): one
entry per distinct external URL cited in docs/**/*.md, with enough metadata
(title, kind, and for GitHub sources a resolved commit SHA) to detect when an
upstream source has moved.
"""

import re
import subprocess
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

USER_AGENT = "voron-24-350-build-manual sources.yml checker (github.com/alexlicohen/voron-24-350-build-manual)"


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None

    def handle_starttag(self, tag, attrs):
        if tag == "title" and self.title is None:
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data


def fetch_status_and_title(url, timeout=15):
    """Returns (status_code_or_None, title_or_None). None status = request error."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            title = None
            ctype = resp.headers.get("Content-Type", "")
            if "html" in ctype:
                body = resp.read(200_000).decode("utf-8", errors="replace")
                parser = _TitleParser()
                parser.feed(body)
                if parser.title:
                    title = " ".join(parser.title.split())
            return status, title
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
SOURCES_YML = REPO / "sources.yml"

IMAGE_EXT_RE = re.compile(r"\.(jpe?g|png|gif|svg|webp)$", re.IGNORECASE)
URL_RE = re.compile(r'https?://[^\s)\]"<>`]+')

# GitHub repos this manual is exposed to, tracked by the weekly drift job
# (R6 V3, git-backed only per the 2026-09-05 ruling). kind here doubles as
# the sources.yml `kind` for any URL under that repo.
GIT_TRACKED_REPOS = {
    "VoronDesign/Voron-2": "voron-manual",
    "VoronDesign/Voron-Documentation": "voron-docs",
    "MotorDynamicsLab/Nitehawk-SB-V2": "ldo-repo",
    "MotorDynamicsLab/LDOVoron2": "ldo-repo",
    "VoronDesign/Voron-Stealthburner": "voron-manual",
    "prusa3d/PrusaSlicer-settings-prusa-fff": "prusa",
}

# Other GitHub repos seen in the docs, classified but not drift-tracked.
OTHER_REPO_KIND = {
    "MotorDynamicsLab/Nitehawk-SB": "ldo-repo",
    "MotorDynamicsLab/Leviathan": "ldo-repo",
    "MotorDynamicsLab/LDOVoronTrident": "ldo-repo",
    "Klipper3d/klipper": "klipper",
    "Arksine/katapult": "klipper",
    "Esoterical/voron_canbus": "klipper",
    "prusa3d/PrusaSlicer": "prusa",
    "VoronDesign/VoronUsers": "community",
    "tanaes/whopping_Voron_mods": "community",
    "jlas1/Klicky-Probe": "community",
    "nevermore3d/Nevermore_Micro": "community",
    "AndrewEllis93/Print-Tuning-Guide": "community",
    "th33xitus/kiauh": "community",
    "dw-0/kiauh": "community",
}

DOMAIN_KIND = {
    "docs.vorondesign.com": "voron-docs",
    "mods.vorondesign.com": "voron-docs",
    "voron.dozuki.com": "voron-docs",
    "docs.ldomotors.com": "ldo-guide",
    "ldomotion.com": "ldo-guide",
    "voronldo.com": "ldo-guide",
    "www.klipper3d.org": "klipper",
    "moonraker.readthedocs.io": "klipper",
    "klipperscreen.github.io": "klipper",
    "canbus.esoterical.online": "klipper",
    "help.prusa3d.com": "prusa",
    "www.fabreeko.com": "vendor",
    "e3d-online.com": "vendor",
    "www.super-lube.com": "vendor",
    "www.raspberrypi.com": "vendor",
    "west3d.com": "vendor",
    "www.onetwo3d.co.uk": "vendor",
}
# Everything else (YouTube, Discord, forums, blogs, docs-os.mainsail.xyz,
# docs.fluidd.xyz, voron.link, pif.voron.dev, cnckitchen.com, kb-3d.com...)
# falls back to "community" in classify_kind().


def extract_urls(exclude_images=True):
    """All http(s) URLs in docs/**/*.md, fragment-stripped and deduped.

    A source is a page/file, not an anchor on it, so #fragments are dropped
    before dedup. Hotlinked image files (jpg/png/gif/svg/webp) are excluded
    by default — they're embedded assets, not citable sources.
    """
    urls = set()
    for md in sorted(DOCS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in URL_RE.finditer(text):
            url = m.group(0).rstrip(".,;:)")
            url = url.split("#", 1)[0]
            if exclude_images and IMAGE_EXT_RE.search(url):
                continue
            if "alexlicohen.github.io" in url:
                continue  # this repo's own published site
            if urlsplit(url).netloc in ("voron.local",):
                continue  # placeholder hostname in a config example, not a real source
            urls.add(url)
    return sorted(urls)


def link_texts(url):
    """Every markdown link-text string used for this URL, across the docs."""
    texts = []
    pattern = re.compile(r"\[([^\]]+)\]\(" + re.escape(url) + r"[^)]*\)")
    for md in sorted(DOCS.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        texts.extend(pattern.findall(text))
    return texts


def github_repo_slug(url):
    """'owner/repo' for a github.com or raw.githubusercontent.com URL, else None."""
    parts = urlsplit(url)
    if parts.netloc not in ("github.com", "raw.githubusercontent.com"):
        return None
    segs = [s for s in parts.path.split("/") if s]
    if len(segs) < 2:
        return None
    repo = segs[1]
    if repo.endswith(".git"):
        repo = repo[: -len(".git")]
    return f"{segs[0]}/{repo}"


def classify_kind(url):
    repo = github_repo_slug(url)
    if repo:
        if repo in GIT_TRACKED_REPOS:
            return GIT_TRACKED_REPOS[repo]
        if repo in OTHER_REPO_KIND:
            return OTHER_REPO_KIND[repo]
        return "github-repo-file"
    domain = urlsplit(url).netloc
    return DOMAIN_KIND.get(domain, "community")


# A URL already carries a pinned commit/tag when its path has a 7-40 char hex
# SHA, or (for GitHub) a `/tree/<tag>/` or `/blob/<tag>/` segment that is not
# a branch name like main/master/HEAD.
_SHA_RE = re.compile(r"/([0-9a-f]{7,40})(?:/|$)")
_BRANCHES = {"main", "master", "HEAD"}


def pinned_ref(url):
    repo = github_repo_slug(url)
    if not repo:
        return None
    parts = urlsplit(url)
    segs = [s for s in parts.path.split("/") if s]
    # owner/repo/(blob|tree|raw)/<ref>/... or owner/repo/<ref>/... (raw.githubusercontent.com)
    tail = segs[2:]
    if not tail:
        return None
    if tail[0] in ("blob", "tree", "raw") and len(tail) > 1:
        ref = tail[1]
    else:
        ref = tail[0]
    m = _SHA_RE.search("/" + ref + "/")
    if m:
        return m.group(1)
    if ref not in _BRANCHES and re.match(r"^[\w.\-]+$", ref):
        return ref  # a tag/version string, e.g. "v2.4r2" or "Voron2.4"
    return None


def default_branch_sha(repo):
    """Resolved commit SHA of a GitHub repo's default branch, via `gh api`."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/commits", "-X", "GET", "-F", "per_page=1"],
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0:
        raise RuntimeError(f"gh api commits failed for {repo}: {out.stderr.strip()}")
    import json
    data = json.loads(out.stdout)
    if not data:
        raise RuntimeError(f"no commits returned for {repo}")
    return data[0]["sha"]


# --- Printables (R6 V3 extension, 2026-10-03) ------------------------------------
# Printables answers plain fetches with 403, so a sources.yml entry carrying a
# `printables:` block is checked through its GraphQL API instead (browser UA plus
# printables.com origin/referer, the same way slicer/fetch_stls.py downloads).
# The pin is what changes when the author updates the model: every file's id and
# size (a re-upload gets a new id) and a hash of the page's Klipper macro text.

PRINTABLES_API = "https://api.printables.com/graphql/"
_PRINTABLES_HEADERS = {
    "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"),
    "origin": "https://www.printables.com",
    "referer": "https://www.printables.com/",
    "content-type": "application/json",
}
_MACRO_START = "[gcode_arcs]"
_MACRO_REV_RE = re.compile(r"Klipper Macro updated for\s+([0-9/]+)")


def _printables_text(html_text):
    """The page description as plain text, one space between words."""
    import html as _html
    text = re.sub(r"<br\s*/?>|</p>", "\n", html_text or "")
    text = _html.unescape(re.sub(r"<[^>]+>", " ", text))
    return " ".join(text.split())


def printables_fingerprint(print_id, timeout=30):
    """{'name', 'files': {name: {'id', 'size'}}, 'macro_sha256', 'macro_rev'} for one
    Printables model, or raises RuntimeError. macro_sha256 hashes the description
    from the first `[gcode_arcs]` to its end, whitespace-normalised, so a macro edit
    (or a note added after it) shows up; None if the page carries no macro."""
    import hashlib
    import json
    query = ('{ print(id:"%s"){ name description stls{ id name fileSize } } }' % print_id)
    req = urllib.request.Request(PRINTABLES_API, data=json.dumps({"query": query}).encode(),
                                 headers=_PRINTABLES_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            out = json.load(resp)
    except Exception as e:  # noqa: BLE001 — any transport failure is one ERROR line
        raise RuntimeError(f"Printables API request failed: {e}")
    data = (out.get("data") or {}).get("print")
    if not data:
        raise RuntimeError(f"Printables API returned no print {print_id}: {out.get('errors')}")
    text = _printables_text(data.get("description"))
    i = text.find(_MACRO_START)
    macro = text[i:] if i >= 0 else None
    rev = _MACRO_REV_RE.search(text)
    return {
        "name": data.get("name"),
        "files": {f["name"]: {"id": str(f["id"]), "size": int(f["fileSize"])}
                  for f in data.get("stls") or []},
        "macro_sha256": hashlib.sha256(macro.encode()).hexdigest() if macro else None,
        "macro_rev": rev.group(1) if rev else None,
    }


def printables_diff(pin, current):
    """Human-readable differences between a stored `printables:` pin and a fresh
    fingerprint; empty list = unchanged."""
    diffs = []
    old_files, new_files = pin.get("files") or {}, current["files"]
    for name in sorted(set(old_files) | set(new_files)):
        a, b = old_files.get(name), new_files.get(name)
        if a is None:
            diffs.append(f"file added: {name!r} (id {b['id']}, {b['size']} B)")
        elif b is None:
            diffs.append(f"file removed: {name!r} (was id {a['id']})")
        elif str(a.get("id")) != b["id"] or int(a.get("size", -1)) != b["size"]:
            diffs.append(f"file changed: {name!r} id {a.get('id')} -> {b['id']}, "
                         f"{a.get('size')} -> {b['size']} B")
    if pin.get("macro_sha256") != current["macro_sha256"]:
        diffs.append(f"macro text changed (revision {pin.get('macro_rev')} -> {current['macro_rev']})")
    return diffs


def printables_local_check(pin):
    """Tracked copies named in the pin (`local: {path: sha256}`) must still match."""
    import hashlib
    bad = []
    for rel, want in (pin.get("local") or {}).items():
        path = REPO / rel
        if not path.exists():
            bad.append(f"local copy missing: {rel}")
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != want:
            bad.append(f"local copy differs from the pin: {rel}")
    return bad


def slugify(text, maxlen=40):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return s[:maxlen].strip("-")


def id_for(url):
    repo = github_repo_slug(url)
    parts = urlsplit(url)
    if repo:
        segs = [s for s in parts.path.split("/") if s][2:]
        # drop blob/tree/raw + ref segments, keep the file/dir tail
        if segs and segs[0] in ("blob", "tree", "raw"):
            segs = segs[2:]
        tail = "-".join(segs) if segs else ""
        base = f"{slugify(repo, 30)}-{slugify(tail, 30)}" if tail else slugify(repo, 40)
    else:
        domain = slugify(parts.netloc.replace("www.", ""), 25)
        path = slugify(parts.path, 30)
        base = f"{domain}-{path}" if path else domain
    return base.strip("-") or "source"


def load_yaml_sources(path=SOURCES_YML):
    import yaml
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("sources", [])
