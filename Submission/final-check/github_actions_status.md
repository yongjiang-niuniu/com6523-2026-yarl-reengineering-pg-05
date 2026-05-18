# GitHub Actions Status

## Latest remote run checked

- Workflow: `Regression tests`
- Event: push to `main`
- Commit: `822f0615793352dfa15179102c1eee4d8168c6ad`
- Run URL: https://github.com/TUOS-COM-Reengineering-2026/group-project-pg_05/actions/runs/26065449947
- Status: completed
- Conclusion: failure

## Failure reason

The GitHub check annotation says the job was not started because recent account
payments failed or the spending limit needs to be increased. No runner was
allocated, so this was an account/quota issue rather than a regression-test
failure in the project code.

## Local fallback evidence

Local verification was run successfully and committed in this directory:

- `final_pytest_result.txt`: 1129 passed, 103 skipped, 2 xfailed
- `final_radon_complexity.txt`
- `final_radon_maintainability.txt`
- `local_url_join_regression_tests.txt`
- `local_url_joinpath_regression_tests.txt`
- `local_existing_join_tests.txt`
