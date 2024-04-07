CREATE TABLE IF NOT EXISTS items (
	product_id INTEGER,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT
);

TRUNCATE items;
COPY items(product_id, category_id, category_code, brand)
FROM '/subject/item/item.csv' DELIMITER ',' CSV HEADER;
