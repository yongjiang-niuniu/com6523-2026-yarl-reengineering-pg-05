from __future__ import annotations

import csv
import os
import subprocess
from argparse import ArgumentParser, Namespace
from collections import Counter
from pathlib import Path


DEFAULT_UPSTREAM = Path(os.environ.get("YARL_UPSTREAM_REPO", "../yarl-upstream"))
DEFAULT_OUT_DIR = Path(os.environ.get("YARL_ANALYSIS_OUT", "Submission/analysis"))
BASE_SNAPSHOT = "e25e8d23e6912db52a23513ef1f6a17f889751ef"
SOURCE_SUFFIXES = {".py", ".pyx", ".pxd", ".pyi"}


def git(upstream: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(upstream), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def write_commits_by_month(upstream: Path, out_dir: Path) -> None:
    log = git(upstream, "log", "--date=format:%Y-%m", "--pretty=format:%ad")
    counts = Counter(line.strip() for line in log.splitlines() if line.strip())

    output = out_dir / "commits_by_month.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "commits"])
        for month in sorted(counts):
            writer.writerow([month, counts[month]])

    print(f"Written {output}")


def list_source_files_at_commit(upstream: Path, commit: str) -> list[str]:
    files = git(upstream, "ls-tree", "-r", "--name-only", commit).splitlines()
    return [
        file
        for file in files
        if file.startswith(("yarl/", "tests/"))
        and Path(file).suffix in SOURCE_SUFFIXES
    ]


def count_lines_at_commit(upstream: Path, commit: str) -> tuple[int, int, int]:
    total_files = 0
    source_lines = 0
    test_lines = 0

    for file in list_source_files_at_commit(upstream, commit):
        try:
            content = git(upstream, "show", f"{commit}:{file}")
        except subprocess.CalledProcessError:
            continue

        total_files += 1
        line_count = len(content.splitlines())

        if file.startswith("yarl/"):
            source_lines += line_count
        elif file.startswith("tests/"):
            test_lines += line_count

    return total_files, source_lines, test_lines


def write_loc_over_time(upstream: Path, out_dir: Path) -> None:
    # Use tagged releases plus HEAD as meaningful historical snapshots.
    tags = git(upstream, "tag", "--sort=creatordate").splitlines()

    selected_tags = []
    if tags:
        step = max(1, len(tags) // 20)
        selected_tags = tags[::step]
        if tags[-1] not in selected_tags:
            selected_tags.append(tags[-1])

    revisions = selected_tags + ["HEAD"]

    output = out_dir / "loc_over_time.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["revision", "commit", "date", "files", "source_lines", "test_lines", "total_lines"])

        for revision in revisions:
            commit = git(upstream, "rev-list", "-n", "1", revision).strip()
            date = git(upstream, "show", "-s", "--format=%cs", commit).strip()
            files, source_lines, test_lines = count_lines_at_commit(upstream, commit)

            writer.writerow([
                revision,
                commit,
                date,
                files,
                source_lines,
                test_lines,
                source_lines + test_lines,
            ])

    print(f"Written {output}")


def write_refactoring_commits(upstream: Path, out_dir: Path) -> None:
    keywords = [
        "refactor",
        "restructure",
        "cleanup",
        "clean up",
        "simplify",
        "rewrite",
        "split",
        "move",
        "remove dead",
        "deprecate",
    ]

    rows = []
    for keyword in keywords:
        log = git(
            upstream,
            "log",
            "--all",
            "--regexp-ignore-case",
            f"--grep={keyword}",
            "--date=short",
            "--pretty=format:%H%x1f%h%x1f%ad%x1f%an%x1f%s",
        )

        for line in log.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 5:
                rows.append([keyword, *parts])

    # Remove duplicates by full commit hash.
    seen = set()
    unique_rows = []
    for row in rows:
        commit_hash = row[1]
        if commit_hash not in seen:
            seen.add(commit_hash)
            unique_rows.append(row)

    output = out_dir / "refactoring_commits.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["matched_keyword", "commit", "short_commit", "date", "author", "subject"])
        writer.writerows(unique_rows)

    print(f"Written {output}")


def write_summary(upstream: Path, out_dir: Path) -> None:
    total_commits = git(upstream, "rev-list", "--count", "HEAD").strip()
    first_hash = git(upstream, "rev-list", "--max-parents=0", "HEAD").splitlines()[0]
    first_commit = git(
        upstream,
        "show",
        "-s",
        "--date=short",
        "--pretty=format:%h %ad %s",
        first_hash,
    ).strip()
    latest_commit = git(
        upstream,
        "log",
        "--date=short",
        "--pretty=format:%h %ad %s",
        "-n",
        "1",
    ).strip()
    snapshot_commit = git(
        upstream,
        "show",
        "-s",
        "--date=short",
        "--pretty=format:%h %ad %s",
        BASE_SNAPSHOT,
    ).strip()

    summary = f"""# Evolution Analysis Summary

## Repository history

- Total commits in upstream repository: {total_commits}
- First commit: {first_commit}
- Latest analysed commit: {latest_commit}
- Coursework base snapshot: {snapshot_commit}

## Generated evidence files

- Submission/analysis/commits_by_month.csv
- Submission/analysis/loc_over_time.csv
- Submission/analysis/refactoring_commits.csv

## Initial interpretation

The generated commit history and LOC data can be used to identify periods of rapid growth, stabilisation, or restructuring. The refactoring commit search is keyword-based, so each candidate commit should be manually inspected before drawing final conclusions in the report.
"""

    output = out_dir / "evolution_summary.md"
    output.write_text(summary, encoding="utf-8")
    print(f"Written {output}")


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Collect yarl upstream evolution metrics for the reengineering report."
    )
    parser.add_argument(
        "--upstream",
        type=Path,
        default=DEFAULT_UPSTREAM,
        help=(
            "Path to a clone of aio-libs/yarl. Defaults to YARL_UPSTREAM_REPO "
            "or ../yarl-upstream."
        ),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=(
            "Directory for generated CSV and summary files. Defaults to "
            "YARL_ANALYSIS_OUT or Submission/analysis."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    upstream = args.upstream.resolve()
    out_dir = args.out_dir

    if not (upstream / ".git").exists():
        raise SystemExit(
            f"Cannot find a git clone at {upstream}. "
            "Clone https://github.com/aio-libs/yarl.git first, or pass --upstream."
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    write_commits_by_month(upstream, out_dir)
    write_loc_over_time(upstream, out_dir)
    write_refactoring_commits(upstream, out_dir)
    write_summary(upstream, out_dir)


if __name__ == "__main__":
    main()
