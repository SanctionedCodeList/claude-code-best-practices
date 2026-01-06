#!/bin/bash
# Install and sync sessions skill
# Idempotent - safe to run multiple times

set -e

# Find the repo root (where pyproject.toml lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# ── Python Environment Checks ────────────────────────────────────────────────

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Get Python version info for diagnostics
PYTHON3_PATH=$(command -v python3)
PYTHON3_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
PYTHON3_PREFIX=$(python3 -c "import sys; print(sys.prefix)")

# Check if pip is available via python3 -m pip
if ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is not available for python3"
    echo "  python3 path: $PYTHON3_PATH"
    echo "  python3 version: $PYTHON3_VERSION"
    echo ""
    echo "Try: python3 -m ensurepip --upgrade"
    exit 1
fi

# Get pip's Python info
PIP_PYTHON_VERSION=$(python3 -m pip --version | grep -oE 'python [0-9.]+' | cut -d' ' -f2)

# Warn if versions look mismatched (compare major.minor)
PYTHON3_MM=$(echo "$PYTHON3_VERSION" | cut -d. -f1,2)
PIP_MM=$(echo "$PIP_PYTHON_VERSION" | cut -d. -f1,2)

if [ "$PYTHON3_MM" != "$PIP_MM" ]; then
    echo "WARNING: Python version mismatch detected!"
    echo "  python3: $PYTHON3_VERSION ($PYTHON3_PATH)"
    echo "  pip reports: python $PIP_PYTHON_VERSION"
    echo ""
    echo "This can happen when:"
    echo "  - pyenv is installed but not fully initialized"
    echo "  - Multiple Python installations exist (Homebrew, pyenv, system)"
    echo ""
    echo "Recommended fix: Ensure your shell initializes pyenv for ALL Python commands."
    echo "Add python3/pip3 wrappers to your shell config alongside python/pip."
    echo ""
    echo "Continuing anyway, but imports may fail..."
    echo ""
fi

echo "Python environment:"
echo "  python3: $PYTHON3_VERSION ($PYTHON3_PATH)"
echo ""

# ── Install Package ──────────────────────────────────────────────────────────

# Use python3 -m pip to ensure we install to the same Python that python3 resolves to
# --break-system-packages handles Homebrew Python (PEP 668) - safe with --user flag
echo "Installing cc-best-practices package..."
if [ -f "$REPO_ROOT/pyproject.toml" ]; then
    python3 -m pip install --user --break-system-packages -q -e "$REPO_ROOT" 2>/dev/null || \
    python3 -m pip install --user -q -e "$REPO_ROOT"
else
    # Fallback: install from PyPI if available, or fail
    python3 -m pip install --user --break-system-packages -q cc-best-practices 2>/dev/null || \
    python3 -m pip install --user -q cc-best-practices || {
        echo "Error: Could not find pyproject.toml at $REPO_ROOT"
        echo "Please run from within the claude-code-best-practices repository"
        exit 1
    }
fi

# ── Verify Installation ──────────────────────────────────────────────────────

echo "Verifying installation..."
if ! python3 -c "import cc_best_practices" 2>/dev/null; then
    echo ""
    echo "ERROR: Package installed but cannot be imported!"
    echo ""
    echo "This usually means python3 and pip point to different Python installations."
    echo ""
    echo "Diagnostic info:"
    echo "  python3 path: $PYTHON3_PATH"
    echo "  python3 prefix: $PYTHON3_PREFIX"
    echo "  User site-packages: $(python3 -m site --user-site)"
    echo ""
    echo "Check that your shell properly initializes pyenv/virtualenv for python3."
    exit 1
fi

# ── Sync Index ───────────────────────────────────────────────────────────────

echo "Syncing session index..."
python3 <<'EOF'
from cc_best_practices.sessions import sync
stats = sync()
print(f"Indexed: {stats.get('indexed', 0)}, Skipped: {stats.get('skipped', 0)}")
EOF

echo ""
echo "Sessions skill ready"
