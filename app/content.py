"""srspady.com — all shared content as plain Python data.

Everything here is a verified fact or an explicit empty state. Nothing is
invented: where no record exists yet, the page shows an empty state and says
so. Edit this file to add records; templates never carry content of their own.

Phase 3 will add an admin dashboard that writes records here; until then,
records are added by editing this file and redeploying.
"""
from __future__ import annotations

SITE_NAME = "S. R. Spady"
SITE_TAGLINE = "A Life in Progress."
SITE_URL = "https://srspady.com"
CONTACT_EMAIL = "spencerawlson.spad@gmail.com"

HERO_LINES = [
    "Everything I've learned.",
    "Everything I've built.",
    "Everywhere I've been.",
    "Everything I'm becoming.",
]

# --- Navigation ---------------------------------------------------------------
# Primary nav groups. Footer lists every section individually.
NAV_GROUPS = [
    ("Life", ["about", "career", "memories", "interests", "achievements",
              "ambitions", "timeline", "legacy"]),
    ("Exploration", ["travels", "photography"]),
    ("Knowledge", ["studies", "knowledge", "research", "library", "skills"]),
    ("Creations", ["built", "repaired"]),
    ("Engineering", ["lab"]),
    ("Ventures", ["ventures"]),
    ("Journal", ["journal"]),
]

# slug -> (title, kicker, intro). The 21 sections (home is not a section).
SECTIONS = {
    "about": ("About", "Life",
              "A living autobiography — the story so far, in chapters, "
              "written as the life happens."),
    "travels": ("Travels", "Exploration",
                "Everywhere I've been, everywhere I'm going — journeys, "
                "destinations, guides and the road ahead."),
    "studies": ("Studies", "Knowledge",
                "What I'm learning, formally and otherwise — courses, "
                "programmes and the road to qualification."),
    "built": ("Built", "Creations",
              "Things I designed and built — systems, platforms and "
              "infrastructure, each told as a build story."),
    "repaired": ("Repaired", "Creations",
                 "Things I fixed — and what the fault taught me."),
    "knowledge": ("Knowledge", "Knowledge",
                  "What I know, organised — notes, references and working "
                  "knowledge, kept where I can find it again."),
    "lab": ("SpencerLab", "Engineering",
            "SpencerLab — Where Knowledge Becomes Practice. The working "
            "homelab and technical journal behind the builds."),
    "career": ("Career", "Life",
               "Work, so far — the jobs, the places and what each one "
               "taught me."),
    "ventures": ("Ventures", "Ventures",
                 "Businesses and projects I'm building — live, in "
                 "development, or on record."),
    "research": ("Research", "Knowledge",
                 "Questions I'm working on — investigations, assessments "
                 "and findings."),
    "library": ("Library", "Knowledge",
                "Books I've read, and what I took from them."),
    "photography": ("Photography", "Exploration",
                    "Photographs from the life — travels, work and home."),
    "memories": ("Memories", "Life",
                 "Moments worth keeping — the ones that shaped the story."),
    "journal": ("Journal", "Journal",
                "Notes from the bench — short entries on the life as it "
                "happens."),
    "interests": ("Interests", "Life",
                  "What holds my attention — the pursuits that fill the "
                  "hours outside work."),
    "skills": ("Skills", "Knowledge",
               "What I can do — skills acquired, practised and proven."),
    "achievements": ("Achievements", "Life",
                     "Milestones reached — the markers on the road so far."),
    "ambitions": ("Ambitions", "Life",
                  "Long-term objectives — where this life is headed."),
    "timeline": ("Timeline", "Life",
                 "The life in order — every dated record on the site, "
                 "newest first."),
    "legacy": ("Legacy", "Life",
               "What I want to leave behind — the work, the record and "
               "the example."),
    "contact": ("Contact", "Life",
                "Get in touch — one address, answered by me."),
}

# All 21 sections, in footer order (alphabetical by title, home excluded).
ALL_SECTIONS = sorted(SECTIONS, key=lambda s: SECTIONS[s][0].lower())

# --- My life in numbers -------------------------------------------------------
# ALL values are empty states. Never put a number here until it is calculated
# from real records. The template renders "—" plus the note below.
LIFE_NUMBERS_NOTE = "Calculated from records once they exist."
LIFE_NUMBERS = [
    ("Countries visited", "countries visited"),
    ("Cities explored", "cities explored"),
    ("Countries lived in", "countries lived in"),
    ("Journeys completed", "journeys completed"),
    ("Projects built", "projects built"),
    ("Things repaired", "things repaired"),
    ("Books read", "books read"),
    ("Courses completed", "courses completed"),
    ("Qualifications earned", "qualifications earned"),
    ("Businesses founded", "businesses founded"),
    ("Technical experiments completed", "technical experiments completed"),
    ("Skills acquired", "skills acquired"),
]

