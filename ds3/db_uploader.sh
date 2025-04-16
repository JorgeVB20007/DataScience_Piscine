source ./.env
echo "Copying the pgsql file into the container..."
docker cp "$DB_LOCATION/Test_knight.csv" "$DB_HOST:/test_knight.csv"
docker cp "$DB_LOCATION/Train_knight.csv" "$DB_HOST:/train_knight.csv"


echo "Copying a sql instructions file..."
docker cp ./create_tables.sql $DB_HOST:/create_tables.sql
echo "Executing it..."
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f /create_tables.sql

# echo "Importing the pgsql into the live Postgres database"
# docker exec -i "$DB_HOST" psql -U "$DB_USER" "$DB_NAME" \
#   -c "\copy test_knight FROM '/tmp/test_knight.pgsql' WITH CSV HEADER"

# docker exec -i "$DB_HOST" psql -U "$DB_USER" "$DB_NAME" \
#   -c "\copy train_knight FROM '/tmp/train_knight.pgsql' WITH CSV HEADER"

