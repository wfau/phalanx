# fork-mgmt

Branch for automating tasks relating to managing and tracking the upstream source of the forked repo.

The folder `fork-mgmt` will hold any scripts or docs relating specifically to managing the fork.
To make this available when other branches are checked out, add to git worktree:

```sh
git worktree add ../repo-mgmt fork-mgmt
```
and run scripts from `../repo-mgmt/fork-mgmt/...`

---
When running scripts, need to ensure `upstream` is added: This should be the source `phalanx` repo from `lsst-sqre`

```sh
git remote add upstream git@github.com:lsst-sqre/phalanx.git
```

---

Update the `fork-mgmt` branch from `main` once `main` is synced with the upstream source.
```sh
git switch fork-mgmt
git fetch origin
git merge origin/main
```