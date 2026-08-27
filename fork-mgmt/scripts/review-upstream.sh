#!/usr/bin/env bash
# After syncing `main` with the upstream `lsst-sqre/phalanx` `main`
# and before updating `fork-mgmt`, check what has changed.


set -euo pipefail

# Print help text from comment then exit
if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    sed -ne '/^#/!q;s/.\{1,2\}//;1d;p' < "$0"
    exit
fi

MAIN_BRANCH="main"
MGMT_BRANCH="fork-mgmt"

BASE="$(git merge-base "$MGMT_BRANCH" "$MAIN_BRANCH")"

# echo "Changes in main since:"
# git show \
#     --no-patch \
#     --format='%h %cs %s' \
#     "$BASE"

# echo
# echo "Upstream commits:"
# git log \
#     --oneline \
#     "$BASE" "$MAIN_BRANCH"

# echo
# echo "Changed files:"
# git diff \
#     --name-status \
#     "$BASE" "$MAIN_BRANCH"


echo "Changed directories:"
git diff \
    --dirstat=files,0 \
    "$BASE" "$MAIN_BRANCH"

# echo
# echo "Diff summary:"
# git diff \
#     --stat \
#     "$BASE" "$MAIN_BRANCH"

# End