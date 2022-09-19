# Request processing as middleware service (RPaMS)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## What is it?
Request routing service, error handling, connection to external proxy servers. This service is build on [mitmproxy](https://github.com/mitmproxy/mitmproxy), for more detals visit GitHub repo of this project.
<hr>

## Microservice architecture
![alt text](../docs/img/index.png "Title")

## Configure
Set in file `config.py`:

| Name         | Description                                                                                             | Type |
|--------------|---------------------------------------------------------------------------------------------------------|------|
| `SQLITE_PATH` | Path to SQLite databse (default: /rpams/db/)                                                            |      |
| `PROXY_JSON_PATH` | Path to external proxy JSON file (default: /cfg/external-proxy.json)                                    |      |
| `SCRUBBER_URL_MAP_JSON_PATH` | Path to scrubber and url mapping JSON file (default: /cfg/scrubber-url-map.json)                        |      |
| `DYNAMIC_PROXY_IP` | IP addr to sencond upstream proxy (is internal service) (default: 0.0.0.0)                              |      |
| `DYNAMIC_PROXY_SCHEME` | Protocol to connect to sencond upstream proxy (default: http)                                           |      |
| `SCRUBBER_DAG_COUNT_DELAY_TIME_MAP` | Dict to mapping request count to specific and delay time in Airflow. Only request count can be modifyed |      |
| `SCRUBBER_DAG_DELAY_TIME` | Dict with mapping time value and measurement                                                            |      |
| `AIRFLOW_API_ENDPOINT_URL` | Endpoint for Airflow REST API                                                                           |      |
| `AIRFLOW_API_USERNAME` | Airflow username (default: airflow)                                                                     |      |
| `AIRFLOW_API_PASSWORD` | Airflow password (default: airflow)                                                                     |      |

## Setup
1. `pip install mitmproxy` (or is available necessary utils in `/mitm`, but is's bad way)
2. `pip install sqlalchemy`

## Startup
1. `mitmdump -s rpams/app.py -p 8081` (exec cmd from root of project. Example: `some/path/reef-etl mitmdump -s rpams/app.py -p 8081`)

## Requirements
- Python 3.9+

## Project structure
- `db` - storage folder
- `mitm` - mitmproxy services
- `src` - source files
- `src/storage/connector.py` - ORM for managing to storage
- `src/utils` - some methods for clear style code 
- `app.py` - core of service
- `config.py` - config file

## Warnnig
If you want to change the JSON structure, you also need to change the code. Keep this in mind when changing `/cfg/external-proxy.json` and `/cfg/scrubber-url-map.json`