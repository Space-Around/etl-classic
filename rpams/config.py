# SQLITE_PATH = 'sqlite://///opt/rpams/db/website.db?check_same_thread=False'

SQLITE_PATH = 'sqlite://///home/maxwellviksna/etl-classic/rpams/db/website.db?check_same_thread=False'

# PROXY_JSON_PATH = '/opt/rpams/cfg/external-proxy.json'

PROXY_JSON_PATH = '/home/maxwellviksna/etl-classic/rpams/cfg/external-proxy.json'

DYNAMIC_PROXY_IP = 'airflow-webserver'
DYNAMIC_PROXY_SCHEME = 'http'

# Delay DAG run time in Airflow, values are the number of request attempts
SCRUBBER_DAG_COUNT_DELAY_TIME_MAP = {
    1: "FIVE_MIN_DELAY_TIME",
    2: "TEN_MIN_DELAY_TIME",
    3: "THIRTY_MIN_DELAY_TIME",
    4: "ONE_HOUR_DELAY_TIME",
    5: "TWO_HOUR_DELAY_TIME",
    6: "FIVE_HOUR_DELAY_TIME",
    7: "TWELVE_HOURS_DELAY_TIME",
    8: "ONE_DAY_DELAY_TIME",
    9: "TWO_DAYS_DELAY_TIME",
    10: "FOUR_DAYS_DELAY_TIME",
    11: "SEVEN_DAYS_DELAY_TIME"
}

SCRUBBER_DAG_DELAY_TIME = {
    "FIVE_MIN_DELAY_TIME": {
        'value': 5,
        'measurement': 'minute'
    },
    "TEN_MIN_DELAY_TIME": {
        'value': 10,
        'measurement': 'minute'
    },
    "THIRTY_MIN_DELAY_TIME": {
        'value': 30,
        'measurement': 'minute'
    },
    "ONE_HOUR_DELAY_TIME": {
        'value': 1,
        'measurement': 'hour'
    },
    "TWO_HOUR_DELAY_TIME": {
        'value': 2,
        'measurement': 'hour'
    },
    "FIVE_HOUR_DELAY_TIME": {
        'value': 5,
        'measurement': 'hour'
    },
    "TWELVE_HOURS_DELAY_TIME": {
        'value': 12,
        'measurement': 'hour'
    },
    "ONE_DAY_DELAY_TIME": {
        'value': 1,
        'measurement': 'day'
    },
    "TWO_DAYS_DELAY_TIME": {
        'value': 2,
        'measurement': 'day'
    },
    "FOUR_DAYS_DELAY_TIME": {
        'value': 4,
        'measurement': 'day'
    },
    "SEVEN_DAYS_DELAY_TIME": {
        'value': 7,
        'measurement': 'day'
    },
}

# Airflow REST API
AIRFLOW_API_ENDPOINT_URL = 'http://0.0.0.0:8080'
AIRFLOW_API_USERNAME = 'airflow'
AIRFLOW_API_PASSWORD = 'airflow'
