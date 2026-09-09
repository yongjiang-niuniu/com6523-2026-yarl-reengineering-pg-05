# Reproducing the final project

The final deliverable is a Python library with regression tests and analysis evidence. There is no separate web application or server to start. The canonical submitted report and evidence map are in the [final-deliverable guide](FINAL_DELIVERABLES.md).

## Use a separate working copy

From a clone of this repository, the following creates a detached working copy at the current archived revision:

```bash
git worktree add --detach ../yarl-final-reproduction HEAD
cd ../yarl-final-reproduction
```

The original scripts write results into `Submission/`. Running them in this separate copy keeps the canonical archived files intact. Record the output of `git rev-parse HEAD` when recording a new run.

## Environment and pure-Python installation

The project declares Python **3.10 or newer** in `setup.cfg`. The recorded baseline used **Python 3.12.13**. Python 3.12 is a suitable starting point for following that environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/test.txt radon
export YARL_NO_EXTENSIONS=1
python -m pip install -e .
python -c 'import yarl; print(yarl.__file__)'
```

The last command should resolve to this working copy's `yarl` package. The pure-Python environment avoids building the optional extension and matches the mode described for the final recorded local verification.

`requirements/test.txt` includes the repository's test dependencies through `test-cibuildwheel.txt`. `radon` is installed separately because the local quality script calls it. The archived [baseline Python version](../Submission/baseline/python_version.txt) and [dependency snapshot](../Submission/baseline/pip_freeze.txt) document the historical environment. The dependency snapshot contains an editable reference to an earlier coursework commit, so use it as a provenance record rather than blindly installing it over the final checkout.

Not every dependency is pinned and operating-system markers affect installed packages. New test totals, skips, timing, and metric-tool output can differ across environments. Preserve the distinction between new results and the original evidence.

## Run regression tests

From the reproduction working copy with the virtual environment activated:

```bash
python -m pytest -q --no-cov tests/test_url_join_regression.py
python -m pytest -q --no-cov tests/test_url_joinpath_regression.py
python -m pytest -q --no-cov tests/test_url.py -k 'join or joinpath or div'
python -m pytest -q --no-cov tests
```

The historical results were 7, 7, and 143 passing tests for the first three checks. The recorded full run had 1,129 passed, 103 skipped, and 2 expected failures. These counts describe the stored run and are not guarantees for every environment.

`--no-cov` matches the original final-check script. Dependencies include coverage support because the repository's test configuration uses it.

## Inspect complexity and maintainability

```bash
python -m radon cc yarl -s -a
python -m radon mi yarl -s
```

The final recorded cyclomatic complexity is 8 for `URL.join` and 1 for `URL._make_child`, compared with 17 each at baseline. Private helpers now hold the corresponding path-resolution decisions. The report claims structural maintainability improvements, not a speed benchmark.

## Regenerate the original verification output set

In the separate reproduction working copy only:

```bash
python tools/run_local_checks.py
```

This runs the focused tests, existing nearby tests, full suite, and both Radon checks in sequence. It stops on a failed command and writes output files under `Submission/final-check/`, including `final_pytest_result.txt` and final Radon reports. The output files are replaced, so do not run this in the canonical archive if you want those original files to stay byte-identical.

## Optional analysis regeneration

The dynamic-analysis script uses Python's standard library and the installed local yarl package:

```bash
python Submission/analysis/collect_dynamic_metrics.py
```

It replaces the dynamic call-count CSV, module-edge CSV, and summary under `Submission/analysis/`. Its scenarios exercise selected URL operations; they are not exhaustive tests or performance measurements.

The evolution script needs a separate full upstream clone. Use the baseline named by the report:

```bash
git clone https://github.com/aio-libs/yarl.git ../yarl-upstream
git -C ../yarl-upstream checkout --detach e25e8d23e6912db52a23513ef1f6a17f889751ef
python Submission/analysis/collect_evolution_metrics.py --upstream ../yarl-upstream
```

The script samples tags as well as `HEAD`. A newly downloaded clone can include newer tags than the historical analysis, so pinning `HEAD` alone does not guarantee the same sampled revisions. Record the available tags and selected revision set with a new run. The full historical upstream clone is not bundled in the personal archive.

The preserved `evolution_summary.md` lists the same abbreviated commit as its first and latest commit. Treat that field as a historical output that requires checking against a complete upstream history before using it as a claim about the project's first commit; the archived file is retained unchanged.

To regenerate the existing charts after reviewing the CSVs:

```bash
python -m pip install pandas matplotlib
python Submission/analysis/create_analysis_charts.py
```

The chart script writes the two existing PNG paths in `Submission/analysis/`.

## Optional compiled build and CI

The coursework's final local evidence used pure-Python mode. A compiled installation additionally needs the compiler/toolchain and Cython setup described by the upstream packaging files; it is a separate environment and should be reported separately.

The original classroom GitHub Actions run could not start because of the organisation account/billing limitation described in [the saved CI record](../Submission/final-check/github_actions_status.md). Personal-archive Actions is disabled and the imported workflow is retained as [inactive reference material](archived-workflows/regression-tests.yml). Use the local checks above for a new run; no successful remote CI run is implied by this archive.
