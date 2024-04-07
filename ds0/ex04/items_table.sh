source ../.env
docker cp ./items_table.sql $DB_HOST:items_table.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f items_table.sql