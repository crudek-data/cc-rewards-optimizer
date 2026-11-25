from pathlib import Path

import duckdb


def get_spending_by_category(
    db_path: str | Path,
) -> dict[str, float]:
    """Calculate total spending grouped by transaction category."""

    connection = duckdb.connect(str(db_path), read_only=True)

    try:
        results = connection.execute(
            """
            SELECT
                category,
                SUM(amount) AS total_spending
            FROM transactions
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()

        return {
            category: float(total_spending)
            for category, total_spending in results
        }

    finally:
        connection.close()