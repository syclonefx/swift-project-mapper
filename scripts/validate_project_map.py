#!/usr/bin/env python3
"""Validate backtick-wrapped repository paths in a PROJECT-MAP.md file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

BACKTICK_PATTERN = re.compile(r"`([^`]+)`")
PATH_SUFFIXES = (
    ".swift",
    ".md",
    ".plist",
    ".entitlements",
    ".xcassets",
    ".xcdatamodeld",
    ".xcodeproj",
    ".xcworkspace",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
)


def looks_like_path(value: str) -> bool:
    if value.startswith(("http://", "https://")):
        return False
    return "/" in value or value.endswith(PATH_SUFFIXES) or value == "Package.swift"


def normalize(value: str) -> str:
    return value.strip().rstrip(".,:;)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate paths referenced by a project map.")
    parser.add_argument("map", help="Path to PROJECT-MAP.md")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    map_path = Path(args.map).expanduser().resolve()

    if not root.is_dir():
        parser.error(f"Repository root is not a directory: {root}")
    if not map_path.is_file():
        parser.error(f"Map file does not exist: {map_path}")

    text = map_path.read_text(encoding="utf-8", errors="ignore")
    candidates = sorted({normalize(value) for value in BACKTICK_PATTERN.findall(text) if looks_like_path(value)})

    missing: list[str] = []
    checked = 0
    for candidate in candidates:
        if any(token in candidate for token in ("<", ">", "*")):
            continue
        checked += 1
        if not (root / candidate).exists():
            missing.append(candidate)

    print(f"Checked {checked} documented paths.")
    if missing:
        print(f"Missing paths ({len(missing)}):")
        for path in missing:
            print(f"- {path}")
        return 1

    print("All checked paths exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
