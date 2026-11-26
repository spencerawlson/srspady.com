"""srspady.com admin — owner-only section (routes under /admin).

Server-rendered Jinja2 pages, like the rest of the app. No public
registration, no other users. See app/admin_auth.py for the login rules.

Routes:
  GET  /admin/login            login form
  POST /admin/login            check credentials (throttled), start session
  GET  /admin/logout           end session
  GET  /admin                  dashboard — all sections, record counts
  GET  /admin/sections/{slug}  edit a section: drafts, published, background
  POST /admin/sections/{slug}/records            create a draft
  POST /admin/sections/{slug}/records/{id}/publish
  POST /admin/sections/{slug}/records/{id}/unpublish
  POST /admin/sections/{slug}/records/{id}/delete
  GET  /admin/sections/{slug}/preview/{id}       draft preview (public template)
  POST /admin/sections/{slug}/background         set section background
  GET  /admin/media                              media library
  POST /admin/media/upload                       upload image/video
  POST /admin/media/derive                       filtered/cropped/rotated copy
  POST /admin/media/delete                       delete a media file
"""
from __future__ import annotations

import json
import re
import shutil
import uuid
from datetime import date
from pathlib import Path

import bleach
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import admin_auth as auth
from app import content as C
from app import media as media_lib
from app import store

ROOT = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(ROOT / "templates"))

router = APIRouter(prefix="/admin")

# --- Rich-text sanitizer: allowlist only. No scripts, no raw HTML. ---------
ALLOWED_TAGS = ["p", "h2", "h3", "strong", "em", "b", "i", "ul", "ol", "li",
                "blockquote", "a", "br"]
ALLOWED_ATTRS = {"a": ["href", "title"]}


def sanitize_html(raw: str) -> str:
    return bleach.clean(raw or "", tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS,
                        protocols=["http", "https", "mailto"], strip=True)


def _ctx(request: Request, **extra) -> dict:
    ctx = {"request": request, "year": date.today().year,
           "sections": C.SECTIONS, "all_sections": C.ALL_SECTIONS,
           "nav_groups": C.NAV_GROUPS, "contact_email": C.CONTACT_EMAIL,
           "backgrounds": store.BACKGROUNDS, "visibilities": store.VISIBILITIES}
    ctx.update(extra)
    return ctx


def _render(request: Request, name: str, ctx: dict, status_code: int = 200) -> HTMLResponse:
    return templates.TemplateResponse(request, name, ctx, status_code=status_code)


def _need_login(request: Request):
    return auth.login_required(request)


# --- Login / logout -----------------------------------------------------------

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if auth.is_logged_in(request):
        return RedirectResponse("/admin", status_code=303)
    return _render(request, "admin/login.html",
                   _ctx(request, configured=auth.is_admin_configured(), error=None))


@router.post("/login")
def login(request: Request, username: str = Form(""), password: str = Form("")):
    if auth.is_locked_out(request):
        return _render(request, "admin/login.html",
                       _ctx(request, configured=auth.is_admin_configured(),
                            error="Too many failed attempts. Try again in 15 minutes."),
                       status_code=429)
    if auth.check_login(username, password):
        auth.record_success(request)
        request.session[auth.SESSION_KEY] = username
        return RedirectResponse("/admin", status_code=303)
    auth.record_failure(request)
    return _render(request, "admin/login.html",
                   _ctx(request, configured=auth.is_admin_configured(),
                        error="Wrong username or password."),
                   status_code=401)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)


# --- Dashboard ----------------------------------------------------------------

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    if (r := _need_login(request)):
        return r
    return _render(request, "admin/dashboard.html",
                   _ctx(request, counts=store.section_counts()))


# --- Per-section editing ------------------------------------------------------

@router.get("/sections/{slug}", response_class=HTMLResponse)
def section_edit(request: Request, slug: str):
    if (r := _need_login(request)):
        return r
    if slug not in C.SECTIONS:
        return RedirectResponse("/admin", status_code=303)
    drafts, published = store.list_records(slug)
    title, kicker, intro = C.SECTIONS[slug]
    return _render(request, "admin/section_edit.html",
                   _ctx(request, slug=slug, title=title, kicker=kicker, intro=intro,
                        drafts=drafts, published=published,
                        background=store.get_background(slug),
                        media=store.list_media()))


@router.post("/sections/{slug}/records")
def create_record(request: Request, slug: str, title: str = Form(""),
                  body: str = Form(""), image: str = Form(""),
                  visibility: str = Form(store.DEFAULT_VISIBILITY)):
    if (r := _need_login(request)):
        return r
    if slug not in C.SECTIONS:
        return RedirectResponse("/admin", status_code=303)
    rec = store.new_record(slug, title or "Untitled",
                           sanitize_html(body), image=image.strip(),
                           visibility=visibility)
    store.save_draft(rec)
    return RedirectResponse(f"/admin/sections/{slug}", status_code=303)


@router.post("/sections/{slug}/records/{record_id}/publish")
def publish(request: Request, slug: str, record_id: str):
    if (r := _need_login(request)):
        return r
    rec = store.get_record(slug, record_id)
    if rec:
        store.publish_record(rec)
    return RedirectResponse(f"/admin/sections/{slug}", status_code=303)


@router.post("/sections/{slug}/records/{record_id}/unpublish")
def unpublish(request: Request, slug: str, record_id: str):
    if (r := _need_login(request)):
        return r
    store.unpublish_record(slug, record_id)
    return RedirectResponse(f"/admin/sections/{slug}", status_code=303)


