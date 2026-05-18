from yarl import URL

import pytest


@pytest.mark.parametrize(
    ("base", "segments", "expected"),
    [
        (
            "https://example.com",
            ("alpha", "beta"),
            "https://example.com/alpha/beta",
        ),
        (
            "https://example.com/root/current?old=1#frag",
            ("child",),
            "https://example.com/root/current/child",
        ),
        (
            "https://example.com/root/current/",
            ("../sibling",),
            "https://example.com/root/sibling",
        ),
        (
            "https://example.com/root",
            ("./child",),
            "https://example.com/root/child",
        ),
        (
            "relative/root",
            ("../child",),
            "relative/root/../child",
        ),
    ],
)
def test_joinpath_regression_path_assembly(
    base: str, segments: tuple[str, ...], expected: str
) -> None:
    assert str(URL(base).joinpath(*segments)) == expected


def test_joinpath_regression_encoded_segment_preserves_raw_path() -> None:
    joined = URL("https://example.com/base").joinpath("%2Fchild", encoded=True)

    assert joined.raw_path == "/base/%2Fchild"


def test_truediv_regression_uses_joinpath_and_clears_query_fragment() -> None:
    joined = URL("https://example.com/base?old=1#frag") / "child"

    assert str(joined) == "https://example.com/base/child"
