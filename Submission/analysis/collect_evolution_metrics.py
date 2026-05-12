from __future__ import annotations

import csv
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path


UPSTREAM = Path("../yarl-upstream")
OUT_DIR = Path("Submission/analysis")
SOURCE_SUFFIXES = {".py", ".pyx", ".pxd", ".pyi"}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(UPSTREAM), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def write_commits_by_month() -> None:
    log = git("log", "--date=format:%Y-%m", "--pretty=format:%ad")
    counts = Counter(line.strip() for line in log.splitlines() if line.strip())

    output = OUT_DIR / "commits_by_month.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "commits"])
        for month in sorted(counts):
            writer.writerow([month, counts[month]])

    print(f"Written {output}")


def list_source_files_at_commit(commit: str) -> list[str]:
    files = git("ls-tree", "-r", "--name-only", commit).splitlines()
    return [
        file
        for file in files
        if file.startswith(("yarl/", "tests/"))
        and Path(file).suffix in SOURCE_SUFFIXES
    ]


def count_lines_at_commit(commit: str) -> tuple[int, int, int]:
    total_files = 0
    source_lines = 0
    test_lines = 0

    for file in list_source_files_at_commit(commit):
        try:
            content = git("show", f"{commit}:{file}")
        except subprocess.CalledProcessError:
            continue

        total_files += 1
        line_count = len(content.splitlines())

        if file.startswith("yarl/"):
            source_lines += line_count
        elif file.startswith("tests/"):
            test_lines += line_count

    return total_files, source_lines, test_lines


def write_loc_over_time() -> None:
    # Use tagged releases plus HEAD as meaningful historical snapshots.
    tags = git("tag", "--sort=creatordate").splitlines()

    selected_tags = []
    if tags:
        step = max(1, len(tags) // 20)
        selected_tags = tags[::step]
        if tags[-1] not in selected_tags:
            selected_tags.append(tags[-1])

    revisions = selected_tags + ["HEAD"]

    output = OUT_DIR / "loc_over_time.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["revision", "commit", "date", "files", "source_lines", "test_lines", "total_lines"])

        for revision in revisions:
            commit = git("rev-list", "-n", "1", revision).strip()
            date = git("show", "-s", "--format=%cs", commit).strip()
            files, source_lines, test_lines = count_lines_at_commit(commit)

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


def write_refactoring_commits() -> None:
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

    output = OUT_DIR / "refactoring_commits.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["matched_keyword", "commit", "short_commit", "date", "author", "subject"])
        writer.writerows(unique_rows)

    print(f"Written {output}")


def write_summary() -> None:
    total_commits = git("rev-list", "--count", "HEAD").strip()
    first_commit = git("log", "--reverse", "--date=short", "--pretty=format:%h %ad %s", "-n", "1").strip()
    latest_commit = git("log", "--date=short", "--pretty=format:%h %ad %s", "-n", "1").strip()

    summary = f"""# Evolution Analysis Summary

## Repository history

- Total commits in upstream repository: {total_commits}
- First commit: {first_commit}
- Latest analysed commit: {latest_commit}

## Generated evidence files

- Submission/analysis/commits_by_month.csv
- Submission/analysis/loc_over_time.csv
- Submission/analysis/refactoring_commits.csv

## Initial interpretation

The generated commit history and LOC data can be used to identify periods of rapid growth, stabilisation, or restructuring. The refactoring commit search is keyword-based, so each candidate commit should be manually inspected before drawing final conclusions in the report.
"""

    output = OUT_DIR / "evolution_summary.md"
    output.write_text(summary, encoding="utf-8")
    print(f"Written {output}")


def main() -> None:
    if not UPSTREAM.exists():
        raise SystemExit("Cannot find ../yarl-upstream. Clone it first.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    write_commits_by_month()
    write_loc_over_time()
    write_refactoring_commits()
    write_summary()


if __name__ == "__main__":
    main()
