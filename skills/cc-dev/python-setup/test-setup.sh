#!/bin/bash
# Test Python environment configuration for Claude Code agents
# Run this script to verify your setup is correct

set -u

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS="${GREEN}PASS${NC}"
FAIL="${RED}FAIL${NC}"
WARN="${YELLOW}WARN${NC}"

echo ""
echo "========================================"
echo "  Python Environment Test for Claude Code"
echo "========================================"
echo ""

ERRORS=0
WARNINGS=0

# ------------------------------------------------------------------------------
# Test 1: Check which python3 is in PATH
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 1: python3 location${NC}"

PYTHON3_PATH=$(command -v python3 2>/dev/null)
if [ -z "$PYTHON3_PATH" ]; then
    echo -e "  [$FAIL] python3 not found in PATH"
    echo ""
    echo "  Fix: Install Python 3 via pyenv or your package manager"
    echo ""
    ERRORS=$((ERRORS + 1))
else
    echo -e "  Path: $PYTHON3_PATH"

    if [[ "$PYTHON3_PATH" == *"pyenv/shims"* ]]; then
        echo -e "  [$PASS] Using pyenv shim (recommended)"
    elif [[ "$PYTHON3_PATH" == "/opt/homebrew"* ]] || [[ "$PYTHON3_PATH" == "/usr/local"* ]]; then
        echo -e "  [$WARN] Using Homebrew Python"
        echo ""
        echo "  This works, but pyenv is recommended for version management."
        echo "  If you have pyenv installed, check that shims are in PATH."
        echo ""
        WARNINGS=$((WARNINGS + 1))
    elif [[ "$PYTHON3_PATH" == "/usr/bin/python3" ]]; then
        echo -e "  [$WARN] Using system Python"
        echo ""
        echo "  This may work but is not recommended. Consider using pyenv."
        echo ""
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "  [$PASS] Custom Python installation"
    fi
fi

PYTHON3_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>/dev/null)
echo -e "  Version: ${PYTHON3_VERSION:-unknown}"
echo ""

# ------------------------------------------------------------------------------
# Test 2: Check pip alignment
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 2: pip alignment${NC}"

if ! python3 -m pip --version &>/dev/null; then
    echo -e "  [$FAIL] pip not available via python3 -m pip"
    echo ""
    echo "  Fix: Run 'python3 -m ensurepip --upgrade'"
    echo ""
    ERRORS=$((ERRORS + 1))
else
    PIP_OUTPUT=$(python3 -m pip --version 2>/dev/null)
    PIP_PYTHON=$(echo "$PIP_OUTPUT" | grep -oE 'python [0-9.]+' | cut -d' ' -f2)

    echo -e "  pip reports: python $PIP_PYTHON"

    PYTHON3_MM=$(echo "$PYTHON3_VERSION" | cut -d. -f1,2)
    PIP_MM=$(echo "$PIP_PYTHON" | cut -d. -f1,2)

    if [ "$PYTHON3_MM" = "$PIP_MM" ]; then
        echo -e "  [$PASS] pip and python3 versions match ($PYTHON3_MM)"
    else
        echo -e "  [$FAIL] Version mismatch: python3=$PYTHON3_MM, pip=$PIP_MM"
        echo ""
        echo "  This means packages installed via pip won't be found by python3."
        echo ""
        echo "  Fix: Always use 'python3 -m pip install' instead of 'pip install'"
        echo "       to ensure packages go to the correct Python."
        echo ""
        ERRORS=$((ERRORS + 1))
    fi
fi
echo ""

# ------------------------------------------------------------------------------
# Test 3: Non-interactive shell test (simulates Claude Code)
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 3: Non-interactive shell (simulates Claude Code)${NC}"

# Spawn a fresh non-interactive zsh and check python3
NI_PYTHON=$(/bin/zsh -c 'command -v python3' 2>/dev/null)
NI_VERSION=$(/bin/zsh -c 'python3 -c "import sys; print(f\"{sys.version_info.major}.{sys.version_info.minor}\")"' 2>/dev/null)

echo -e "  Non-interactive python3: $NI_PYTHON"
echo -e "  Non-interactive version: $NI_VERSION"

if [ "$PYTHON3_PATH" = "$NI_PYTHON" ]; then
    echo -e "  [$PASS] Same python3 in interactive and non-interactive shells"
else
    echo -e "  [$FAIL] Different python3 between shell types!"
    echo ""
    echo "  Interactive:     $PYTHON3_PATH"
    echo "  Non-interactive: $NI_PYTHON"
    echo ""
    echo "  This is the #1 cause of 'module not found' errors in Claude Code."
    echo ""
    echo "  Fix: Add pyenv shims to ~/.zshenv (not just ~/.zshrc):"
    echo ""
    echo "    # ~/.zshenv"
    echo "    export PYENV_ROOT=\"\$HOME/.pyenv\""
    echo "    [[ -d \"\$PYENV_ROOT/shims\" ]] && PATH=\"\$PYENV_ROOT/shims:\$PATH\""
    echo ""
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ------------------------------------------------------------------------------
# Test 4: Heredoc syntax test
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 4: Heredoc syntax${NC}"

HEREDOC_RESULT=$(python3 <<'EOF'
data = {"status": "ok", "count": 42}
print(f"Result: {data['status']}, count={data['count']}")
EOF
2>&1)

