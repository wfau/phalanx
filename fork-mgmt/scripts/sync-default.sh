#!/usr/bin/env bash
# Merge default branch of WFAU phalanx fork with `main` branch
# Exclude specified files and dirs from the merge

set -euo pipefail

# Print help text from comment then exit
if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    sed -ne '/^#/!q;s/.\{1,2\}//;1d;p' < "$0"
    exit
fi

###############################

DEFAULT_BRANCH="fork-mgmt"
MERGE_BRANCH="main"

echo "${MERGE_BRANCH}"
echo "${DEFAULT_BRANCH}"

# Array of files/dirs to exclude from the merge
exclude_items=( "fork-mgmt/*"
                "README.md"
                ".github/*"
)

git switch "$DEFAULT_BRANCH"
git merge --no-ff --no-commit "$MERGE_BRANCH"

for i in "${exclude_items[@]}" ; do
    git reset HEAD "$i"
    git checkout -- "$i"
done

git commit -m "Sync ${DEFAULT_BRANCH} with ${MERGE_BRANCH}"
