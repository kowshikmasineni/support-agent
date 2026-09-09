from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_PATH = Path("data/evaluation/golden_set.csv")
OUTPUT_PATH = Path("data/evaluation/golden_set.csv")


# ============================================================
# LABEL TAXONOMY
# ============================================================

INTENTS = [
    "account_access",
    "billing_payment",
    "trip_issue",
    "fare_pricing",
    "driver_issue",
    "app_technical_issue",
    "refund_request",
    "cancellation",
    "lost_item",
    "safety_issue",
    "promotion_offer",
    "service_availability",
    "general_question",
    "other",
]

SEVERITIES = [
    "low",
    "medium",
    "high",
    "critical",
]

ACTIONS = [
    "provide_information",
    "troubleshoot",
    "explain_charge",
    "process_refund",
    "investigate_trip",
    "contact_driver",
    "escalate_safety",
    "cancel_trip",
    "recover_lost_item",
    "resolve_account",
    "other",
]


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def show_options(title, options):
    print(f"\n{title}:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")


def get_number(prompt, maximum):
    while True:
        value = input(prompt).strip()

        if value.isdigit():
            number = int(value)

            if 1 <= number <= maximum:
                return number

        print(f"Please enter a number between 1 and {maximum}.")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 7 - HAND LABEL GOLDEN EVALUATION SET")
    print("=" * 70)

    if not INPUT_PATH.exists():
        print(f"\nERROR: File not found: {INPUT_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)

    required_columns = [
        "example_id",
        "tweet_id",
        "author_id",
        "created_at",
        "text",
        "intent",
        "severity",
        "expected_action",
        "label_notes",
    ]

    for column in required_columns:
        if column not in df.columns:
            print(f"\nERROR: Missing column: {column}")
            return

    total = len(df)

    # --------------------------------------------------------
    # Find first unlabeled example
    # --------------------------------------------------------

    for index in df.index:

        intent_value = str(df.at[index, "intent"]).strip()
        severity_value = str(df.at[index, "severity"]).strip()
        action_value = str(df.at[index, "expected_action"]).strip()

        # Skip already completed rows
        if (
            intent_value
            and intent_value != "nan"
            and severity_value
            and severity_value != "nan"
            and action_value
            and action_value != "nan"
        ):
            continue

        example_number = list(df.index).index(index) + 1

        print("\n" + "=" * 70)
        print(f"EXAMPLE {example_number} / {total}")
        print("=" * 70)

        print(f"\nExample ID : {df.at[index, 'example_id']}")
        print(f"Tweet ID   : {df.at[index, 'tweet_id']}")

        print("\nCUSTOMER MESSAGE")
        print("-" * 70)
        print(str(df.at[index, "text"]))
        print("-" * 70)

        # ----------------------------------------------------
        # Show compact instructions
        # ----------------------------------------------------

        print("\nEnter labels using:")
        print("INTENT, SEVERITY, ACTION")
        print("Example: 2,2,3")

        show_options("INTENT", INTENTS)
        show_options("SEVERITY", SEVERITIES)
        show_options("EXPECTED ACTION", ACTIONS)

        # ----------------------------------------------------
        # Get all 3 labels in one line
        # ----------------------------------------------------

        while True:

            answer = input(
                "\nEnter labels (intent,severity,action): "
            ).strip()

            parts = [x.strip() for x in answer.split(",")]

            if len(parts) != 3:
                print("Invalid format. Example: 2,2,3")
                continue

            if not all(x.isdigit() for x in parts):
                print("Use numbers only. Example: 2,2,3")
                continue

            intent_num = int(parts[0])
            severity_num = int(parts[1])
            action_num = int(parts[2])

            if not (1 <= intent_num <= len(INTENTS)):
                print("Invalid intent number.")
                continue

            if not (1 <= severity_num <= len(SEVERITIES)):
                print("Invalid severity number.")
                continue

            if not (1 <= action_num <= len(ACTIONS)):
                print("Invalid action number.")
                continue

            break

        intent = INTENTS[intent_num - 1]
        severity = SEVERITIES[severity_num - 1]
        expected_action = ACTIONS[action_num - 1]

        # ----------------------------------------------------
        # Label notes
        # ----------------------------------------------------

        print("\nLabel note (short reason, optional):")

        label_notes = input("> ").strip()

        if not label_notes:
            label_notes = "Manual label based on customer message."

        # ----------------------------------------------------
        # Save immediately
        # ----------------------------------------------------

        df.at[index, "intent"] = intent
        df.at[index, "severity"] = severity
        df.at[index, "expected_action"] = expected_action
        df.at[index, "label_notes"] = label_notes

        df.to_csv(OUTPUT_PATH, index=False)

        print("\n✓ Saved.")

        # ----------------------------------------------------
        # Progress
        # ----------------------------------------------------

        labeled = 0

        for i in df.index:

            i_intent = str(df.at[i, "intent"]).strip()
            i_severity = str(df.at[i, "severity"]).strip()
            i_action = str(df.at[i, "expected_action"]).strip()

            if (
                i_intent
                and i_intent != "nan"
                and i_severity
                and i_severity != "nan"
                and i_action
                and i_action != "nan"
            ):
                labeled += 1

        remaining = total - labeled

        print(f"Labeled   : {labeled}/{total}")
        print(f"Remaining : {remaining}")

        if remaining == 0:
            break

        # ----------------------------------------------------
        # Continue
        # ----------------------------------------------------

        answer = input(
            "\nContinue to next example? [Y/n]: "
        ).strip().lower()

        if answer == "n":
            break

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    labeled = 0

    for index in df.index:

        intent_value = str(df.at[index, "intent"]).strip()
        severity_value = str(df.at[index, "severity"]).strip()
        action_value = str(df.at[index, "expected_action"]).strip()

        if (
            intent_value
            and intent_value != "nan"
            and severity_value
            and severity_value != "nan"
            and action_value
            and action_value != "nan"
        ):
            labeled += 1

    print("\n" + "=" * 70)
    print("STEP 7 COMPLETE / PROGRESS SAVED")
    print("=" * 70)

    print(f"Labeled examples : {labeled}")
    print(f"Total examples   : {total}")
    print(f"Remaining        : {total - labeled}")
    print(f"Saved to         : {OUTPUT_PATH}")

    print("=" * 70)


if __name__ == "__main__":
    main()