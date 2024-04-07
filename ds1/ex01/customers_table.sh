source ../.env
rm -f final_table.sql
touch final_table.sql

cat customers_table.header.sql > final_table.sql
for filename in ../subject/customer/data_202*_*.csv; do
	dockerpath="\/subject\/customer\/"$(basename $filename)
	cat customers_table.body.sql | sed "s/thepath/'$dockerpath'/g" >> final_table.sql
done

docker cp ./final_table.sql $DB_HOST:/customers_table.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f customers_table.sql

rm -f final_table.sql