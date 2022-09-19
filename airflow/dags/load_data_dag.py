import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

# from load_data import LoadData
# from dag_creation import DAGCreation


# consts
# # DAG config
# DAG_NAME = 'load_data'
# DAG_DESC = 'Load data from Python project folders'
# DAG_TAGS = ['etl']
#
# # Task id
# EXTRACT_LOAD_TASK_ID = 'extract_load'
# GET_DAGS_LIST_TASK_ID = 'get_dags_list'
#
# # Task status
# SUCCESS_TASK_STATUS = 'task success'
#
# # XCom key
# DAGS_LIST_XCOM_KEY = 'dags_list'
#
# PATH_TO_PROJECTS = '/opt/airflow/scrubbers'
# DATA_FILE_EXTENSION = '.csv'
#
# SERVICE_NAME_S3 = 's3'
# ENDPOINT_URL_S3 = 'http://minio1:9000'
# ACCESS_KEY_S3 = 'lkQIBnxMJKXmKEqp'
# SECRET_ACCESS_KEY_S3 = 'WCEcAL2eiKFRMJZhTGdXV7IKvwo3ed6M'
# BUCKET_S3 = 'test-bucket'

sys.path.insert(0, "/opt/airflow/modules/load_data/")
sys.path.insert(0, "/opt/airflow/modules/dag_creation/")
sys.path.insert(0, "/opt/airflow/config/")
sys.path.insert(0, "/opt/airflow/const/")
sys.path.insert(0, "/opt/airflow/scrubbers/")

try:
    import config
    import const
except Exception as err:
    print(err)

# load_data = LoadData()
# dag_creation_instance = DAGCreation()


with DAG(
    config.LOAD_DATA_DAG_NAME,
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description=config.LOAD_DATA_DAG_DESC,
    schedule_interval=timedelta(days=30),
    start_date=datetime(2022, 8, 30),
    catchup=False,
    tags=config.LOAD_DATA_DAG_TAGS,
) as dag:
    @task(task_id=const.GET_DAGS_LIST_TASK_ID)
    def get_dags_list(ds=None, **kwargs):
        """
        Get DAGs list Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation
            from load_data import LoadData

            load_data = LoadData()
            dag_creation_instance = DAGCreation()
        except Exception:
            pass

        dags_list = dag_creation_instance.get_dags_list(filters=True)

        task_instance = kwargs['task_instance']
        task_instance.xcom_push(key=const.DAGS_LIST_XCOM_KEY, value=dags_list)

        return f'{const.GET_DAGS_LIST_TASK_ID} {const.SUCCESS_TASK_STATUS}'

    @task(task_id=const.EXTRACT_LOAD_TASK_ID)
    def extract_load(ds=None, **kwargs):
        """
        Extract and load data Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation
            from load_data import LoadData

            load_data = LoadData()
        except Exception:
            pass

        task_instance = kwargs['task_instance']
        dags_list = task_instance.xcom_pull(task_ids=const.GET_DAGS_LIST_TASK_ID, key=const.DAGS_LIST_XCOM_KEY)

        load_data.configure(
            service_name=config.SERVICE_NAME_S3,
            endpoint_url=config.ENDPOINT_URL_S3,
            access_key=config.ACCESS_KEY_S3,
            secret_access_key=config.SECRET_ACCESS_KEY_S3,
            bucket=config.BUCKET_S3,
            path_to_projects=config.PATH_TO_PROJECTS,
            extension=[config.CSV_DATA_FILE_EXTENSION, config.JSON_DATA_FILE_EXTENSION]
        )

        load_data.extract_load(dags_list)

        return f'{const.EXTRACT_LOAD_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    GET_DAGS_LIST_TASK = get_dags_list()
    EXTRACT_LOAD_TASK = extract_load()

    GET_DAGS_LIST_TASK >> EXTRACT_LOAD_TASK
