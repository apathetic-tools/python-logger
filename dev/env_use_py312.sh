#!/bin/bash
set -euo pipefail
# Switch Poetry environment to Python 3.12
# Tries system Python 3.12 first, then falls back to pyenv

# Try system python3.12 first (avoid pyenv shims), then pyenv
PY312_PATH=""
# Check common system locations
for POSSIBLE_PATH in /usr/bin/python3.12 /usr/local/bin/python3.12; do
  if [ -x "$POSSIBLE_PATH" ] && "$POSSIBLE_PATH" --version 2>&1 | grep -q "3.12"; then
    PY312_PATH="$POSSIBLE_PATH"
    break
  fi
done
# If not in system locations, check PATH but exclude pyenv shims
if [ -z "$PY312_PATH" ]; then
  CMD_PATH=$(command -v python3.12 2>/dev/null)
  if [ -n "$CMD_PATH" ] && ! echo "$CMD_PATH" | grep -q "pyenv/shims"; then
    if "$CMD_PATH" --version 2>&1 | grep -q "3.12"; then
      PY312_PATH="$CMD_PATH"
    fi
  fi
fi
# Use system Python if found
if [ -n "$PY312_PATH" ]; then
  poetry env use "$PY312_PATH" && poetry install
# Fall back to pyenv
elif [ -d "$HOME/.pyenv/versions/3.12.3" ]; then
  poetry env use "$HOME/.pyenv/versions/3.12.3/bin/python3" && poetry install
elif command -v pyenv >/dev/null 2>&1; then
  export PYENV_ROOT="$HOME/.pyenv"
  [ -d "$PYENV_ROOT/bin" ] && export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init - bash 2>/dev/null)" || true
  PY312_VER=$(pyenv versions 2>/dev/null | grep "3.12" | head -1 | awk '{print $1}' | tr -d '* ')
  if [ -n "$PY312_VER" ] && [ -d "$HOME/.pyenv/versions/$PY312_VER" ]; then
    poetry env use "$HOME/.pyenv/versions/$PY312_VER/bin/python3" && poetry install
  else
    echo "❌ Python 3.12 not found. Run: poetry run poe setup:pyenv:check"
    exit 1
  fi
else
  echo "❌ Python 3.12 not found. Run: poetry run poe setup:pyenv:check"
  exit 1
fi

