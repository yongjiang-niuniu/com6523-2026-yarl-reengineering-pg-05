"""Utilities for working with paths."""

from collections.abc import Callable, Sequence
from contextlib import suppress


def normalize_path_segments(segments: Sequence[str]) -> list[str]:
    """Drop '.' and '..' from a sequence of str segments"""

    resolved_path: list[str] = []

    for seg in segments:
        if seg == "..":
            # ignore any .. segments that would otherwise cause an
            # IndexError when popped from resolved_path if
            # resolving for rfc3986
            with suppress(IndexError):
                resolved_path.pop()
        elif seg != ".":
            resolved_path.append(seg)

    if segments and segments[-1] in (".", ".."):
        # do some post-processing here.
        # if the last segment was a relative dir,
        # then we need to append the trailing '/'
        resolved_path.append("")

    return resolved_path


def normalize_path(path: str) -> str:
    # Drop '.' and '..' from str path
    prefix = ""
    if path and path[0] == "/":
        # preserve the "/" root element of absolute paths, copying it to the
        # normalised output as per sections 5.2.4 and 6.2.2.3 of rfc3986.
        prefix = "/"
        path = path[1:]

    segments = path.split("/")
    return prefix + "/".join(normalize_path_segments(segments))


def _make_child_path(
    base_path: str,
    paths: Sequence[str],
    *,
    encoded: bool,
    has_netloc: bool,
    path_quoter: Callable[[str], str],
) -> str:
    """
    Add path elements to base_path, accounting for absolute vs relative paths.

    Existing empty segments are preserved, but new empty segments are not created.
    """
    parsed, needs_normalize = _make_child_segments(
        paths, encoded=encoded, path_quoter=path_quoter
    )
    _extend_with_base_path(parsed, base_path)

    # If the netloc is present, inject a leading slash when adding a path to an
    # absolute URL where there was none before.
    if has_netloc and parsed and parsed[-1] != "":
        parsed.append("")

    parsed.reverse()
    if not has_netloc or not needs_normalize:
        return "/".join(parsed)

    path = "/".join(normalize_path_segments(parsed))
    # If normalizing the path segments removed the leading slash, add it back.
    return f"/{path}" if path and path[0] != "/" else path


def _make_child_segments(
    paths: Sequence[str],
    *,
    encoded: bool,
    path_quoter: Callable[[str], str],
) -> tuple[list[str], bool]:
    parsed: list[str] = []
    needs_normalize = False
    for idx, path in enumerate(reversed(paths)):
        # Empty segment of last is not removed.
        last = idx == 0
        if path and path[0] == "/":
            raise ValueError(f"Appending path {path!r} starting from slash is forbidden")

        # The existing path is already quoted, so quote each new element before
        # combining the old and new segments.
        path = path if encoded else path_quoter(path)
        needs_normalize |= "." in path
        _extend_with_child_segments(parsed, path, last=last)

    return parsed, needs_normalize


def _extend_with_child_segments(parsed: list[str], path: str, *, last: bool) -> None:
    segments = path.split("/")
    segments.reverse()
    # Remove trailing empty segment for all but the last path.
    parsed += segments[1:] if not last and segments[0] == "" else segments


def _extend_with_base_path(parsed: list[str], base_path: str) -> None:
    if not base_path:
        return

    # If the old path ends with a slash, the last segment is an empty string
    # and should be removed before adding the new path segments.
    old_segments = base_path.split("/")
    old = old_segments[:-1] if old_segments[-1] == "" else old_segments
    old.reverse()
    parsed += old
