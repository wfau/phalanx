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

exclude_items=( "fork-mgmt/*"
                "README.md"
                ".github/*"
)

for i in "${exclude_items[@]}" ; do
    echo "$i"
done




# git switch fork-mgmt
# git merge --no-ff --no-commit main
# git reset HEAD README.md
# git reset HEAD fork-mgmt/*
# git reset HEAD .github/*
# git checkout -- README.md
# git checkout -- fork-mgmt/*
# git checkout -- .github/*
# git commit -m "Sync with main"