source ./.env
echo "Copying the pgsql file into the container..."
docker cp $DB_LOCATION $DB_HOST:/db.pgsql
echo "Importing the pgsql into the live Postgres database"
docker exec -it $DB_HOST "psql" -U "$DB_USER" "$DB_NAME" -f db.pgsql