if [[ "$HEREDOC_RESULT" == "Result: ok, count=42" ]]; then
    echo -e "  [$PASS] Heredoc with f-strings works correctly"
else
    echo -e "  [$FAIL] Heredoc test failed"
    echo "  Output: $HEREDOC_RESULT"
    echo ""
    echo "  This shouldn't happen if python3 is working."
    echo ""
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ------------------------------------------------------------------------------
# Test 5: Check for problematic lazy-load functions
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 5: Shell function conflicts${NC}"

# Check if python3 is a function (it shouldn't be)
PYTHON3_TYPE=$(type -t python3 2>/dev/null || type python3 2>/dev/null | head -1)

if [[ "$PYTHON3_TYPE" == *"function"* ]]; then
    echo -e "  [$FAIL] python3 is a shell function (causes recursion issues)"
    echo ""
    echo "  Your shell config defines python3 as a function, likely for lazy-loading."
    echo "  This can cause infinite recursion or unexpected behavior."
    echo ""
    echo "  Fix: Remove the python3() function from ~/.zshrc"
    echo "       Instead, add pyenv shims to PATH in ~/.zshenv"
    echo ""
    ERRORS=$((ERRORS + 1))
else
    echo -e "  [$PASS] python3 is not a shell function"
fi
echo ""

# ------------------------------------------------------------------------------
# Test 6: Check PYENV_ROOT
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 6: Environment variables${NC}"

if [ -n "${PYENV_ROOT:-}" ]; then
    echo -e "  PYENV_ROOT: $PYENV_ROOT"
    if [ -d "$PYENV_ROOT/shims" ]; then
        echo -e "  [$PASS] PYENV_ROOT/shims exists"
    else
        echo -e "  [$WARN] PYENV_ROOT set but shims directory not found"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "  PYENV_ROOT: (not set)"
    if command -v pyenv &>/dev/null; then
        echo -e "  [$WARN] pyenv installed but PYENV_ROOT not set"
        echo ""
        echo "  Fix: Add to ~/.zshenv:"
        echo "    export PYENV_ROOT=\"\$HOME/.pyenv\""
        echo ""
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "  [INFO] pyenv not installed (optional)"
    fi
fi
echo ""

# ------------------------------------------------------------------------------
# Test 7: PATH order check
# ------------------------------------------------------------------------------
echo -e "${BLUE}Test 7: PATH priority${NC}"

# Find positions of pyenv and homebrew in PATH
PYENV_POS=-1
HOMEBREW_POS=-1
POS=0

IFS=':' read -ra PATH_PARTS <<< "$PATH"
for part in "${PATH_PARTS[@]}"; do
    if [[ "$part" == *"pyenv/shims"* ]] && [ $PYENV_POS -eq -1 ]; then
        PYENV_POS=$POS
    fi
    if [[ "$part" == "/opt/homebrew/bin" ]] || [[ "$part" == "/usr/local/bin" ]]; then
        if [ $HOMEBREW_POS -eq -1 ]; then
            HOMEBREW_POS=$POS
        fi
    fi
    POS=$((POS + 1))
done

if [ $PYENV_POS -ge 0 ] && [ $HOMEBREW_POS -ge 0 ]; then
    if [ $PYENV_POS -lt $HOMEBREW_POS ]; then
        echo -e "  [$PASS] pyenv shims (position $PYENV_POS) before Homebrew (position $HOMEBREW_POS)"
    else
        echo -e "  [$FAIL] Homebrew (position $HOMEBREW_POS) before pyenv shims (position $PYENV_POS)"
        echo ""
        echo "  This means Homebrew's python3 will be used instead of pyenv's."
        echo ""
        echo "  Fix: Add pyenv shims at the END of ~/.zshrc to ensure priority:"
        echo ""
        echo "    # At the very end of ~/.zshrc"
        echo "    [[ -d \"\$PYENV_ROOT/shims\" ]] && PATH=\"\$PYENV_ROOT/shims:\$PATH\""
        echo ""
        ERRORS=$((ERRORS + 1))
    fi
elif [ $PYENV_POS -ge 0 ]; then
    echo -e "  [$PASS] pyenv shims in PATH (position $PYENV_POS), no Homebrew conflict"
elif [ $HOMEBREW_POS -ge 0 ]; then
    echo -e "  [INFO] Homebrew in PATH (position $HOMEBREW_POS), pyenv not configured"
else
    echo -e "  [INFO] Neither pyenv nor Homebrew in standard locations"
fi
echo ""

# ------------------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------------------
echo "========================================"
echo "  Summary"
echo "========================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC} Your Python environment is correctly configured."
    echo ""
    echo "Agents can reliably use:"
    echo ""
    echo "  python3 <<'EOF'"
    echo "  from my_package import my_function"
    echo "  result = my_function()"
    echo "  print(result)"
    echo "  EOF"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}$WARNINGS warning(s), 0 errors${NC}"
    echo ""
    echo "Your setup should work, but review the warnings above."
    echo ""
    exit 0
else
    echo -e "${RED}$ERRORS error(s), $WARNINGS warning(s)${NC}"
    echo ""
    echo "Fix the errors above to ensure Claude Code agents can run Python reliably."
    echo ""
    echo "For detailed guidance, see:"
    echo "  skills/cc-dev/python-setup/index.md"
    echo ""
    exit 1
fi
