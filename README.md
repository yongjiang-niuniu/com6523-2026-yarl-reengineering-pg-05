# YARL Software Reengineering

A team study of how to make URL path resolution easier to understand and maintain without changing the public API of [yarl](README.rst). The project combines system and repository analysis, focused refactoring, regression tests, and a final evaluation for COM6523 at the University of Sheffield.

**Start with the [final group report](Report/PG_05_COM6523_Software_Reengineering_Group_Project_Report.pdf)** or use the [deliverable guide](docs/FINAL_DELIVERABLES.md) to follow its claims into the source and saved evidence.

The Overleaf version checked on **10 September 2026** was still an **11-page unfinished earlier draft**. The verified **19-page submitted report** linked above remains canonical; the incomplete draft is not included as a competing final deliverable.

> **中文概述：** 本项目是 COM6523 的五人团队软件重构作业。团队围绕 yarl 的 URL 路径拼接逻辑开展分析、职责拆分和回归验证，保留了最终实现、报告及历史测试记录。Yongjiang Liu 的贡献包括协调、需求分析、系统理解、集成与报告整合；底层 yarl 库及其他成员贡献均保留原有署名。

## Project at a glance

| Item | Details |
| --- | --- |
| Project type | Team software reengineering study; group PG_05 / Blackboard PGT05 |
| Course | COM6523, University of Sheffield, 2026 |
| Technologies | Python, pytest, Radon, Git-based repository analysis |
| Scope | Internal responsibilities behind `URL.join()`, `URL.joinpath()`, and `/` |
| Available artifacts | Final source, regression tests, analysis scripts, saved evaluation outputs, report and report sources |
| Status | Final coursework preserved; documented test results are historical, not a new test run |

## What the project changes

URL joining must coordinate paths, queries, fragments and edge cases while retaining existing behaviour. The team selected two areas where those responsibilities were concentrated in `yarl/_url.py`:

- **Joining URLs:** private helpers in [`yarl/_join.py`](yarl/_join.py) separate path, query and fragment resolution from `URL.join()`.
- **Building child paths:** helpers in [`yarl/_path.py`](yarl/_path.py) handle the child-path assembly used by `URL.joinpath()` and the `/` operator.
- **Protecting behaviour:** seven focused join tests and seven child-path tests supplement the existing regression suite.

The goal is a clearer internal structure. Decision logic remains in the extracted helpers; the work does not establish a runtime performance improvement.

## Design and evaluation

The project first recorded the system structure, upstream evolution and baseline measurements. Focused regression cases then protected the selected behaviour during refactoring. Static metrics, selected dynamic traces and local tests provided the before/after evaluation.

| Measure | Baseline | Final recorded result |
| --- | --- | --- |
| Full local pytest suite | 1,115 passed, 103 skipped, 2 expected failures | 1,129 passed, 103 skipped, 2 expected failures |
| `URL.join()` cyclomatic complexity | 17 | 8 |
| `URL._make_child()` cyclomatic complexity | 17 | 1 |

These values come from the report and committed coursework outputs. See the [historical evaluation and evidence links](docs/FINAL_DELIVERABLES.md#historical-evaluation) for the focused tests, nearby regression cases and Radon files. Neither archival work nor this documentation refresh reran the full suite.

## Repository guide

| Path | Use it for |
| --- | --- |
| [`docs/README.md`](docs/README.md) | Choose a reading, reproduction or provenance route |
| [`Report/`](Report/) | Read the final report or inspect its source documents and figures |
| [`yarl/`](yarl/) | Inspect the library and the refactored internals |
| [`tests/test_url_join_regression.py`](tests/test_url_join_regression.py), [`tests/test_url_joinpath_regression.py`](tests/test_url_joinpath_regression.py) | Read the 14 focused regression cases |
| [`Submission/analysis/`](Submission/analysis/) | Review system understanding, evolution and dynamic analysis |
| [`Submission/baseline/`](Submission/baseline/), [`Submission/reengineering/`](Submission/reengineering/), [`Submission/final-check/`](Submission/final-check/) | Compare the recorded baseline, changes and final checks |
| [`tools/run_local_checks.py`](tools/run_local_checks.py) | Run the broader local evaluation in a separate working copy |
| [`README.rst`](README.rst) | Read the original upstream library documentation |

## Getting started

For a pure-Python development environment, use Python 3.10 or newer as specified in [`setup.cfg`](setup.cfg):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/test.txt
YARL_NO_EXTENSIONS=1 python -m pip install -e .
YARL_NO_EXTENSIONS=1 python -m pytest -q --no-cov tests/test_url_join_regression.py tests/test_url_joinpath_regression.py
```

This runs the focused tests without intentionally replacing the saved coursework outputs. For the full suite, Radon, optional compiled extensions and analysis regeneration, follow [Reproducing the final project](docs/REPRODUCING_FINAL_PROJECT.md). In particular, `tools/run_local_checks.py` writes to `Submission/final-check/`, and the dynamic-analysis script writes to `Submission/analysis/`; the guide uses a separate working copy to protect historical evidence.

## Verification and limitations

Previous archive checks matched the submitted PDF byte for byte, checked the stored test totals, and matched all 302 numbered source lines in the report's six code listings to the named source files after ignoring surrounding whitespace. The source, tests, analysis outputs, tools and original report remain unchanged from the final classroom snapshot. This documentation refresh checks links and preservation, rather than generating new experiment results.

The dynamic traces cover selected scenarios. Some environment dependencies are unpinned, and reproducing repository evolution requires the separate upstream history and the original sampled revisions. The original classroom Actions run could not start because of account/billing limits; the saved local results do not establish a passing remote CI run. See [reproduction constraints](docs/REPRODUCING_FINAL_PROJECT.md) and [archive scope](docs/ARCHIVE_NOTES.md).

## Attribution and provenance

The report credits **Dibing Bai, Yongjiang Liu, Jingxuan Wang, Ziqi Zhao and Xuhao Zhou**. Yongjiang Liu's recorded responsibilities include coordination, requirements, target selection, system understanding, integration and report/evidence synthesis. The [team contribution table](docs/FINAL_DELIVERABLES.md#team-credit), original Git authorship and report retain the fuller record.

The underlying library is upstream `aio-libs/yarl` work. Its [Apache 2.0 license](LICENSE), [NOTICE](NOTICE) and original documentation remain intact. No new license is asserted over team or course materials.

The canonical report is the official Blackboard submission from **20 May 2026, 10:01 (UTC+8)**. This personal copy preserves the original classroom history through `090d39f005a881a68ade8c62983ee2420d590bd1`; later commits document preservation and navigation. See the [submission record](reports/submission_record.json), [report versions](reports/README.md) and [archive notes](docs/ARCHIVE_NOTES.md).
