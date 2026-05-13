# Current System Understanding: yarl

## Purpose of the system

yarl is a Python library for URL parsing, construction, normalization, quoting, and manipulation. Its central abstraction is the URL object.

## Main source modules

| Module | Initial understanding |
|---|---|
| yarl/_url.py | Core URL class and most URL transformation methods. This appears to be the main module and has the highest complexity. |
| yarl/_parse.py | URL parsing and low-level splitting logic. |
| yarl/_path.py | Path normalization and path segment processing. |
| yarl/_query.py | Query string handling and query variable conversion. |
| yarl/_quoting_py.py | Python implementation of quoting and unquoting logic. |
| yarl/_quoting_c.pyx | Cython acceleration for quoting logic. |

## Baseline observations

- Local regression tests pass: 1115 passed, 103 skipped, 2 xfailed.
- GitHub Actions was configured, but remote workflow execution is unavailable because the course organisation reached its GitHub Actions quota.
- Baseline complexity analysis suggests yarl/_url.py is the most important candidate for deeper inspection.
- The highest-complexity function identified so far is URL.build, with cyclomatic complexity E (38).
- Other complex areas include encode_url, URL._make_child, URL.join, and _encode_host.

## Possible reengineering direction

A suitable direction may be to reduce complexity in yarl/_url.py without changing the public URL API. Candidate work includes extracting helper functions, clarifying URL construction logic, and adding focused regression tests before refactoring.

## Evidence files

- Submission/baseline/baseline_pytest.txt
- Submission/baseline/coverage_baseline.txt
- Submission/baseline/radon_complexity.txt
- Submission/baseline/radon_maintainability.txt
- Submission/baseline/loc_by_file.csv
- Submission/analysis/module_inventory.csv
- Submission/analysis/test_inventory.csv
- Submission/analysis/public_api.txt
