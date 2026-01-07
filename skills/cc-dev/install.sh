#!/usr/bin/env bash
# CC Dev - Parent Installer
# Delegates to sub-skill installers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing cc-dev dependencies..."

# Sessions sub-skill has dependencies
if [[ -x "$SCRIPT_DIR/sessions/install.sh" ]]; then
    echo "Running sessions installer..."
    "$SCRIPT_DIR/sessions/install.sh"
fi

echo "cc-dev installation complete."
