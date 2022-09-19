# ETL Airflow
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Airflow task management service, a data collector for running tasks such as: creating dags, running scrubbers and uploading data to Data Lake.

### Requirements
- Python 3.9+

## Airflow
### Setup
1. `mkdir -p ./dags ./logs ./plugins`
2. `echo -e "AIRFLOW_UID=$(id -u)" > .env`
3. `docker-compose up -d airflow-init`
4. `docker-compose up -d` 

For more details: [airflow doc link](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

### Project structure
- `./dags` - you can put your DAG files here.
- `./logs` - contains logs from task execution and scheduler.
- `./plugins` - you can put your custom plugins here.
- `./src` - daemon of DAG creation from.

## DAG creation daemon
Entry point for every Python projects is `main.py`. Prepare Python projects to use as task in Airflow and run it.

### Setup
1. Define path to folder with scrubbers in .env file (default is `../scrubbers/`).
2. Install `requirements.txt`.

## Load data daemon
Collect data and load to Data Lake from Python projects.

### Configure
Configure in file: `/airflow/dags/load_data_dag.py`

Name  | Description |
------------- | -------------
`PATH_TO_PROJECTS`  | path to Python projects in Docker container (default: `/opt/airflow/dags/scrubbers`)
`DATA_FILE_EXTENSION`  | Extension of data file (default: `.csv`) 
`SERVICE_NAME_S3`  | S3 service name (default: `s3`)
`ENDPOINT_URL_S3`  | S3 service enpoint of REST API
`ACCESS_KEY_S3`  | S3 access key
`SECRET_ACCESS_KEY_S3`  | S3 secret access key
`BUCKET_S3`  | S3 bucket (default: `test-bucket`)

### Testing
For local testing collect and upload data, S3 server needs to be run, an example would be minio.
1. ```bash
    docker run --network airflow-test-net \
           -p 9000:9000 -p 9001:9001 \
           --name minio1 \
           -v ~/minio/data:/data \
           -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
           -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" quay.io/minio/minio server /data --console-address ":9001"
    ```
2. Create bucket and named it: `test-bucket`
3. Create new user throw minio web ui, copy `access_key` and `secret_access_key`
4. Set in `/airflow/dags/load_data_dag.py` necessary data

### Setup
1. Define path to folder with scrubbers in .env file (default is `../scrubbers/`).
2. Define connection to DB in `./const.py`.
3. Define data file extension `./const.py` (default mask is `*.csv`).
4. Install `requirements.txt`.

## Project structure
- `api` - API to manage Airflow DAGs actions
- `dags/dag_creation` - class of creation DAG for Python projects and run it as task 
- `dags/load_data` - class of load data from Python projects to Data Lake via S3 protocol
- `scrubbers` - folders with Python projects
- `dag_creation_dag.py` - DAG for creation new DAGs 
- `load_data_dag.py` - DAG for collect and load data to storage via S3 protocol
- `scrubber_1.py` - example of a created Python project DAG