# Evaluation: URL.join Module Restructuring

## Reengineering purpose

After refactoring `URL.join()` by extracting helper functions, a further system-level restructuring was performed. The join-specific helper functions were moved from `yarl/_url.py` into a new private module, `yarl/_join.py`.

## Changed structure

Moved private helper logic into:

- `yarl/_join.py`

The moved helpers are:

- `_resolve_join_path`
- `_resolve_join_query`
- `_resolve_join_fragment`

`yarl/_url.py` now imports these helpers instead of defining them directly.

## Rationale

`yarl/_url.py` is the largest and most complex core module in the system. Moving join-specific helper logic into a focused private module reduces the responsibility of `_url.py` and makes the URL joining logic easier to locate, test, and maintain.

## Behaviour preservation

The public API was not changed. `URL.join()` remains the public method used by callers.

Local regression testing after the restructuring showed:

- 1122 passed
- 103 skipped
- 2 xfailed

## Complexity result

After restructuring:

- `URL.join`: B (8)
- `_resolve_join_path`: B (6)
- `_resolve_join_query`: A (3)
- `_resolve_join_fragment`: A (3)

This indicates that the main public method remained simplified while the extracted helper functions stayed small and manageable.
