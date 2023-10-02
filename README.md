# Database

## Initializing Database

- Start Database using Docker Compose by running:

```sh
docker-compose up -d
```

- Create Database by running restore.sql with the command:

```sh
psql --host=localhost -U postgres -W  -f physical_verification/restore.sql
```
