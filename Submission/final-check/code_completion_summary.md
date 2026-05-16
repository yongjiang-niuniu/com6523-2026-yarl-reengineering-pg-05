# Code Completion Summary

## Completed code work

The project completed one focused reengineering task around `URL.join()`.

## Regression tests

Focused regression tests were added for `URL.join()` covering:

- relative path resolution
- current-directory relative paths
- root-relative paths
- query-only references
- fragment-only references
- network-path references
- absolute URL replacement

## Unit-level refactoring

`URL.join()` was refactored by extracting path, query, and fragment resolution logic into helper functions.

## System-level restructuring

The extracted join helper functions were moved into a new private module:

- `yarl/_join.py`

This reduces the responsibility of `yarl/_url.py` while keeping `URL.join()` as the public API entry point.

## Behaviour preservation

The public API was not changed.

Final local regression result:

- 1122 passed
- 103 skipped
- 2 xfailed

## Complexity outcome

The final complexity result shows:

- `URL.join`: B (8)
- `_resolve_join_path`: B (6)
- `_resolve_join_query`: A (3)
- `_resolve_join_fragment`: A (3)

Compared with the baseline result, `URL.join()` was reduced from C (17) to B (8).

## CI limitation

Remote GitHub Actions could not run automatically because the course organisation reached its GitHub Actions quota. All verification was therefore performed locally and evidence files were committed.
