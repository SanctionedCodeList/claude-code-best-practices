#!/usr/bin/env python3
"""
Claude Code Configuration Introspection Tool

Provides programmatic access to view and manage Claude Code configuration:
- MCP servers (via claude mcp CLI)
- Plugins (install, remove, enable, disable, update)
- Skills (discovery only)
- Marketplaces (add, remove, update)

Uses only stdlib - no external dependencies required.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# === Configuration Paths ===

def get_claude_home() -> Path:
    """Get the Claude home directory (~/.claude)."""
    return Path.home() / ".claude"


def get_settings_path() -> Path:
    """Get user settings path (~/.claude/settings.json)."""
    return get_claude_home() / "settings.json"


def get_plugins_dir() -> Path:
    """Get plugins directory (~/.claude/plugins)."""
    return get_claude_home() / "plugins"


def get_installed_plugins_path() -> Path:
    """Get installed plugins registry path."""
    return get_plugins_dir() / "installed_plugins.json"


def get_known_marketplaces_path() -> Path:
    """Get known marketplaces registry path."""
    return get_plugins_dir() / "known_marketplaces.json"


def get_marketplaces_dir() -> Path:
    """Get marketplaces cache directory."""
    return get_plugins_dir() / "marketplaces"


def get_plugins_cache_dir() -> Path:
    """Get plugins cache directory."""
    return get_plugins_dir() / "cache"


def get_user_skills_dir() -> Path:
    """Get user skills directory (~/.claude/skills)."""
    return get_claude_home() / "skills"


def get_project_skills_dir() -> Path:
    """Get project skills directory (.claude/skills)."""
    return Path.cwd() / ".claude" / "skills"


# === JSON Utilities ===

def read_json(path: Path) -> dict:
    """Read JSON file, return empty dict if not found."""
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_json(path: Path, data: dict) -> None:
    """Write JSON file with pretty printing."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content (simple regex-based)."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                frontmatter[key] = value
    return frontmatter


def find_skill_files(directory: Path) -> list[Path]:
    """Find SKILL.md files (case-insensitive) in a directory."""
    skill_files = []
    if not directory.exists():
        return skill_files

    for path in directory.rglob("*"):
        if path.is_file() and path.name.lower() == "skill.md":
            skill_files.append(path)

    return skill_files


# === MCP Functions ===

def list_mcp_servers() -> dict:
    """List MCP servers using claude mcp CLI."""
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except FileNotFoundError:
        return {"success": False, "error": "claude CLI not found"}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}


# === Plugin Functions ===

def list_plugins() -> dict:
    """List all installed plugins with enabled status."""
    installed = read_json(get_installed_plugins_path())
    settings = read_json(get_settings_path())
    enabled_plugins = settings.get("enabledPlugins", {})

    plugins = []
    for plugin_id, installs in installed.get("plugins", {}).items():
        if not installs:
            continue
        install = installs[0]  # Take first installation

        plugins.append({
            "id": plugin_id,
            "name": plugin_id.split("@")[0] if "@" in plugin_id else plugin_id,
            "marketplace": plugin_id.split("@")[1] if "@" in plugin_id else None,
            "version": install.get("version"),
            "enabled": enabled_plugins.get(plugin_id, False),
            "scope": install.get("scope"),
            "installPath": install.get("installPath"),
            "installedAt": install.get("installedAt"),
            "lastUpdated": install.get("lastUpdated"),
            "isLocal": install.get("isLocal", False)
        })

    return {
        "success": True,
        "plugins": sorted(plugins, key=lambda p: p["id"]),
        "count": len(plugins)
    }


def enable_plugin(plugin_id: str) -> dict:
    """Enable a plugin by modifying settings.json."""
    settings_path = get_settings_path()
    settings = read_json(settings_path)

    if "enabledPlugins" not in settings:
        settings["enabledPlugins"] = {}

    settings["enabledPlugins"][plugin_id] = True
    write_json(settings_path, settings)

    return {"success": True, "message": f"Enabled plugin: {plugin_id}"}


def disable_plugin(plugin_id: str) -> dict:
    """Disable a plugin by modifying settings.json."""
    settings_path = get_settings_path()
    settings = read_json(settings_path)

    if "enabledPlugins" not in settings:
        settings["enabledPlugins"] = {}

    settings["enabledPlugins"][plugin_id] = False
    write_json(settings_path, settings)

    return {"success": True, "message": f"Disabled plugin: {plugin_id}"}


