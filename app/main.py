"""srspady.com — S. R. Spady, A Life in Progress.

A small FastAPI + Jinja2 site (same three dependencies as SpencerLab:
fastapi, uvicorn[standard], jinja2), served through a Cloudflare Tunnel
on UbuntuServ. All content lives in app/content.py as plain Python data —
no database, no admin yet (Phase 3).

Routes: one per section (see app/content.py SECTIONS) plus the travels
sub-routes, /sitemap.xml, /robots.txt and /healthz. Unknown paths get a
custom 404 page.
"""
from __future__ import annotations

import os
import secrets
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from app import admin as admin_routes
from app import admin_auth as auth
from app import content as C
from app import store

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://srspady.com"

app = FastAPI(title="srspady.com", docs_url=None, redoc_url=None, openapi_url=None)
# Session cookie for the owner-only /admin login. The secret comes from
# ADMIN_SESSION_SECRET; without it a random per-process secret is used and
# the admin login stays disabled (check_login requires the env vars anyway).
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("ADMIN_SESSION_SECRET") or secrets.token_hex(32),
                   same_site="lax")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
app.include_router(admin_routes.router)
templates = Jinja2Templates(directory=str(ROOT / "templates"))


def _pretty_date(value: str) -> str:
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y", "%d %b %Y"):
        try:
            d = datetime.strptime(value, fmt).date()
            return f"{d:%b} {d.day}, {d.year}" if fmt in ("%Y-%m-%d", "%d %b %Y") else (
                f"{d:%b} {d.year}" if fmt == "%Y-%m" else f"{d.year}")
        except (TypeError, ValueError):
            continue
    return value or ""


templates.env.filters["pretty_date"] = _pretty_date


def _sort_key(item: dict) -> tuple:
    v = item.get("date", "")
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y", "%d %b %Y"):
        try:
            d = datetime.strptime(v, fmt).date()
            return (d.year, d.month, d.day)
        except (TypeError, ValueError):
            continue
    return (0, 0, 0)


def _render(request: Request, name: str, ctx: dict, status_code: int = 200) -> HTMLResponse:
    ctx.setdefault("year", date.today().year)
    ctx.setdefault("nav", None)
    ctx.setdefault("nav_groups", C.NAV_GROUPS)
    ctx.setdefault("sections", C.SECTIONS)
    ctx.setdefault("all_sections", C.ALL_SECTIONS)
    ctx.setdefault("contact_email", C.CONTACT_EMAIL)
    ctx.setdefault("site_url", BASE_URL)
    ctx.setdefault("page_bg", "graph-paper")
    ctx.setdefault("published_records", [])
    ctx.setdefault("preview", False)
    return templates.TemplateResponse(request, name, ctx, status_code=status_code)


@app.exception_handler(StarletteHTTPException)
async def _http_error(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return _render(request, "404.html", {"path": request.url.path}, status_code=404)
    return Response(f"{exc.status_code} — {exc.detail}", status_code=exc.status_code)


# --- Home ---------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return _render(request, "home.html", {
        "nav": "home",
        "hero_lines": C.HERO_LINES,
        "life_numbers": C.LIFE_NUMBERS,
        "life_numbers_note": C.LIFE_NUMBERS_NOTE,
        "lab_posts": C.LAB_POSTS[:3],
        "built": C.BUILT_PROJECTS[:3],
        "ventures": C.VENTURES[:4],
        "timeline": sorted(C.build_timeline(), key=_sort_key, reverse=True)[:5],
        "studies": C.STUDIES,
        "destinations": C.DESTINATIONS,
        "video_series": C.VIDEO_SERIES,
    })


# --- Sections -----------------------------------------------------------------

def _section(request: Request, slug: str, template: str = "section.html", **extra):
    title, kicker, intro = C.SECTIONS[slug]
    # Published PUBLIC records from the admin store come first; when none
    # exist the page falls back to the built-in defaults in app/content.py.
    # Drafts and non-public records never reach a public template.
    return _render(request, template, {
        "nav": slug, "slug": slug, "title": title, "kicker": kicker,
        "intro": intro, "empty_state": C.EMPTY_STATE,
        "published_records": store.published_public(slug),
        "page_bg": store.get_background(slug), **extra,
    })


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return _section(request, "about", "about.html",
                    studies=C.STUDIES, career=C.CAREER, languages=C.LANGUAGES)


@app.get("/studies", response_class=HTMLResponse)
def studies(request: Request):
    return _section(request, "studies", "studies.html",
                    studies=C.STUDIES, course=C.CURRENT_COURSE)


@app.get("/career", response_class=HTMLResponse)
def career(request: Request):
    return _section(request, "career", "career.html",
                    career=C.CAREER, languages=C.LANGUAGES)


@app.get("/built", response_class=HTMLResponse)
def built(request: Request):
    return _section(request, "built", "built.html",
                    projects=C.BUILT_PROJECTS, steps=C.BUILD_STEPS,
                    reports=C.TECHNICAL_REPORTS)


@app.get("/repaired", response_class=HTMLResponse)
def repaired(request: Request):
    return _section(request, "repaired")


@app.get("/knowledge", response_class=HTMLResponse)
def knowledge(request: Request):
    return _section(request, "knowledge")


