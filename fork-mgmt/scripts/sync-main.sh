#!/usr/bin/env bash
# Sync `main` branch of WFAU phalanx fork with upstream source `main`
# Must be run from branch `fork-mgmt`
# Must have git@github.com:lsst-sqre/phalanx.git added as upstream remote

set -euo pipefail

# Print help text from comment then exit
if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    sed -ne '/^#/!q;s/.\{1,2\}//;1d;p' < "$0"
    exit
fi


echo "Checking branch..."

BRANCH="fork-mgmt"
CURRENT_BRANCH="$(git branch --show-current)"
UPSTREAM_URL="git@github.com:lsst-sqre/phalanx.git"

echo "Branch: $CURRENT_BRANCH"

if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
    echo "ERROR: Must be on '$BRANCH'; currently on '$CURRENT_BRANCH'." >&2
    exit 1
fi

echo "Checking upstream..."

if ! UPSTREAM_URL="$(git remote get-url upstream 2>/dev/null)"; then
    echo "ERROR: Git remote 'upstream' is not configured." >&2
    exit 1
fi

if ! git ls-remote --exit-code upstream HEAD >/dev/null 2>&1; then
    echo "ERROR: Unable to access upstream repository." >&2
    exit 1
fi

echo "Upstream: $UPSTREAM_URL accessible"

echo "Fetching..."
git fetch upstream

git switch main
git merge --ff-only upstream/main
git push origin main
git switch $BRANCH

# End
