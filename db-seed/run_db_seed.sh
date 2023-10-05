YOUR_DIR="./db-seed"
for file in $YOUR_DIR/*.sql; do
    psql --host=localhost -U postgres -W  -f "${file}"
done