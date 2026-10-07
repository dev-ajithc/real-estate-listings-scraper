from pathlib import Path

import pandas as pd


DATA_FILE = Path("data/listings_clean.csv")
REPORT_FILE = Path("reports/data_quality_report.md")


def generate_report():
    df = pd.read_csv(DATA_FILE)

    total_records = len(df)

    lines = [
        "# Real Estate Data Quality Report",
        "",
        "## Dataset Summary",
        "",
        f"- Total records: **{total_records:,}**",
        f"- Columns: **{len(df.columns)}**",
        "",
        "## Field Completeness",
        "",
        "| Field | Filled | Completeness |",
        "|---|---:|---:|",
    ]

    for column in df.columns:
        filled = df[column].notna().sum()

        percentage = (
            filled / total_records * 100
            if total_records
            else 0
        )

        lines.append(
            f"| {column} | {filled:,} | "
            f"{percentage:.1f}% |"
        )

    duplicate_ids = (
        df["listing_id"]
        .duplicated()
        .sum()
    )

    duplicate_urls = (
        df["listing_url"]
        .duplicated()
        .sum()
    )

    lines.extend(
        [
            "",
            "## Validation Checks",
            "",
            f"- Duplicate listing IDs: **{duplicate_ids}**",
            f"- Duplicate listing URLs: **{duplicate_urls}**",
            f"- Missing listing IDs: **{df['listing_id'].isna().sum()}**",
            f"- Missing prices: **{df['price'].isna().sum()}**",
            f"- Missing addresses: **{df['address'].isna().sum()}**",
            f"- Missing listing URLs: **{df['listing_url'].isna().sum()}**",
            "",
            "## Price Summary",
            "",
            f"- Minimum price: **{df['price'].min():,.2f}**",
            f"- Maximum price: **{df['price'].max():,.2f}**",
            f"- Average price: **{df['price'].mean():,.2f}**",
        ]
    )

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Report written to {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
