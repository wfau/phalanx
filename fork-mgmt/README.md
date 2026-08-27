# fork-mgmt

Branch for tasks relating to managing and tracking the upstream source of the forked repo.

The intention is that this will be replaced with automation (e.g., via GitHub Actions) once the project is stable.

## Branch policy

- Branch `main` is a fork of `lsst-sqre/phalanx:main`. No changes should be made to `main`.
- Branch `fork-mgmt` is created from `main`. The only difference should be the folder `fork-mgmt`. No other changes should be made to branch `fork-mgmt`
- At least one deployment branch should be created. `main` should not be used for deployment.
- Where changes are required, create a candidate branch.
- When the changes on the candidate branch have been tested and validated, merge these into a deployment branch.

## Mgmt tasks

The folder `fork-mgmt` will hold any scripts or docs relating specifically to managing the fork. This should be the only local change between branch `fork-mgmt` and branch `main`.

To make this available when other branches are checked out, add to git worktree:

```sh
git worktree add ../repo-mgmt fork-mgmt
```
and run scripts from `../repo-mgmt/fork-mgmt/...`

---
For syncing `main` with the upstream source `lsst-sqre/phalanx:main`, the source should be added as an additional fetch-only remote labelled `upstream`

```sh
# Add the source remote
git remote add upstream git@github.com:lsst-sqre/phalanx.git

# Replace the push url with a non-url string
git remote set-url --push upstream DISABLED

# upstream fetch should have correct url
git remote -v
```

Run the script [scripts/sync-main.sh](scripts/sync-main.sh) to fetch the upstream main and fast-forward merge it with the local main checkout.

This can then be compared with the branch `fork-mgmt` (which will be behind `main`). Once the changes are noted, update branch `fork-mgmt` to bring it in line with `main` (except for the current folder).


Update the `fork-mgmt` branch from `main` once `main` is synced with the upstream source.
```sh
git switch fork-mgmt
git fetch origin
git merge origin/main
```

## lsst-uk branch

The `lsst-uk/phalanx` repo is a separate fork of `lsst-sqre/phalanx`. The branch `lsst-uk/phalanx:u/etoledo/rspwfau` has been used to create a test deployment of the RSP called rspwfau on Somerville, currently available at https://wfau.lsst.ac.uk/.


`https://github.com/lsst-uk/phalanx/tree/u/etoledo/rspwfau`



<!-- End -->