@app.get("/research", response_class=HTMLResponse)
def research(request: Request):
    return _section(request, "research")


@app.get("/library", response_class=HTMLResponse)
def library(request: Request):
    return _section(request, "library")


@app.get("/skills", response_class=HTMLResponse)
def skills(request: Request):
    return _section(request, "skills", languages=C.LANGUAGES)


@app.get("/lab", response_class=HTMLResponse)
def lab(request: Request):
    return _section(request, "lab", "lab.html",
                    lab_url=C.LAB_URL, lab_intro=C.LAB_INTRO,
                    posts=C.LAB_POSTS, services=C.LAB_SERVICES)


@app.get("/ventures", response_class=HTMLResponse)
def ventures(request: Request):
    return _section(request, "ventures", "ventures.html", ventures=C.VENTURES)


@app.get("/photography", response_class=HTMLResponse)
def photography(request: Request):
    return _section(request, "photography")


@app.get("/memories", response_class=HTMLResponse)
def memories(request: Request):
    return _section(request, "memories")


@app.get("/journal", response_class=HTMLResponse)
def journal(request: Request):
    return _section(request, "journal")


@app.get("/interests", response_class=HTMLResponse)
def interests(request: Request):
    return _section(request, "interests")


@app.get("/achievements", response_class=HTMLResponse)
def achievements(request: Request):
    return _section(request, "achievements")


@app.get("/ambitions", response_class=HTMLResponse)
def ambitions(request: Request):
    return _section(request, "ambitions")


@app.get("/legacy", response_class=HTMLResponse)
def legacy(request: Request):
    return _section(request, "legacy")


@app.get("/timeline", response_class=HTMLResponse)
def timeline(request: Request):
    items = sorted(C.build_timeline(), key=_sort_key, reverse=True)
    return _section(request, "timeline", "timeline.html", items=items)


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return _section(request, "contact", "contact.html")


# --- Travels ------------------------------------------------------------------

def _travels_ctx():
    return {
        "farelune_url": C.FARELUNE_URL, "farelune_heading": C.FARELUNE_HEADING,
        "farelune_text": C.FARELUNE_TEXT, "disclosure": C.FARELUNE_DISCLOSURE,
        "destinations": C.DESTINATIONS, "video_series": C.VIDEO_SERIES,
    }


@app.get("/travels", response_class=HTMLResponse)
def travels(request: Request):
    return _section(request, "travels", "travels.html", **_travels_ctx())


@app.get("/travels/map", response_class=HTMLResponse)
def travels_map(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Map", sub_intro="A map of everywhere I've been — "
                    "drawn from journey records once they exist.",
                    **_travels_ctx())


@app.get("/travels/destinations", response_class=HTMLResponse)
def travels_destinations(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Destinations", sub_intro="Places worth going — "
                    "each one with a Farelune link to compare flights.",
                    show_destinations=True, **_travels_ctx())


@app.get("/travels/journal", response_class=HTMLResponse)
def travels_journal(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Travel journal",
                    sub_intro="Notes from the road — written while travelling.",
                    **_travels_ctx())


@app.get("/travels/gallery", response_class=HTMLResponse)
def travels_gallery(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Gallery",
                    sub_intro="Photographs from the road.",
                    show_gallery=True, **_travels_ctx())


@app.get("/travels/guides", response_class=HTMLResponse)
def travels_guides(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Guides",
                    sub_intro="Practical guides from journeys taken — "
                    "written from experience, not from research.",
                    **_travels_ctx())


@app.get("/travels/bucket-list", response_class=HTMLResponse)
def travels_bucket(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Bucket list",
                    sub_intro="Where I want to go next.",
                    show_destinations=True, **_travels_ctx())


@app.get("/travels/book", response_class=HTMLResponse)
def travels_book(request: Request):
    return _section(request, "travels", "travels_sub.html",
                    sub="Book",
                    sub_intro="Start a journey — compare flights on Farelune.",
                    show_destinations=True, **_travels_ctx())


# --- Feeds & health -----------------------------------------------------------

@app.get("/healthz")
def healthz():
    return {"status": "ok", "sections": len(C.SECTIONS),
            "admin_configured": auth.is_admin_configured()}


@app.get("/media/{name}")
def public_media(name: str):
    """Serve DERIVED media only — the files published records may reference.
    Original uploads are never served publicly."""
    f = store.MEDIA_DERIVED / Path(name).name
    if not f.exists() or not f.is_file():
        from fastapi import HTTPException
        raise HTTPException(404)
    return FileResponse(f, headers={"Cache-Control": "public, max-age=86400"})


@app.get("/sitemap.xml")
def sitemap():
    urls = ["/"] + [f"/{s}" for s in C.SECTIONS]
    urls += ["/travels/map", "/travels/destinations", "/travels/journal",
             "/travels/gallery", "/travels/guides", "/travels/bucket-list",
             "/travels/book"]
    xml = "".join(f"<url><loc>{BASE_URL}{u}</loc></url>" for u in urls)
    return Response('<?xml version="1.0" encoding="UTF-8"?>'
                    f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xml}</urlset>',
                    media_type="application/xml")


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"
