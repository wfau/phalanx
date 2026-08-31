# fork-mgmt

Branch for tasks relating to managing and tracking the upstream source of the forked repo.
The intention is that this will be replaced with automation (e.g., via GitHub Actions) once the project is stable.

## Branch policy

The current default branch is: `fork-mgmt`

- Branch `main` is a fork of `lsst-sqre/phalanx:main`. No changes should be made to `main`.
- Branch `fork-mgmt` is used for sync and management tasks.

## Mgmt tasks





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

## lsst-uk

### rspwfau deployment branch

The `lsst-uk/phalanx` repo is a separate fork of `lsst-sqre/phalanx`. The branch `lsst-uk/phalanx:u/etoledo/rspwfau` has been used to create a test deployment of the RSP called rspwfau on Somerville, currently available at https://wfau.lsst.ac.uk/.


`https://github.com/lsst-uk/phalanx/tree/u/etoledo/rspwfau`

```sh
# Add lsst-uk remote
git remote add lsst git@github.com:lsst-uk/phalanx.git

# Replace the push url
git remote set-url --push lsstuk DISABLED

# Check remotes
git remote -v

# Add the branch to the current repo
git fetch lsstuk u/etoledo/rspwfau:u/etoledo/rspwfau
git checkout u/etoledo/rspwfau
git push --set-upstream origin u/etoledo/rspwfau
```

### Compare `lsst-uk/phalanx:main` with `wfau/phalanx:main`

```sh
git diff --name-only main u/etoledo/rspwfau
```

<!-- End -->