# --- Studies ------------------------------------------------------------------
STUDIES = [
    {
        "school": "MCIT — Montréal",
        "programme": "Cybersecurity & Cloud Computing",
        "status": "In progress",
        "expected": "Expected graduation December 2027",
    },
    {
        "school": "UQÀM — Université du Québec à Montréal",
        "programme": "Economics & Finance",
        "status": "In progress",
        "expected": "Expected December 2027",
    },
]
CURRENT_COURSE = {
    "title": "Cloud Architecture and Design Principles",
    "code": "420-DF9-UM / CCRS2601",
    "instructor": "Mr. Sami Islam",
    "schedule": "Tue / Thu, 6:00–9:00 p.m.",
}

# --- Career -------------------------------------------------------------------
CAREER = [
    {
        "role": "Building Management Technician",
        "org": "Altasciences",
        "dates": "April 2025 – present",
        "detail": "Health & Safety Committee member since September 2025.",
    },
    {
        "role": "Owner / Operator",
        "org": "Spadlong International",
        "dates": "≈2021 – March 2025",
        "detail": "",
    },
    {
        "role": "Muraflex",
        "org": "Muraflex",
        "dates": "2018 – 2021",
        "detail": "",
    },
    {
        "role": "Digicel Haiti",
        "org": "Digicel Haiti",
        "dates": "2012 – 2016",
        "detail": "",
    },
    {
        "role": "GOAL Ireland Haiti",
        "org": "GOAL Ireland",
        "dates": "2010 – 2012",
        "detail": "",
    },
]
LANGUAGES = [
    ("English", "Fluent"),
    ("French", "Fluent"),
    ("Haitian Creole", "Native"),
    ("Spanish", "Intermediate"),
    ("Arabic", "Learning — via Duolingo"),
]

# --- Built --------------------------------------------------------------------
# The 9-step storytelling format. Steps whose details are not yet documented
# say so honestly instead of inventing them.
BUILD_STEPS = ["Why", "What", "Design", "Materials", "Process",
               "Challenges", "Result", "Lessons", "Future"]
BUILT_PROJECTS = [
    {
        "name": "Aegis CloudOps",
        "category": "Cloud & Infrastructure",
        "dates": "2024 – present",
        "status": "In production",
        "carried_over": True,
        "steps": {
            "Why": "A cloud operations platform built from real homelab "
                   "practice — the same infrastructure that runs the lab.",
            "What": "Cloud & infrastructure platform, in production since 2024.",
            "Design": "To be documented.",
            "Materials": "To be documented.",
            "Process": "To be documented.",
            "Challenges": "To be documented.",
            "Result": "In production.",
            "Lessons": "To be documented.",
            "Future": "To be documented.",
        },
    },
    {
        "name": "LabNet Cyber Range",
        "category": "Cybersecurity",
        "dates": "2026",
        "status": "Complete",
        "carried_over": True,
        "steps": {
            "Why": "A place to practise security work safely — an isolated "
                   "range where attacks and defences can be tested for real.",
            "What": "Cybersecurity range, built 2026.",
            "Design": "To be documented.",
            "Materials": "To be documented.",
            "Process": "To be documented.",
            "Challenges": "To be documented.",
            "Result": "Built and used for assessments in 2026.",
            "Lessons": "To be documented.",
            "Future": "To be documented.",
        },
    },
    {
        "name": "Windows Server Department File Services",
        "category": "System Administration",
        "dates": "2026",
        "status": "Complete",
        "carried_over": True,
        "steps": {
            "Why": "Department file services done properly — shares, "
                   "permissions and access control that hold up under test.",
            "What": "System administration project, 2026.",
            "Design": "To be documented.",
            "Materials": "To be documented.",
            "Process": "To be documented.",
            "Challenges": "To be documented.",
            "Result": "Complete. The department-share RBAC held under an "
                      "assumed-breach assessment (see SpencerLab).",
            "Lessons": "To be documented.",
            "Future": "To be documented.",
        },
    },
    {
        "name": "GNS3 to Virtualization Interconnect",
        "category": "Networking",
        "dates": "2026",
        "status": "Complete",
        "carried_over": True,
        "steps": {
            "Why": "To connect simulated networks to real virtual machines — "
                   "so a lab topology can talk to live systems.",
            "What": "Networking project, 2026.",
            "Design": "To be documented.",
            "Materials": "To be documented.",
            "Process": "To be documented.",
            "Challenges": "To be documented.",
            "Result": "Complete.",
            "Lessons": "To be documented.",
            "Future": "To be documented.",
        },
    },
    {
        "name": "Fishing Rod",
        "category": "AI & Automation",
        "dates": "2024 – present",
        "status": "In production",
        "carried_over": True,
        "steps": {
            "Why": "An AI and automation project, built alongside Aegis "
                   "CloudOps.",
            "What": "AI & automation, in production since 2024.",
            "Design": "To be documented.",
            "Materials": "To be documented.",
            "Process": "To be documented.",
            "Challenges": "To be documented.",
            "Result": "In production.",
            "Lessons": "To be documented.",
            "Future": "To be documented.",
        },
    },
]
TECHNICAL_REPORTS = [
    {
        "title": "Internal Network Assessment — Linux Server",
        "detail": "Unauthenticated internal network penetration test.",
        "date": "17 Aug 2026",
    },
    {
        "title": "Internal Network Assessment — Linux Server (second report)",
        "detail": "Follow-up assessment.",
        "date": "30 Aug 2026",
        "status": "Complete",
    },
]

