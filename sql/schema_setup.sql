-- SQL queries to set up schemas in BigQuery
CREATE TABLE IF NOT EXISTS l_enriched_posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    body_length INTEGER NOT NULL,
    total_length_with_title INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('concise', 'lengthy')),
    user_name TEXT,
    username TEXT,
    user_email TEXT,
    city TEXT,
    company_name TEXT
);