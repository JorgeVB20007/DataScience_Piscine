COPY customers(event_time, event_type, product_id, price, user_id, user_session)
FROM thepath DELIMITER ',' CSV HEADER;

