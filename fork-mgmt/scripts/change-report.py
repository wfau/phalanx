"""
Report upstream changes:
Generate a report formatted for GitHub markdown that
summarises the changes between the just-synced upstream and
a branch in the current repo.

Output a tabular report that can be displayed in
GitHub using "$GITHUB_STEP_SUMMARY" within
a workflow.
"""

import sys
import argparse
from pathlib import PurePosixPath
from typing import Any

import yaml
from git import Repo, GitCommandError
from tabulate import tabulate


# Helper funcs

def ref_exists(repo: Repo, branch: str) -> bool:
    """
    Return whether a branch exists in local 
    or remote tracking.
    """
    refs = (
        f"refs/heads/{branch}",
        f"refs/remotes/{branch}",
    )

    for ref in refs:
        try:
            repo.git.show_ref("--verify", "--quiet", ref)
            return True
        except GitCommandError:
            continue

    return False

def read_file_at_ref(repo: Repo, ref: str, path: str) -> str | None:
    """Read file at git commit ref."""
    commit = repo.commit(ref)
    try:
        blob = commit.tree / path
    except KeyError:
        return None
    return blob.data_stream.read().decode("utf-8")


def read_yaml_at_ref(repo: Repo, ref: str, path: str) -> dict | None:
    """Read YAML file at git commit ref."""
    text = read_file_at_ref(repo, ref, path)
    if text is None:
        return None
    return yaml.safe_load(text) or {}


def chart_app_version(repo: Repo, ref: str, app: str) -> str | None:
    """Read Helm chart yaml file at git commit ref."""
    data = read_yaml_at_ref(repo, ref, f"applications/{app}/Chart.yaml")
    if not data:
        return None
    return data.get("appVersion")


def get_nested(data: dict, keys: tuple[str, ...]) -> Any:
    """Get nested dicts."""
    value = data
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def image_tag(repo: Repo, ref: str, path: str) -> str | None:
    """Read image tag from a values YAML file."""
    data = read_yaml_at_ref(repo, ref, path)
    if not data:
        return None
    return get_nested(data, ("image", "tag"))


def table(records: list[dict], headers: dict[str, str]) -> str:
    """Build GitHub-flavor markdown table."""
    if not records:
        return "_None._"
    return tabulate(records, headers=headers, tablefmt="github")

def render_markdown(report: dict) -> str:
    """Build the markdown report sections."""
    comparison = report["comparison"]

    overview = [
        {
            "metric": "Changed applications",
            "count": len({row["application"] for row in report["changed_files"]}),
        },
        {
            "metric": "Changed files",
            "count": len(report["changed_files"]),
        },
        {
            "metric": "App version changes",
            "count": len(report["app_version_changes"]),
        },
        {
            "metric": "Image tag changes",
            "count": len(report["image_tag_changes"]),
        },
    ]

    return "\n\n".join(
        [
            "## Fork Sync Change Report",
            f"Compared `{comparison['base_ref']}...{comparison['target_ref']}`.",
            "### Overview\n\n"
            + tabulate(overview, headers="keys", tablefmt="github"),
            "### App Version Changes\n\n"
            + table(
                report["app_version_changes"],
                {
                    "application": "Application",
                    "old": "Old",
                    "new": "New",
                },
            ),
            "### Image Tag Changes\n\n"
            + table(
                report["image_tag_changes"],
                {
                    "application": "Application",
                    "file": "File",
                    "old": "Old",
                    "new": "New",
                },
            ),
            "### Changed Application Files\n\n"
            + table(
                report["changed_files"],
                {
                    "status": "Status",
                    "application": "Application",
                    "file": "File",
                },
            ),
        ]
    )

# Global vars
DEFAULT_BASE_REF = "origin/fork-mgmt"
DEFAULT_TARGET_REF = "origin/main"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Compare changed apps in two branches and generate tabulated output"
    )

    # Specify branches to compare
    parser.add_argument(
        "-b",
        "--base",
        type=str, 
        default=DEFAULT_BASE_REF,
        help="Base Git ref for comparison."
        )

    parser.add_argument(
        "-t",
        "--target", 
        type=str, 
        default=DEFAULT_TARGET_REF,
        help="Target Git ref for comparison."
        )

    args = parser.parse_args()

    # Use current context
    repo = Repo(".")

    base_ref = args.base
    target_ref = args.target

    # Validate branches
    if not ref_exists(repo, base_ref):
        parser.error(f"base ref does not exist: {base_ref!r}")

    if not ref_exists(repo, target_ref):
        parser.error(f"target ref does not exist: {target_ref!r}")

    base_commit = repo.commit(base_ref)
    target_commit = repo.commit(target_ref)

    # Check merge base exists
    merge_bases = repo.merge_base(base_commit, target_commit)
    if not merge_bases:
        parser.error(
            f"Git refs have no common ancestor: {base_ref!r}, {target_ref!r}"
        )
    # Take the most recent if exists
    merge_base = merge_bases[0]
    
    
    old_ref = merge_base.hexsha

    # Build report dict
    report = {
        "comparison": {
            "base_ref": base_ref,
            "target_ref": target_ref,
            "base_commit": base_commit.hexsha,
            "target_commit": target_commit.hexsha,
            "merge_base": merge_base.hexsha,
        },
        "changed_files": [],
        "app_version_changes": [],
        "image_tag_changes": [],
    }

    # Populate dict #
    
    # Diff latest common merge with tip of target branch
    name_status = repo.git.diff(
        "--name-status",
        old_ref,
        target_ref,
        "--",
        "applications/",
    ).splitlines()

    # Preserve the source path to avoid returning none for old tags
    old_paths = {}

    for row in name_status:
        parts = row.split("\t")
        status = parts[0]
        path = parts[-1]  # for renames this is the new path
        old_path = parts[-2] if status.startswith(("R", "C")) else path
        old_paths[path] = old_path


        app = PurePosixPath(path).parts[1]

        report["changed_files"].append(
            {
                "status": status,
                "application": app,
                "file": path,
            }
        )

    # Changed applications
    changed_apps = sorted(
        {row["application"] for row in report["changed_files"]}
    )

    for app in changed_apps:
        old = chart_app_version(repo, old_ref, app)
        new = chart_app_version(repo, target_ref, app)

        if old != new:
            report["app_version_changes"].append(
                {
                    "application": app,
                    "old": old,
                    "new": new,
                }
            )

    # Changed files
    for row in report["changed_files"]:
        path = row["file"]
        p = PurePosixPath(path)

        if not (
            p.name.startswith("values")
            and p.suffix in {".yaml", ".yml"}
        ):
            continue

        old = image_tag(repo, old_ref, old_paths[path])
        new = image_tag(repo, target_ref, path)

        if old != new:
            report["image_tag_changes"].append(
                {
                    "application": row["application"],
                    "file": path,
                    "old": old,
                    "new": new,
                }
            )


    # Output report
    sys.stdout.write(render_markdown(report))






