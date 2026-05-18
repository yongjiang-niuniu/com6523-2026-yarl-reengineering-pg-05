from __future__ import annotations

import csv
import sys
from collections import Counter
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from types import FrameType

from yarl import URL


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "Submission" / "analysis"

CallKey = tuple[str, str, str]
EdgeKey = tuple[str, str, str, str, str]
FrameInfo = tuple[str, str]


def scenario_join() -> str:
    return str(
        URL("https://example.com/a/b/c?old=1#old").join(URL("../d?x=1#frag"))
    )


def scenario_joinpath() -> str:
    return str(
        URL("https://example.com/a/b?old=1#old").joinpath(
            "../c", "%2Fencoded", encoded=True
        )
    )


def scenario_build() -> str:
    return str(
        URL.build(
            scheme="https",
            host="example.com",
            path="/a/./b",
            query={"x": "1", "lang": "en"},
            fragment="top",
        )
    )


def scenario_update_query() -> str:
    return str(
        URL("https://example.com/a?x=1").update_query({"x": "2", "new": "3"})
    )


SCENARIOS: dict[str, Callable[[], str]] = {
    "URL.join": scenario_join,
    "URL.joinpath": scenario_joinpath,
    "URL.build": scenario_build,
    "URL.update_query": scenario_update_query,
}


def yarl_frame_info(frame: FrameType) -> FrameInfo | None:
    module = frame.f_globals.get("__name__", "")
    if not module.startswith("yarl"):
        return None

    function = frame.f_code.co_name
    self_obj = frame.f_locals.get("self")
    if self_obj is not None and type(self_obj).__module__.startswith("yarl"):
        function = f"{type(self_obj).__name__}.{function}"

    return module, function


def trace_scenario(name: str, scenario: Callable[[], str]) -> tuple[Counter[CallKey], Counter[EdgeKey], str]:
    calls: Counter[CallKey] = Counter()
    edges: Counter[EdgeKey] = Counter()
    stack: list[FrameInfo] = []

    def profiler(frame: FrameType, event: str, arg: object) -> None:
        info = yarl_frame_info(frame)
        if info is None:
            return

        if event == "call":
            module, function = info
            calls[(name, module, function)] += 1
            if stack:
                caller_module, caller = stack[-1]
                edges[(name, caller_module, caller, module, function)] += 1
            stack.append(info)
            return

        if event == "return" and stack:
            if stack[-1] == info:
                stack.pop()
                return
            with suppress(ValueError):
                stack.pop(len(stack) - 1 - stack[::-1].index(info))

    sys.setprofile(profiler)
    try:
        result = scenario()
    finally:
        sys.setprofile(None)

    return calls, edges, result


def write_call_counts(rows: Counter[CallKey]) -> None:
    output = OUT_DIR / "dynamic_call_counts.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["scenario", "module", "function", "calls"])
        for (scenario, module, function), calls in sorted(rows.items()):
            writer.writerow([scenario, module, function, calls])
    print(f"Written {output}")


def write_edges(rows: Counter[EdgeKey]) -> None:
    output = OUT_DIR / "dynamic_module_edges.csv"
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["scenario", "caller_module", "caller", "callee_module", "callee", "calls"]
        )
        for (scenario, caller_module, caller, callee_module, callee), calls in sorted(
            rows.items()
        ):
            writer.writerow([scenario, caller_module, caller, callee_module, callee, calls])
    print(f"Written {output}")


def write_summary(call_counts: Counter[CallKey], results: dict[str, str]) -> None:
    lines = [
        "# Dynamic Analysis Summary",
        "",
        "## Scenarios",
        "",
    ]
    for scenario, result in results.items():
        lines.append(f"- `{scenario}` -> `{result}`")

    lines.extend(["", "## Runtime Hotspots", ""])
    for scenario in SCENARIOS:
        scenario_calls = Counter(
            {
                f"{module}:{function}": calls
                for (name, module, function), calls in call_counts.items()
                if name == scenario
            }
        )
        lines.append(f"### {scenario}")
        for symbol, calls in scenario_calls.most_common(8):
            lines.append(f"- `{symbol}`: {calls}")
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "The traced scenarios exercise URL joining, child path assembly, URL construction, and query updates inside the final coursework repository. The evidence shows that `yarl._url` remains the coordinating module, while path assembly now delegates child-path work to `yarl._path` and URL joining delegates join-specific work to `yarl._join`.",
            "",
            "This supports the reengineering rationale: the public `URL` API is preserved, but path-specific responsibilities have been moved out of the large `_url.py` module into focused private helpers.",
        ]
    )

    output = OUT_DIR / "dynamic_analysis_summary.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written {output}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_calls: Counter[CallKey] = Counter()
    all_edges: Counter[EdgeKey] = Counter()
    results: dict[str, str] = {}

    for name, scenario in SCENARIOS.items():
        calls, edges, result = trace_scenario(name, scenario)
        all_calls.update(calls)
        all_edges.update(edges)
        results[name] = result

    write_call_counts(all_calls)
    write_edges(all_edges)
    write_summary(all_calls, results)


if __name__ == "__main__":
    main()
