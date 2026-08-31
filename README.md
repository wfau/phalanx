# WFAU/Phalanx

- [WFAU/Phalanx](#wfauphalanx)
  - [Phalanx info](#phalanx-info)
  - [Branch strategy](#branch-strategy)
  - [Branch protection rules](#branch-protection-rules)
  - [Workflows](#workflows)

This is a fork of the Argo CD repository for the Rubin Science Platform, customised for WFAU.

It stores the root Argo CD application, deployment configuration for the other applications, and a command-line tool to manage Phalanx environments.

## Phalanx info
See [phalanx.lsst.io](https://phalanx.lsst.io/) for full documentation.

Phalanx is developed by the [Vera C. Rubin Observatory](https://www.lsst.org/).

A phalanx is a SQuaRE deployment (Science Quality and Reliability Engineering, the team responsible for the Rubin Science Platform).

## Branch strategy

* Default branch: `fork-mgmt`
* Sync branch: `main`

`main` is used for one-to-one sync with the upstream `lsst-square/phalanx:main`. It is synchronised automatically on a schedule (see workflows below).

`fork-mgmt` is currently used to hold scripts and workflows for managing the repository.

The branching and update strategy is broadly expected to be:

- `main` gets synchronised automatically with the upstream.
- Changes to `main` are evaluated periodically against the current production deployment branch.
- When any changes need to be tested, a candidate branch is created:
  - By merging `main` with the current production deployment branch to test upstream changes.
  - By creating a new development branch from the current production deployment branch to test a new customisation or other WFAU-specific change.
- The candidate branch is used by Argo CD to sync changes in a test environment.
- When the changes are validated, the candidate branch is merged with the current production deployment branch.
- The changes are deployed to production.

## Branch protection rules
To protect the `main` branch from direct changes, a classic branch protetion rule has been defined as follows:

- Lock branch = true
  - Allow fork syncing = true


## Workflows
GitHub workflows are defined per branch in [.github/workflows](.github/workflows).

The workflows in `main` are from the upstream repo. These are disabled in the current repo.

The workflows for the current repo are defined in the default branch and are expected to run from that branch.

- [syncfork.yaml](.github/workflows/syncfork.yaml): Runs on a daily schedule to synchronise `main` with upstream `lsst-sqre/phalanx:main`. Can also be run manually from the GitHub UI.


<!-- End -->