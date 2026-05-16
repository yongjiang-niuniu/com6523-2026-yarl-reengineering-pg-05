from yarl import URL

import pytest


@pytest.mark.parametrize(
    ("base", "relative", "expected"),
    [
        (
            "https://example.com/a/b/c",
            "../d?x=1#frag",
            "https://example.com/a/d?x=1#frag",
        ),
        (
            "https://example.com/a/b/c",
            "./d",
            "https://example.com/a/b/d",
        ),
        (
            "https://example.com/a/b/c",
            "/root/path",
            "https://example.com/root/path",
        ),
        (
            "https://example.com/a/b/c?old=1#old-fragment",
            "?new=2",
            "https://example.com/a/b/c?new=2#old-fragment",
        ),
        (
            "https://example.com/a/b/c?x=1",
            "#section",
            "https://example.com/a/b/c?x=1#section",
        ),
        (
            "https://example.com/a/b/c",
            "//cdn.example.com/lib.js",
            "https://cdn.example.com/lib.js",
        ),
        (
            "https://example.com/a/b/c",
            "http://other.example.org/new",
            "http://other.example.org/new",
        ),
    ],
)
def test_url_join_rfc3986_regression_cases(base, relative, expected):
    result = URL(base).join(URL(relative))

    assert result == URL(expected)
