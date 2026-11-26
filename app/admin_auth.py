"""srspady.com admin — owner-only authentication.

Single owner, no registration, no other users. Credentials come from
environment variables ONLY — never hardcoded, never committed:

- ADMIN_USERNAME        the owner's login name
- ADMIN_PASSWORD_HASH   PBKDF2-HMAC-SHA256 hash from scripts/make_admin_hash.py
- ADMIN_SESSION_SECRET  secret for the signed session cookie

Login is a session form (Starlette SessionMiddleware). Every /admin route
except /admin/login redirects to /admin/login when unauthenticated.
A simple in-memory throttle slows brute force: 5 failed attempts from one
address locks that address out for 15 minutes.

MFA / passkeys are NOT built here — recorded as a follow-up in the README.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import time
from functools import wraps

from fastapi import Request
from fastapi.responses import RedirectResponse

SESSION_KEY = "admin_user"

# --- Throttle: ip -> (failures, locked_until) -----------------------------------
_ATTEMPTS: dict[str, tuple[int, float]] = {}
MAX_FAILURES = 5
LOCKOUT_SECONDS = 15 * 60


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def is_locked_out(request: Request) -> bool:
    failures, locked_until = _ATTEMPTS.get(_client_ip(request), (0, 0.0))
    if locked_until and time.time() < locked_until:
        return True
    if locked_until and time.time() >= locked_until:
        _ATTEMPTS.pop(_client_ip(request), None)
    return False


def record_failure(request: Request) -> None:
    ip = _client_ip(request)
    failures, _ = _ATTEMPTS.get(ip, (0, 0.0))
    failures += 1
    locked_until = time.time() + LOCKOUT_SECONDS if failures >= MAX_FAILURES else 0.0
    _ATTEMPTS[ip] = (failures, locked_until)


def record_success(request: Request) -> None:
    _ATTEMPTS.pop(_client_ip(request), None)


# --- Password check -------------------------------------------------------------

def _parse_hash(stored: str) -> tuple[int, bytes, bytes] | None:
    try:
        scheme, iters, salt_hex, hash_hex = stored.split("$")
        if scheme != "pbkdf2_sha256":
            return None
        return int(iters), bytes.fromhex(salt_hex), bytes.fromhex(hash_hex)
    except (ValueError, TypeError):
        return None


def verify_password(password: str, stored: str) -> bool:
    parsed = _parse_hash(stored)
    if not parsed:
        return False
    iterations, salt, expected = parsed
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(dk, expected)


def check_login(username: str, password: str) -> bool:
    """True only when the env vars are set AND the credentials match."""
    env_user = os.environ.get("ADMIN_USERNAME", "")
    env_hash = os.environ.get("ADMIN_PASSWORD_HASH", "")
    if not env_user or not env_hash:
        return False
    if not hmac.compare_digest(username.encode(), env_user.encode()):
        return False
    return verify_password(password, env_hash)


def is_admin_configured() -> bool:
    return bool(os.environ.get("ADMIN_USERNAME") and os.environ.get("ADMIN_PASSWORD_HASH")
                and os.environ.get("ADMIN_SESSION_SECRET"))


def is_logged_in(request: Request) -> bool:
    return bool(request.session.get(SESSION_KEY))


def login_required(request: Request):
    """Return a redirect response when unauthenticated, else None."""
    if not is_logged_in(request):
        return RedirectResponse("/admin/login", status_code=303)
    return None
