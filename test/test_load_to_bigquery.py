import sqlite3
from pathlib import Path
from etl_pipeline.load_to_database import load_to_sqlite


def test_load_to_sqlite(tmp_path: Path):
    schema_path = Path(__file__).resolve().parent.parent / "sql" / "schema_setup.sql"
    db_path = tmp_path / "test_warehouse.db"

    sample_rows = [
        {
            "post_id": 1,
            "user_id": 1,
            "title": "Sample Title",
            "body": "Sample Body",
            "body_length": 11,
            "total_length_with_title": 23,
            "status": "concise",
            "user_name": "Test User",
            "username": "testuser",
            "user_email": "test@example.com",
            "city": "Hyderabad",
            "company_name": "Test Org",
        }
    ]

    load_to_sqlite(sample_rows, db_path=db_path, schema_path=schema_path)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM l_enriched_posts").fetchone()[0]

    assert count == 1# Put your unit tests here