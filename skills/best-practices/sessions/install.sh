#!/bin/bash
# Install and sync sessions skill
# Idempotent - safe to run multiple times

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
SESSIONS_SCRIPT="$SCRIPT_DIR/scripts/sessions.py"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Create virtual environment if needed
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Install/upgrade dependencies (pip handles idempotency)
echo "Checking dependencies..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet \
    sentence-transformers \
    numpy

# Build/sync the index (incremental - only indexes new/changed sessions)
echo "Syncing session index..."
"$PYTHON" "$SESSIONS_SCRIPT" build

echo "Sessions skill ready"
