#!/usr/bin/env bash
# Best Practices - Parent Installer
# Delegates to sub-skill installers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing best-practices dependencies..."

# Sessions sub-skill has dependencies
if [[ -x "$SCRIPT_DIR/sessions/install.sh" ]]; then
    echo "Running sessions installer..."
    "$SCRIPT_DIR/sessions/install.sh"
fi

echo "best-practices installation complete."
