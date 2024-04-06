CREATE TABLE data_2022_dec (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

CREATE TABLE data_2022_nov (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

CREATE TABLE data_2022_oct (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

CREATE TABLE data_2023_jan (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID
);

TRUNCATE data_2022_dec;
COPY data_2022_dec(event_time, event_type, product_id, price, user_id, user_session)
FROM '/subject/customer/data_2022_dec.csv' DELIMITER ',' CSV HEADER;

TRUNCATE data_2022_nov;
COPY data_2022_nov(event_time, event_type, product_id, price, user_id, user_session)
FROM '/subject/customer/data_2022_nov.csv' DELIMITER ',' CSV HEADER;

TRUNCATE data_2022_oct;
COPY data_2022_oct(event_time, event_type, product_id, price, user_id, user_session)
FROM '/subject/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;

TRUNCATE data_2023_jan;
COPY data_2023_jan(event_time, event_type, product_id, price, user_id, user_session)
FROM '/subject/customer/data_2023_jan.csv' DELIMITER ',' CSV HEADER;

