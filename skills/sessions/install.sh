#!/bin/bash
# Install dependencies for sessions skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "Installing sessions skill dependencies..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install
source "$VENV_DIR/bin/activate"

echo "Installing Python packages..."
pip install --quiet --upgrade pip
pip install --quiet \
    sentence-transformers \
    numpy

echo "Dependencies installed successfully"
echo ""
echo "To use the sessions skill, either:"
echo "  1. Run: source $VENV_DIR/bin/activate"
echo "  2. Or use: $VENV_DIR/bin/python scripts/sessions.py ..."
