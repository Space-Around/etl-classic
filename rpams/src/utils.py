import json
import socket
import datetime


def read_json(path: str) -> list:
    """
    Read JSON file.

    :param path: Path to JSON file
    :return: JSON data
    """
    json_dict: list = []

    if '.json' not in path:
        raise Exception('File extension should be .json')

    with open(path, mode='r', encoding='utf8') as json_file:
        json_dict = json.load(json_file)

    return json_dict


def get_external_proxies(path: str) -> list:
    """
    Read JSON file to return external proxy list.

    :param path: Path to JSON file
    :return: JSON data
    """
    return read_json(path)


def get_free_port() -> int:
    """
    Get free port.

    :return: port
    """
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]


def get_scrubber_url_map(path: str) -> list:
    """
    Read JSON file to return scrubber and url mapping.

    :param path: Path to JSON file
    :return: JSON data
    """
    return read_json(path)


def get_scrubber_by_url(url: str, mapping_list: list):
    """
    Get scrubber name by url.

    :param url: URL
    :param mapping_list: Scrubber and url mapping list
    :return: scrubber name
    """
    for obj in mapping_list:
        if url in obj["url"]:
            return obj["scrubber"]

    return None


def get_delay_time_scrubber_dag(requests_count: int, scrubber_dag_count_delay_time_map: dict,
                                scrubber_dag_delay_time: dict) -> str:
    """
    Get delay time scrubber DAG in Airflow format.

    :param requests_count: Requests count
    :param scrubber_dag_count_delay_time_map: Scrubber DAG delay time from config
    :param scrubber_dag_delay_time:
    :return:
    """
    try:
        count_delay_time_map: str = scrubber_dag_count_delay_time_map[requests_count]

        now = datetime.datetime.utcnow()

        delay_time: dict = scrubber_dag_delay_time[count_delay_time_map]

        if delay_time["measurement"] == "minute":
            now = now + datetime.timedelta(minutes=delay_time["value"])

        if delay_time["measurement"] == "hour":
            now = now + datetime.timedelta(hours=delay_time["value"])

        if delay_time["measurement"] == "day":
            now = now + datetime.timedelta(days=delay_time["value"])

        # now = now - datetime.timedelta(hours=2)

        now_format: str = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        return now_format
    except Exception:
        return ""
