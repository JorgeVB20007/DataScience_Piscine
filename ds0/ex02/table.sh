source ../.env
docker cp ./table.sql $DB_HOST:table.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f table.sql