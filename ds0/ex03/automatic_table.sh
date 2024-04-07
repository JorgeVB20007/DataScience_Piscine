source ../.env
rm -f final_table.sql
touch final_table.sql

for filename in ../subject/customer/*.csv; do
	tablename=$(basename $filename)
	tablename=${tablename%.*}
	dockerpath="\/subject\/customer\/"$(basename $filename)
	cat automatic_table.sql | sed "s/thefile/$tablename/g" | sed "s/thepath/'$dockerpath'/g" >> final_table.sql
done

docker cp ./final_table.sql $DB_HOST:/automatic_table.sql
docker exec -it $DB_HOST psql -U $DB_USER -d $DB_NAME -f automatic_table.sql

rm -f final_table.sql