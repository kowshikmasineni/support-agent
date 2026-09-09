from pathlib import Path
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


# ============================================================
# CONFIGURATION
# ============================================================

GOLDEN_PATH = Path("data/evaluation/golden_set.csv")
PREDICTIONS_PATH = Path("evaluation/predictions.csv")
RESULTS_PATH = Path("evaluation/results.csv")
CONFUSION_PATH = Path("evaluation/confusion_matrix.csv")


# ============================================================
# REQUIRED COLUMNS
# ============================================================

LABEL_COLUMNS = [
    "intent",
    "severity",
    "expected_action",
]


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print("=" * 70)
    print("STEP 8 - EVALUATION HARNESS")
    print("=" * 70)

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not GOLDEN_PATH.exists():
        print(f"\nERROR: Golden set not found:")
        print(GOLDEN_PATH)
        return

    if not PREDICTIONS_PATH.exists():
        print(f"\nERROR: Predictions file not found:")
        print(PREDICTIONS_PATH)
        print(
            "\nCreate evaluation/predictions.csv with these columns:"
        )
        print("example_id, intent, severity, expected_action")
        return

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------

    gold = pd.read_csv(GOLDEN_PATH)
    pred = pd.read_csv(PREDICTIONS_PATH)

    print(f"\nGolden examples: {len(gold)}")
    print(f"Prediction examples: {len(pred)}")

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    required_gold = ["example_id"] + LABEL_COLUMNS
    required_pred = ["example_id"] + LABEL_COLUMNS

    for column in required_gold:
        if column not in gold.columns:
            raise ValueError(
                f"Golden set missing column: {column}"
            )

    for column in required_pred:
        if column not in pred.columns:
            raise ValueError(
                f"Predictions missing column: {column}"
            )

    # --------------------------------------------------------
    # Merge
    # --------------------------------------------------------

    df = gold[
        ["example_id"] + LABEL_COLUMNS
    ].merge(
        pred[
            ["example_id"] + LABEL_COLUMNS
        ],
        on="example_id",
        suffixes=("_gold", "_pred"),
        how="inner",
    )

    print(f"Matched examples: {len(df)}")

    if len(df) == 0:
        raise ValueError(
            "No matching example_id values were found."
        )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    results = []

    for column in LABEL_COLUMNS:

        accuracy = accuracy_score(
            df[f"{column}_gold"],
            df[f"{column}_pred"],
        )

        results.append(
            {
                "metric": f"{column}_accuracy",
                "value": accuracy,
            }
        )

        print(
            f"\n{column} accuracy: "
            f"{accuracy:.4f}"
        )

    # --------------------------------------------------------
    # Exact match
    # --------------------------------------------------------

    df["exact_match"] = (
        (df["intent_gold"] == df["intent_pred"])
        &
        (df["severity_gold"] == df["severity_pred"])
        &
        (
            df["expected_action_gold"]
            == df["expected_action_pred"]
        )
    )

    exact_match_accuracy = df["exact_match"].mean()

    results.append(
        {
            "metric": "overall_exact_match_accuracy",
            "value": exact_match_accuracy,
        }
    )

    print(
        f"\nOverall exact-match accuracy: "
        f"{exact_match_accuracy:.4f}"
    )

    # --------------------------------------------------------
    # Per-intent report
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("INTENT CLASSIFICATION REPORT")
    print("=" * 70)

    report = classification_report(
        df["intent_gold"],
        df["intent_pred"],
        zero_division=0,
        output_dict=True,
    )

    report_rows = []

    for label, values in report.items():

        if isinstance(values, dict):

            report_rows.append(
                {
                    "label": label,
                    "precision": values.get("precision"),
                    "recall": values.get("recall"),
                    "f1": values.get("f1-score"),
                    "support": values.get("support"),
                }
            )

    report_df = pd.DataFrame(report_rows)

    print(
        report_df.to_string(index=False)
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    labels = sorted(
        set(df["intent_gold"])
        | set(df["intent_pred"])
    )

    matrix = confusion_matrix(
        df["intent_gold"],
        df["intent_pred"],
        labels=labels,
    )

    confusion_df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels,
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        RESULTS_PATH,
        index=False,
    )

    confusion_df.to_csv(
        CONFUSION_PATH,
    )

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(f"\nResults saved to:")
    print(RESULTS_PATH)

    print("\nConfusion matrix saved to:")
    print(CONFUSION_PATH)


if __name__ == "__main__":
    main()