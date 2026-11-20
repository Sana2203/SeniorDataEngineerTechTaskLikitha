import logging
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "blog_warehouse.db"
DEFAULT_SCHEMA_PATH = BASE_DIR / "sql" / "schema_setup.sql"

logger = logging.getLogger(__name__)


def load_to_sqlite(
    rows: list[dict],
    db_path: Path = DEFAULT_DB_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> None:
    """Create schema if needed and upsert enriched post records into SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text(encoding="utf-8")

    insert_sql = """
    INSERT OR REPLACE INTO l_enriched_posts (
        post_id, user_id, title, body, body_length, total_length_with_title,
        status, user_name, username, user_email, city, company_name
    ) VALUES (
        :post_id, :user_id, :title, :body, :body_length, :total_length_with_title,
        :status, :user_name, :username, :user_email, :city, :company_name
    );
    """

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.executemany(insert_sql, rows)
        conn.commit()

    logger.info("Loaded %s records into %s", len(rows), db_path)