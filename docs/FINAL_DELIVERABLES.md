# Final project deliverables and report guide

This guide follows the **officially submitted COM6523 Software Reengineering Group Project Report, PG_05**. It connects the final project's argument to the preserved implementation and evidence. Page references below refer to PDF viewer pages in the [19-page report](../Report/PG_05_COM6523_Software_Reengineering_Group_Project_Report.pdf).

## Project identity

| Item | Report-grounded value |
| --- | --- |
| Subject system | `aio-libs/yarl`, a Python URL manipulation library |
| Upstream baseline | `e25e8d23e6912db52a23513ef1f6a17f889751ef` |
| Original group repository | [TUOS-COM-Reengineering-2026/group-project-pg_05](https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05) |
| Final classroom export snapshot | `090d39f005a881a68ade8c62983ee2420d590bd1` |
| Target | Internal path-resolution responsibilities behind `URL.join()`, `URL.joinpath()`, and `/` |
| Intended outcome | Better internal structure and maintainability with the existing public API preserved |

The upstream SHA is the source snapshot imported into the coursework repository. It is not a claim that this archive contains the entire upstream Git history. The import is recorded in coursework commit `35dde5f06b4f55dce101717b11fe0651585736a7`; separate upstream history was used for evolution mining.

## Read the final project in order

| Report area | Pages | Preserved deliverables |
| --- | --- | --- |
| Project identity, team and goal | 1–2 | [Group report](../Report/PG_05_COM6523_Software_Reengineering_Group_Project_Report.pdf) and original report sources in [Report/](../Report/) |
| System understanding | 3–6 | [Architecture notes](../Submission/analysis/current_system_understanding.md), [module inventory](../Submission/analysis/module_inventory.csv), [public API inventory](../Submission/analysis/public_api.txt), [test inventory](../Submission/analysis/test_inventory.csv) |
| Baseline and static analysis | 5–6; Appendix B | [Baseline evidence](../Submission/baseline/): environment, pytest, coverage, LOC, complexity, and maintainability |
| Evolution analysis | 3–5 | [Evolution summary](../Submission/analysis/evolution_summary.md), [collection script](../Submission/analysis/collect_evolution_metrics.py), [LOC history](../Submission/analysis/loc_over_time.csv), [commit activity](../Submission/analysis/commits_by_month.csv), [reproducibility notes](../Submission/analysis/reproducibility_notes.md) |
| Regression design | 7–8; Appendix C | [URL.join regression cases](../tests/test_url_join_regression.py) and [URL.joinpath/operator cases](../tests/test_url_joinpath_regression.py) |
| URL.join refactoring | 8; Appendix C | [Private join helpers](../yarl/_join.py), [URL coordination](../yarl/_url.py), [before/after evaluation](../Submission/reengineering/before_after_url_join_refactor.md), [module restructuring summary](../Submission/reengineering/url_join_module_restructure_summary.md) |
| Child-path restructuring | 8; Appendix C | [Path helpers](../yarl/_path.py), [URL coordination](../yarl/_url.py), [child-path summary](../Submission/reengineering/url_child_path_restructure_summary.md) |
| Dynamic analysis | 9 | [Scenario script](../Submission/analysis/collect_dynamic_metrics.py), [summary](../Submission/analysis/dynamic_analysis_summary.md), [call counts](../Submission/analysis/dynamic_call_counts.csv), [module edges](../Submission/analysis/dynamic_module_edges.csv) |
| Final evaluation | 9–11 | [Completion summary](../Submission/final-check/code_completion_summary.md), [pytest output](../Submission/final-check/final_pytest_result.txt), [complexity](../Submission/final-check/final_radon_complexity.txt), [maintainability](../Submission/final-check/final_radon_maintainability.txt) |
| Reflections and AI disclosure | 12–13 | Member reflections and Appendix A in the report |
| Verification procedure and CI limit | 18–19 | [Local check script](../tools/run_local_checks.py), [original Actions limitation](../Submission/final-check/github_actions_status.md), [inactive preserved workflow](archived-workflows/regression-tests.yml) |

These files form one final reengineering project. Existing paths are retained so references in the report, scripts, source history, and evidence remain valid.

## Requirements stated in the report

Blackboard identifies the final deliverables as a PDF report submitted there, code and activity in the GitHub Classroom repository, and separate evidence/data in `Submission/`. All three are represented in this archive. The following are the report's R1–R5 project requirements on page 7.