def install_plugin(plugin_name: str, marketplace: str) -> dict:
    """
    Install a plugin from a marketplace.

    This clones the plugin from the marketplace to the cache and registers it.
    """
    # Check marketplace exists
    marketplaces = read_json(get_known_marketplaces_path())
    if marketplace not in marketplaces:
        return {"success": False, "error": f"Marketplace not found: {marketplace}"}

    marketplace_info = marketplaces[marketplace]
    marketplace_path = Path(marketplace_info.get("installLocation", ""))

    if not marketplace_path.exists():
        return {"success": False, "error": f"Marketplace not cloned: {marketplace}"}

    # Read marketplace manifest
    manifest_path = marketplace_path / ".claude-plugin" / "marketplace.json"
    if not manifest_path.exists():
        manifest_path = marketplace_path / ".claude-plugin" / "plugin.json"

    manifest = read_json(manifest_path)

    # Find the plugin in the manifest
    plugin_def = None
    for p in manifest.get("plugins", []):
        if p.get("name") == plugin_name:
            plugin_def = p
            break

    if not plugin_def:
        return {"success": False, "error": f"Plugin not found in marketplace: {plugin_name}"}

    # Determine source
    source = plugin_def.get("source", "./")
    version = plugin_def.get("version", manifest.get("metadata", {}).get("version", "latest"))

    if isinstance(source, str) and source == "./":
        # Plugin is in the same repo
        source_path = marketplace_path
    elif isinstance(source, dict) and source.get("source") == "github":
        # Plugin is in a different repo - clone it
        repo = source.get("repo")
        source_path = get_plugins_cache_dir() / marketplace / plugin_name / version
        source_path.parent.mkdir(parents=True, exist_ok=True)

        if source_path.exists():
            shutil.rmtree(source_path)

        result = subprocess.run(
            ["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", str(source_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"success": False, "error": f"Failed to clone: {result.stderr}"}
    else:
        source_path = marketplace_path / source if isinstance(source, str) else marketplace_path

    # Get git commit sha
    git_sha = None
    try:
        result = subprocess.run(
            ["git", "-C", str(source_path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            git_sha = result.stdout.strip()[:12]
            version = git_sha
    except Exception:
        pass

    # Copy to cache if not already there
    cache_path = get_plugins_cache_dir() / marketplace / plugin_name / version
    if not cache_path.exists():
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, cache_path, dirs_exist_ok=True)

    # Register in installed_plugins.json
    installed = read_json(get_installed_plugins_path())
    if "version" not in installed:
        installed["version"] = 2
    if "plugins" not in installed:
        installed["plugins"] = {}

    plugin_id = f"{plugin_name}@{marketplace}"
    now = datetime.now(timezone.utc).isoformat()

    installed["plugins"][plugin_id] = [{
        "scope": "user",
        "installPath": str(cache_path),
        "version": version,
        "installedAt": now,
        "lastUpdated": now,
        "gitCommitSha": git_sha,
        "isLocal": False
    }]

    write_json(get_installed_plugins_path(), installed)

    # Enable by default
    enable_plugin(plugin_id)

    return {
        "success": True,
        "message": f"Installed plugin: {plugin_id}",
        "installPath": str(cache_path),
        "version": version
    }


def remove_plugin(plugin_id: str, delete_cache: bool = False) -> dict:
    """Remove a plugin from the registry, optionally deleting cached files."""
    installed = read_json(get_installed_plugins_path())

    if plugin_id not in installed.get("plugins", {}):
        return {"success": False, "error": f"Plugin not installed: {plugin_id}"}

    # Get install path before removing
    install_info = installed["plugins"][plugin_id][0] if installed["plugins"][plugin_id] else None
    install_path = install_info.get("installPath") if install_info else None

    # Remove from registry
    del installed["plugins"][plugin_id]
    write_json(get_installed_plugins_path(), installed)

    # Disable in settings
    settings = read_json(get_settings_path())
    if plugin_id in settings.get("enabledPlugins", {}):
        del settings["enabledPlugins"][plugin_id]
        write_json(get_settings_path(), settings)

    # Optionally delete cache
    if delete_cache and install_path:
        path = Path(install_path)
        if path.exists():
            shutil.rmtree(path)

    return {"success": True, "message": f"Removed plugin: {plugin_id}"}


def update_plugin(plugin_id: str) -> dict:
    """Update a plugin by pulling latest changes."""
    installed = read_json(get_installed_plugins_path())

    if plugin_id not in installed.get("plugins", {}):
        return {"success": False, "error": f"Plugin not installed: {plugin_id}"}

    install_info = installed["plugins"][plugin_id][0]
    install_path = Path(install_info.get("installPath", ""))

    if not install_path.exists():
        return {"success": False, "error": f"Install path not found: {install_path}"}

    # Git pull
    result = subprocess.run(
        ["git", "-C", str(install_path), "pull", "--ff-only"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"success": False, "error": f"Git pull failed: {result.stderr}"}

    # Update version info
    git_result = subprocess.run(
        ["git", "-C", str(install_path), "rev-parse", "HEAD"],
        capture_output=True,
        text=True
    )

    if git_result.returncode == 0:
        new_sha = git_result.stdout.strip()[:12]
        install_info["version"] = new_sha
        install_info["gitCommitSha"] = new_sha
        install_info["lastUpdated"] = datetime.now(timezone.utc).isoformat()
        write_json(get_installed_plugins_path(), installed)

    return {
        "success": True,
        "message": f"Updated plugin: {plugin_id}",
        "output": result.stdout
    }


# === Health Check Functions ===

def check_plugin_health() -> dict:
    """Check for orphaned or broken plugin installations."""
    installed = read_json(get_installed_plugins_path())
    marketplaces = read_json(get_known_marketplaces_path())
    settings = read_json(get_settings_path())
    enabled_plugins = settings.get("enabledPlugins", {})

    issues = []

    for plugin_id, installs in installed.get("plugins", {}).items():
        if not installs:
            continue

        install = installs[0]
        install_path = Path(install.get("installPath", ""))

        # Parse plugin ID
        if "@" in plugin_id:
            plugin_name, marketplace_name = plugin_id.split("@", 1)
        else:
            plugin_name = plugin_id
            marketplace_name = None

        # Check if install path exists
        if not install_path.exists():
            issues.append({
                "plugin_id": plugin_id,
                "issue": "missing_path",
                "message": f"Install path does not exist: {install_path}",
                "suggestion": f"Remove with: remove_plugin('{plugin_id}')"
            })
            continue

        # Check if marketplace exists
        if marketplace_name and marketplace_name not in marketplaces:
            issues.append({
                "plugin_id": plugin_id,
                "issue": "missing_marketplace",
                "message": f"Marketplace not found: {marketplace_name}",
                "suggestion": f"Add marketplace or remove plugin"
            })
            continue

        # Check if marketplace has the plugin
        if marketplace_name and marketplace_name in marketplaces:
            marketplace_path = Path(marketplaces[marketplace_name].get("installLocation", ""))
            if marketplace_path.exists():
                manifest_path = marketplace_path / ".claude-plugin" / "marketplace.json"
                if not manifest_path.exists():
                    manifest_path = marketplace_path / ".claude-plugin" / "plugin.json"

                if manifest_path.exists():
                    manifest = read_json(manifest_path)
                    plugin_names = [p.get("name") for p in manifest.get("plugins", [])]
                    if plugin_name not in plugin_names:
                        issues.append({
                            "plugin_id": plugin_id,
                            "issue": "plugin_not_in_marketplace",
                            "message": f"Plugin '{plugin_name}' not found in marketplace '{marketplace_name}'",
                            "suggestion": f"Plugin may have been removed from marketplace"
                        })

    # Check for plugins in enabledPlugins that aren't installed
    # (The TUI validates ALL entries in enabledPlugins, not just enabled=True)
    for plugin_id in enabled_plugins.keys():
        if plugin_id not in installed.get("plugins", {}):
            # Parse plugin ID to check marketplace
            if "@" in plugin_id:
                plugin_name, marketplace_name = plugin_id.split("@", 1)
            else:
                plugin_name = plugin_id
                marketplace_name = None

            # Check if marketplace exists and has this plugin
            if marketplace_name:
                if marketplace_name not in marketplaces:
                    issues.append({
                        "plugin_id": plugin_id,
                        "issue": "orphaned_settings_entry",
                        "message": f"In settings but marketplace '{marketplace_name}' not found",
                        "suggestion": f"Remove from settings.json enabledPlugins"
                    })
                else:
                    # Marketplace exists, check if plugin is in it
                    marketplace_path = Path(marketplaces[marketplace_name].get("installLocation", ""))
                    if marketplace_path.exists():
                        manifest_path = marketplace_path / ".claude-plugin" / "marketplace.json"
                        if not manifest_path.exists():
                            manifest_path = marketplace_path / ".claude-plugin" / "plugin.json"

                        if manifest_path.exists():
                            manifest = read_json(manifest_path)
                            plugin_names = [p.get("name") for p in manifest.get("plugins", [])]
                            if plugin_name not in plugin_names:
                                issues.append({
                                    "plugin_id": plugin_id,
                                    "issue": "orphaned_settings_entry",
                                    "message": f"Plugin '{plugin_name}' not found in marketplace '{marketplace_name}'",
                                    "suggestion": f"Remove from settings.json enabledPlugins"
                                })
                        else:
                            issues.append({
                                "plugin_id": plugin_id,
                                "issue": "orphaned_settings_entry",
                                "message": f"Marketplace '{marketplace_name}' has no manifest",
                                "suggestion": f"Remove from settings.json enabledPlugins"
                            })

    return {
        "success": True,
        "healthy": len(issues) == 0,
        "issues": issues,
        "issue_count": len(issues)
    }


# === Skills Functions ===

def list_skills() -> dict:
    """Discover all available skills from user, project, and plugin sources."""
    skills = []
    seen_names = set()  # For deduplication

    def add_skill(name: str, description: str, source: str, path: str):
        """Add skill if not already seen (dedupe by name)."""
        if name not in seen_names:
            seen_names.add(name)
            skills.append({
                "name": name,
                "description": description,
                "source": source,
                "path": path
            })

    def find_top_level_skill(directory: Path) -> Path | None:
        """Find skill.md (case-insensitive) directly in a directory."""
        if not directory.exists():
            return None
        for item in directory.iterdir():
            if item.is_file() and item.name.lower() == "skill.md":
                return item
        return None

    # User skills
    user_skills_dir = get_user_skills_dir()
    if user_skills_dir.exists():
        for skill_dir in user_skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = find_top_level_skill(skill_dir)
                if skill_md:
                    frontmatter = parse_yaml_frontmatter(skill_md.read_text())
                    add_skill(
                        frontmatter.get("name", skill_dir.name),
                        frontmatter.get("description", ""),
                        "user",
                        str(skill_dir)
                    )

    # Project skills
    project_skills_dir = get_project_skills_dir()
    if project_skills_dir.exists():
        for skill_dir in project_skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = find_top_level_skill(skill_dir)
                if skill_md:
                    frontmatter = parse_yaml_frontmatter(skill_md.read_text())
                    add_skill(
                        frontmatter.get("name", skill_dir.name),
                        frontmatter.get("description", ""),
                        "project",
                        str(skill_dir)
                    )

    # Plugin skills (from enabled plugins)
    plugins = list_plugins()
    for plugin in plugins.get("plugins", []):
        if not plugin.get("enabled"):
            continue

        install_path = Path(plugin.get("installPath", ""))
        if not install_path.exists():
            continue

        # Look for skills/ directory in plugin
        skills_dir = install_path / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = find_top_level_skill(skill_dir)
                    if skill_md:
                        frontmatter = parse_yaml_frontmatter(skill_md.read_text())
                        add_skill(
                            frontmatter.get("name", skill_dir.name),
                            frontmatter.get("description", ""),
                            f"plugin:{plugin['id']}",
                            str(skill_dir)
                        )

    return {
        "success": True,
        "skills": sorted(skills, key=lambda s: (s["source"], s["name"])),
        "count": len(skills)
    }


# === Marketplace Functions ===

def list_marketplaces() -> dict:
    """List all known marketplaces."""
    marketplaces = read_json(get_known_marketplaces_path())

    result = []
    for name, info in marketplaces.items():
        source = info.get("source", {})
        result.append({
            "name": name,
            "repo": source.get("repo") if isinstance(source, dict) else None,
            "installLocation": info.get("installLocation"),
            "lastUpdated": info.get("lastUpdated"),
            "autoUpdate": info.get("autoUpdate", True)
        })

    return {
        "success": True,
        "marketplaces": sorted(result, key=lambda m: m["name"]),
        "count": len(result)
    }


def add_marketplace(repo: str) -> dict:
    """Add a new marketplace from a GitHub repo (owner/repo format)."""
    if "/" not in repo:
        return {"success": False, "error": "Repo must be in owner/repo format"}

    # Derive marketplace name from repo
    name = repo.split("/")[1]
    if name.endswith("-marketplace"):
        name = name.replace("-marketplace", "")
    name = name.replace("_", "-").lower()

    # Check if already exists
    marketplaces = read_json(get_known_marketplaces_path())
    if name in marketplaces:
        return {"success": False, "error": f"Marketplace already exists: {name}"}

    # Clone the repo
    install_location = get_marketplaces_dir() / name
    install_location.parent.mkdir(parents=True, exist_ok=True)

    if install_location.exists():
        shutil.rmtree(install_location)

    result = subprocess.run(
        ["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", str(install_location)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"success": False, "error": f"Failed to clone: {result.stderr}"}

    # Add to registry
    now = datetime.now(timezone.utc).isoformat()
    marketplaces[name] = {
        "source": {"source": "github", "repo": repo},
        "installLocation": str(install_location),
        "lastUpdated": now
    }

    write_json(get_known_marketplaces_path(), marketplaces)

    return {
        "success": True,
        "message": f"Added marketplace: {name}",
        "name": name,
        "installLocation": str(install_location)
    }


def remove_marketplace(name: str, delete_files: bool = True) -> dict:
    """Remove a marketplace from the registry and optionally delete cloned files."""
    marketplaces = read_json(get_known_marketplaces_path())

    if name not in marketplaces:
        return {"success": False, "error": f"Marketplace not found: {name}"}

    install_location = marketplaces[name].get("installLocation")

    # Remove from registry
    del marketplaces[name]
    write_json(get_known_marketplaces_path(), marketplaces)

    # Delete files if requested
    if delete_files and install_location:
        path = Path(install_location)
        if path.exists():
            shutil.rmtree(path)

    return {"success": True, "message": f"Removed marketplace: {name}"}


def update_marketplace(name: str) -> dict:
    """Update a marketplace by pulling latest changes."""
    marketplaces = read_json(get_known_marketplaces_path())

    if name not in marketplaces:
        return {"success": False, "error": f"Marketplace not found: {name}"}

    install_location = Path(marketplaces[name].get("installLocation", ""))

    if not install_location.exists():
        return {"success": False, "error": f"Marketplace not cloned: {install_location}"}

    # Git pull
    result = subprocess.run(
        ["git", "-C", str(install_location), "pull", "--ff-only"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"success": False, "error": f"Git pull failed: {result.stderr}"}

    # Update timestamp
    marketplaces[name]["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    write_json(get_known_marketplaces_path(), marketplaces)

    return {
        "success": True,
        "message": f"Updated marketplace: {name}",
        "output": result.stdout
    }


# === CLI Interface ===

def print_json(data: dict) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))


def print_help() -> None:
    """Print usage information."""
    help_text = """
Claude Code Introspection Tool

Usage: python3 introspect.py <category> <command> [args]

Categories:
  mcp          MCP server management (uses claude mcp CLI)
  plugins      Plugin management
  skills       Skills discovery
  marketplaces Marketplace management

Commands by category:

  mcp list                         List MCP servers

  plugins list                     List installed plugins
  plugins enable <id>              Enable a plugin
  plugins disable <id>             Disable a plugin
  plugins install <name> <market>  Install plugin from marketplace
  plugins remove <id> [--cache]    Remove plugin (--cache deletes files)
  plugins update <id>              Update plugin to latest

  skills list                      List all available skills

  marketplaces list                List known marketplaces
  marketplaces add <owner/repo>    Add marketplace from GitHub
  marketplaces remove <name>       Remove marketplace
  marketplaces update <name>       Update marketplace to latest

Examples:
  python3 introspect.py plugins list
  python3 introspect.py plugins enable dev-browser@scl-marketplace
  python3 introspect.py marketplaces add anthropics/claude-plugins-official
"""
    print(help_text.strip())


def main() -> int:
    """Main CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print_help()
        return 0

    category = args[0]
    command = args[1] if len(args) > 1 else "list"

    # MCP commands
    if category == "mcp":
        if command == "list":
            print_json(list_mcp_servers())
        else:
            print(f"Unknown mcp command: {command}")
            return 1

    # Plugin commands
    elif category == "plugins":
        if command == "list":
            print_json(list_plugins())
        elif command == "enable" and len(args) > 2:
            print_json(enable_plugin(args[2]))
        elif command == "disable" and len(args) > 2:
            print_json(disable_plugin(args[2]))
        elif command == "install" and len(args) > 3:
            print_json(install_plugin(args[2], args[3]))
        elif command == "remove" and len(args) > 2:
            delete_cache = "--cache" in args
            print_json(remove_plugin(args[2], delete_cache))
        elif command == "update" and len(args) > 2:
            print_json(update_plugin(args[2]))
        else:
            print(f"Unknown or incomplete plugins command: {command}")
            return 1

    # Skills commands
    elif category == "skills":
        if command == "list":
            print_json(list_skills())
        else:
            print(f"Unknown skills command: {command}")
            return 1

    # Marketplace commands
    elif category == "marketplaces":
        if command == "list":
            print_json(list_marketplaces())
        elif command == "add" and len(args) > 2:
            print_json(add_marketplace(args[2]))
        elif command == "remove" and len(args) > 2:
            print_json(remove_marketplace(args[2]))
        elif command == "update" and len(args) > 2:
            print_json(update_marketplace(args[2]))
        else:
            print(f"Unknown or incomplete marketplaces command: {command}")
            return 1

    else:
        print(f"Unknown category: {category}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
