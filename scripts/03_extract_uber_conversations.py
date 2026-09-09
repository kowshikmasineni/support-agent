from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = Path("data/raw/twcs.csv")

OUTPUT_PATH = Path(
    "data/processed/uber_support_conversations.csv"
)

SUPPORT_ACCOUNT = "Uber_Support"


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 3 - EXTRACT UBER SUPPORT CONVERSATIONS")
    print("=" * 70)

    if not DATA_PATH.exists():
        print(f"\nERROR: Dataset not found:")
        print(DATA_PATH)
        return

    print("\nSupport account:")
    print(SUPPORT_ACCOUNT)

    print("\nDataset:")
    print(DATA_PATH)

    # --------------------------------------------------------
    # STEP 1: Find all Uber Support tweets
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 1 - FINDING SUPPORT TWEETS")
    print("=" * 70)

    support_ids = set()

    chunk_number = 0

    for chunk in pd.read_csv(
        DATA_PATH,
        usecols=[
            "tweet_id",
            "author_id"
        ],
        chunksize=100_000
    ):

        chunk_number += 1

        matches = chunk[
            chunk["author_id"] == SUPPORT_ACCOUNT
        ]

        support_ids.update(
            matches["tweet_id"]
            .dropna()
            .astype(str)
        )

        print(
            f"Processed chunk {chunk_number} | "
            f"Uber tweets found: {len(support_ids):,}"
        )

    print(
        f"\nTotal Uber Support tweets: "
        f"{len(support_ids):,}"
    )

    if len(support_ids) == 0:
        print("\nERROR: No Uber Support tweets found.")
        return

    # --------------------------------------------------------
    # STEP 2: Find directly connected tweets
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 2 - FINDING CONNECTED CUSTOMER TWEETS")
    print("=" * 70)

    connected_ids = set(support_ids)

    chunk_number = 0

    for chunk in pd.read_csv(
        DATA_PATH,
        usecols=[
            "tweet_id",
            "in_response_to_tweet_id",
            "response_tweet_id"
        ],
        chunksize=100_000
    ):

        chunk_number += 1

                # Normalize IDs to strings so they match support_ids
        chunk["tweet_id"] = (
            chunk["tweet_id"]
            .astype(str)
        )

        chunk["in_response_to_tweet_id"] = (
            chunk["in_response_to_tweet_id"]
            .astype("Int64")
            .astype("string")
        )

        # ----------------------------------------------------
        # Customer tweet responding to Uber
        # ----------------------------------------------------

        mask_customer = (
            chunk["in_response_to_tweet_id"]
            .isin(support_ids)
        )

        customer_ids = (
            chunk.loc[
                mask_customer,
                "tweet_id"
            ]
            .dropna()
            .astype(str)
            .tolist()
        )

        connected_ids.update(customer_ids)
        customer_ids = (
            chunk.loc[
                mask_customer,
                "tweet_id"
            ]
            .dropna()
            .astype(str)
            .tolist()
        )

        

        connected_ids.update(customer_ids)

        # ----------------------------------------------------
        # Uber response to another tweet
        # ----------------------------------------------------

        parent_ids = (
            chunk.loc[
                chunk["tweet_id"].isin(support_ids),
                "in_response_to_tweet_id"
            ]
            .dropna()
            .astype(str)
            .tolist()
        )

        connected_ids.update(parent_ids)

        print(
            f"Processed chunk {chunk_number} | "
            f"Connected tweets: {len(connected_ids):,}"
        )

    print(
        f"\nTotal directly connected tweets: "
        f"{len(connected_ids):,}"
    )

    # --------------------------------------------------------
    # STEP 3: Extract complete records
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("STEP 3 - EXTRACTING CONVERSATION RECORDS")
    print("=" * 70)

    columns = [
        "tweet_id",
        "author_id",
        "inbound",
        "created_at",
        "text",
        "response_tweet_id",
        "in_response_to_tweet_id"
    ]

    conversation_parts = []

    chunk_number = 0

    for chunk in pd.read_csv(
        DATA_PATH,
        usecols=columns,
        chunksize=100_000
    ):

        chunk_number += 1

        chunk["tweet_id"] = (
            chunk["tweet_id"]
            .astype(str)
        )

        matches = chunk[
            chunk["tweet_id"].isin(connected_ids)
        ]

        if not matches.empty:
            conversation_parts.append(matches)

        print(
            f"Processed chunk {chunk_number}"
        )

    if not conversation_parts:
        print("\nERROR: No conversation records found.")
        return

    conversations = pd.concat(
        conversation_parts,
        ignore_index=True
    )

    # --------------------------------------------------------
    # STEP 4: Sort conversations
    # --------------------------------------------------------

    print("\nSorting conversations...")

    conversations["created_at"] = pd.to_datetime(
        conversations["created_at"],
        errors="coerce"
    )

    conversations = conversations.sort_values(
        "created_at"
    )

    # --------------------------------------------------------
    # STEP 5: Add message role
    # --------------------------------------------------------

    conversations["role"] = conversations[
        "inbound"
    ].map(
        {
            True: "customer",
            False: "support"
        }
    )

    # --------------------------------------------------------
    # STEP 6: Save
    # --------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conversations.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("EXTRACTION RESULTS")
    print("=" * 70)

    print(
        f"Total extracted messages : "
        f"{len(conversations):,}"
    )

    print(
        f"Customer messages        : "
        f"{(conversations['role'] == 'customer').sum():,}"
    )

    print(
        f"Support messages         : "
        f"{(conversations['role'] == 'support').sum():,}"
    )

    print(
        f"Unique authors           : "
        f"{conversations['author_id'].nunique():,}"
    )

    print(
        f"Date range               : "
        f"{conversations['created_at'].min()} "
        f"to "
        f"{conversations['created_at'].max()}"
    )

    print("\nSaved to:")

    print(OUTPUT_PATH)

    print("\n" + "=" * 70)
    print("STEP 3 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()