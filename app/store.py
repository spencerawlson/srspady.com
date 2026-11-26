"""srspady.com admin — JSON stores under data/ (gitignored, never committed).

- data/drafts/<section>/<record-id>.json   — unpublished drafts
- data/content/<section>/<record-id>.json  — published records
- data/media/originals/                    — original uploads (never modified)
- data/media/derived/                      — filtered/cropped/rotated copies
- data/settings.json                       — per-section background choices

A record: {id, section, title, body_html (sanitized), image, visibility,
status, created, updated}. Visibility: Public / Private / Family-only /
Unlisted. Default Private. Only Public published records ever reach the
public site.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DRAFTS = DATA / "drafts"
CONTENT = DATA / "content"
MEDIA_ORIGINALS = DATA / "media" / "originals"
MEDIA_DERIVED = DATA / "media" / "derived"
SETTINGS_FILE = DATA / "settings.json"

VISIBILITIES = ["Public", "Private", "Family-only", "Unlisted"]
DEFAULT_VISIBILITY = "Private"

# Named background options. The public templates read the section's
# setting and add `bg-<name>` to <body>.
BACKGROUNDS = {
    "graph-paper": "Graph paper (default)",
    "ivory": "Ivory paper",
    "dark-bench": "Dark bench-ink",
    "gold-tint": "Muted gold tint",
}
DEFAULT_BACKGROUND = "graph-paper"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def new_record(section: str, title: str, body_html: str, image: str = "",
               visibility: str = DEFAULT_VISIBILITY) -> dict:
    return {
        "id": uuid.uuid4().hex[:12],
        "section": section,
        "title": title.strip(),
        "body_html": body_html,
        "image": image,
        "visibility": visibility if visibility in VISIBILITIES else DEFAULT_VISIBILITY,
        "status": "draft",
        "created": _now(),
        "updated": _now(),
    }


def save_draft(record: dict) -> None:
    record["status"] = "draft"
    record["updated"] = _now()
    _write_json(DRAFTS / record["section"] / f'{record["id"]}.json', record)


def publish_record(record: dict) -> None:
    record["status"] = "published"
    record["updated"] = _now()
    _write_json(CONTENT / record["section"] / f'{record["id"]}.json', record)
    draft = DRAFTS / record["section"] / f'{record["id"]}.json'
    draft.unlink(missing_ok=True)


def unpublish_record(section: str, record_id: str) -> dict | None:
    """Move a published record back to drafts. Returns the record or None."""
    src = CONTENT / section / f"{record_id}.json"
    rec = _read_json(src)
    if not rec:
        return None
    src.unlink()
    save_draft(rec)
    return rec


def delete_record(section: str, record_id: str) -> bool:
    gone = False
    for base in (DRAFTS, CONTENT):
        p = base / section / f"{record_id}.json"
        if p.exists():
            p.unlink()
            gone = True
    return gone


def get_record(section: str, record_id: str) -> dict | None:
    for base in (DRAFTS, CONTENT):
        rec = _read_json(base / section / f"{record_id}.json")
        if rec:
            return rec
    return None


def list_records(section: str) -> tuple[list[dict], list[dict]]:
    """(drafts, published) for a section, newest first."""
    def _all(base: Path) -> list[dict]:
        d = base / section
        if not d.exists():
            return []
        out = [r for f in sorted(d.glob("*.json")) if (r := _read_json(f))]
        return sorted(out, key=lambda r: r.get("updated", ""), reverse=True)
    return _all(DRAFTS), _all(CONTENT)


def published_public(section: str) -> list[dict]:
    """Published records with visibility Public — the only ones the public
    site may show. Drafts and non-public records never leave the admin."""
    _, published = list_records(section)
    return [r for r in published if r.get("visibility") == "Public"]


def section_counts() -> dict[str, dict[str, int]]:
    from app import content as C
    out = {}
    for slug in C.SECTIONS:
        drafts, published = list_records(slug)
        out[slug] = {
            "drafts": len(drafts),
            "published": len(published),
            "public": sum(1 for r in published if r.get("visibility") == "Public"),
        }
    return out


# --- Backgrounds ---------------------------------------------------------------

def get_background(section: str) -> str:
    settings = _read_json(SETTINGS_FILE) or {}
    bg = (settings.get("backgrounds") or {}).get(section, DEFAULT_BACKGROUND)
    return bg if bg in BACKGROUNDS else DEFAULT_BACKGROUND


def set_background(section: str, background: str) -> bool:
    if background not in BACKGROUNDS:
        return False
    settings = _read_json(SETTINGS_FILE) or {}
    settings.setdefault("backgrounds", {})[section] = background
    _write_json(SETTINGS_FILE, settings)
    return True


# --- Media ---------------------------------------------------------------------

def list_media() -> list[dict]:
    """Originals plus their derivatives, newest first."""
    out = []
    for base, kind in ((MEDIA_ORIGINALS, "original"), (MEDIA_DERIVED, "derived")):
        if not base.exists():
            continue
        for f in sorted(base.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if f.is_file():
                meta = _read_json(f.with_suffix(f.suffix + ".json")) or {}
                out.append({"name": f.name, "kind": kind, "size": f.stat().st_size,
                            "alt": meta.get("alt", ""), "filter": meta.get("filter", ""),
                            "source": meta.get("source", "")})
    return out
