import requests


class DAGRun:
    """
    Manage DAG running.

    Attributes:
        endpoint_url Endpoint URL of Airflow server
        username     Airflow username
        password     Airflow password
    """
    def __init__(self):
        self.endpoint_url: str = ""
        self.username: str = ""
        self.password: str = ""

    def configure(self, endpoint_url: str, username: str, password: str) -> None:
        """
        Configure clinet side connection to Airflow server.

        :param endpoint_url: Endpoint URL of Airflow server
        :param username: Airflow username
        :param password: Airflow password
        :return:
        """
        self.endpoint_url = endpoint_url
        self.username = username
        self.password = password

    def trigger(self, dag_id: str, date: str):
        """
        Trigger Airflow DAG at date.

        :param dag_id: DAG ID
        :param date: Date to run DAG
        :return:
        """
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
          "conf": {},
          "dag_run_id": dag_id,
          "logical_date": date
        }

        response = requests.post(
            url=f"{self.endpoint_url}/api/v1/dags/{dag_id}/dagRuns",
            headers=headers,
            json=json_data,
            auth=(self.username, self.password)
        )

        if response.status_code != 200:
            response = requests.delete(
                url=f"{self.endpoint_url}/api/v1/dags/{dag_id}/dagRuns/{dag_id}",
                auth=(self.username, self.password)
            )

            response = requests.post(
                url=f"{self.endpoint_url}/api/v1/dags/{dag_id}/dagRuns",
                headers=headers,
                json=json_data,
                auth=(self.username, self.password)
            )

        return response
