from dataflow import Dataflow

# consts
# Data Lake connection
SERVICE_NAME_S3 = 's3'
ENDPOINT_URL_S3 = 'http://0.0.0.0:9000'
ACCESS_KEY_S3 = 'lkQIBnxMJKXmKEqp'
SECRET_ACCESS_KEY_S3 = 'WCEcAL2eiKFRMJZhTGdXV7IKvwo3ed6M'
BUCKET_S3 = 'test-data-lake-bucket'

# Data Lake connection
SERVICE_NAME_S3_DWH = 's3'
ENDPOINT_URL_S3_DWH = 'http://0.0.0.0:9000'
ACCESS_KEY_S3_DWH = 'lkQIBnxMJKXmKEqp'
SECRET_ACCESS_KEY_S3_DWH = 'WCEcAL2eiKFRMJZhTGdXV7IKvwo3ed6M'
BUCKET_S3_DWH = 'test-data-warehouse-bucket'

DATAFLOW_LOCAL_STORAGE_PATH = '/home/user/Desktop/sandbox/reef-etl-main/airflow/tmp/'


def main():
    dataflow = Dataflow()

    dataflow.configure_source(
            service_name=SERVICE_NAME_S3,
            endpoint_url=ENDPOINT_URL_S3,
            access_key=ACCESS_KEY_S3,
            secret_access_key=SECRET_ACCESS_KEY_S3,
            bucket=BUCKET_S3,
            local_storage_path=DATAFLOW_LOCAL_STORAGE_PATH
        )

    dataflow.configure_target(
        service_name=SERVICE_NAME_S3_DWH,
        endpoint_url=ENDPOINT_URL_S3_DWH,
        access_key=ACCESS_KEY_S3_DWH,
        secret_access_key=SECRET_ACCESS_KEY_S3_DWH,
        bucket=BUCKET_S3_DWH,
        local_storage_path=DATAFLOW_LOCAL_STORAGE_PATH
    )

    dataflow.extract_from_data_lake()
    print('extract_from_data_lake complete')

    dataflow.first_normal_form()
    print('first_normal_form complete')

    dataflow.formatting_date()
    print('formatting_date complete')

    dataflow.union_data_codec()
    print('union_data_codec complete')

    dataflow.index_data()
    print('index_data complete')

    dataflow.upload_to_data_warehouse()
    print('upload_to_data_warehouse complete')

    dataflow.delete_local_data()
    print('delete_local_data complete')


if __name__ == '__main__':
    main()