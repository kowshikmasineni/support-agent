from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_PATH = Path(
    "data/processed/uber_support_clean.csv"
)

OUTPUT_PATH = Path(
    "data/evaluation/golden_set.csv"
)

SAMPLE_SIZE = 200
RANDOM_STATE = 42


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 6 - BUILD GOLDEN EVALUATION SET")
    print("=" * 70)

    if not INPUT_PATH.exists():
        print(f"\nERROR: Input file not found:")
        print(INPUT_PATH)
        return

    print(f"\nLoading:")
    print(INPUT_PATH)

    df = pd.read_csv(INPUT_PATH)

    print(f"Total records: {len(df):,}")

    # --------------------------------------------------------
    # Keep customer messages only
    # --------------------------------------------------------

    if "role" in df.columns:
        df = df[df["role"] == "customer"].copy()

    # --------------------------------------------------------
    # Remove empty messages
    # --------------------------------------------------------

    df["text"] = df["text"].fillna("").astype(str).str.strip()

    df = df[df["text"].str.len() > 0].copy()

    # --------------------------------------------------------
    # Remove duplicate messages
    # --------------------------------------------------------

    df = df.drop_duplicates(
        subset=["text"]
    )

    print(
        f"Unique customer messages available: "
        f"{len(df):,}"
    )

    if len(df) < SAMPLE_SIZE:
        print(
            f"\nERROR: Only {len(df)} usable messages "
            f"are available."
        )
        return

    # --------------------------------------------------------
    # Random reproducible sample
    # --------------------------------------------------------

    golden = df.sample(
        n=SAMPLE_SIZE,
        random_state=RANDOM_STATE
    ).copy()

    # --------------------------------------------------------
    # Keep useful columns
    # --------------------------------------------------------

    columns = [
        "tweet_id",
        "author_id",
        "created_at",
        "text",
    ]

    columns = [
        column
        for column in columns
        if column in golden.columns
    ]

    golden = golden[columns]

    # --------------------------------------------------------
    # Add manual-label columns
    # --------------------------------------------------------

    golden["intent"] = ""
    golden["severity"] = ""
    golden["expected_action"] = ""
    golden["label_notes"] = ""

    # --------------------------------------------------------
    # Sort by tweet ID for easier review
    # --------------------------------------------------------

    golden = golden.sort_values(
        "tweet_id"
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    golden.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("GOLDEN SET RESULTS")
    print("=" * 70)

    print(
        f"Examples selected : "
        f"{len(golden):,}"
    )

    print(
        f"Output file       : "
        f"{OUTPUT_PATH}"
    )

    print("\nManual labels to complete:")

    print("  intent")
    print("  severity")
    print("  expected_action")
    print("  label_notes")

    print("\n" + "=" * 70)
    print("STEP 6 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()