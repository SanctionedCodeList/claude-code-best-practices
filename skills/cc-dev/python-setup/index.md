# Python Environment Setup for Claude Code Agents

This guide covers how to configure Python on macOS/Linux so that Claude Code agents can reliably run Python scriptlets without virtual environments or special configuration.

## The Problem

Claude Code runs shell commands in **non-interactive mode**. This means:

- `.zshrc` / `.bashrc` are NOT loaded (these are for interactive shells only)
- `.zshenv` IS loaded (for all zsh shells)
- `.profile` / `.bash_profile` may or may not be loaded depending on shell type

If you use pyenv, nvm, or similar version managers with "lazy loading" patterns in `.zshrc`, Claude Code won't see them.

### Common Symptoms

```bash
# Agent runs this:
python3 -c "import my_package"

# Gets:
ModuleNotFoundError: No module named 'my_package'
```

Or worse, the agent installs packages to the wrong Python (e.g., Homebrew's Python instead of pyenv's).

## The Solution

### 1. Configure `.zshenv` for Non-Interactive Shells

Add version manager paths to `~/.zshenv` so ALL shells (including Claude Code) see them:

```bash
# ~/.zshenv

# Cargo (Rust)
. "$HOME/.cargo/env"

# Pyenv - add shims to PATH for all shells
export PYENV_ROOT="$HOME/.pyenv"
[[ -d "$PYENV_ROOT/shims" ]] && PATH="$PYENV_ROOT/shims:$PATH"
```

### 2. Ensure Priority in `.zshrc`

If you have Homebrew or other tools that prepend to PATH in `.zshrc`, add pyenv shims again at the END of `.zshrc` to ensure they take priority:

```bash
# ~/.zshrc (at the very end)

# Ensure pyenv takes priority over Homebrew
[[ -d "$PYENV_ROOT/shims" ]] && PATH="$PYENV_ROOT/shims:$PATH"
```

### 3. Avoid Lazy-Load Wrappers for Python Commands

Don't wrap `python3`, `pip`, etc. in lazy-load functions. This pattern causes infinite recursion:

```bash
# BAD - causes infinite recursion
python3() {
  _init_pyenv
  python3 "$@"  # calls itself!
}
```

Instead, just ensure pyenv shims are in PATH. The shims handle version selection automatically.

You CAN lazy-load the `pyenv` command itself for shell integration features:

```bash
# OK - only wraps the pyenv command, not python3/pip
pyenv() {
  unfunction pyenv 2>/dev/null
  eval "$(command pyenv init -)"
  pyenv "$@"
}
```

## Writing Python Scriptlets for Agents

### Use Quoted Heredocs

Always quote the heredoc delimiter to prevent shell expansion:

```bash
# CORRECT - quoted delimiter prevents shell expansion
python3 <<'EOF'
data = {"key": "value"}
print(f"Result: {data['key']}")
EOF

# WRONG - unquoted delimiter allows shell expansion, breaks f-strings
python3 <<EOF
data = {"key": "value"}
print(f"Result: {data['key']}")  # Shell tries to expand {data['key']}
EOF
```

### Don't Nest in Shell Wrappers

Avoid wrapping heredocs in `bash -c` or `zsh -c` - the nested quoting causes escaping nightmares:

```bash
# BAD - nested quoting causes escaping issues
zsh -c 'python3 <<'"'"'EOF'"'"'
print("hello")
EOF'

# GOOD - direct heredoc
python3 <<'EOF'
print("hello")
EOF
```

### Use `python3 -m pip` for Installs

Ensure packages install to the same Python that will run them:

```bash
# CORRECT - installs to whichever python3 is in PATH
python3 -m pip install --user package-name

# RISKY - pip might point to different Python than python3
pip install --user package-name
```

## Structuring Python Packages for Agent Use

### Use `src/` Layout

```
my-package/
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
└── install.sh
```

### Provide a Simple Install Script

```bash
#!/bin/bash
# install.sh - idempotent, safe to run multiple times

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check Python environment
PYTHON3_PATH=$(command -v python3)
PYTHON3_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

echo "Python: $PYTHON3_VERSION ($PYTHON3_PATH)"

# Verify pip uses same Python
PIP_VERSION=$(python3 -m pip --version | grep -oE 'python [0-9.]+' | cut -d' ' -f2)
PIP_MM=$(echo "$PIP_VERSION" | cut -d. -f1,2)

if [ "$PYTHON3_VERSION" != "$PIP_MM" ]; then
    echo "WARNING: Python version mismatch!"
    echo "  python3: $PYTHON3_VERSION"
    echo "  pip: $PIP_VERSION"
    echo ""
    echo "Check your shell config. See: python-setup best practices"
fi

# Install package
# --break-system-packages needed for Homebrew Python (PEP 668), safe with --user
python3 -m pip install --user --break-system-packages -q -e "$REPO_ROOT" 2>/dev/null || \
python3 -m pip install --user -q -e "$REPO_ROOT"

# Verify import works
if ! python3 -c "import my_package" 2>/dev/null; then
    echo "ERROR: Package installed but cannot be imported!"
    echo "This usually means python3 and pip point to different Pythons."
    exit 1
fi

echo "Installation complete"
```

### Export a Clean API

```python
# src/my_package/__init__.py
from my_package.core import function1, function2, function3

__all__ = ["function1", "function2", "function3"]
```

This lets agents write concise imports:

```python
from my_package import function1, function2
```

## Verification

Run the test script to check your configuration:

```bash
./skills/cc-dev/python-setup/test-setup.sh
```

This tests:
1. python3 location and version
2. pip alignment with python3
3. Non-interactive shell behavior (simulates Claude Code)
4. Heredoc syntax with f-strings
5. Shell function conflicts
6. Environment variables (PYENV_ROOT)
7. PATH priority (pyenv vs Homebrew)

### Manual Verification

If you prefer manual checks:

```bash
# 1. Check python3 resolves to correct version
which python3
# Should show: ~/.pyenv/shims/python3 (not /opt/homebrew/bin/python3)

# 2. Check version
python3 --version

# 3. Test in fresh non-interactive shell (simulates Claude Code)
/bin/zsh -c 'which python3 && python3 --version'

# 4. Verify pip alignment
python3 -m pip --version
# Should show same Python version as step 2
```

## Troubleshooting

### "command not found: _init_pyenv"

You have lazy-load wrapper functions for `python3`/`pip` that reference undefined helper functions. Remove the wrappers and rely on PATH-based shims instead.

### Module imports fail in Claude Code but work in terminal

Your terminal is interactive (loads `.zshrc`) but Claude Code is non-interactive. Move the PATH setup to `.zshenv`.

### Wrong Python version despite pyenv setup

Check PATH order. Homebrew or other tools may be prepending their paths after pyenv. Add pyenv shims at the END of `.zshrc` to ensure priority.
