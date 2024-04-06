CREATE TABLE &1 (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

TRUNCATE &1;
COPY &1(event_time, event_type, product_id, price, user_id, user_session)
FROM &2 DELIMITER ',' CSV HEADER;

-- ! FIX THIS TODAY