from rpams.src.utils import get_delay_time_scrubber_dag

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


def minutes():
    request_count = 1
    return get_delay_time_scrubber_dag(request_count, SCRUBBER_DAG_COUNT_DELAY_TIME_MAP, SCRUBBER_DAG_DELAY_TIME)


def hours():
    request_count = 4
    return get_delay_time_scrubber_dag(request_count, SCRUBBER_DAG_COUNT_DELAY_TIME_MAP, SCRUBBER_DAG_DELAY_TIME)


def days():
    request_count = 8
    return get_delay_time_scrubber_dag(request_count, SCRUBBER_DAG_COUNT_DELAY_TIME_MAP, SCRUBBER_DAG_DELAY_TIME)


def main():
    print(minutes())
    print(hours())
    print(days())


if __name__ == '__main__':
    main()