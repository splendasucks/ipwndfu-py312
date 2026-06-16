#!/usr/bin/env bash
# Verify Homebrew libusb is installed and visible on Apple Silicon macOS.
set -euo pipefail

BREW_PREFIX="${HOMEBREW_PREFIX:-/opt/homebrew}"
LIB_PATH="${BREW_PREFIX}/lib/libusb-1.0.dylib"

if [[ "$(uname -m)" != "arm64" ]]; then
  echo "warning: this script targets Apple Silicon (arm64); detected $(uname -m)" >&2
fi

if [[ ! -x "${BREW_PREFIX}/bin/brew" ]]; then
  echo "error: Homebrew not found at ${BREW_PREFIX}/bin/brew" >&2
  exit 1
fi

if [[ ! -f "$LIB_PATH" ]]; then
  echo "error: libusb not installed. Run: brew install libusb" >&2
  exit 1
fi

echo "ok: libusb found at $LIB_PATH"
echo "hint: export DYLD_LIBRARY_PATH=\"${BREW_PREFIX}/lib:\${DYLD_LIBRARY_PATH:-}\""

if command -v uv >/dev/null 2>&1; then
  echo "ok: uv $(uv --version)"
else
  echo "warning: uv not in PATH; install via: brew install uv" >&2
fi
