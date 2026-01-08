#!/usr/bin/env python3
"""
Skill structure validation script.

Validates the internal structure of a skill to ensure consistency and navigability.

Checks:
1. No orphan .md files (files with no incoming links that should be reachable)
2. Max depth from entry points ≤ configurable limit
3. No broken links (links to non-existent files)
4. Generated files have AUTO-GENERATED headers
5. File length within recommended limits

Can be dropped into any skill directory. Configuration via .validate.json or auto-detection.

Usage:
    python structure_validate.py                    # Run all checks
    python structure_validate.py --focus subdir     # Only check subdirectory
    python structure_validate.py --graph            # Output mermaid diagram
    python structure_validate.py --root /path/to/skill  # Specify skill root
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

# Default configuration (can be overridden by .validate.json)
DEFAULT_CONFIG = {
    "max_depth": 3,
    "max_lines_warning": 300,  # Files longer than this get a warning
    "max_lines_error": 500,  # Files longer than this are flagged as errors
    "excluded_patterns": [
        "_includes/",
        "_partials/",
        "assets/",
        "scripts/",
        ".build-manifest",
    ],
    "known_issues": {},
}


def load_config(skill_root: Path) -> dict:
    """Load configuration from .validate.json or use defaults."""
    config_file = skill_root / ".validate.json"
    config = DEFAULT_CONFIG.copy()

    if config_file.exists():
        user_config = json.loads(config_file.read_text())
        config.update(user_config)

    return config


def find_entry_points(skill_root: Path) -> list[str]:
    """Auto-detect entry points (skill.md, SKILL.md files)."""
    entry_points = []

    # Check root level
    for name in ["skill.md", "SKILL.md"]:
        if (skill_root / name).exists():
            entry_points.append(name)

    # Check immediate subdirectories for SKILL.md
    for subdir in skill_root.iterdir():
        if subdir.is_dir() and not subdir.name.startswith((".", "_")):
            for name in ["skill.md", "SKILL.md"]:
                if (subdir / name).exists():
                    entry_points.append(f"{subdir.name}/{name}")

    return entry_points


def should_exclude(path: Path, patterns: list[str]) -> bool:
    """Check if a file should be excluded from orphan detection."""
    path_str = str(path)
    return any(pattern in path_str for pattern in patterns)


def extract_links(file_path: Path) -> list[tuple[str, int]]:
    """Extract markdown links from a file. Returns [(target, line_number), ...]."""
    content = file_path.read_text()
    links = []

    for i, line in enumerate(content.split("\n"), 1):
        # Match [text](path) but not [text](http...) or [text](#anchor)
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            target = match.group(2)
            # Skip external links, anchors, and non-md files
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Remove anchor from link
            target = target.split("#")[0]
            if target:
                links.append((target, i))

    return links


def resolve_link(source: Path, target: str) -> Path | None:
    """Resolve a relative link to an absolute path."""
    resolved = (source.parent / target).resolve()

    if resolved.exists():
        return resolved

    # Try with .md extension
    if not target.endswith(".md"):
        resolved_md = (source.parent / (target + ".md")).resolve()
        if resolved_md.exists():
            return resolved_md

    return None


def build_link_graph(skill_root: Path, excluded_patterns: list[str]) -> tuple[dict, dict, list]:
    """Build a graph of links between files."""
    incoming = defaultdict(list)
    outgoing = defaultdict(list)
    broken = []

    for md_file in skill_root.rglob("*.md"):
        if should_exclude(md_file.relative_to(skill_root), excluded_patterns):
            continue

        rel_source = md_file.relative_to(skill_root)

        for target, line_num in extract_links(md_file):
            resolved = resolve_link(md_file, target)

            if resolved is None:
                broken.append((str(rel_source), target, line_num))
            elif resolved.is_relative_to(skill_root):
                rel_target = resolved.relative_to(skill_root)
                incoming[str(rel_target)].append(str(rel_source))
                outgoing[str(rel_source)].append(str(rel_target))

    return dict(incoming), dict(outgoing), broken


def find_orphans(
    skill_root: Path, incoming: dict, entry_points: list[str], excluded_patterns: list[str]
) -> list[str]:
    """Find .md files with no incoming links."""
    orphans = []

    for md_file in skill_root.rglob("*.md"):
        rel_path = md_file.relative_to(skill_root)
        rel_str = str(rel_path)

        if should_exclude(rel_path, excluded_patterns):
            continue

        if rel_str in entry_points:
            continue

        if rel_str not in incoming:
            orphans.append(rel_str)

    return sorted(orphans)


def calculate_depths(entry_points: list[str], outgoing: dict, skill_root: Path) -> dict[str, int]:
    """Calculate depth from entry points using BFS."""
    depths = {}

    queue = []
    for entry in entry_points:
        entry_path = skill_root / entry
        if entry_path.exists():
            depths[entry] = 0
            queue.append((entry, 0))

    while queue:
        current, depth = queue.pop(0)

        for target in outgoing.get(current, []):
            if target not in depths:
                depths[target] = depth + 1
                queue.append((target, depth + 1))

    return depths


def find_deep_files(depths: dict, max_depth: int) -> list[tuple[str, int]]:
    """Find files deeper than max_depth."""
    return sorted([(f, d) for f, d in depths.items() if d > max_depth], key=lambda x: (-x[1], x[0]))


def check_generated_headers(skill_root: Path) -> list[str]:
    """Check that generated files have AUTO-GENERATED headers."""
    missing_headers = []

    for j2_file in skill_root.rglob("*.md.j2"):
        output_file = j2_file.with_suffix("")

        if output_file.exists():
            content = output_file.read_text()
            if not content.startswith("<!-- AUTO-GENERATED"):
                rel_path = output_file.relative_to(skill_root)
                missing_headers.append(str(rel_path))

    return missing_headers


def check_file_lengths(
    skill_root: Path,
    excluded_patterns: list[str],
    max_warning: int,
    max_error: int,
) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    """Check file lengths against thresholds.

    Returns:
        (errors, warnings) - Lists of (path, line_count) tuples
    """
    errors = []
    warnings = []

    for md_file in skill_root.rglob("*.md"):
        rel_path = md_file.relative_to(skill_root)

        if should_exclude(rel_path, excluded_patterns):
            continue

        try:
            content = md_file.read_text()
            line_count = len(content.split("\n"))

            if line_count > max_error:
                errors.append((str(rel_path), line_count))
            elif line_count > max_warning:
                warnings.append((str(rel_path), line_count))
        except Exception:
            pass  # Skip files that can't be read

    # Sort by line count descending
    errors.sort(key=lambda x: -x[1])
    warnings.sort(key=lambda x: -x[1])

    return errors, warnings


def generate_mermaid_graph(outgoing: dict, depths: dict) -> str:
    """Generate a mermaid flowchart of the link structure."""
    lines = ["```mermaid", "flowchart TD"]

    by_depth = defaultdict(list)
    for f, d in depths.items():
        by_depth[d].append(f)

    for depth in sorted(by_depth.keys()):
        lines.append(f"    subgraph Depth{depth}[Depth {depth}]")
        for f in sorted(by_depth[depth]):
            node_id = re.sub(r"[^a-zA-Z0-9]", "_", f)
            display = Path(f).name
            lines.append(f'        {node_id}["{display}"]')
        lines.append("    end")

    for source, targets in outgoing.items():
        source_id = re.sub(r"[^a-zA-Z0-9]", "_", source)
        for target in targets:
            if target in depths:
                target_id = re.sub(r"[^a-zA-Z0-9]", "_", target)
                lines.append(f"    {source_id} --> {target_id}")

    lines.append("```")
    return "\n".join(lines)


def is_known_issue(known_issues: dict, category: str, path: str) -> bool:
    """Check if an issue is in the known issues list."""
    patterns = known_issues.get(category, [])
    return any(pattern in path for pattern in patterns)


def matches_focus(path: str, focus: str | None) -> bool:
    """Check if a path matches the focus filter."""
    if focus is None:
        return True
    return path.startswith(focus + "/") or path == focus


def find_skill_root(start: Path) -> Path:
    """Find skill root by looking for skill.md or SKILL.md."""
    current = start
    while current != current.parent:
        if (current / "skill.md").exists() or (current / "SKILL.md").exists():
            return current
        current = current.parent
    return start


def main():
    parser = argparse.ArgumentParser(description="Validate skill structure")
    parser.add_argument("--graph", action="store_true", help="Output mermaid graph")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--focus", type=str, help="Focus on subdirectory")
    parser.add_argument("--strict", action="store_true", help="Don't suppress known issues")
    parser.add_argument("--root", type=Path, help="Skill root directory")
    args = parser.parse_args()

    # Determine skill root
    if args.root:
        skill_root = args.root.resolve()
    else:
        skill_root = find_skill_root(Path(__file__).parent)

    if not skill_root.exists():
        print(f"Error: Skill root not found: {skill_root}")
        return 1

    # Load configuration
    config = load_config(skill_root)
    entry_points = find_entry_points(skill_root)
    max_depth = config["max_depth"]
    excluded_patterns = config["excluded_patterns"]
    known_issues = config.get("known_issues", {})

    focus_msg = f" (focus: {args.focus}/)" if args.focus else ""
    print(f"Validating {skill_root.name} skill{focus_msg}...\n")

    if args.verbose:
        print(f"Entry points: {entry_points}")

    # Build link graph
    incoming, outgoing, broken = build_link_graph(skill_root, excluded_patterns)
    depths = calculate_depths(entry_points, outgoing, skill_root)

    issues = 0
    suppressed = 0

    # Check for broken links
    filtered_broken = []
    for source, target, line in broken:
        if not matches_focus(source, args.focus):
            continue
        if not args.strict and is_known_issue(known_issues, "broken_links", source):
            suppressed += 1
            continue
        filtered_broken.append((source, target, line))

    if filtered_broken:
        print(f"❌ BROKEN LINKS ({len(filtered_broken)}):")
        for source, target, line in filtered_broken:
            print(f"   {source}:{line} -> {target}")
        issues += len(filtered_broken)
        print()
    else:
        print("✅ No broken links")

    # Check for orphans
    orphans = find_orphans(skill_root, incoming, entry_points, excluded_patterns)
    filtered_orphans = [o for o in orphans if matches_focus(o, args.focus)]
    if filtered_orphans:
        print(f"\n❌ ORPHAN FILES ({len(filtered_orphans)}) - no incoming links:")
        for orphan in filtered_orphans:
            print(f"   {orphan}")
        issues += len(filtered_orphans)
    else:
        print("✅ No orphan files")

    # Check for deep files
    deep = find_deep_files(depths, max_depth)
    filtered_deep = []
    for f, d in deep:
        if not matches_focus(f, args.focus):
            continue
        if not args.strict and is_known_issue(known_issues, "deep_files", f):
            suppressed += 1
            continue
        filtered_deep.append((f, d))

    if filtered_deep:
        print(f"\n❌ FILES TOO DEEP ({len(filtered_deep)}) - depth > {max_depth}:")
        for f, d in filtered_deep:
            print(f"   {f} (depth {d})")
        issues += len(filtered_deep)
    else:
        print(f"✅ All files within depth {max_depth}")

    # Check for unreachable files
    all_md = set()
    for md_file in skill_root.rglob("*.md"):
        rel = md_file.relative_to(skill_root)
        if not should_exclude(rel, excluded_patterns):
            all_md.add(str(rel))

    unreachable = all_md - set(depths.keys()) - set(entry_points)
    unreachable = unreachable - set(orphans)
    filtered_unreachable = [u for u in unreachable if matches_focus(u, args.focus)]
    if filtered_unreachable:
        count = len(filtered_unreachable)
        print(f"\n❌ UNREACHABLE FILES ({count}) - not connected to any entry point:")
        for f in sorted(filtered_unreachable):
            print(f"   {f}")
        issues += len(filtered_unreachable)

    # Check generated file headers
    missing_headers = check_generated_headers(skill_root)
    filtered_headers = [h for h in missing_headers if matches_focus(h, args.focus)]
    if filtered_headers:
        print(f"\n❌ MISSING AUTO-GENERATED HEADERS ({len(filtered_headers)}):")
        for f in filtered_headers:
            print(f"   {f}")
        issues += len(filtered_headers)
    else:
        print("✅ All generated files have headers")

    # Check file lengths
    max_warning = config.get("max_lines_warning", 300)
    max_error = config.get("max_lines_error", 500)
    length_errors, length_warnings = check_file_lengths(
        skill_root, excluded_patterns, max_warning, max_error
    )

    # Filter by focus
    length_errors = [(f, n) for f, n in length_errors if matches_focus(f, args.focus)]
    length_warnings = [(f, n) for f, n in length_warnings if matches_focus(f, args.focus)]

    # Apply known issues filtering
    if not args.strict:
        filtered_errors = []
        for f, n in length_errors:
            if is_known_issue(known_issues, "long_files", f):
                suppressed += 1
            else:
                filtered_errors.append((f, n))
        length_errors = filtered_errors

        filtered_warnings = []
        for f, n in length_warnings:
            if is_known_issue(known_issues, "long_files", f):
                suppressed += 1
            else:
                filtered_warnings.append((f, n))
        length_warnings = filtered_warnings

    if length_errors:
        print(f"\n❌ FILES TOO LONG ({len(length_errors)}) - exceeds {max_error} lines:")
        for f, n in length_errors:
            print(f"   {f} ({n} lines)")
        issues += len(length_errors)

    if length_warnings:
        print(f"\n⚠️  LONG FILES ({len(length_warnings)}) - exceeds {max_warning} lines:")
        for f, n in length_warnings:
            print(f"   {f} ({n} lines)")
        # Warnings don't count as issues but are displayed

    if not length_errors and not length_warnings:
        print(f"✅ All files within {max_warning} lines")

    # Summary
    print(f"\n{'─' * 40}")
    if issues == 0:
        print("✅ All checks passed!")
    else:
        print(f"❌ {issues} issue(s) found")

    if suppressed > 0:
        print(f"   ({suppressed} known issues suppressed, use --strict to show)")

    if args.verbose:
        focused_md = [f for f in all_md if matches_focus(f, args.focus)]
        print("\nStats:")
        print(f"  Total .md files: {len(focused_md)}")
        print(f"  Entry points: {len(entry_points)}")
        print(f"  Max depth found: {max(depths.values()) if depths else 0}")
        print(f"  Links tracked: {sum(len(v) for v in outgoing.values())}")

        # File length stats
        all_lengths = []
        for md_file in skill_root.rglob("*.md"):
            rel = md_file.relative_to(skill_root)
            if not should_exclude(rel, excluded_patterns) and matches_focus(str(rel), args.focus):
                try:
                    all_lengths.append(len(md_file.read_text().split("\n")))
                except Exception:
                    pass
        if all_lengths:
            avg = sum(all_lengths) // len(all_lengths)
            print(f"  File lengths: min={min(all_lengths)}, avg={avg}, max={max(all_lengths)}")

    if args.graph:
        print("\n" + generate_mermaid_graph(outgoing, depths))

    return 0 if issues == 0 else 1


if __name__ == "__main__":
    exit(main())
