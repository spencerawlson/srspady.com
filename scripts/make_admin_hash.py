#!/usr/bin/env python3
"""Make a PBKDF2-HMAC-SHA256 password hash for the srspady.com admin login.

Usage:
    python3 scripts/make_admin_hash.py

Prompts for the password twice (never echoed), then prints the hash value
to put in the ADMIN_PASSWORD_HASH environment variable. The hash format is:

    pbkdf2_sha256$<iterations>$<salt hex>$<hash hex>

Stdlib only. The password itself is never printed, stored or committed.
"""
import getpass
import hashlib
import secrets

ITERATIONS = 600_000


def make_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${dk.hex()}"


def main() -> None:
    pw = getpass.getpass("Admin password: ")
    pw2 = getpass.getpass("Repeat admin password: ")
    if pw != pw2:
        raise SystemExit("Passwords do not match.")
    if len(pw) < 12:
        raise SystemExit("Password must be at least 12 characters.")
    print()
    print("Put this in ADMIN_PASSWORD_HASH (keep it secret, never commit it):")
    print(make_hash(pw))


if __name__ == "__main__":
    main()
