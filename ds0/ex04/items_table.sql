CREATE TABLE items (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

COPY data_2022_oct(event_time, event_type, product_id, price, user_id, user_session)
FROM '/subject/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;
