# Analysis Reproducibility Notes

## Purpose

The analysis evidence in this directory is generated from two sources:

- the coursework repository, which contains the downloaded yarl base snapshot and our reengineering commits
- a separate clone of the original upstream repository, `https://github.com/aio-libs/yarl.git`, used for historical evolution mining

The coursework base snapshot recorded in the initial import commit is:

`e25e8d23e6912db52a23513ef1f6a17f889751ef`

## Re-running the Evolution Analysis

The evolution mining script is:

`Submission/analysis/collect_evolution_metrics.py`

It can be run with an explicit upstream repository path:

```bash
python Submission/analysis/collect_evolution_metrics.py --upstream ../yarl-upstream
```

Alternatively, set `YARL_UPSTREAM_REPO` to the upstream clone path. The output directory defaults to `Submission/analysis`, and can be changed with `--out-dir` or `YARL_ANALYSIS_OUT`.

## Generated Evidence

The script regenerates:

- `commits_by_month.csv`
- `loc_over_time.csv`
- `refactoring_commits.csv`
- `evolution_summary.md`

The script deliberately keeps the upstream repository outside the coursework repository so the submitted repository contains evidence files and reproducible scripts, not a second full copy of yarl history.
