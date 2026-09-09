# COM6523 Final Project: YARL Software Reengineering

A group software reengineering study of the Python URL library **yarl**, completed for COM6523 at the University of Sheffield in 2026. The project combines repository evolution analysis, static and dynamic analysis, focused refactoring, regression tests, and a written evaluation.

> Personal preservation copy maintained by **Yongjiang Liu**. This archive is private because the source combines coursework, teaching materials, and/or team contributions.

## Start with the final report

The project is organised around the **PG_05 group report and its final implementation**: reengineering URL path resolution in `aio-libs/yarl` while preserving its public behaviour.

- [Read the officially submitted 19-page group report](Report/PG_05_COM6523_Software_Reengineering_Group_Project_Report.pdf).
- [Follow the report-to-deliverable guide](docs/FINAL_DELIVERABLES.md) for requirements, source changes, regression tests, analysis, evaluation, and the relevant original commits.
- [Check the canonical report and alternate file copy](reports/README.md). The classroom export and Downloads copy have different PDF file hashes but identical extracted text and identical page renders in the recorded comparison.

The report identifies upstream snapshot `e25e8d23e6912db52a23513ef1f6a17f889751ef` and the group repository linked below. This archive preserves the final classroom source snapshot `090d39f005a881a68ade8c62983ee2420d590bd1`, with current archival documentation added afterwards. The canonical report was verified byte for byte against **Attempt 1** of Blackboard’s **Group Project Final Submission (Group Feedback)**, submitted **20 May 2026 at 10:01 (UTC+8)**. The [submission record](reports/submission_record.json) contains file provenance without grades or feedback.

## Final implementation

- Extracted `URL.join()` path, query, and fragment resolution into private helpers in `yarl/_join.py`.
- Moved child-path construction behind `URL.joinpath()` and `/` into `yarl/_path.py`.
- Added seven focused join regression tests and seven child-path regression tests.
- Preserved baseline, analysis, and before/after evidence in `Submission/`.

The recorded final coursework results are **1,129 passed, 103 skipped, and 2 expected failures**. Recorded cyclomatic complexity fell from 17 to 8 for `URL.join()` and from 17 to 1 for `URL._make_child()`. These are historical results in the final report and committed local evidence. They were not rerun during archival.

## Repository guide

| Path | Contents |
| --- | --- |
| [`docs/FINAL_DELIVERABLES.md`](docs/FINAL_DELIVERABLES.md) | Report-led index of the final project and its evidence |
| [`reports/`](reports/) | Additional local PDF version and verified report comparison |
| [`Report/`](Report/) | Final report, source document, LaTeX export, and figures |
| [`Submission/final-check/code_completion_summary.md`](Submission/final-check/code_completion_summary.md) | Completed work and recorded verification results |
| [`Submission/analysis/`](Submission/analysis/) | System understanding, evolution and dynamic analysis |
| [`Submission/reengineering/`](Submission/reengineering/) | Before/after evaluation and restructuring evidence |
| [`yarl/_join.py`](yarl/_join.py), [`yarl/_path.py`](yarl/_path.py) | Refactored internal responsibilities |
| [`tests/test_url_join_regression.py`](tests/test_url_join_regression.py), [`tests/test_url_joinpath_regression.py`](tests/test_url_joinpath_regression.py) | Added regression coverage |
| [`README.rst`](README.rst) | Original upstream yarl documentation |

## Build and test the final project

Use Python 3.10 or newer, as specified in `setup.cfg`. For a local pure-Python development environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/test.txt
YARL_NO_EXTENSIONS=1 python -m pip install -e .
YARL_NO_EXTENSIONS=1 python -m pytest -q --no-cov tests/test_url_join_regression.py tests/test_url_joinpath_regression.py
```

These commands run the focused tests without intentionally rewriting the saved coursework outputs. The existing `tools/run_local_checks.py` runs a broader verification sequence and **overwrites** files in `Submission/final-check/`; use a separate working copy for a new full evaluation if you want to preserve the historical evidence.

For the full suite, Radon, analysis scripts, and a separate worktree that protects the saved evidence, follow [reproducing the final project](docs/REPRODUCING_FINAL_PROJECT.md). The optional compiled build requires the compiler/Cython setup described in the upstream files. Historical full-suite output is retained in [`Submission/final-check/local_full_pytest.txt`](Submission/final-check/local_full_pytest.txt). For the separate upstream history used in mining, see [`reproducibility_notes.md`](Submission/analysis/reproducibility_notes.md).

## Contribution and attribution

This is team work. The project report credits Yongjiang Liu with coordination, requirements analysis, system understanding, integration, and report synthesis. Original Git authorship and the team report preserve the fuller contribution record; the archive does not assign all implementation work to one person. The underlying yarl library is an upstream open-source project, with its Apache 2.0 license and NOTICE retained.

## Verification and limits

Archive validation checks history preservation, file integrity, source attribution, README links, and secret/large-file screening. The report review also matched all 302 numbered lines in its six code listings to the corresponding source text (ignoring surrounding whitespace), checked the recorded test totals, and confirmed that `yarl/`, `tests/`, `Submission/`, `tools/`, and `Report/` remain unchanged from the final classroom snapshot. The full yarl test suite was not rerun as part of this documentation archive.

## Archive provenance

- Original classroom repository: [TUOS-COM-Reengineering-2026/group-project-pg_05](https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05).
- Original default branch: `main`, snapshot [`090d39f005a8`](https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05/commit/090d39f005a881a68ade8c62983ee2420d590bd1).
- Preserved source branches: `main`; preserved tags: 0.
- Original README: [`README.rst`](README.rst). Its original wording is retained; any root-relative links in a copied course README refer to the original repository root.
- Machine-readable record: [`docs/ARCHIVE_PROVENANCE.json`](docs/ARCHIVE_PROVENANCE.json).

The original Git authors, dates, and commits are preserved. The archive adds current documentation without rewriting past work. Existing licenses and notices remain applicable; no new license is asserted over course or team materials. GitHub Actions is disabled in this personal copy. Imported classroom/release workflow files are retained in [`docs/archived-workflows/`](docs/archived-workflows/) as inactive reference material, alongside the upstream Dependabot configuration; their original paths remain in Git history. GitHub issues, pull-request conversations, Actions logs, and external resources are outside this Git archive.
