import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

sys.path.insert(0, "/opt/airflow/modules/dataflow/")
sys.path.insert(0, "/opt/airflow/config/")
sys.path.insert(0, "/opt/airflow/const/")
sys.path.insert(0, "/opt/airflow/tmp/")

try:
    import config
    import const
    from dataflow import Dataflow

    dataflow = Dataflow()

    dataflow.configure_source(
        service_name=config.SERVICE_NAME_S3,
        endpoint_url=config.ENDPOINT_URL_S3,
        access_key=config.ACCESS_KEY_S3,
        secret_access_key=config.SECRET_ACCESS_KEY_S3,
        bucket=config.BUCKET_S3,
        local_storage_path=config.DATAFLOW_LOCAL_STORAGE_PATH
    )
    dataflow.configure_target(
        service_name=config.SERVICE_NAME_S3_DWH,
        endpoint_url=config.ENDPOINT_URL_S3_DWH,
        access_key=config.ACCESS_KEY_S3_DWH,
        secret_access_key=config.SECRET_ACCESS_KEY_S3_DWH,
        bucket=config.BUCKET_S3_DWH,
        local_storage_path=config.DATAFLOW_LOCAL_STORAGE_PATH
    )
except Exception as err:
    print(err)

with DAG(
    config.DATAFLOW_DAG_NAME,
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description=config.DATAFLOW_DAG_DESC,
    schedule_interval=timedelta(days=30),
    start_date=datetime(2022, 8, 30),
    catchup=False,
    tags=config.DATAFLOW_DAG_TAGS,
) as dag:
    @task(task_id=const.SETUP_TASK_ID)
    def setup(ds=None, **kwargs):
        """
        Setup connection to Data Lake and Data Warehouse Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """

        return f'{const.SETUP_TASK_ID} {const.SUCCESS_TASK_STATUS}'

    @task(task_id=const.DOWNLOAD_DATA_TASK_ID)
    def download_data(ds=None, **kwargs):
        """
        Download data from Data Lake to local storage Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        dataflow.extract_from_data_lake()

        return f'{const.DOWNLOAD_DATA_TASK_ID} {const.SUCCESS_TASK_STATUS}'

    @task(task_id=const.FIRST_NORMAL_FORM_TASK_ID)
    def first_normal_form(ds=None, **kwargs):
        """
        Reach first normal form Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """

        dataflow.first_normal_form()

        return f'{const.FIRST_NORMAL_FORM_TASK_ID} {const.SUCCESS_TASK_STATUS}'

    @task(task_id=const.FORMATTING_DATA_TASK_ID)
    def formatting_data(ds=None, **kwargs):
        """
        Formatting data Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """

        dataflow.formatting_date()

        return f'{const.FORMATTING_DATA_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.UNION_CODEC_TASK_ID)
    def union_codec(ds=None, **kwargs):
        """
        Union codec Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        dataflow.union_data_codec()
        return f'{const.UNION_CODEC_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.INDEX_DATA_TASK_ID)
    def index_data(ds=None, **kwargs):
        """
        Index data Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        dataflow.index_data()

        return f'{const.INDEX_DATA_TASK_ID} {const.SUCCESS_TASK_STATUS}'

    @task(task_id=const.UPLOAD_DATA_TASK_ID)
    def upload_data(ds=None, **kwargs):
        """
        Upload data from local storage to Data Warehouse Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        dataflow.upload_to_data_warehouse()

        return f'{const.UPLOAD_DATA_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.DELETE_LOCAL_DATA_TASK_ID)
    def delete_local_data(ds=None, **kwargs):
        """
        Delete local data Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        dataflow.delete_local_data()

        return f'{const.DELETE_LOCAL_DATA_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    SETUP_TASK = setup()
    DOWNLOAD_DATA_TASK = download_data()
    FIRST_NORMAL_FORM_TASK = first_normal_form()
    FORMATTING_DATA_TASK = formatting_data()
    UNION_CODEC_TASK = union_codec()
    INDEX_DATA_TASK = index_data()
    UPLOAD_DATA_TASK = upload_data()
    DELETE_LOCAL_DATA = delete_local_data()

    SETUP_TASK >> DOWNLOAD_DATA_TASK >> FIRST_NORMAL_FORM_TASK >> FORMATTING_DATA_TASK >> UNION_CODEC_TASK >> INDEX_DATA_TASK >> UPLOAD_DATA_TASK >> DELETE_LOCAL_DATA