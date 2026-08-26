#!/usr/bin/env bash
# Block commits from main branch.

set -euo pipefail

PROTECTED_BRANCH="main"
CURRENT_BRANCH="$(git branch --show-current)"

if [[ "$CURRENT_BRANCH" == "$PROTECTED_BRANCH" ]]; then
    echo "ERROR: Direct commits to '$PROTECTED_BRANCH' are not allowed." >&2
    exit 1
fi