# Before/After Evaluation: URL.join Refactoring

## Reengineering target

The selected reengineering target was `URL.join()` in `yarl/_url.py`.

This method was chosen because baseline complexity analysis identified it as one of the more complex methods in the core URL module. The method is also important because URL joining is part of the public behaviour of the `URL` class.

## Baseline evidence

Before refactoring, the baseline Radon complexity report identified:

- `URL.join` complexity: C (17)

The local baseline regression test result was:

- 1115 passed
- 103 skipped
- 2 xfailed

## Refactoring performed

The refactoring extracted the path, query, and fragment resolution logic from `URL.join()` into private helper functions.

The aim was to reduce the complexity of the main public method while preserving the public API and behaviour.

## Regression tests added

Focused regression tests were added for `URL.join()` covering:

- relative path resolution
- current-directory path resolution
- root-relative paths
- query-only references
- fragment-only references
- network-path references
- absolute URL replacement

These tests were added before relying on the refactoring result.

## After-refactoring evidence

After refactoring, the final local regression test result was:

- 1122 passed
- 103 skipped
- 2 xfailed

The final Radon complexity result showed:

- `URL.join`: B (8)
- `_resolve_join_path`: B (6)
- `_resolve_join_query`: A (3)
- `_resolve_join_fragment`: A (3)

## Evaluation

The refactoring reduced the cyclomatic complexity of `URL.join()` from C (17) to B (8). This makes the public method shorter and easier to understand, while moving detailed component-selection logic into focused private helper functions.

The full local regression test suite still passed after the change. This suggests that the refactoring preserved existing behaviour.

The number of passing tests increased because additional focused regression tests were added for `URL.join()`.

## Limitation

Remote GitHub Actions could not be used for automatic verification because the course organisation reached its GitHub Actions quota. Following the course announcement, tests and metrics were run locally and the output files were committed as evidence.
