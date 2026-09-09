from pathlib import Path
import pandas as pd


GOLDEN_PATH = Path("data/evaluation/golden_set.csv")
OUTPUT_DIR = Path("evaluation")

TRIVIAL_PATH = OUTPUT_DIR / "predictions_trivial.csv"
SIMPLE_PATH = OUTPUT_DIR / "predictions_simple.csv"


def trivial_baseline(df):
    """
    Trivial baseline:
    Always predict the most common label for each field.
    """

    intent = df["intent"].mode()[0]
    severity = df["severity"].mode()[0]
    action = df["expected_action"].mode()[0]

    result = pd.DataFrame({
        "example_id": df["example_id"],
        "intent": intent,
        "severity": severity,
        "expected_action": action,
    })

    return result


def simple_intent(text):
    """
    Simple keyword-based intent classifier.
    """

    text = str(text).lower()

    if any(x in text for x in [
        "refund",
        "refunded",
        "money back",
        "refund me",
    ]):
        return "refund_request"

    if any(x in text for x in [
        "charged",
        "charge",
        "payment",
        "paid",
        "card",
        "billing",
    ]):
        return "billing_payment"

    if any(x in text for x in [
        "cancel",
        "cancellation",
    ]):
        return "cancellation"

    if any(x in text for x in [
        "lost",
        "left my",
        "forgot",
        "missing item",
        "phone",
        "wallet",
    ]):
        return "lost_item"

    if any(x in text for x in [
        "driver",
        "driver cancelled",
        "driver rude",
        "driver behavior",
    ]):
        return "driver_issue"

    if any(x in text for x in [
        "danger",
        "dangerous",
        "unsafe",
        "safety",
        "accident",
        "threat",
    ]):
        return "safety_issue"

    if any(x in text for x in [
        "app",
        "application",
        "error",
        "crash",
        "login",
        "doesn't work",
        "not working",
    ]):
        return "app_technical_issue"

    if any(x in text for x in [
        "fare",
        "price",
        "pricing",
        "cost",
        "expensive",
    ]):
        return "fare_pricing"

    if any(x in text for x in [
        "promo",
        "promotion",
        "coupon",
        "offer",
        "discount",
    ]):
        return "promotion_offer"

    if any(x in text for x in [
        "available",
        "availability",
        "service",
        "area",
    ]):
        return "service_availability"

    if any(x in text for x in [
        "account",
        "password",
        "verification",
        "verify",
        "access",
    ]):
        return "account_access"

    if any(x in text for x in [
        "trip",
        "ride",
        "pickup",
        "dropoff",
        "route",
    ]):
        return "trip_issue"

    return "general_question"


def simple_action(intent):
    """
    Deterministic action mapping for the simple baseline.
    """

    mapping = {
        "account_access": "resolve_account",
        "billing_payment": "explain_charge",
        "trip_issue": "investigate_trip",
        "fare_pricing": "provide_information",
        "driver_issue": "contact_driver",
        "app_technical_issue": "troubleshoot",
        "refund_request": "process_refund",
        "cancellation": "cancel_trip",
        "lost_item": "recover_lost_item",
        "safety_issue": "escalate_safety",
        "promotion_offer": "provide_information",
        "service_availability": "provide_information",
        "general_question": "provide_information",
        "other": "other",
    }

    return mapping.get(intent, "other")


def simple_severity(text):
    """
    Simple severity rules.
    """

    text = str(text).lower()

    critical_words = [
        "rape",
        "assault",
        "weapon",
        "kidnap",
        "threatened",
        "emergency",
    ]

    high_words = [
        "danger",
        "dangerous",
        "unsafe",
        "accident",
        "injured",
        "stolen",
        "fraud",
    ]

    medium_words = [
        "angry",
        "annoyed",
        "failed",
        "error",
        "charged",
        "cancelled",
    ]

    if any(x in text for x in critical_words):
        return "critical"

    if any(x in text for x in high_words):
        return "high"

    if any(x in text for x in medium_words):
        return "medium"

    return "low"


def simple_baseline(df):

    intents = []
    severities = []
    actions = []

    for text in df["text"]:

        intent = simple_intent(text)

        intents.append(intent)
        severities.append(simple_severity(text))
        actions.append(simple_action(intent))

    return pd.DataFrame({
        "example_id": df["example_id"],
        "intent": intents,
        "severity": severities,
        "expected_action": actions,
    })


def main():

    print("=" * 70)
    print("STEP 9 - BASELINES")
    print("=" * 70)

    if not GOLDEN_PATH.exists():
        raise FileNotFoundError(
            f"Golden set not found: {GOLDEN_PATH}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(GOLDEN_PATH)

    print(f"\nGolden examples: {len(df)}")

    # --------------------------------------------------------
    # Trivial baseline
    # --------------------------------------------------------

    trivial = trivial_baseline(df)

    trivial.to_csv(
        TRIVIAL_PATH,
        index=False,
    )

    print("\nTrivial baseline created:")
    print(TRIVIAL_PATH)

    # --------------------------------------------------------
    # Simple baseline
    # --------------------------------------------------------

    simple = simple_baseline(df)

    simple.to_csv(
        SIMPLE_PATH,
        index=False,
    )

    print("\nSimple baseline created:")
    print(SIMPLE_PATH)

    print("\n" + "=" * 70)
    print("STEP 9 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()