# YARL Software Reengineering — Group PG_05

A group software reengineering study of the Python URL library **yarl**, completed for COM6523 at the University of Sheffield in 2026. The project combines repository evolution analysis, static and dynamic analysis, focused refactoring, regression tests, and a written evaluation.

> Personal preservation copy maintained by **Yongjiang Liu**. This archive is private because the source combines coursework, teaching materials, and/or team contributions.

## Work represented here

- Extracted `URL.join()` path, query, and fragment resolution into private helpers in `yarl/_join.py`.
- Moved child-path construction behind `URL.joinpath()` and `/` into `yarl/_path.py`.
- Added seven focused join regression tests and seven child-path regression tests.
- Preserved baseline, analysis, and before/after evidence in `Submission/`.

The recorded final coursework results are **1,129 passed, 103 skipped, and 2 expected failures**. Recorded cyclomatic complexity fell from 17 to 8 for `URL.join()` and from 17 to 1 for `URL._make_child()`. These are historical results in the submitted evidence, not a new test run performed during archival.

## Repository guide

| Path | Contents |
| --- | --- |
| [`reports/`](reports/) | Additional local PDF version, with source filename and SHA-256 provenance |
| [`Report/`](Report/) | Final report, source document, LaTeX export, and figures |
| [`Submission/final-check/code_completion_summary.md`](Submission/final-check/code_completion_summary.md) | Completed work and recorded verification results |
| [`Submission/analysis/`](Submission/analysis/) | System understanding, evolution and dynamic analysis |
| [`Submission/reengineering/`](Submission/reengineering/) | Before/after evaluation and restructuring evidence |
| [`yarl/_join.py`](yarl/_join.py), [`yarl/_path.py`](yarl/_path.py) | Refactored internal responsibilities |
| [`tests/test_url_join_regression.py`](tests/test_url_join_regression.py), [`tests/test_url_joinpath_regression.py`](tests/test_url_joinpath_regression.py) | Added regression coverage |
| [`README.rst`](README.rst) | Original upstream yarl documentation |

## Using the archive

Use Python 3.10 or newer, as specified in `setup.cfg`. For a local pure-Python development environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/test.txt
YARL_NO_EXTENSIONS=1 python -m pip install -e .
YARL_NO_EXTENSIONS=1 python -m pytest tests/test_url_join_regression.py tests/test_url_joinpath_regression.py
```

The optional compiled build requires the compiler/Cython setup described in the upstream files. Historical full-suite output is retained in [`Submission/final-check/local_full_pytest.txt`](Submission/final-check/local_full_pytest.txt). For the separate upstream history used in mining, see [`reproducibility_notes.md`](Submission/analysis/reproducibility_notes.md).

## Contribution and attribution

This is team work. The project report credits Yongjiang Liu with coordination, requirements analysis, system understanding, integration, and report synthesis. Original Git authorship and the team report preserve the fuller contribution record; the archive does not assign all implementation work to one person. The underlying yarl library is an upstream open-source project, with its Apache 2.0 license and NOTICE retained.

## Verification and limits

Archive validation checks history preservation, file integrity, source attribution, README links, and secret/large-file screening. The full yarl test suite was not rerun as part of this documentation archive.

## Archive provenance

- Original classroom repository: [TUOS-COM-Reengineering-2026/group-project-pg_05](https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05).
- Original default branch: `main`, snapshot [`090d39f005a8`](https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05/commit/090d39f005a881a68ade8c62983ee2420d590bd1).
- Preserved source branches: `main`; preserved tags: 0.
- Original README: [`README.rst`](README.rst). Its original wording is retained; any root-relative links in a copied course README refer to the original repository root.
- Machine-readable record: [`docs/ARCHIVE_PROVENANCE.json`](docs/ARCHIVE_PROVENANCE.json).

The original Git authors, dates, and commits are preserved. The archive adds current documentation without rewriting past work. Existing licenses and notices remain applicable; no new license is asserted over course or team materials. GitHub Actions is disabled in this personal copy. Imported classroom/release workflow files are retained in [`docs/archived-workflows/`](docs/archived-workflows/) as inactive reference material, alongside the upstream Dependabot configuration; their original paths remain in Git history. GitHub issues, pull-request conversations, Actions logs, and external resources are outside this Git archive.
