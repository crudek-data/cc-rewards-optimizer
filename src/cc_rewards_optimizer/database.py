import csv
import hashlib
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

import duckdb


def initialize_database(db_path: str | Path) -> None:
    """Create the DuckDB database and initialize its tables."""

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(str(db_path))

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id VARCHAR PRIMARY KEY,
                transaction_date DATE NOT NULL,
                description VARCHAR NOT NULL,
                category VARCHAR NOT NULL,
                amount DECIMAL(12, 2) NOT NULL,
                card_used VARCHAR
            )
            """
        )
    finally:
        connection.close()


def load_transactions_from_csv(
    csv_path: str | Path,
    db_path: str | Path,
) -> int:
    """Load transactions from a CSV file into DuckDB.

    Returns the number of newly inserted transactions.
    """

    csv_path = Path(csv_path)
    db_path = Path(db_path)

    # Track repeated identical transactions separately.
    occurrences = defaultdict(int)
    transactions = []

    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            transaction_date = date.fromisoformat(row["transaction_date"])
            description = row["description"].strip()
            category = row["category"].strip()
            amount = Decimal(row["amount"]).quantize(Decimal("0.01"))

            # Create a repeatable ID from the transaction details.
            signature = (
                f"{transaction_date}|{description}|{category}|{amount}"
            )
            occurrence = occurrences[signature]
            occurrences[signature] += 1

            transaction_id = hashlib.sha256(
                f"{signature}|{occurrence}".encode("utf-8")
            ).hexdigest()

            transactions.append(
                (
                    transaction_id,
                    transaction_date,
                    description,
                    category,
                    amount,
                    row.get("card_used") or None,
                )
            )

    connection = duckdb.connect(str(db_path))

    try:
        before_count = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        connection.executemany(
            """
            INSERT INTO transactions (
                transaction_id,
                transaction_date,
                description,
                category,
                amount,
                card_used
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (transaction_id) DO NOTHING
            """,
            transactions,
        )

        after_count = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]

        return after_count - before_count

    finally:
        connection.close()