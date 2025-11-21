#!/bin/bash
set -euo pipefail
# Switch Poetry environment to Python 3.11
# Tries system Python 3.11 first, then falls back to pyenv

# Try system python3.11 first (avoid pyenv shims), then pyenv
PY311_PATH=""
# Check common system locations
for POSSIBLE_PATH in /usr/bin/python3.11 /usr/local/bin/python3.11; do
  if [ -x "$POSSIBLE_PATH" ] && "$POSSIBLE_PATH" --version 2>&1 | grep -q "3.11"; then
    PY311_PATH="$POSSIBLE_PATH"
    break
  fi
done
# If not in system locations, check PATH but exclude pyenv shims
if [ -z "$PY311_PATH" ]; then
  CMD_PATH=$(command -v python3.11 2>/dev/null)
  if [ -n "$CMD_PATH" ] && ! echo "$CMD_PATH" | grep -q "pyenv/shims"; then
    if "$CMD_PATH" --version 2>&1 | grep -q "3.11"; then
      PY311_PATH="$CMD_PATH"
    fi
  fi
fi
# Use system Python if found
if [ -n "$PY311_PATH" ]; then
  poetry env use "$PY311_PATH" && poetry install
# Fall back to pyenv
elif [ -d "$HOME/.pyenv/versions/3.11.10" ]; then
  poetry env use "$HOME/.pyenv/versions/3.11.10/bin/python3" && poetry install
elif command -v pyenv >/dev/null 2>&1; then
  export PYENV_ROOT="$HOME/.pyenv"
  [ -d "$PYENV_ROOT/bin" ] && export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init - bash 2>/dev/null)" || true
  PY311_VER=$(pyenv versions 2>/dev/null | grep "3.11" | head -1 | awk '{print $1}' | tr -d '* ')
  if [ -n "$PY311_VER" ] && [ -d "$HOME/.pyenv/versions/$PY311_VER" ]; then
    poetry env use "$HOME/.pyenv/versions/$PY311_VER/bin/python3" && poetry install
  else
    echo "❌ Python 3.11 not found. Run: poetry run poe setup:pyenv:check"
    exit 1
  fi
else
  echo "❌ Python 3.11 not found. Run: poetry run poe setup:pyenv:check"
  exit 1
fi

