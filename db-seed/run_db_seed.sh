YOUR_DIR="./db-seed"
for file in $YOUR_DIR/*.sql; do
    PGPASSWORD=changeme psql --host=localhost -U postgres -f "${file}"
done