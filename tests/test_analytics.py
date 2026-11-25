
import duckdb

from cc_rewards_optimizer.analytics import get_spending_by_category


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