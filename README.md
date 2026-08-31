# WFAU/Phalanx

- [WFAU/Phalanx](#wfauphalanx)
  - [Phalanx info](#phalanx-info)
  - [Branch strategy](#branch-strategy)
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



## Workflows
tbd