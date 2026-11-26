# srspady.com — S. R. Spady, A Life in Progress

A lifelong personal website: living autobiography, digital museum,
personal archive and private Life OS (the archive and Life OS arrive in
later phases). This repository is Phase 2 — the public site.

- **Design:** the Workshop (Direction B) — graph paper, dark bench-ink,
  safety-orange accents. See `docs/DESIGN_SYSTEM.md`.
- **Stack:** FastAPI + Jinja2 + Uvicorn — the same three dependencies as
  SpencerLab. No database. All content lives in `app/content.py` as plain
  Python data, so records can be edited without touching templates.
- **Content rule:** only verified facts are published. Where no record
  exists yet, the page shows an empty state — never a fabricated record.

## Sections

22 sections: about, travels (+ map, destinations, journal, gallery,
guides, bucket-list, book), studies, built, repaired, knowledge, lab,
career, ventures, research, library, photography, memories, journal,
interests, skills, achievements, ambitions, timeline, legacy, contact
— 21 sections plus the homepage.

SpencerLab (`spencerlab.tech`) and Farelune (`farelune.com`) stay
independent sites, linked from here. Travelpayouts stays inside Farelune
only — there is no Travelpayouts integration, booking engine or
Travelpayouts credential in this repository.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 — every route is listed in `app/main.py`.

## Deploy

See `DEPLOYMENT_GUIDE.md`. Summary: git pull + `systemctl restart
srspady` on UbuntuServ, behind a Cloudflare Tunnel. Deploy is Spencer's
step; DNS and hosting decisions are his, not covered here.

## Project layout

```
app/main.py       FastAPI app, routes, sitemap/robots/healthz, custom 404
app/content.py    All shared content as plain Python data
templates/        base.html + one template per section family
static/           site.css (Workshop design system), site.js (theme + nav)
docs/             DESIGN_SYSTEM.md
```

## Adding a record

Edit `app/content.py` — add the record to the right list (studies,
career, built projects, lab posts, ventures, destinations…). The
timeline on `/timeline` is generated from the dated records, so it picks
new dated items up automatically. Phase 3 adds an admin dashboard that
writes records without code edits.

## Admin (owner only)

The owner-only admin lives at `/admin` in this same app. No public
registration, no other users — one owner login.

### Setup (deploy time — Spencer's step)

Three environment variables, set on the server (systemd unit
`Environment=` lines or an `EnvironmentFile=`, never in git):

```bash
ADMIN_USERNAME=spencer          # the owner login name
ADMIN_PASSWORD_HASH=pbkdf2_sha256$600000$<salt hex>$<hash hex>
ADMIN_SESSION_SECRET=<a long random string>
```

Generate the hash — never type a password into chat or a file:

```bash
python3 scripts/make_admin_hash.py
```

It prompts for the password twice and prints the hash value to put in
`ADMIN_PASSWORD_HASH`. Passwords must be at least 12 characters. Without
all three variables set, the admin login is disabled (the login page says
so, and no login succeeds).

### Login flow

1. Go to `/admin/login`, enter the username and password.
2. A signed session cookie keeps the owner logged in; `/admin/logout`
   ends it. Every `/admin` route except the login page redirects to
   `/admin/login` when unauthenticated.
3. Five failed logins from one address lock that address out for
   15 minutes.

### What the admin does

- **Dashboard** (`/admin`) — all sections with draft / published /
  public record counts.
- **Per-section editing** (`/admin/sections/<slug>`) — title + body with
  a hand-rolled rich-text toolbar (bold, italic, H2/H3, bullet and
  numbered lists, blockquote, link). No raw HTML: submitted HTML is
  sanitized server-side against an allowlist.
- **Background per page** — ivory paper, graph paper, dark bench-ink or
  muted gold tint, chosen per section; the public page reads the setting
  on every request.
- **Media library** (`/admin/media`) — upload images/video (stored under
  `data/media/`, gitignored, never committed). Filter presets (warm,
  cool, black-and-white, faded, high-contrast) plus crop and rotate are
  previewed client-side with CSS and applied server-side with Pillow to
  a **derived copy** — the original upload is never modified, and
  derivatives are saved with no EXIF data (GPS stripped).
- **Workflow** — drafts live as JSON under `data/drafts/`; **Preview**
  renders a draft through the public Workshop templates so the owner
  sees exactly how it will look; **Publish** moves it to
  `data/content/`, which the public site reads. Visibility per record:
  Public / Private / Family-only / Unlisted (default Private). Only
  Public published records ever appear on the public site — drafts,
  private records and all admin UI never do. The public site falls back
  to the built-in defaults in `app/content.py` when no published record
  exists for a section.

### Follow-up (not built yet)

MFA / passkeys for the admin login. The password + session login above
is the Phase 2 control; adding a second factor is a separate, later
step.
```

## License

Personal site. All content © S. R. Spady.
