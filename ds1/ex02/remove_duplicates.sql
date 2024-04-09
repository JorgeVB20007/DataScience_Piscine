-- WITH remove_duplicates AS (
-- 	SELECT event_type, product_id, price, user_id, user_session,
-- 	ROW_NUMBER() OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_type, product_id, price, user_id, user_session) AS group_num
-- 	FROM customers
-- )
-- DELETE FROM customers
-- WHERE (event_type, product_id, price, user_id, user_session)
-- IN (SELECT event_type, product_id, price, user_id, user_session FROM remove_duplicates WHERE group_num > 1);


CREATE TABLE temp_table AS WITH remove_duplicates AS(
	SELECT *, LAG(event_time) OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_time) AS prev_event_time
	FROM customers
)
SELECT event_time, event_type, product_id, price, user_id, user_session
FROM remove_duplicates
WHERE event_time - prev_event_time > INTERVAL '1 second'
OR prev_event_time IS NULL;

DROP TABLE customers;
ALTER TABLE temp_table RENAME TO customers;
