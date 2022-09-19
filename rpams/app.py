"""Redirect HTTP requests to another server."""
import psutil
import subprocess
from subprocess import Popen, PIPE
from random import randint

from mitmproxy import http
from mitmproxy.net.server_spec import ServerSpec
from mitmproxy.connection import ConnectionState

import config
from src.storage import Website, StorageORM, Process

from src.utils import get_free_port, get_scrubber_url_map, get_scrubber_by_url, get_external_proxies, \
    get_delay_time_scrubber_dag
# from airflow.api.dag_run import DAGRun

from airflow_api import DAGRun

# define db (orm)
storage = StorageORM()
Website.set_session(storage.session)
Process.set_session(storage.session)

# Setup conntion to Airflow REST API on client side
dr = DAGRun()
dr.configure(
    endpoint_url=config.AIRFLOW_API_ENDPOINT_URL,
    username=config.AIRFLOW_API_USERNAME,
    password=config.AIRFLOW_API_PASSWORD
)


def request(flow: http.HTTPFlow) -> None:
    """
    Processing requests.

    :param flow: http.HTTPFlow instance
    :return:
    """
    scrubber: str = dict(flow.request.headers)['scrubber-name']

    # first upstream proxy (fup)
    fup_list: list = get_external_proxies(config.PROXY_JSON_PATH)
    fup_list_len: int = len(fup_list)
    fup: dict = fup_list[randint(0, fup_list_len - 1)]
    fup_scheme = fup["scheme"]
    fup_ip = fup["ip"]
    fup_port = fup["port"]
    fup_username = fup["username"]
    fup_password = fup["password"]

    # second upstream proxy (sup)
    sup_port = get_free_port()

    cmd: str = f"mitmproxy -p {sup_port} --mode upstream:{fup_scheme}://{fup_ip}:{fup_port} " \
               f"--upstream-auth {fup_username}:{fup_password}"

    try:
        process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")

        # redirect connection to second upstream proxy
        flow.server_conn.state = ConnectionState.CLOSED
        flow.server_conn.via = ServerSpec('http', (config.DYNAMIC_PROXY_IP, sup_port))

        process.kill()
    except Exception as err:
        pass

    try:
        website = Website.get(
            column='scrubber',
            value=scrubber
        )

        if website is None:
            result = Website.add(
                scrubber=scrubber
            )

            print(f"request result: {result}")
    except Exception as err:
        print(err)


def response(flow: http.HTTPFlow) -> None:
    """
    Processing response.

    :param flow:
    :return:
    """
    status_code = flow.get_state()['response']['status_code']
    scrubber: str = dict(flow.request.headers)['scrubber-name']

    # if status_code == 200:
        # Get website data from DB by URL
    storage = StorageORM()
    Website.set_session(storage.session)
    Process.set_session(storage.session)

    website = Website.get(
        column='scrubber',
        value=scrubber
    )

    if website is None:
        return

    print(f"response website: {website}")

    Website.delete(
        website_id=website.id
    )
    # else:
        # storage = StorageORM()
        # Website.set_session(storage.session)
        # Process.set_session(storage.session)
        #
        # process = None
        # try:
        #     process = Process.get('scrubber', scrubber)
        # except Exception as err:
        #     print(err)
        #
        # psutil.Process(process.pid).kill()
        # Process.delete(process.pid)
        #
        # # Get website data from DB by URL
        # website = Website.get(
        #     column='scrubber',
        #     value=scrubber
        # )
        #
        # if website is None:
        #     return
        #
        # print(website)
        #
        # # Update request count
        # Website.update(
        #     website_id=website.id,
        #     column='requests_count',
        #     value=website.requests_count + 1
        # )
        #
        # # Trigger Airflow DAG
        # request_result = dr.trigger(
        #     dag_id=scrubber,
        #     date=get_delay_time_scrubber_dag(website.requests_count + 1, config.SCRUBBER_DAG_COUNT_DELAY_TIME_MAP,
        #                                      config.SCRUBBER_DAG_DELAY_TIME)
        # )
        #
        # print(request_result)


# def error(flow: http.HTTPFlow):
#     """
#     Errors handlers.
#
#     :param flow:
#     :return:
#     """
#     # Get website data from DB by URL
#     storage = StorageORM()
#     Website.set_session(storage.session)
#     Process.set_session(storage.session)
#
#     scrubber: str = dict(flow.request.headers)['scrubber-name']
#
#     process = Process.get('scrubber', scrubber)
#     psutil.Process(process.pid).kill()
#     Process.delete(process.pid)
#
#     website = Website.get(
#         column='scrubber',
#         value=scrubber
#     )
#
#     # Update request count
#     Website.update(
#         website_id=website.id,
#         column='requests_count',
#         value=website.requests_count + 1
#     )
#
#     date = get_delay_time_scrubber_dag(website.requests_count + 1, config.SCRUBBER_DAG_COUNT_DELAY_TIME_MAP,
#                                        config.SCRUBBER_DAG_DELAY_TIME)
#
#     # Trigger Airflow DAG
#     request_result = dr.trigger(
#         dag_id=scrubber,
#         date=date
#     )
