# ETL Proccess
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## What is it?
ETL process, which includes integration with Data Lake, Data Wirehouse and Dataflow. The connection to the storage is made via the S3 protocol.
<hr>

## Project info
A microservices approach is used.
### Microservice architecture
- **Request processing as middleware service (RPaMS)**
Request routing, error handling and upstream connetion service
- **Airflow dags**
Airflow task management service, a data collector for running tasks such as: creating dags, running scrubbers and uploading data to Data Lake.

### Requirements
- Python 3.9+
- Airflow 2.3.4+
- Docker 20.10.18, build b40c2f6

### Other
Please vitsit:
- `/airflow` - Airflow service and dags list and additional urils
- `/rpams` -  Request routing service and additional urils
- `/cfg` - Folder config

<hr>

## Documentation