| ID | Requirement | Evidence in this archive |
| --- | --- | --- |
| R1 | Preserve public API and existing behaviour | Existing URL methods plus focused, nearby, and full-suite historical regression outputs |
| R2 | Add focused regression tests | Seven `URL.join` cases and seven `joinpath`/operator cases in the two regression files |
| R3 | Reduce complexity in `URL.join` and `URL._make_child` | Baseline/final Radon reports and before/after evaluation |
| R4 | Move path-specific responsibilities out of `_url.py` | Private `yarl/_join.py` and child-path helpers in `yarl/_path.py` |
| R5 | Make verification repeatable and visible | `tools/run_local_checks.py`, committed outputs, reproducibility notes, and recorded CI limitation |

## Historical evaluation

| Check | Baseline | Final recorded result | Evidence |
| --- | --- | --- | --- |
| Full local pytest | 1,115 passed, 103 skipped, 2 expected failures | 1,129 passed, 103 skipped, 2 expected failures | [Baseline](../Submission/baseline/baseline_pytest.txt), [final](../Submission/final-check/final_pytest_result.txt) |
| Focused `URL.join` regressions | Added during project | 7 passed | [Saved output](../Submission/final-check/local_url_join_regression_tests.txt) |
| Focused `joinpath`/operator regressions | Added during project | 7 passed | [Saved output](../Submission/final-check/local_url_joinpath_regression_tests.txt) |
| Existing nearby regressions | Existing tests | 143 passed | [Saved output](../Submission/final-check/local_existing_join_tests.txt) |
| `URL.join` cyclomatic complexity | C (17) | B (8) | [Baseline](../Submission/baseline/radon_complexity.txt), [final](../Submission/final-check/final_radon_complexity.txt) |
| `URL._make_child` cyclomatic complexity | C (17) | A (1) | Same Radon reports |

These are preserved results from the project, not new measurements. Complexity is redistributed into private helpers as part of responsibility separation; the report does not claim that all decision logic disappeared or that performance improved. Dynamic traces cover selected scenarios rather than every possible URL.

## Original implementation and evidence history

All abbreviated commits below resolve in the preserved Git history.

| Commit | Role in the final project |
| --- | --- |
| `35dde5f` | Import the named upstream baseline |
| `6fbd572` | Add URL.join regression tests |
| `037e9d4` | Refactor URL.join path resolution |
| `6b5a93a` | Move join helpers into a private module |
| `64cee18` | Add joinpath/operator regression tests |
| `eb405b9` | Move child-path assembly into path helpers |
| `26270ef` | Make analysis scripts reproducible |
| `309e713` | Add dynamic-analysis evidence |
| `822f061` | Refresh final local verification evidence |
| `c6f57ff` | Record the original Actions account/billing limitation |
| `0529b57` | Expand final report body and evidence figures |
| `090d39f` | Select the polished report PDF as the final classroom export |

Later personal-archive commits add documentation and preserve an additional report copy. They do not replace or backdate the original work. Source code, regression tests, analysis evidence, and original report files remain unchanged from `090d39f`.

## Team credit

The report's page 2 contribution table credits:

| Member | Recorded responsibilities |
| --- | --- |
| Dibing Bai | Project setup, repository preparation, baseline environment evidence, and focused local regression testing |
| Yongjiang Liu | Coordination, requirement interpretation, target selection, system understanding, branch/PR integration, and final report/evidence synthesis |
| Jingxuan Wang | Static analysis, Radon/code-smell interpretation, restructuring rationale, and requirement alignment |
| Ziqi Zhao | Regression test design, URL.join refactoring evidence, and before/after evaluation |
| Xuhao Zhou | Upstream evolution analysis, dynamic evidence, workflow/local verification evidence, and document preparation |

The underlying yarl library remains upstream work. Its [LICENSE](../LICENSE), [NOTICE](../NOTICE), [upstream README](../README.rst), and original authorship are preserved. The report's AI-use disclosure is also retained.

## Report consistency and submission provenance

The classroom PDF and local Downloads PDF have identical text on all 19 pages. Their page renders also matched exactly at the recorded 85 dpi comparison, despite differing file hashes and PDF metadata. See [report versions](../reports/README.md) and [machine-readable comparison](../reports/version_comparison.json).

The six source-code listings in Appendix C contain 302 numbered lines. Each was checked against the named file and line number; the code text matched after removing surrounding whitespace. The final report's recorded test counts also match the stored outputs.

The submitted Blackboard attachment was subsequently downloaded and matched byte for byte to the canonical `Report/` PDF. [The submission record](../reports/submission_record.json) identifies Attempt 1, submitted 20 May 2026 at 10:01 (UTC+8), for Blackboard group PGT05. The report labels the team PG_05. Grades and feedback are excluded from this provenance record.

[Reproduction instructions](REPRODUCING_FINAL_PROJECT.md) cover setup, focused/full regression checks, Radon, and optional analysis regeneration while keeping the archived evidence intact.
