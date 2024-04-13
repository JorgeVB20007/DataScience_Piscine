CREATE TABLE IF NOT EXISTS items (
	product_id INTEGER,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT
);

TRUNCATE items;
COPY items(product_id, category_id, category_code, brand)
FROM '/subject/item/item.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE IF NOT EXISTS merged_table (
    product_id INTEGER PRIMARY KEY,
    category_id BIGINT,
    category_code TEXT,
    brand TEXT
);
TRUNCATE merged_table;

INSERT INTO merged_table (product_id, category_id, category_code, brand)
SELECT 
    product_id,
    MAX(category_id) AS category_id,
    MAX(category_code) AS category_code,
    MAX(brand) AS brand
FROM (
    SELECT * FROM items
    UNION ALL
    SELECT * FROM items WHERE category_id IS NULL OR category_code IS NULL OR brand IS NULL
) AS subquery
GROUP BY product_id;


ALTER TABLE customers
ADD category_id BIGINT;
ALTER TABLE customers
ADD category_code TEXT;
ALTER TABLE customers
ADD brand TEXT;


CREATE TABLE IF NOT EXISTS final_customers (
	event_time TIMESTAMPTZ,
	event_type TEXT,
	product_id INTEGER,
	price FLOAT,
	user_id BIGINT,
	user_session UUID,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT
);

TRUNCATE final_customers;

INSERT INTO final_customers(
  event_time, 
  event_type, 
  product_id, 
  price, 
  user_id, 
  user_session, 
  category_id, 
  category_code, 
  brand
)
SELECT 
  c.event_time, 
  c.event_type, 
  c.product_id, 
  c.price, 
  c.user_id, 
  c.user_session, 
  i.category_id, 
  i.category_code, 
  i.brand
FROM
  customers c
  LEFT JOIN merged_table i USING  (product_id)
ORDER BY
  c.event_time;

DROP TABLE customers;
DROP TABLE items;
DROP TABLE merged_table;

ALTER TABLE final_customers
RENAME TO customers;
