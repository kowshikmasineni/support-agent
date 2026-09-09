from pathlib import Path
import pandas as pd
import re


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_PATH = Path(
    "data/processed/uber_support_clean.csv"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 5 - DISCOVER UBER CUSTOMER INTENTS")
    print("=" * 70)

    if not INPUT_PATH.exists():
        print("\nERROR: Clean dataset not found:")
        print(INPUT_PATH)
        return

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_PATH)

    print(f"\nTotal messages: {len(df):,}")

    # Only customer messages
    customers = df[
        df["role"] == "customer"
    ].copy()

    print(
        f"Customer messages: "
        f"{len(customers):,}"
    )

    # --------------------------------------------------------
    # Basic keyword analysis
    # --------------------------------------------------------

    text = (
        customers["text"]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    intent_keywords = {
        "fare_or_charge": [
            "charge",
            "charged",
            "fare",
            "price",
            "cost",
            "fee",
            "payment",
            "refund",
            "money"
        ],

        "ride_or_trip_issue": [
            "ride",
            "trip",
            "driver",
            "pickup",
            "drop",
            "destination",
            "cancel",
            "cancelled",
            "canceled"
        ],

        "account_issue": [
            "account",
            "login",
            "password",
            "phone",
            "email",
            "sign in",
            "logged"
        ],

        "app_or_technical_issue": [
            "app",
            "website",
            "error",
            "crash",
            "bug",
            "not working",
            "unable",
            "cannot"
        ],

        "lost_item": [
            "lost",
            "left",
            "forgot",
            "missing",
            "item",
            "phone",
            "wallet",
            "bag"
        ],

        "driver_issue": [
            "driver",
            "rude",
            "behavior",
            "behaviour",
            "unsafe",
            "driving",
            "professional"
        ],

        "promotion_or_discount": [
            "promo",
            "promotion",
            "coupon",
            "discount",
            "code",
            "offer",
            "credit"
        ],

        "waiting_or_delay": [
            "wait",
            "waiting",
            "late",
            "delay",
            "delayed",
            "arrive",
            "arrival"
        ]
    }

    print("\n" + "=" * 70)
    print("KEYWORD DISTRIBUTION")
    print("=" * 70)

    results = []

    for intent, keywords in intent_keywords.items():

        pattern = "|".join(
            re.escape(keyword)
            for keyword in keywords
        )

        count = text.str.contains(
            pattern,
            regex=True,
            na=False
        ).sum()

        results.append(
            (intent, count)
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for intent, count in results:

        percentage = (
            count / len(customers) * 100
        )

        print(
            f"{intent:<28} "
            f"{count:>8,} "
            f"({percentage:>5.2f}%)"
        )

    # --------------------------------------------------------
    # Show example customer messages
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("CUSTOMER MESSAGE EXAMPLES")
    print("=" * 70)

    for intent, keywords in results:

        pattern = "|".join(
            re.escape(keyword)
            for keyword in intent_keywords[intent]
        )

        matches = customers[
            text.str.contains(
                pattern,
                regex=True,
                na=False
            )
        ]

        print("\n" + "-" * 70)
        print(intent.upper())
        print("-" * 70)

        examples = (
            matches["text"]
            .drop_duplicates()
            .head(5)
        )

        for i, message in enumerate(
            examples,
            start=1
        ):
            print(
                f"{i}. {message[:300]}"
            )

    print("\n" + "=" * 70)
    print("STEP 5 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()