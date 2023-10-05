## Setting up local environment

- Create virtual environment

  ```sh
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

- Seed Database by running:

  ```sh
  bash db-seed/run_db_seed.sh
  ```

## Running the application

- Run the command below to run the application:

  ```sh
  python manage.py runserver
  ```

- The database seed files insert a default `admin` user with password `1234`

## Running tests

- To run tests and see coverage use the command:

  ```sh
  coverage run ./manage.py test && coverage report -m
  ```

## Running Sonarqube analysis locally

- Run Sonarqube server in Docker

  ```sh
  docker run -d --name sonarqube -p 9000:9000 -p 9092:9092 sonarqube
  ```

- Access Sonarqube in `http://localhost:9000/` and login with default user `admin` with password `admin`

- Create project with name and key `physical-verification-project`

- In `run_analysis.sh` Replace `-Dsonar.login` value with a new token generated in your local Sonarqube.

- Install [Sonarqube Scanner](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner/).

- Run command below to run tests and generate Sonarqube analysis

  ```sh
  bash run_analysis.sh $PATH_TO_SONARSCANNER_BINARIES
  ```

  `$PATH_TO_SONARSCANNER_BINARIES` usually looks like /Users/{USER}/Downloads/sonar-scanner-{VERSION}-{OS}/bin
