from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")
OUTPUT_PATH = Path("data/processed/support_accounts.csv")


def main():

    print("=" * 70)
    print("STEP 2 - FIND SUPPORT ACCOUNTS")
    print("=" * 70)

    # --------------------------------------------------------
    # Check dataset
    # --------------------------------------------------------

    if not DATA_PATH.exists():
        print(f"ERROR: Dataset not found: {DATA_PATH}")
        return

    print(f"\nLoading: {DATA_PATH}")
    print("Please wait...")

    # We only need these columns for this analysis
    df = pd.read_csv(
        DATA_PATH,
        usecols=[
            "author_id",
            "inbound",
            "text"
        ]
    )

    print(f"\nLoaded {len(df):,} tweets.")

    # --------------------------------------------------------
    # Find outbound tweets
    # --------------------------------------------------------

    print("\nFinding support-account tweets...")

    outbound = df[df["inbound"] == False].copy()

    print(
        f"Outbound tweets: "
        f"{len(outbound):,}"
    )

    # --------------------------------------------------------
    # Count tweets by author
    # --------------------------------------------------------

    account_counts = (
        outbound
        .groupby("author_id")
        .agg(
            outbound_tweets=("author_id", "size"),
            unique_messages=("text", "nunique")
        )
        .reset_index()
        .sort_values(
            "outbound_tweets",
            ascending=False
        )
    )

    # --------------------------------------------------------
    # Display top accounts
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TOP SUPPORT ACCOUNTS")
    print("=" * 70)

    print(
        account_counts.head(50).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    account_counts.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n" + "=" * 70)
    print("RESULT SAVED")
    print("=" * 70)

    print(f"Output: {OUTPUT_PATH}")

    print("\nTop 10 accounts:")

    for _, row in account_counts.head(10).iterrows():

        print(
            f"{row['author_id']:30} "
            f"{row['outbound_tweets']:10,} tweets"
        )

    print("\n" + "=" * 70)
    print("STEP 2 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()