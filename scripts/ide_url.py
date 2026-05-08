#!/usr/bin/env python3
"""Normalize a 1C:Element IDE id or URL into the IDE workspace API URL."""

from __future__ import annotations

import re
import sys


UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def normalize(value: str, host: str = "https://app-71777.1cmycloud.com") -> str:
    value = value.strip()
    if not value:
        raise ValueError("empty IDE id or URL")
    if value.startswith("http://") or value.startswith("https://"):
        return value if value.endswith("/") else value + "/"
    match = UUID_RE.search(value)
    if not match:
        raise ValueError("expected an IDE UUID or full IDE URL")
    return f"{host.rstrip('/')}/ide/api/v1/{match.group(0)}/"


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("Usage: ide_url.py <ide-id-or-url> [https://app-host.1cmycloud.com]", file=sys.stderr)
        return 2
    host = argv[2] if len(argv) == 3 else "https://app-71777.1cmycloud.com"
    try:
        print(normalize(argv[1], host))
    except ValueError as exc:
        print(f"ide_url.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
