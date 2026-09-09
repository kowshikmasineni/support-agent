from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/raw/twcs.csv")


def main():

    print("=" * 70)
    print("HIVER SDE ASSESSMENT")
    print("DATASET INSPECTION")
    print("=" * 70)

    # Check dataset exists
    if not DATA_PATH.exists():
        print("\nERROR: Dataset not found.")
        print(f"Expected location: {DATA_PATH}")
        return

    print(f"\nDataset found: {DATA_PATH}")

    # Check file size
    file_size = DATA_PATH.stat().st_size

    print(f"File size: {file_size:,} bytes")

    if file_size == 0:
        print("\nERROR: twcs.csv is empty.")
        return

    # Load dataset
    print("\nLoading dataset...")
    print("Please wait...")

    df = pd.read_csv(DATA_PATH)

    print("\nDataset loaded successfully.")

    # Shape
    print("\n" + "=" * 70)
    print("DATASET SHAPE")
    print("=" * 70)

    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]}")

    # Columns
    print("\n" + "=" * 70)
    print("COLUMNS")
    print("=" * 70)

    for number, column in enumerate(df.columns, start=1):
        print(f"{number}. {column}")

    # Data types
    print("\n" + "=" * 70)
    print("DATA TYPES")
    print("=" * 70)

    print(df.dtypes)

    # Missing values
    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)

    missing = df.isnull().sum()

    for column, count in missing.items():
        percentage = count / len(df) * 100

        print(
            f"{column:30} "
            f"{count:10,} "
            f"({percentage:6.2f}%)"
        )

    # Inbound / outbound
    if "inbound" in df.columns:

        print("\n" + "=" * 70)
        print("INBOUND / OUTBOUND DISTRIBUTION")
        print("=" * 70)

        print(df["inbound"].value_counts(dropna=False))

    # Text statistics
    if "text" in df.columns:

        print("\n" + "=" * 70)
        print("TEXT STATISTICS")
        print("=" * 70)

        text_lengths = (
            df["text"]
            .fillna("")
            .astype(str)
            .str.len()
        )

        print(
            f"Average text length : "
            f"{text_lengths.mean():.2f}"
        )

        print(
            f"Minimum text length : "
            f"{text_lengths.min()}"
        )

        print(
            f"Maximum text length : "
            f"{text_lengths.max()}"
        )

    # First records
    print("\n" + "=" * 70)
    print("FIRST 5 RECORDS")
    print("=" * 70)

    print(df.head(5).to_string(index=False))

    print("\n" + "=" * 70)
    print("INSPECTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()