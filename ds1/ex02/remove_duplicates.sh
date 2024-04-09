source ../.env
docker cp ./remove_duplicates.sql $DB_HOST:remove_duplicates.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f remove_duplicates.sql