# --- SpencerLab ---------------------------------------------------------------
LAB_URL = "https://spencerlab.tech"
LAB_INTRO = ("SpencerLab — Where Knowledge Becomes Practice. The working "
             "homelab and technical journal: infrastructure built, faults "
             "repaired, systems pentested and assessed, networks "
             "administered. The commands, the wrong turns, and why each fix "
             "mattered.")
LAB_SERVICES = [
    {
        "name": "Mini home servers",
        "price": "$500–$1,500 CAD",
        "detail": "Built in person, in Montréal. Hardware at cost on top of "
                  "the build price.",
    },
    {
        "name": "Website builds",
        "price": "$1,000–$5,000 CAD",
        "detail": "Built remotely. Price depends on complexity — a landing "
                  "page starts at $1,000, a full business site runs up to "
                  "$5,000.",
    },
]
# Newest first. Summaries copied exactly from spencerlab.tech. Never republish
# LAN IP addresses from any post.
LAB_POSTS = [
    {"title": "Domainfolio: one app, a sale page for every domain",
     "date": "2026-10-16", "category": "Built",
     "url": "https://spencerlab.tech/built/domainfolio",
     "summary": "A self-hosted domain portfolio: every domain I own points at one Next.js app, which reads the Host header and renders that domain's for-sale page, with an offers inbox, per-domain visit stats and lease-to-own terms. It runs in Docker behind its own Cloudflare Tunnel, and the names are also listed on Afternic."},
    {"title": "Every VM, every night: homelab backups to the Time Capsule",
     "date": "2026-10-14", "category": "Administered",
     "url": "https://spencerlab.tech/administered/homelab-backups-time-capsule",
     "summary": "Nightly vzdump backups on all three Proxmox hosts, pushed to a Time Capsule on the LAN and pruned to four copies per guest. The pruning had never worked: one host's disk filled to 98.8% and every backup on it failed before the bug was found. Fixing it freed about 530 GB."},
    {"title": "Market-readiness review: five billing and signup holes in my own SaaS",
     "date": "2026-10-14", "category": "Assessed",
     "url": "https://spencerlab.tech/assessed/aegis-market-readiness-review",
     "summary": "A pre-launch review of Aegis CloudOps and Fishing Rod Terminal found that signup could join any tenant or choose a paid plan, checkout granted plans for free without Stripe, pay-as-you-go unlocked paid features with no card, and two products could charge each other's prices. All five were fixed and verified live. None had been used."},
    {"title": "The Great Migration: Aegis production comes home",
     "date": "2026-10-13", "category": "Built",
     "url": "https://spencerlab.tech/built/the-great-migration",
     "summary": "The production API behind Aegis CloudOps and Fishing Rod Terminal moved off a DigitalOcean droplet and onto a VM in this homelab, behind its own Cloudflare Tunnel. The move, an exposed Kubernetes API found on the new box, an outage, and the claims that had to be corrected afterwards."},
    {"title": "Cloud Migration Readiness: a 6R assessment inside Aegis",
     "date": "2026-10-13", "category": "Built",
     "url": "https://spencerlab.tech/built/aegis-migration-readiness",
     "summary": "A new Aegis feature: upload a server inventory, or run a read-only Proxmox discovery script, and get a 6R call per workload, an end-of-support check, AWS sizing at list price, a readiness score and dependency-grouped move waves. Its first real test was the Proxmox host that had just taken production out of the cloud."},
    {"title": "Road to CISSP: building a study platform from fundamentals to CISSP",
     "date": "2026-10-10", "category": "Built",
     "url": "https://spencerlab.tech/built/road-to-cissp",
     "summary": "road2cissp.com: a React study platform with an AI tutor, interactive labs, a Security+ exam simulator and synced progress. The frontend is on Vercel and the FastAPI backend runs on a Fedora VM in this homelab, behind its own Cloudflare Tunnel."},
    {"title": "A third Proxmox host, outside the cluster",
     "date": "2026-10-10", "category": "Built",
     "url": "https://spencerlab.tech/built/proxmox-third-host",
     "summary": "A third machine running Proxmox VE as a standalone host, next to the two-node cluster rather than in it. It started with the Minecraft server and now also runs production for Aegis CloudOps and Fishing Rod Terminal, with production-first boot order and nightly backups to the Time Capsule."},
    {"title": "A self-hosted Minecraft server, run with Crafty",
     "date": "2026-10-10", "category": "Administered",
     "url": "https://spencerlab.tech/administered/minecraft-server-crafty",
     "summary": "A Paper Minecraft server on its own VM on the third Proxmox host, managed with Crafty Controller, with Geyser so phones and consoles can join the Java world. The panel stays LAN-only, and this site shows the server's live status without exposing anything new."},
    {"title": "The Real-Life ATM — my backend, Claude Code's frontend",
     "date": "2026-09-24", "category": "Built",
     "url": "https://spencerlab.tech/built/the-real-life-atm",
     "summary": "A three-bank ATM in Python: I wrote the object-oriented banking backend, Claude Code built the Pygame arcade machine on top of it — and the same game now runs in your browser, compiled to WebAssembly."},
    {"title": "Proxmox & GNS3 Homelab Implementation Plan",
     "date": "2026-09-19", "category": "Built",
     "url": "https://spencerlab.tech/built/proxmox-gns3-homelab-implementation-plan",
     "summary": "Build and operations plan for a two-node Proxmox VE cluster with GNS3 network simulation and a Windows-based security workstation."},
    {"title": "Aegis Managed VPS — building in the open",
     "date": "2026-09-13", "category": "Built",
     "url": "https://spencerlab.tech/built/aegis-managed-vps",
     "summary": "A Linux-first, automation-first managed VPS service, in design. Coming soon — the trials and errors of building it will be documented and published here via Fieldnote as the work happens."},
    {"title": "LabNet Internal Assessment - UbuntuServ",
     "date": "2026-09-08", "category": "Pentested",
     "url": "https://spencerlab.tech/pentested/labnet-internal-assessment-ubuntuserv",
     "summary": "An authorized internal assessment of UbuntuServ on the isolated LabNet segment, to determine whether the host could be compromised from an attacker already positioned on the internal network."},
    {"title": "Authenticated Security Assessment - WinServ",
     "date": "2026-09-08", "category": "Assessed",
     "url": "https://spencerlab.tech/assessed/authenticated-security-assessment-winserv",
     "summary": "An assumed-breach assessment of WinServ, a Windows Server 2025 file server on LabNet. The department-share RBAC held — but exposed WinRM plus a valid admin credential gave full remote control of the server. 1 Critical, 2 Medium findings."},
    {"title": "Active Directory Domain Services",
     "date": "2026-09-08", "category": "Administered",
     "url": "https://spencerlab.tech/administered/active-directory-domain-services",
     "summary": "Building a minimal AD DS lab in VirtualBox: a static-IP Windows Server promoted to domain controller for adlab.com, DNS on the DC, and clients joined to the domain — with the DNS and time-sync warnings left open for follow-up."},
    {"title": "Going live via Cloudflare Tunnel",
     "date": "2026-09-05", "category": "Built",
     "url": "https://spencerlab.tech/built/going-live-cloudflare-tunnel",
     "summary": "Every command, manual step, and lesson from taking spencerlab.tech live over HTTPS — including the discovery that the ISP made port-forwarding physically impossible, and the tunnel that solved it."},
]

