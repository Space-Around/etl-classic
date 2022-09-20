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
ENDPOINT_URL_S3 = 'https://storage.googleapis.com'
ACCESS_KEY_S3 = 'GOOG6UBFBJZR6HG3V3PQGJB4'
SECRET_ACCESS_KEY_S3 = 'hlEE8ctDKZPiPaDSMrhKt+CFXbjNEAVusEgWrD1x'
BUCKET_S3 = 'prod-data-lake-storage'

# Data Lake connection
SERVICE_NAME_S3_DWH = 's3'
ENDPOINT_URL_S3_DWH = 'https://storage.googleapis.com'
ACCESS_KEY_S3_DWH = 'GOOG6UBFBJZR6HG3V3PQGJB4'
SECRET_ACCESS_KEY_S3_DWH = 'hlEE8ctDKZPiPaDSMrhKt+CFXbjNEAVusEgWrD1x'
BUCKET_S3_DWH = 'prod-data-warehouse-storage'

DATAFLOW_LOCAL_STORAGE_PATH = '/opt/airflow/tmp/'

# DAG config
DAG_CREATION_DAG_NAME = 'dag_creation'
DAG_CREATION_DAG_DESC = 'DAG of factory of DAGs from Python projects'
DAG_CREATION_DAG_TAGS = ['etl']

DATAFLOW_DAG_NAME = 'dataflow'
DATAFLOW_DAG_DESC = 'DAG Dataflow from Data Lake to Data Warehouse'
DATAFLOW_DAG_TAGS = ['etl']
