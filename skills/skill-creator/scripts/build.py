#!/usr/bin/env python3
"""
Jinja2 template build script for skills.

Enables composable skill content by allowing templates to include shared fragments.

Convention:
- Templates (*.md.j2) are placed adjacent to their outputs
- Output is the same path with .j2 extension stripped
- Generated files get an AUTO-GENERATED header
- Files without .j2 extension are editable directly

Can be dropped into any skill directory that uses this convention.

Usage:
    python build.py           # Build all
    python build.py --clean   # Remove generated files first
    python build.py --check   # Check if rebuild needed (for CI)
    python build.py --root /path/to/skill  # Specify skill root
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, TemplateNotFound
except ImportError:
    print("Error: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)


# Header added to all generated files
GENERATED_HEADER = """\
<!-- AUTO-GENERATED from {template} — DO NOT EDIT -->
<!-- Edit the .j2 template file instead, then run: python build.py -->

"""


def get_file_hash(path: Path) -> str:
    """Get SHA256 hash of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest(manifest_file: Path) -> dict:
    """Load the build manifest tracking generated files."""
    if manifest_file.exists():
        return json.loads(manifest_file.read_text())
    return {"files": {}, "version": 2}


def save_manifest(manifest_file: Path, manifest: dict) -> None:
    """Save the build manifest."""
    manifest_file.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def clean_generated_files(skill_root: Path, manifest: dict) -> None:
    """Remove files that were created by previous builds."""
    for rel_path in manifest.get("files", {}).keys():
        full_path = skill_root / rel_path
        if full_path.exists():
            full_path.unlink()
            print(f"  Removed: {rel_path}")


def get_all_include_hashes(env: Environment, skill_root: Path, template_path: Path) -> str:
    """Get combined hash of template and all its includes."""
    hashes = [get_file_hash(template_path)]

    # Parse template for includes
    content = template_path.read_text()

    includes = re.findall(r"{%\s*include\s+['\"]([^'\"]+)['\"]", content)

    for include_path in includes:
        full_include = skill_root / include_path
        if full_include.exists():
            hashes.append(get_file_hash(full_include))

    return hashlib.sha256("".join(hashes).encode()).hexdigest()


def build_template(
    env: Environment, skill_root: Path, template_path: Path, output_path: Path
) -> None:
    """Render a Jinja2 template and write to output with header."""
    rel_template = template_path.relative_to(skill_root)
    try:
        template = env.get_template(str(rel_template))
        content = template.render()

        # Add generated header
        header = GENERATED_HEADER.format(template=rel_template)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(header + content)
    except TemplateNotFound as e:
        print(f"  Error: Include not found: {e}")
        raise


def build_all(skill_root: Path, clean: bool = False) -> dict:
    """Build all templates in the skill directory."""
    manifest_file = skill_root / ".build-manifest.json"
    manifest = load_manifest(manifest_file)

    if clean:
        print("Cleaning previous build...")
        clean_generated_files(skill_root, manifest)
        manifest = {"files": {}, "version": 2}

    # Set up Jinja environment with skill root as the template root
    env = Environment(
        loader=FileSystemLoader(str(skill_root)),
        keep_trailing_newline=True,
    )

    new_manifest = {"files": {}, "version": 2}
    built_count = 0
    skipped_count = 0

    skill_name = skill_root.name
    print(f"Building {skill_name} skill...")

    # Find all .j2 templates
    for template_path in skill_root.rglob("*.j2"):
        # Output path is adjacent, with .j2 stripped
        output_path = template_path.with_suffix("")  # foo.md.j2 -> foo.md
        rel_template = template_path.relative_to(skill_root)
        rel_output = output_path.relative_to(skill_root)

        # Check if source or includes changed
        combined_hash = get_all_include_hashes(env, skill_root, template_path)
        old_hash = manifest.get("files", {}).get(str(rel_output), {}).get("combined_hash")

        if combined_hash != old_hash or not output_path.exists():
            build_template(env, skill_root, template_path, output_path)
            print(f"  Built: {rel_output}")
            built_count += 1
        else:
            skipped_count += 1

        new_manifest["files"][str(rel_output)] = {
            "template": str(rel_template),
            "combined_hash": combined_hash,
        }

    # Remove files that are no longer generated (template was deleted)
    old_files = set(manifest.get("files", {}).keys())
    new_files = set(new_manifest["files"].keys())
    removed_files = old_files - new_files

    for rel_path in removed_files:
        full_path = skill_root / rel_path
        if full_path.exists():
            full_path.unlink()
            print(f"  Removed (stale): {rel_path}")

    save_manifest(manifest_file, new_manifest)

    print(f"\nBuild complete: {built_count} built, {skipped_count} unchanged")
    return new_manifest


def check_rebuild_needed(skill_root: Path) -> bool:
    """Check if any templates or includes have changed since last build."""
    manifest_file = skill_root / ".build-manifest.json"
    manifest = load_manifest(manifest_file)

    env = Environment(
        loader=FileSystemLoader(str(skill_root)),
        keep_trailing_newline=True,
    )

    for template_path in skill_root.rglob("*.j2"):
        output_path = template_path.with_suffix("")
        rel_output = str(output_path.relative_to(skill_root))

        combined_hash = get_all_include_hashes(env, skill_root, template_path)
        old_hash = manifest.get("files", {}).get(rel_output, {}).get("combined_hash")

        if combined_hash != old_hash:
            return True

        if not output_path.exists():
            return True

    return False


def find_skill_root(start: Path) -> Path:
    """Find skill root by looking for skill.md or SKILL.md."""
    current = start
    while current != current.parent:
        if (current / "skill.md").exists() or (current / "SKILL.md").exists():
            return current
        current = current.parent
    return start  # Fall back to start directory


def main():
    parser = argparse.ArgumentParser(description="Build skill from Jinja2 templates")
    parser.add_argument("--clean", action="store_true", help="Clean before building")
    parser.add_argument("--check", action="store_true", help="Check if rebuild needed")
    parser.add_argument("--root", type=Path, help="Skill root directory (auto-detected if omitted)")
    args = parser.parse_args()

    # Determine skill root
    if args.root:
        skill_root = args.root.resolve()
    else:
        # Auto-detect: look for skill.md going up from script location
        skill_root = find_skill_root(Path(__file__).parent)

    if not skill_root.exists():
        print(f"Error: Skill root not found: {skill_root}")
        sys.exit(1)

    if args.check:
        if check_rebuild_needed(skill_root):
            print("Rebuild needed")
            sys.exit(1)
        else:
            print("Build is up to date")
            sys.exit(0)

    build_all(skill_root, clean=args.clean)


if __name__ == "__main__":
    main()
