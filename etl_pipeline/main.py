# This is the main script where you will orchestrate the ETL process, feel free to completely modify the files/structure as you see fit.
import logging
from etl_pipeline.api_client import POSTS_URL, USERS_URL, fetch_json
from etl_pipeline.load_to_database import load_to_sqlite
from etl_pipeline.transform_data import flatten_users, transform_posts

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    """Run the end-to-end Extract, Transform, and Load pipeline."""
    logger.info("ETL Job Started")

    # Extract phase
    logger.info("Extracting posts and users from JSONPlaceholder...")
    posts = fetch_json(POSTS_URL)
    users = fetch_json(USERS_URL)

    # Transform phase
    logger.info("Transforming and enriching records...")
    user_lookup = flatten_users(users)
    enriched_rows = transform_posts(posts, user_lookup)

    # Load phase
    logger.info("Loading records into SQLite...")
    load_to_sqlite(enriched_rows)

    logger.info("ETL Job Finished")


if __name__ == "__main__":
    run_pipeline()