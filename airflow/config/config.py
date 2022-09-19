PATH_TO_SCRUBBERS = '/scrubbers/'
NEW_DAG_EXTENSION = '.py'
PATH_TO_DAGS = '/opt/airflow/dags/'

# DAG config
LOAD_DATA_DAG_NAME = 'load_data'
LOAD_DATA_DAG_DESC = 'Load data from Python project folders'
LOAD_DATA_DAG_TAGS = ['etl']


PATH_TO_PROJECTS = '/opt/airflow/scrubbers'
CSV_DATA_FILE_EXTENSION = '.csv'
JSON_DATA_FILE_EXTENSION = '.json'

# Data Lake connection
SERVICE_NAME_S3 = 's3'
ENDPOINT_URL_S3 = 'http://10.168.0.5:9000'
ACCESS_KEY_S3 = 'lkQIBnxMJKXmKEqp'
SECRET_ACCESS_KEY_S3 = 'WCEcAL2eiKFRMJZhTGdXV7IKvwo3ed6M'
BUCKET_S3 = 'test-data-lake-bucket'

# Data Lake connection
SERVICE_NAME_S3_DWH = 's3'
ENDPOINT_URL_S3_DWH = 'http://10.168.0.5:9000'
ACCESS_KEY_S3_DWH = 'lkQIBnxMJKXmKEqp'
SECRET_ACCESS_KEY_S3_DWH = 'WCEcAL2eiKFRMJZhTGdXV7IKvwo3ed6M'
BUCKET_S3_DWH = 'test-data-warehouse-bucket'

DATAFLOW_LOCAL_STORAGE_PATH = '/opt/airflow/tmp/'

# DAG config
DAG_CREATION_DAG_NAME = 'dag_creation'
DAG_CREATION_DAG_DESC = 'DAG of factory of DAGs from Python projects'
DAG_CREATION_DAG_TAGS = ['etl']

DATAFLOW_DAG_NAME = 'dataflow'
DATAFLOW_DAG_DESC = 'DAG Dataflow from Data Lake to Data Warehouse'
DATAFLOW_DAG_TAGS = ['etl']