@router.post("/sections/{slug}/records/{record_id}/delete")
def delete(request: Request, slug: str, record_id: str):
    if (r := _need_login(request)):
        return r
    store.delete_record(slug, record_id)
    return RedirectResponse(f"/admin/sections/{slug}", status_code=303)


@router.get("/sections/{slug}/preview/{record_id}", response_class=HTMLResponse)
def preview(request: Request, slug: str, record_id: str):
    """Render a draft through the PUBLIC section template, admin-only, so
    the owner sees exactly how it will look before posting."""
    if (r := _need_login(request)):
        return r
    if slug not in C.SECTIONS:
        return RedirectResponse("/admin", status_code=303)
    rec = store.get_record(slug, record_id)
    if not rec:
        return RedirectResponse(f"/admin/sections/{slug}", status_code=303)
    title, kicker, intro = C.SECTIONS[slug]
    return _render(request, "section.html", _ctx(
        request, nav=slug, slug=slug, title=title, kicker=kicker, intro=intro,
        empty_state=C.EMPTY_STATE, published_records=[rec], preview=True,
        page_bg=store.get_background(slug)))


@router.post("/sections/{slug}/background")
def set_background(request: Request, slug: str, background: str = Form("")):
    if (r := _need_login(request)):
        return r
    if slug in C.SECTIONS:
        store.set_background(slug, background)
    return RedirectResponse(f"/admin/sections/{slug}", status_code=303)


# --- Media library ------------------------------------------------------------

@router.get("/media/originals/{name}")
def original_media(request: Request, name: str):
    """Originals are admin-only — they are never served publicly."""
    if (r := _need_login(request)):
        return r
    from fastapi import HTTPException
    from fastapi.responses import FileResponse
    f = store.MEDIA_ORIGINALS / Path(name).name
    if not f.exists() or not f.is_file():
        raise HTTPException(404)
    return FileResponse(f)


@router.get("/media", response_class=HTMLResponse)
def media_library(request: Request):
    if (r := _need_login(request)):
        return r
    return _render(request, "admin/media.html",
                   _ctx(request, media=store.list_media(), filters=media_lib.FILTERS))


_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


@router.post("/media/upload")
async def upload_media(request: Request, file: UploadFile = File(...),
                       alt: str = Form("")):
    if (r := _need_login(request)):
        return r
    ext = Path(file.filename or "").suffix.lower()
    if ext not in media_lib.ALLOWED_EXTS:
        return RedirectResponse("/admin/media?error=type", status_code=303)
    safe = _SAFE_NAME.sub("_", Path(file.filename).stem)[:40]
    name = f"{uuid.uuid4().hex[:8]}-{safe}{ext}"
    dest = store.MEDIA_ORIGINALS / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with dest.open("wb") as f:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > 50 * 1024 * 1024:
                dest.unlink(missing_ok=True)
                return RedirectResponse("/admin/media?error=size", status_code=303)
            f.write(chunk)
    (dest.with_suffix(dest.suffix + ".json")).write_text(
        json.dumps({"alt": alt.strip(), "kind": "original"}, ensure_ascii=False),
        encoding="utf-8")
    return RedirectResponse("/admin/media", status_code=303)


@router.post("/media/derive")
def derive_media(request: Request, source: str = Form(""),
                 filter_name: str = Form("none"),
                 crop: str = Form(""), rotate: float = Form(0.0),
                 alt: str = Form("")):
    """Build a filtered/cropped/rotated DERIVATIVE. The original is never touched."""
    if (r := _need_login(request)):
        return r
    src = store.MEDIA_ORIGINALS / Path(source).name
    if not src.exists():
        return RedirectResponse("/admin/media?error=missing", status_code=303)
    stem, ext = src.stem, src.suffix.lower()
    if ext in media_lib.VIDEO_EXTS:
        # No pixel work for video: copy as-is to derived/ so it gets a public URL.
        dest = store.MEDIA_DERIVED / f"{stem}-copy{ext}"
        shutil.copyfile(src, dest)
    else:
        crop_box = None
        if crop.strip():
            try:
                x, y, w, h = (float(v) for v in crop.split(","))
                crop_box = (x, y, w, h)
            except ValueError:
                crop_box = None
        tag = filter_name if filter_name != "none" else "plain"
        if crop_box:
            tag += "-cropped"
        if rotate:
            tag += "-rotated"
        dest = store.MEDIA_DERIVED / f"{stem}-{tag}{ext}"
        media_lib.derive_image(src, dest, filter_name, crop_box, rotate)
    (dest.with_suffix(dest.suffix + ".json")).write_text(json.dumps(
        {"alt": alt.strip(), "kind": "derived", "filter": filter_name,
         "source": src.name}, ensure_ascii=False), encoding="utf-8")
    return RedirectResponse("/admin/media", status_code=303)


@router.post("/media/delete")
def delete_media(request: Request, name: str = Form("")):
    if (r := _need_login(request)):
        return r
    for base in (store.MEDIA_ORIGINALS, store.MEDIA_DERIVED):
        p = base / Path(name).name
        if p.exists():
            p.unlink()
            p.with_suffix(p.suffix + ".json").unlink(missing_ok=True)
    return RedirectResponse("/admin/media", status_code=303)
