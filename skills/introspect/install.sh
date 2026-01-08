#!/bin/bash
# Install script for introspect skill
# Uses only Python stdlib - no external dependencies needed

set -e

# Verify Python 3.8+ is available
python3 -c "import sys; assert sys.version_info >= (3, 8), 'Python 3.8+ required'" 2>/dev/null || {
    echo "Error: Python 3.8+ is required but not found"
    echo "Please install Python 3.8 or later"
    exit 1
}

# Verify git is available (needed for marketplace/plugin operations)
command -v git >/dev/null 2>&1 || {
    echo "Error: git is required but not found"
    echo "Please install git"
    exit 1
}

# Verify claude CLI is available (needed for MCP operations)
command -v claude >/dev/null 2>&1 || {
    echo "Warning: claude CLI not found - MCP operations will not work"
    echo "Install Claude Code CLI for full functionality"
}

echo "introspect skill ready - no additional dependencies needed"