# --- Travels ------------------------------------------------------------------
FARELUNE_URL = "https://www.farelune.com"
FARELUNE_HEADING = "Inspired by my journeys? Start your own."
FARELUNE_TEXT = ("Discover destinations, compare flights and explore your "
                 "next adventure with Farelune.")
FARELUNE_DISCLOSURE = ("Farelune is my travel platform. Links to Farelune "
                       "may earn a commission at no extra cost to you — the "
                       "commission is paid by the partner.")
# Verified deep-link format (locale prefix required). Round trips of 30 days
# or fewer, or no dates at all. Fares on Farelune are cached — never call
# them "live prices". Farelune offers flights only: no hotels, car rentals,
# tours, insurance or eSIM.
DESTINATIONS = [
    {"name": "Paris", "code": "CDG",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=CDG&trip=round_trip"},
    {"name": "Rome", "code": "FCO",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=FCO"},
    {"name": "Barcelona", "code": "BCN",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=BCN"},
    {"name": "Lisbon", "code": "LIS",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=LIS"},
    {"name": "Cancún", "code": "CUN",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=CUN"},
    {"name": "Punta Cana", "code": "PUJ",
     "url": "https://www.farelune.com/en/flights?from=YUL&to=PUJ"},
]
VIDEO_SERIES = [
    {"title": "Paris or Rome?", "status": "In production"},
    {"title": "Barcelona or Lisbon?", "status": "In production"},
    {"title": "Cancún or Punta Cana?", "status": "In production"},
    {"title": "4 pièges à éviter à l'aéroport de Paris-CDG",
     "status": "In production"},
]

# --- Ventures -----------------------------------------------------------------
VENTURES = [
    {"name": "Road to CISSP", "url": "https://road2cissp.com",
     "detail": "Live study platform — from fundamentals to CISSP.",
     "status": "Live"},
    {"name": "Farelune", "url": "https://farelune.com",
     "detail": "Live travel platform — compare flights and explore destinations.",
     "status": "Live"},
    {"name": "Aegis CloudOps", "url": "",
     "detail": "Cloud & infrastructure platform.",
     "status": "In production · 2024–present"},
    {"name": "ShipItAyiti", "url": "https://shipitayiti.com",
     "detail": "Haitian producer marketplace.",
     "status": "Live"},
    {"name": "Kay Ayiti", "url": "",
     "detail": "Rental app for Haiti.",
     "status": "In development"},
    {"name": "Project Zero", "url": "",
     "detail": "Roblox game — an underground robot metropolis.",
     "status": "In development"},
    {"name": "Fishing Rod Terminal", "url": "",
     "detail": "AI & automation.",
     "status": "2024–present"},
    {"name": "Axionory", "url": "",
     "detail": "Record in progress — status being verified.",
     "status": "Status being verified"},
    {"name": "Kouzia", "url": "",
     "detail": "Record in progress — status being verified.",
     "status": "Status being verified"},
    {"name": "Se Nou S.A.", "url": "",
     "detail": "Record in progress — status being verified.",
     "status": "Status being verified"},
]

# --- Timeline -----------------------------------------------------------------
# Built from real dated records only: lab posts, career dates, studies,
# built projects and technical reports. No invented entries.
def build_timeline() -> list[dict]:
    items: list[dict] = []
    for p in LAB_POSTS:
        items.append({"date": p["date"], "kind": "SpencerLab",
                      "title": p["title"], "detail": p["summary"]})
    for r in TECHNICAL_REPORTS:
        # Dates are "17 Aug 2026" style; normalise for sorting.
        items.append({"date": r["date"], "kind": "Technical report",
                      "title": r["title"], "detail": r["detail"]})
    items.append({"date": "2025-04", "kind": "Career",
                  "title": "Building Management Technician, Altasciences",
                  "detail": "Health & Safety Committee member since "
                            "September 2025."})
    items.append({"date": "2025-03", "kind": "Career",
                  "title": "Spadlong International ends",
                  "detail": "Owner / operator, ≈2021 – March 2025."})
    items.append({"date": "2024", "kind": "Built",
                  "title": "Aegis CloudOps and Fishing Rod enter production",
                  "detail": "Both in production since 2024."})
    items.append({"date": "2021", "kind": "Career",
                  "title": "Muraflex ends; Spadlong International begins",
                  "detail": "Muraflex 2018–2021."})
    items.append({"date": "2018", "kind": "Career",
                  "title": "Muraflex begins",
                  "detail": "Muraflex 2018–2021."})
    items.append({"date": "2016", "kind": "Career",
                  "title": "Digicel Haiti ends",
                  "detail": "Digicel Haiti 2012–2016."})
    items.append({"date": "2012", "kind": "Career",
                  "title": "Digicel Haiti begins",
                  "detail": "Digicel Haiti 2012–2016."})
    items.append({"date": "2010", "kind": "Career",
                  "title": "GOAL Ireland Haiti begins",
                  "detail": "GOAL Ireland Haiti 2010–2012."})
    return items


EMPTY_STATE = ("No records published yet — records are added through the "
               "admin dashboard, coming in Phase 3.")
