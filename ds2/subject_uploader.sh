source ./.env
docker cp subject/ $DB_HOST:subject/
# docker exec -it $DB_HOST mkdir -p subject/customer
# docker cp data_2023_jan.csv $DB_HOST:subject/customer/data_2023_jan.csv