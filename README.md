## Setting up local environment

- Create virtual environment

```bash
python -m venv venv
```

- Activate virtual environment with

```sh
source venv/bin/activate
```

- Run Script for installing dependencies

```sh
bash install-deps.sh
```

## Initializing Database

- Start Database using Docker Compose by running:

```sh
docker-compose up -d
```

- Apply migrations with:

```sh
python manage.py migrate
```

- Seed Database by running

```sh
bash db-seed/run_db_seed.sh`:
```

## Running the application

- Run the command below to run the application:

```sh
python manage.py runserver
```

- The database seed files insert a default `admin` user with password `1234`
