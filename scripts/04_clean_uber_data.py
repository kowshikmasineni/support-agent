from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_PATH = Path(
    "data/processed/uber_support_conversations.csv"
)

OUTPUT_PATH = Path(
    "data/processed/uber_support_clean.csv"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 4 - CLEAN UBER SUPPORT DATA")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: Check input
    # --------------------------------------------------------

    if not INPUT_PATH.exists():
        print("\nERROR: Input file not found:")
        print(INPUT_PATH)
        return

    print("\nInput file:")
    print(INPUT_PATH)

    # --------------------------------------------------------
    # STEP 2: Load data
    # --------------------------------------------------------

    print("\nLoading data...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Original rows: {len(df):,}")

    # --------------------------------------------------------
    # STEP 3: Keep required columns
    # --------------------------------------------------------

    required_columns = [
        "tweet_id",
        "author_id",
        "inbound",
        "created_at",
        "text",
        "response_tweet_id",
        "in_response_to_tweet_id",
        "role"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("\nERROR: Missing columns:")
        print(missing_columns)
        return

    df = df[required_columns].copy()

    # --------------------------------------------------------
    # STEP 4: Clean tweet IDs
    # --------------------------------------------------------

    id_columns = [
        "tweet_id",
        "response_tweet_id",
        "in_response_to_tweet_id"
    ]

    for column in id_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # --------------------------------------------------------
    # STEP 5: Clean author IDs
    # --------------------------------------------------------

    df["author_id"] = (
        df["author_id"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # STEP 6: Clean text
    # --------------------------------------------------------

    df["text"] = (
        df["text"]
        .fillna("")
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # --------------------------------------------------------
    # STEP 7: Remove rows without usable text
    # --------------------------------------------------------

    before_text_filter = len(df)

    df = df[df["text"].str.len() > 0].copy()

    removed_empty = (
        before_text_filter - len(df)
    )

    print(
        f"\nRemoved empty-text rows: "
        f"{removed_empty:,}"
    )

    # --------------------------------------------------------
    # STEP 8: Convert timestamp
    # --------------------------------------------------------

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce",
        utc=True
    )

    invalid_dates = df["created_at"].isna().sum()

    print(
        f"Invalid timestamps: "
        f"{invalid_dates:,}"
    )

    # Remove rows without valid timestamps
    df = df.dropna(
        subset=["created_at"]
    ).copy()

    # --------------------------------------------------------
    # STEP 9: Normalize inbound
    # --------------------------------------------------------

    df["inbound"] = (
        df["inbound"]
        .astype(str)
        .str.upper()
        .map(
            {
                "TRUE": True,
                "FALSE": False
            }
        )
    )

    # --------------------------------------------------------
    # STEP 10: Normalize role
    # --------------------------------------------------------

    df["role"] = (
        df["role"]
        .astype("string")
        .str.lower()
        .str.strip()
    )

    # Keep only customer/support messages
    df = df[
        df["role"].isin(
            ["customer", "support"]
        )
    ].copy()

    # --------------------------------------------------------
    # STEP 11: Remove duplicate tweets
    # --------------------------------------------------------

    before_dedup = len(df)

    df = df.drop_duplicates(
        subset=["tweet_id"],
        keep="first"
    ).copy()

    duplicates_removed = (
        before_dedup - len(df)
    )

    print(
        f"Duplicate tweets removed: "
        f"{duplicates_removed:,}"
    )

    # --------------------------------------------------------
    # STEP 12: Add useful text statistics
    # --------------------------------------------------------

    df["text_length"] = (
        df["text"]
        .str.len()
    )

    df["word_count"] = (
        df["text"]
        .str.split()
        .str.len()
    )

    # --------------------------------------------------------
    # STEP 13: Sort chronologically
    # --------------------------------------------------------

    df = df.sort_values(
        "created_at"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # STEP 14: Save cleaned dataset
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # STEP 15: Statistics
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CLEANING RESULTS")
    print("=" * 70)

    print(
        f"Final rows             : "
        f"{len(df):,}"
    )

    print(
        f"Customer messages      : "
        f"{(df['role'] == 'customer').sum():,}"
    )

    print(
        f"Support messages       : "
        f"{(df['role'] == 'support').sum():,}"
    )

    print(
        f"Unique authors         : "
        f"{df['author_id'].nunique():,}"
    )

    print(
        f"Average text length    : "
        f"{df['text_length'].mean():.2f}"
    )

    print(
        f"Average word count     : "
        f"{df['word_count'].mean():.2f}"
    )

    print(
        f"Date range             : "
        f"{df['created_at'].min()} "
        f"to "
        f"{df['created_at'].max()}"
    )

    print("\nRole distribution:")
    print(
        df["role"].value_counts()
    )

    print("\nSaved to:")
    print(OUTPUT_PATH)

    print("\n" + "=" * 70)
    print("STEP 4 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()