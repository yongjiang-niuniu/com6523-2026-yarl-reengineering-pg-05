# Evaluation: URL Child Path Restructuring

## Reengineering purpose

After the earlier `URL.join()` work, a second focused restructuring was applied
to `URL._make_child()`, the private method behind `URL.joinpath()` and the `/`
operator.

This was chosen because baseline complexity analysis identified `_make_child()`
as C (17), and because child path assembly is path-specific behaviour that was
still embedded inside the large `yarl/_url.py` module.

## Changed structure

Child path assembly was moved into `yarl/_path.py`.

The new private helpers are:

- `_make_child_path`
- `_make_child_segments`
- `_extend_with_child_segments`
- `_extend_with_base_path`

`URL._make_child()` now coordinates URL state and delegates path-specific
assembly to `_make_child_path()`.

## Regression tests added

Focused regression tests were added in `tests/test_url_joinpath_regression.py`
before relying on the restructuring. They cover child path assembly, query and
fragment cleanup, dot-segment behaviour, relative URL behaviour, encoded path
segments, and the `/` operator.

## Behaviour preservation

The public API was not changed. `URL.joinpath()` and `URL.__truediv__()` remain
the public entry points.

Focused local tests after restructuring showed:

- `tests/test_url_joinpath_regression.py`: 7 passed
- existing URL join/joinpath/div tests: 143 passed

The final local regression run showed:

- 1129 passed
- 103 skipped
- 2 xfailed

## Complexity result

Before this restructuring, baseline complexity showed:

- `URL._make_child`: C (17)

After restructuring, final complexity showed:

- `URL._make_child`: A (1)
- `_make_child_path`: B (8)
- `_make_child_segments`: A (5)
- `_extend_with_child_segments`: A (3)
- `_extend_with_base_path`: A (3)

The result reduces the complexity of the URL class method while keeping the
moved path logic in small, focused helpers.
