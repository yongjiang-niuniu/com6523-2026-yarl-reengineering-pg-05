# Dynamic Analysis Summary

## Scenarios

- `URL.join` -> `https://example.com/a/d?x=1#frag`
- `URL.joinpath` -> `https://example.com/a/c/%2Fencoded`
- `URL.build` -> `https://example.com/a/b?x=1&lang=en#top`
- `URL.update_query` -> `https://example.com/a?x=2&new=3`

## Runtime Hotspots

### URL.join
- `yarl._quoting_py:_Quoter.__call__`: 6
- `yarl._url:<genexpr>`: 5
- `yarl._quoting_py:_Unquoter.__call__`: 4
- `yarl._url:__new__`: 2
- `yarl._url:encode_url`: 2
- `yarl._parse:split_url`: 2
- `yarl._url:_encode_host`: 1
- `yarl._url:URL.join`: 1

### URL.joinpath
- `yarl._quoting_py:_Quoter.__call__`: 3
- `yarl._path:_extend_with_child_segments`: 2
- `yarl._url:__new__`: 1
- `yarl._url:encode_url`: 1
- `yarl._parse:split_url`: 1
- `yarl._url:URL.joinpath`: 1
- `yarl._url:URL._make_child`: 1
- `yarl._path:_make_child_path`: 1

### URL.build
- `yarl._quoting_py:_Quoter.__call__`: 6
- `yarl._url:build`: 1
- `yarl._query:get_str_query`: 1
- `yarl._query:get_str_query_from_sequence_iterable`: 1
- `yarl._url:_encode_host`: 1
- `yarl._path:normalize_path`: 1
- `yarl._path:normalize_path_segments`: 1
- `yarl._url:URL.__str__`: 1

### URL.update_query
- `yarl._quoting_py:_Quoter.__call__`: 6
- `yarl._quoting_py:_Unquoter.__call__`: 2
- `yarl._url:__new__`: 1
- `yarl._url:encode_url`: 1
- `yarl._parse:split_url`: 1
- `yarl._url:URL.update_query`: 1
- `yarl._url:URL._parsed_query`: 1
- `yarl._parse:query_to_pairs`: 1

## Interpretation

The traced scenarios exercise URL joining, child path assembly, URL construction, and query updates inside the final coursework repository. The evidence shows that `yarl._url` remains the coordinating module, while path assembly now delegates child-path work to `yarl._path` and URL joining delegates join-specific work to `yarl._join`.

This supports the reengineering rationale: the public `URL` API is preserved, but path-specific responsibilities have been moved out of the large `_url.py` module into focused private helpers.
