#!/usr/bin/env bash
set -euo pipefail

# Safe GitHub auth smoke test for softwarefactorypublisher.
# This script never prints GITHUB_TOKEN or credential file contents.

MODE="${1:-}"
if [[ -n "${SOFTWAREFACTORYPUBLISHER_ENV_FILE:-}" ]]; then
  ENV_FILE="$SOFTWAREFACTORYPUBLISHER_ENV_FILE"
elif [[ -n "${HERMES_HOME:-}" && -d "$(dirname "$HERMES_HOME")" ]]; then
  ENV_FILE="$(dirname "$HERMES_HOME")/softwarefactorypublisher/.env"
else
  ENV_FILE="$HOME/.hermes/profiles/softwarefactorypublisher/.env"
fi
PROFILE_REPO="${SOFTWAREFACTORYPUBLISHER_AUTH_TEST_REPO:-jack-michaud/software-factory-publisher-profile}"

redact() {
  sed -E 's/(ghp_|github_pat_|sk-)[A-Za-z0-9_:-]+/[REDACTED]/g; s#https://[^/@[:space:]]+@github.com/#https://[REDACTED]@github.com/#g'
}

if [[ ! -f "$ENV_FILE" ]]; then
  echo "GITHUB_TOKEN source missing: $ENV_FILE"
  exit 1
fi

mode="$(stat -c '%a' "$ENV_FILE" 2>/dev/null || echo unknown)"
if [[ "$mode" != "600" ]]; then
  echo "GITHUB_TOKEN source has unexpected mode: $mode (expected 600)"
  exit 1
fi

if ! grep -q '^GITHUB_TOKEN=' "$ENV_FILE"; then
  echo "GITHUB_TOKEN variable is not present in $ENV_FILE"
  exit 1
fi

if [[ "$MODE" == "--check-env-only" ]]; then
  echo "publisher credential env file check passed: GITHUB_TOKEN present, mode 600"
  exit 0
fi

set +x
set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN is empty after loading $ENV_FILE"
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI missing"
  exit 1
fi

# Prefer the token for this process without printing it. gh reads GH_TOKEN non-interactively.
export GH_TOKEN="$GITHUB_TOKEN"

echo "Running non-secret GitHub auth checks for $PROFILE_REPO"
gh auth status 2>&1 | redact
gh repo view "$PROFILE_REPO" --json nameWithOwner,visibility 2>&1 | redact

echo "GitHub auth smoke test passed without printing token values"
