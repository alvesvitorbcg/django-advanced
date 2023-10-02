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

## Setting up local environment

- Create virtual environment

```bash
python -m venv venv
```

- Run Script for installing dependencies

```sh
bash install-deps.sh
```
