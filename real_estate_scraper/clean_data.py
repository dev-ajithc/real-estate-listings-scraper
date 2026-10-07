from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/listings_raw.csv")
OUTPUT_FILE = Path("data/listings_clean.csv")


def clean_data():
    df = pd.read_csv(INPUT_FILE)

    raw_count = len(df)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Normalize text fields
    text_columns = [
        "title",
        "status",
        "price_period",
        "property_type",
        "address",
        "city",
        "postal_code",
        "agent",
        "listing_url",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Convert numeric fields
    numeric_columns = [
        "price",
        "bedrooms",
        "bathrooms",
        "area_sqft",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Remove duplicate listing IDs
    before_id_dedup = len(df)

    df = df.drop_duplicates(
        subset=["listing_id"],
        keep="first",
    )

    duplicate_ids_removed = (
        before_id_dedup - len(df)
    )

    # Remove duplicate URLs
    before_url_dedup = len(df)

    df = df.drop_duplicates(
        subset=["listing_url"],
        keep="first",
    )

    duplicate_urls_removed = (
        before_url_dedup - len(df)
    )

    # Validate required fields
    required_fields = [
        "listing_id",
        "price",
        "address",
        "listing_url",
    ]

    before_validation = len(df)

    df = df.dropna(
        subset=required_fields
    )

    invalid_records_removed = (
        before_validation - len(df)
    )

    # Keep sensible values
    df = df[
        (df["price"] > 0)
        & (df["area_sqft"] > 0)
    ]

    # Sort
    df = df.sort_values(
        by=["city", "price"],
        ascending=[True, True],
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\nREAL ESTATE DATA QUALITY SUMMARY")
    print("=" * 50)
    print(f"Raw records:              {raw_count}")
    print(f"Duplicate IDs removed:    {duplicate_ids_removed}")
    print(f"Duplicate URLs removed:   {duplicate_urls_removed}")
    print(f"Invalid records removed:  {invalid_records_removed}")
    print(f"Final records:            {len(df)}")
    print(f"Output:                   {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_data()
