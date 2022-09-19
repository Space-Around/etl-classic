DEFAULT_ENCODING = 'utf8'
# Task id
EXTRACT_LOAD_TASK_ID = 'extract_load'
GET_DAGS_LIST_TASK_ID = 'get_dags_list'

# Task status
SUCCESS_TASK_STATUS = 'task success'

# XCom key
DAGS_LIST_XCOM_KEY = 'dags_list'

DAG_TEMPLATE = """
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    '%s',
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
    description='DAG of factory of DAGs from Python projects',
    schedule_interval=timedelta(days=30),
    start_date=datetime(2022, 8, 30),
    catchup=False,
    tags=['etl'],
) as dag:
    SETUP_PROJECT = BashOperator(
        task_id='setup',
        depends_on_past=False,
        bash_command='''curl --header "Content-Type: application/json" --header "scrubber-name: %s" --request POST --data '{"command":"pip install -r /home/user/Desktop/sandbox/reef-etl-main/airflow/scrubbers/%s/requirements.txt"}' http://host.docker.internal:8082/exec''',
    )
    
    RUN_PROJECT = BashOperator(
        task_id='run',
        depends_on_past=False,
        trigger_rule='all_done',
        bash_command='''curl --header "Content-Type: application/json" --header "scrubber-name: %s" --request POST --data '{"command":"python3 /home/user/Desktop/sandbox/reef-etl-main/airflow/scrubbers/%s/main.py"}' http://host.docker.internal:8082/exec''',
    )

    SETUP_PROJECT >> RUN_PROJECT
"""

# Task id
SETUP_TASK_ID = 'setup'
READ_ENV_TASK_ID = 'read_env'
GET_PROJECTS_LIST_TASK_ID = 'get_projects_list'
# GET_DAGS_LIST_TASK_ID = 'get_dags_list'
COMPARE_PROJECTS_DAGS_TASK_ID = 'compare_projects_dags'
CREATE_DAG_TASK_ID = 'create_dag'

# Task status
# SUCCESS_TASK_STATUS = 'task success'

# XCom key
PROJECT_LIST_XCOM_KEY = 'projects_list'
# DAGS_LIST_XCOM_KEY = 'dags_list'
NEW_DAGS_LIST_XCOM_KEY = 'new_dags_list'


# Task id
DOWNLOAD_DATA_TASK_ID = 'download_data'
FIRST_NORMAL_FORM_TASK_ID = 'first_normal_form'
FORMATTING_DATA_TASK_ID = 'formatting_data'
UNION_CODEC_TASK_ID = 'union_codec'
INDEX_DATA_TASK_ID = 'index_data'
UPLOAD_DATA_TASK_ID = 'upload_data'
DELETE_LOCAL_DATA_TASK_ID = 'delete_local_data'

# docker run -p 9000:9000 -p 9001:9001 --name minio1 -v ~/minio/data:/data -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" quay.io/minio/minio server /data --console-address ":9001"