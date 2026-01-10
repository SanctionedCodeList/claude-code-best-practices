#!/usr/bin/env python3
"""
Generate a sitemap for a skill.

Produces a hierarchical listing of all files with descriptions,
pulled from ## Links sections or file content.

Usage:
    python scripts/sitemap.py [skill_path]
    python scripts/sitemap.py --root /path/to/skill
    python scripts/sitemap.py --root /path/to/skill --output SITEMAP.md
    python scripts/sitemap.py --root /path/to/skill --include-exceptions

If no path provided, auto-detects skill root from current directory.
"""

import argparse
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FileInfo:
    path: Path
    rel_path: Path
    title: str
    description: str
    is_index: bool
    is_exception: bool


def is_exception_folder(path: Path) -> bool:
    """Check if path is in an exception folder (prefixed with _)."""
    return any(part.startswith("_") for part in path.parts)


def extract_title(content: str) -> str:
    """Extract the first # heading from markdown content."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def extract_first_paragraph(content: str) -> str:
    """Extract first non-empty paragraph after the title."""
    # Remove frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].strip()

    # Skip the title
    lines = content.split("\n")
    started = False
    paragraph = []

    for line in lines:
        # Skip title
        if line.startswith("# "):
            started = True
            continue

        if not started:
            continue

        # Skip empty lines before paragraph
        if not paragraph and not line.strip():
            continue

        # End at next heading or empty line after content
        if paragraph and (not line.strip() or line.startswith("#")):
            break

        # Skip special markers
        if line.startswith("**") and line.endswith("**"):
            continue

        paragraph.append(line.strip())

    result = " ".join(paragraph)
    # Truncate if too long
    if len(result) > 150:
        result = result[:147] + "..."
    return result


def extract_links_descriptions(skill_path: Path) -> dict[Path, str]:
    """
    Extract descriptions from ## Links sections across all index files.
    Returns a dict mapping resolved file paths to their descriptions.
    """
    descriptions = {}

    for f in skill_path.rglob("*.md"):
        if f.name not in ("SKILL.md", "index.md", "INDEX.md"):
            continue

        content = f.read_text()

        # Find ## Links section
        links_match = re.search(r"^## Links\s*$", content, re.MULTILINE)
        if not links_match:
            continue

        # Get content after ## Links until next ## or end
        links_section = content[links_match.end():]
        next_section = re.search(r"^## ", links_section, re.MULTILINE)
        if next_section:
            links_section = links_section[:next_section.start()]

        # Parse links in format: - [Name](path) - description
        link_pattern = r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*-\s*(.+?)$"

        for line in links_section.split("\n"):
            match = re.match(link_pattern, line)
            if match:
                _, path, desc = match.groups()
                if not path.startswith("http"):
                    target = (f.parent / path).resolve()
                    if target.exists():
                        descriptions[target] = desc.strip()

    return descriptions


def get_file_info(file_path: Path, skill_path: Path, link_descriptions: dict[Path, str]) -> FileInfo:
    """Get information about a file."""
    rel_path = file_path.relative_to(skill_path)
    content = file_path.read_text()

    title = extract_title(content)
    if not title:
        title = file_path.stem.replace("-", " ").replace("_", " ").title()

    # Try to get description from links first
    description = link_descriptions.get(file_path.resolve(), "")

    # Fall back to first paragraph
    if not description:
        description = extract_first_paragraph(content)

    if not description:
        description = "[no description]"

    return FileInfo(
        path=file_path,
        rel_path=rel_path,
        title=title,
        description=description,
        is_index=file_path.name in ("index.md", "INDEX.md", "SKILL.md"),
        is_exception=is_exception_folder(rel_path),
    )


def build_tree(skill_path: Path, include_exceptions: bool = False) -> dict:
    """
    Build a tree structure of the skill.
    Returns nested dict with files and folders.
    """
    tree = {"__files__": [], "__folders__": {}}

    for f in sorted(skill_path.rglob("*.md")):
        rel_path = f.relative_to(skill_path)

        # Skip exception folders (prefixed with _) unless explicitly included
        if not include_exceptions and is_exception_folder(rel_path):
            continue

        parts = rel_path.parts

        # Navigate to correct location in tree
        current = tree
        for part in parts[:-1]:
            if part not in current["__folders__"]:
                current["__folders__"][part] = {"__files__": [], "__folders__": {}}
            current = current["__folders__"][part]

        current["__files__"].append(f)

    return tree


def render_tree(
    tree: dict,
    skill_path: Path,
    link_descriptions: dict[Path, str],
    indent: int = 0,
    folder_name: str = "",
) -> list[str]:
    """Render tree to markdown lines."""
    lines = []
    prefix = "  " * indent

    # Sort files: index first, then alphabetically
    files = sorted(tree["__files__"], key=lambda f: (
        0 if f.name in ("SKILL.md", "index.md", "INDEX.md") else 1,
        f.name.lower()
    ))

    # Render files
    for f in files:
        info = get_file_info(f, skill_path, link_descriptions)

        # Special formatting for index files
        if info.is_index:
            if f.name == "SKILL.md":
                lines.append(f"{prefix}- **[{info.title}]({info.rel_path})** - {info.description}")
            else:
                # Index files show folder name
                display_name = folder_name or info.title
                lines.append(f"{prefix}- **[{display_name}]({info.rel_path})** - {info.description}")
        else:
            lines.append(f"{prefix}- [{info.title}]({info.rel_path}) - {info.description}")

    # Render subfolders
    for folder_name in sorted(tree["__folders__"].keys()):
        subtree = tree["__folders__"][folder_name]

        # Add folder header if it has content beyond just an index
        has_content = len(subtree["__files__"]) > 1 or subtree["__folders__"]

        if has_content:
            # Check if exception folder
            is_exception = folder_name.startswith("_")
            folder_display = f"`{folder_name}/`" if is_exception else f"`{folder_name}/`"

            lines.append(f"{prefix}- {folder_display}")
            lines.extend(render_tree(
                subtree, skill_path, link_descriptions,
                indent=indent + 1, folder_name=folder_name.lstrip("_").replace("-", " ").title()
            ))
        else:
            # Just render the files at current level
            lines.extend(render_tree(
                subtree, skill_path, link_descriptions,
                indent=indent, folder_name=folder_name.replace("-", " ").title()
            ))

    return lines


def find_skill_root(start: Path) -> Path:
    """Find skill root by looking for skill.md or SKILL.md."""
    current = start
    while current != current.parent:
        if (current / "skill.md").exists() or (current / "SKILL.md").exists():
            return current
        current = current.parent
    return start


def generate_sitemap(skill_path: Path, include_exceptions: bool = False) -> str:
    """Generate sitemap markdown content."""
    lines = ["# Sitemap", ""]
    lines.append(f"Knowledge base structure for `{skill_path.name}/`")
    lines.append("")
    if not include_exceptions:
        lines.append("Exception folders (`_*`) are searchable reference materials, not shown here.")
        lines.append("")

    # Extract descriptions from links
    link_descriptions = extract_links_descriptions(skill_path)

    # Build and render tree
    tree = build_tree(skill_path, include_exceptions=include_exceptions)
    tree_lines = render_tree(tree, skill_path, link_descriptions)
    lines.extend(tree_lines)

    # Add generation note
    lines.append("")
    lines.append("*Generated by sitemap.py*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate sitemap for a skill")
    parser.add_argument(
        "skill_path",
        nargs="?",
        help="Path to the skill directory (default: auto-detect)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Skill root directory (alternative to positional argument)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: print to stdout)",
    )
    parser.add_argument(
        "--include-exceptions",
        action="store_true",
        help="Include exception folders (_*) in sitemap",
    )

    args = parser.parse_args()

    # Determine skill path
    if args.root:
        skill_path = args.root.resolve()
    elif args.skill_path:
        skill_path = Path(args.skill_path).resolve()
    else:
        skill_path = find_skill_root(Path.cwd())

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}")
        return 1

    if not (skill_path / "SKILL.md").exists() and not (skill_path / "skill.md").exists():
        print(f"Error: No SKILL.md found in: {skill_path}")
        return 1

    sitemap = generate_sitemap(skill_path, include_exceptions=args.include_exceptions)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(sitemap)
        print(f"Sitemap written to: {output_path}")
    else:
        print(sitemap)

    return 0


if __name__ == "__main__":
    exit(main())
