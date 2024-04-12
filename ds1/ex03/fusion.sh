source ../.env
docker cp ./fusion.sql $DB_HOST:fusion.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f fusion.sql