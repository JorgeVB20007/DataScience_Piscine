docker cp ./automatic_table.sql DS:automatic_table.sql
docker exec -it DS psql -U jvacaris -d piscineds -f automatic_table.sql