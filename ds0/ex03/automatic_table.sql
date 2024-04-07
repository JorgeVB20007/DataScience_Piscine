CREATE TABLE IF NOT EXISTS thefile (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

TRUNCATE thefile; 
COPY thefile(event_time, event_type, product_id, price, user_id, user_session)
FROM thepath DELIMITER ',' CSV HEADER;
