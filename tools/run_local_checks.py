from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Submission" / "final-check"


def run(command: list[str], output_file: Path | None = None) -> None:
    print(f"\n$ {' '.join(command)}")

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(result.stdout)

    if output_file is not None:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result.stdout, encoding="utf-8")

    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    run(
        [sys.executable, "-m", "pytest", "-q", "--no-cov", "tests/test_url_join_regression.py"],
        OUT_DIR / "local_url_join_regression_tests.txt",
    )

    run(
        [sys.executable, "-m", "pytest", "-q", "--no-cov", "tests/test_url.py", "-k", "join"],
        OUT_DIR / "local_existing_join_tests.txt",
    )

    run(
        [sys.executable, "-m", "pytest", "-q", "--no-cov", "tests"],
        OUT_DIR / "local_full_pytest.txt",
    )

    run(
        ["radon", "cc", "yarl", "-s", "-a"],
        OUT_DIR / "local_radon_complexity.txt",
    )

    run(
        ["radon", "mi", "yarl", "-s"],
        OUT_DIR / "local_radon_maintainability.txt",
    )

    print("\nLocal quality checks completed successfully.")


if __name__ == "__main__":
    main()
