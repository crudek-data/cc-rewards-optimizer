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


def get_spending_by_merchant(
    db_path: str | Path,
) -> dict[str, float]:
    """Calculate total spending grouped by merchant."""

    connection = duckdb.connect(str(db_path), read_only=True)

    try:
        results = connection.execute(
            """
            SELECT
                description,
                SUM(amount) AS total_spending
            FROM transactions
            GROUP BY description
            ORDER BY total_spending DESC
            """
        ).fetchall()

        return {
            merchant: float(total_spending)
            for merchant, total_spending in results
        }

    finally:
        connection.close()


def get_monthly_spending(
    db_path: str | Path,
) -> dict[str, float]:
    """Calculate total spending grouped by calendar month."""

    connection = duckdb.connect(str(db_path), read_only=True)

    try:
        results = connection.execute(
            """
            SELECT
                DATE_TRUNC('month', transaction_date)::DATE AS month,
                SUM(amount) AS total_spending
            FROM transactions
            GROUP BY month
            ORDER BY month
            """
        ).fetchall()

        return {
            month.strftime("%Y-%m"): float(total_spending)
            for month, total_spending in results
        }

    finally:
        connection.close()


def get_annual_spending(
    db_path: str | Path,
) -> dict[int, float]:
    """Calculate total spending grouped by calendar year."""

    connection = duckdb.connect(str(db_path), read_only=True)

    try:
        results = connection.execute(
            """
            SELECT
                EXTRACT(YEAR FROM transaction_date)::INTEGER AS year,
                SUM(amount) AS total_spending
            FROM transactions
            GROUP BY year
            ORDER BY year
            """
        ).fetchall()

        return {
            year: float(total_spending)
            for year, total_spending in results
        }

    finally:
        connection.close()
