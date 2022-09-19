import os
import sys

from airflow.models import DagBag, DagRun

# consts
# DAG_TEMPLATE = '''
# import sys
# from datetime import datetime, timedelta
#
# from airflow import DAG
# from airflow.decorators import task
# from airflow.operators.bash import BashOperator
#
# with DAG(
#     '%s',
#     default_args={
#         'depends_on_past': False,
#         'email': ['airflow@example.com'],
#         'email_on_failure': False,
#         'email_on_retry': False,
#         'retries': 1,
#         'retry_delay': timedelta(minutes=5),
#         # 'queue': 'bash_queue',
#         # 'pool': 'backfill',
#         # 'priority_weight': 10,
#         # 'end_date': datetime(2016, 1, 1),
#         # 'wait_for_downstream': False,
#         # 'sla': timedelta(hours=2),
#         # 'execution_timeout': timedelta(seconds=300),
#         # 'on_failure_callback': some_function,
#         # 'on_success_callback': some_other_function,
#         # 'on_retry_callback': another_function,
#         # 'sla_miss_callback': yet_another_function,
#         # 'trigger_rule': 'all_success'
#     },
#     description='DAG of factory of DAGs from Python projects',
#     schedule_interval=timedelta(days=1),
#     start_date=datetime(2022, 8, 30),
#     catchup=False,
#     tags=['etl'],
# ) as dag:
#     run_project = BashOperator(
#         task_id='run',
#         depends_on_past=False,
#         bash_command='python /opt/airflow/scrubbers/%s/main.py',
#     )
#
#     run_project
# '''
# PATH_TO_SCRUBBERS = '/scrubbers/'
# NEW_DAG_EXTENSION = '.py'
# PATH_TO_DAGS = '/opt/airflow/dags/'
# DEFAULT_ENCODING = 'utf8'

sys.path.insert(0, "/opt/airflow/config/")
sys.path.insert(0, "/opt/airflow/const/")

try:
    import config
    import const
except Exception as err:
    print(err)

class DAGCreation:
    """
    Sequence of tasks to create a new dag based on a Python project.

    Attributes:
        path_to_projects    Path to project
        airflow_uid         Airflow worker id
    """

    def __init__(self):
        self.path_to_projects: str = os.path.abspath(os.getcwd()) + config.PATH_TO_SCRUBBERS
        self.airflow_uid: int = 0

    def read_env(self) -> None:
        """
        Read .env.

        :return:
        """
        print(self.path_to_projects)

    def get_projects_list(self) -> list:
        """
        Get projects list in folder.

        :return: projects list
        """
        projects_list: list = []

        sys.path.insert(0, "/opt/airflow/scrubbers/")

        projects_list = os.listdir(self.path_to_projects)
        print(f'project list: {projects_list}')

        return projects_list

    def get_dags_list(self, filters=None) -> list:
        """
        Get airflow DAGs.

        :return: DAGs list
        """
        dags_list: list = []

        if filters is None:
            for dag in DagBag().dags.values():
                print(dag)
                print(dir(dag))
                dags_list.append(dag.dag_id)
        else:
            for dag in DagBag().dags.values():
                dag_runs = DagRun.find(dag_id=dag.dag_id)
                if len(dag_runs) > 0:
                    if dag_runs[len(dag_runs) - 1].state != 'running':
                        if dag.dag_id not in ('dag_creation', 'load_data'):
                            dags_list.append(dag.dag_id)

        print(f'dags list: {dags_list}')

        return dags_list

    def compare_projects_dags(self, projects_list, dags_list) -> list:
        """
        Compare projects list with DAGs list and make a difference.

        :param projects_list: Projects list
        :param dags_list: Dags list
        :return: new dags list
        """
        new_dags_list:list = []

        for project in projects_list:
            if project not in dags_list:
                print(project)
                new_dags_list.append(project)

        print(f'new airflow dags: {new_dags_list}')

        return new_dags_list

    def create_dag(self, new_dags_list) -> None:
        """
        Create DAG.

        :param new_dags_list: New DAGs list
        :return: none
        """
        for new_airflow_task in new_dags_list:
            print(new_airflow_task)
            with open(file=f'{config.PATH_TO_DAGS}{new_airflow_task}{config.NEW_DAG_EXTENSION}', mode='w', encoding=const.DEFAULT_ENCODING) as file:
                file.write(const.DAG_TEMPLATE % (new_airflow_task, new_airflow_task, new_airflow_task, new_airflow_task, new_airflow_task))
