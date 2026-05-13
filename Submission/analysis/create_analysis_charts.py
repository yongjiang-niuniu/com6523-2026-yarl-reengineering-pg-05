from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUT_DIR = Path("Submission/analysis")


def create_loc_chart() -> None:
    df = pd.read_csv(OUT_DIR / "loc_over_time.csv")
    df["date"] = pd.to_datetime(df["date"])

    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["source_lines"], marker="o", label="Source lines")
    plt.plot(df["date"], df["test_lines"], marker="o", label="Test lines")
    plt.plot(df["date"], df["total_lines"], marker="o", label="Total lines")

    plt.title("yarl LOC growth over selected releases")
    plt.xlabel("Date")
    plt.ylabel("Lines of code")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "loc_over_time.png", dpi=200)
    plt.close()


def create_commit_chart() -> None:
    df = pd.read_csv(OUT_DIR / "commits_by_month.csv")
    df["month"] = pd.to_datetime(df["month"])

    plt.figure(figsize=(12, 6))
    plt.bar(df["month"], df["commits"], width=20)

    plt.title("yarl commits by month")
    plt.xlabel("Month")
    plt.ylabel("Number of commits")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "commits_by_month.png", dpi=200)
    plt.close()


def main() -> None:
    create_loc_chart()
    create_commit_chart()
    print("Written:")
    print(OUT_DIR / "loc_over_time.png")
    print(OUT_DIR / "commits_by_month.png")


if __name__ == "__main__":
    main()
