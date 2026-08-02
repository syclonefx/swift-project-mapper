#!/usr/bin/env python3
"""Generate a concise Swift repository inventory for a project map.

This script performs mechanical discovery only. It does not attempt to replace
architectural review of the source code.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {
    ".build",
    ".git",
    ".swiftpm",
    "Build",
    "DerivedData",
    "Pods",
    "Carthage",
    "SourcePackages",
    "node_modules",
}

DECLARATION_PATTERN = re.compile(
    r"^\s*(?:@[A-Za-z_][\w.()\s,\"]*\s+)*"
    r"(?:public\s+|internal\s+|private\s+|fileprivate\s+|open\s+|package\s+)*"
    r"(?:final\s+|indirect\s+|nonisolated\s+)*"
    r"(struct|class|actor|enum|protocol|extension)\s+([A-Za-z_][A-Za-z0-9_.]*)",
    re.MULTILINE,
)

IMPORT_PATTERN = re.compile(r"^\s*import\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)


@dataclass(frozen=True)
class SwiftFileInfo:
    path: Path
    imports: tuple[str, ...]
    declarations: tuple[str, ...]
    annotations: tuple[str, ...]


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def classify_annotations(text: str) -> tuple[str, ...]:
    markers = {
        "@main": "Application or extension entry point",
        "@Model": "SwiftData model",
        "@Observable": "Observation state type",
        "ObservableObject": "Combine observable state type",
        "View": "SwiftUI view",
        "AppIntent": "App Intent",
        "Widget": "WidgetKit type",
        "XCTestCase": "XCTest type",
        "@Test": "Swift Testing tests",
        "@MainActor": "Main-actor isolated",
    }
    return tuple(description for marker, description in markers.items() if marker in text)


def scan_swift_file(path: Path) -> SwiftFileInfo:
    text = path.read_text(encoding="utf-8", errors="ignore")
    imports = tuple(sorted(set(IMPORT_PATTERN.findall(text))))
    declarations = tuple(f"{kind} {name}" for kind, name in DECLARATION_PATTERN.findall(text))
    annotations = classify_annotations(text)
    return SwiftFileInfo(path=path, imports=imports, declarations=declarations, annotations=annotations)


def discover(root: Path) -> list[SwiftFileInfo]:
    files: list[SwiftFileInfo] = []
    for path in sorted(root.rglob("*.swift")):
        relative = path.relative_to(root)
        if is_excluded(relative):
            continue
        files.append(scan_swift_file(path))
    return files


def discover_containers(root: Path) -> list[Path]:
    patterns = ("*.xcodeproj", "*.xcworkspace", "Package.swift")
    results: list[Path] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            relative = path.relative_to(root)
            if not is_excluded(relative):
                results.append(relative)
    return sorted(set(results))


def render_markdown(root: Path, files: list[SwiftFileInfo]) -> str:
    lines = [
        "<!-- BEGIN GENERATED INVENTORY -->",
        "## Generated Swift Inventory",
        "",
        "This section is mechanically generated. Verify responsibilities in source before relying on them.",
        "",
        "### Project Containers",
        "",
    ]

    containers = discover_containers(root)
    if containers:
        lines.extend(f"- `{path.as_posix()}`" for path in containers)
    else:
        lines.append("- None detected")

    grouped: dict[str, list[SwiftFileInfo]] = {}
    for info in files:
        relative = info.path.relative_to(root)
        group = relative.parts[0] if len(relative.parts) > 1 else "Root"
        grouped.setdefault(group, []).append(info)

    for group, group_files in sorted(grouped.items()):
        lines.extend(["", f"### {group}", ""])
        for info in group_files:
            relative = info.path.relative_to(root).as_posix()
            lines.append(f"#### `{relative}`")
            if info.declarations:
                lines.append(f"- Declarations: {', '.join(f'`{d}`' for d in info.declarations)}")
            if info.annotations:
                lines.append(f"- Signals: {', '.join(info.annotations)}")
            if info.imports:
                lines.append(f"- Imports: {', '.join(f'`{i}`' for i in info.imports)}")
            if not (info.declarations or info.annotations or info.imports):
                lines.append("- No declarations or imports detected")
            lines.append("")

    lines.append("<!-- END GENERATED INVENTORY -->")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Swift project inventory in Markdown.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument("--output", "-o", help="Write output to this file instead of stdout")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"Repository root does not exist or is not a directory: {root}")

    output = render_markdown(root, discover(root))
    if args.output:
        destination = Path(args.output).expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
