-- 1. Top 5 users posting the longest posts (excluding title), ranked by longest single post body
SELECT
    user_id,
    user_name,
    username,
    MAX(body_length) AS max_post_body_length
FROM l_enriched_posts
GROUP BY user_id, user_name, username
ORDER BY max_post_body_length DESC
LIMIT 5;

-- 2. Average post length (including title) for each of those top 5 users
WITH top_5_users AS (
    SELECT
        user_id
    FROM l_enriched_posts
    GROUP BY user_id
    ORDER BY MAX(body_length) DESC
    LIMIT 5
)
SELECT
    p.user_id,
    p.user_name,
    p.username,
    ROUND(AVG(p.total_length_with_title), 2) AS avg_post_length_incl_title,
    COUNT(*) AS total_posts
FROM l_enriched_posts p
JOIN top_5_users t ON p.user_id = t.user_id
GROUP BY p.user_id, p.user_name, p.username
ORDER BY avg_post_length_incl_title DESC;

-- 3. Day of the week when the most 'lengthy' posts are created
-- Using post_id as day offset from UNIX epoch ('1970-01-01')
SELECT
    CASE strftime('%w', date('1970-01-01', '+' || post_id || ' days'))
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS day_of_week,
    COUNT(*) AS lengthy_post_count
FROM l_enriched_posts
WHERE status = 'lengthy'
GROUP BY day_of_week
ORDER BY lengthy_post_count DESC;-- Write SQL queries to answer these questions using the data you have loaded into BigQuery:
-- 1. Find the top 5 users with the highest number of posts.
-- 2. For each of these top 5 users, calculate the average post length.
-- 3. Identify the day of the week when the most `lengthy` posts are created (assume all posts were created in the UTC timezone).