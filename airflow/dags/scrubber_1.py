
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    'scrubber_1',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        # 'retries': 1,
        # 'retry_delay': timedelta(minutes=5),
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
        bash_command='pip install -r /opt/airflow/scrubbers/scrubber_1/requirements.txt',
    )

    RUN_PROJECT = BashOperator(
        task_id='run',
        depends_on_past=False,
        trigger_rule='all_done',
        bash_command='python /opt/airflow/scrubbers/scrubber_1/main.py',
    )

    SETUP_PROJECT >> RUN_PROJECT
