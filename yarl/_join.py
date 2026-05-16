from typing import TYPE_CHECKING

from ._path import normalize_path

if TYPE_CHECKING:
    from ._url import URL


def _resolve_join_path(base: "URL", join_path: str) -> str:
    orig_path = base._path
    if join_path[0] == "/":
        path = join_path
    elif not orig_path:
        path = f"/{join_path}"
    elif orig_path[-1] == "/":
        path = f"{orig_path}{join_path}"
    else:
        # …
        # and relativizing ".."
        # parts[0] is / for absolute urls,
        # this join will add a double slash there
        path = "/".join([*base.parts[:-1], ""]) + join_path
        # which has to be removed
        if orig_path[0] == "/":
            path = path[1:]
    return normalize_path(path) if "." in path else path


def _resolve_join_query(base_query: str, join_path: str, join_query: str) -> str:
    return join_query if join_path or join_query else base_query


def _resolve_join_fragment(
    base_fragment: str, join_path: str, join_fragment: str
) -> str:
    return join_fragment if join_path or join_fragment else base_fragment
