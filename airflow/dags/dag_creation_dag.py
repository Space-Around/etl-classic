import sys
import pickle
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

# from dag_creation import DAGCreation

sys.path.insert(0, "/opt/airflow/modules/dag_creation/")
sys.path.insert(0, "/opt/airflow/scrubbers/")
sys.path.insert(0, "/opt/airflow/config/")
sys.path.insert(0, "/opt/airflow/const/")

try:
    import config
    import const
except Exception as err:
    print(err)

# # consts
# # DAG config
# DAG_NAME = 'dag_creation'
# DAG_DESC = 'DAG of factory of DAGs from Python projects'
# DAG_TAGS = ['etl']
#
# # Task id
# SETUP_TASK_ID = 'setup'
# READ_ENV_TASK_ID = 'read_env'
# GET_PROJECTS_LIST_TASK_ID = 'get_projects_list'
# GET_DAGS_LIST_TASK_ID = 'get_dags_list'
# COMPARE_PROJECTS_DAGS_TASK_ID = 'compare_projects_dags'
# CREATE_DAG_TASK_ID = 'create_dag'
#
# # Task status
# SUCCESS_TASK_STATUS = 'task success'
#
# # XCom key
# PROJECT_LIST_XCOM_KEY = 'projects_list'
# DAGS_LIST_XCOM_KEY = 'dags_list'
# NEW_DAGS_LIST_XCOM_KEY = 'new_dags_list'


with DAG(
    config.DAG_CREATION_DAG_NAME,
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
    description=config.DAG_CREATION_DAG_DESC,
    # schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 8, 30),
    catchup=False,
    tags=config.DAG_CREATION_DAG_TAGS,
) as dag:
    @task(task_id=const.SETUP_TASK_ID)
    def setup(ds=None, **kwargs):
        """
        Setup dag creation Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """

        return f'{const.SETUP_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.READ_ENV_TASK_ID)
    def read_env(ds=None, **kwargs):
        """
        Read env Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation

            dag_creation_instance = DAGCreation()
        except Exception as err:
            print(err)

        dag_creation_instance.read_env()

        return f'{const.READ_ENV_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.GET_PROJECTS_LIST_TASK_ID)
    def get_projects_list(ds=None, **kwargs):
        """
        Get projects list Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation

            dag_creation_instance = DAGCreation()
        except Exception as err:
            print(err)

        projects_list = dag_creation_instance.get_projects_list()

        task_instance = kwargs['task_instance']
        task_instance.xcom_push(key=const.PROJECT_LIST_XCOM_KEY, value=projects_list)

        return f'{const.GET_PROJECTS_LIST_TASK_ID} {const.SUCCESS_TASK_STATUS}'


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

            dag_creation_instance = DAGCreation()
        except Exception as err:
            print(err)

        dags_list = dag_creation_instance.get_dags_list()

        task_instance = kwargs['task_instance']
        task_instance.xcom_push(key=const.DAGS_LIST_XCOM_KEY, value=dags_list)

        return f'{const.GET_DAGS_LIST_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.COMPARE_PROJECTS_DAGS_TASK_ID)
    def compare_projects_dags(ds=None, **kwargs):
        """
        Compare projects DAGs Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation

            dag_creation_instance = DAGCreation()
        except Exception as err:
            print(err)

        task_instance = kwargs['task_instance']
        projects_list = task_instance.xcom_pull(task_ids=const.GET_PROJECTS_LIST_TASK_ID, key=const.PROJECT_LIST_XCOM_KEY)
        dags_list = task_instance.xcom_pull(task_ids=const.GET_DAGS_LIST_TASK_ID, key=const.DAGS_LIST_XCOM_KEY)

        new_dags_list = dag_creation_instance.compare_projects_dags(projects_list, dags_list)

        task_instance.xcom_push(key=const.NEW_DAGS_LIST_XCOM_KEY, value=new_dags_list)

        return f'{const.COMPARE_PROJECTS_DAGS_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    @task(task_id=const.CREATE_DAG_TASK_ID)
    def create_dag(ds=None, **kwargs):
        """
        Create DAG Airflow task.

        :param ds:
        :param kwargs:
        :return: task status
        """
        try:
            from dag_creation import DAGCreation

            dag_creation_instance = DAGCreation()
        except Exception as err:
            print(err)

        task_instance = kwargs['task_instance']
        new_dags_list = task_instance.xcom_pull(task_ids=const.COMPARE_PROJECTS_DAGS_TASK_ID, key=const.NEW_DAGS_LIST_XCOM_KEY)

        dag_creation_instance.create_dag(new_dags_list)

        return f'{const.CREATE_DAG_TASK_ID} {const.SUCCESS_TASK_STATUS}'


    SETUP_TASK = setup()
    READ_ENV_TASK = read_env()
    GET_PROJECTS_LIST_TASK = get_projects_list()
    GET_DAGS_LIST_TASK = get_dags_list()
    COMPARE_PROJECTS_DAGS_TASK = compare_projects_dags()
    CREATE_DAG_TASK = create_dag()

    SETUP_TASK >> READ_ENV_TASK >> GET_PROJECTS_LIST_TASK >> GET_DAGS_LIST_TASK >> COMPARE_PROJECTS_DAGS_TASK >> CREATE_DAG_TASK
