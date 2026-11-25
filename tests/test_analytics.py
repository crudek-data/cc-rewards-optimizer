
import duckdb
from cc_rewards_optimizer.analytics import (
    get_spending_by_category,
    get_spending_by_merchant,
    get_monthly_spending,
    get_annual_spending,
)

def test_get_spending_by_category(tmp_path):
    """Test category spending totals from a DuckDB database."""

    db_path = tmp_path / "test.duckdb"

    connection = duckdb.connect(str(db_path))

    try:
        connection.execute(
            """
            CREATE TABLE transactions (
                category VARCHAR,
                amount DECIMAL(12, 2)
            )
            """
        )

        connection.execute(
            """
            INSERT INTO transactions VALUES
                ('groceries', 100.00),
                ('groceries', 50.00),
                ('gas', 40.00)
            """
        )
    finally:
        connection.close()

    result = get_spending_by_category(db_path)

    assert result == {
        "gas": 40.0,
        "groceries": 150.0,
    }


def test_get_spending_by_merchant(tmp_path):
    """Test spending grouped by merchant."""

    db_path = tmp_path / "merchant_test.duckdb"

    connection = duckdb.connect(str(db_path))

    try:
        connection.execute(
            """
            CREATE TABLE transactions (
                description VARCHAR,
                amount DECIMAL(12, 2)
            )
            """
        )

        connection.execute(
            """
            INSERT INTO transactions VALUES
                ('Kroger', 100.00),
                ('Kroger', 50.00),
                ('Amazon', 40.00)
            """
        )
    finally:
        connection.close()

    result = get_spending_by_merchant(db_path)

    assert result == {
        "Kroger": 150.0,
        "Amazon": 40.0,
    }


def test_get_monthly_spending(tmp_path):
    """Test spending grouped by calendar month."""

    db_path = tmp_path / "monthly_test.duckdb"

    connection = duckdb.connect(str(db_path))

    try:
        connection.execute(
            """
            CREATE TABLE transactions (
                transaction_date DATE,
                amount DECIMAL(12, 2)
            )
            """
        )

        connection.execute(
            """
            INSERT INTO transactions VALUES
                ('2026-01-05', 100.00),
                ('2026-01-15', 50.00),
                ('2026-02-10', 40.00)
            """
        )
    finally:
        connection.close()

    result = get_monthly_spending(db_path)

    assert result == {
        "2026-01": 150.0,
        "2026-02": 40.0,
    }


def test_get_annual_spending(tmp_path):
    """Test spending grouped by calendar year."""

    db_path = tmp_path / "annual_test.duckdb"

    connection = duckdb.connect(str(db_path))

    try:
        connection.execute(
            """
            CREATE TABLE transactions (
                transaction_date DATE,
                amount DECIMAL(12, 2)
            )
            """
        )

        connection.execute(
            """
            INSERT INTO transactions VALUES
                ('2026-01-05', 100.00),
                ('2026-06-15', 50.00),
                ('2027-02-10', 40.00)
            """
        )
    finally:
        connection.close()

    result = get_annual_spending(db_path)

    assert result == {
        2026: 150.0,
        2027: 40.0,
    }
