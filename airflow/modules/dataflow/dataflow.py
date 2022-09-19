import os
import boto3
import codecs
import pandas as pd
from dateutil.parser import parse


def to_timestamp(string: str, fuzzy: bool=False):
    """
    Return timestamp.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        dt = parse(string, fuzzy=fuzzy)
        return str(int(round(dt.timestamp())))
    except Exception:
        return float('nan')


def is_date(string: str, fuzzy: bool=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)

        if len(string) < 6:
            return False

        return True
    except Exception:
        return False


class Dataflow:
    def __init__(self):
        # source storage connection data
        self.service_name_s3_s: str = ''
        self.endpoint_url_s3_s: str = ''
        self.access_key_s3_s: str = ''
        self.secret_access_key_s3_s: str = ''
        self.bucket_s3_s: str = ''

        # target storage connection data
        self.service_name_s3_t: str = ''
        self.endpoint_url_s3_t: str = ''
        self.access_key_s3_t: str = ''
        self.secret_access_key_s3_t: str = ''
        self.bucket_s3_t: str = ''

        # common
        self.default_codec = 'utf-8'
        self.default_blocksize = 1024
        self.local_storage_path = ''

    def configure_source(self, service_name: str, endpoint_url: str, access_key: str, secret_access_key: str,
                         bucket: str, local_storage_path: str):
        """
        Configure connection to Data Lake via S3 protocol.

        :param service_name:
        :param endpoint_url:
        :param access_key:
        :param secret_access_key:
        :param bucket:
        :param local_storage_path:
        :return:
        """
        self.service_name_s3_s = service_name
        self.endpoint_url_s3_s = endpoint_url
        self.access_key_s3_s = access_key
        self.secret_access_key_s3_s = secret_access_key
        self.bucket_s3_s = bucket
        self.local_storage_path = local_storage_path

    def configure_target(self, service_name: str, endpoint_url: str, access_key: str, secret_access_key: str,
                         bucket: str, local_storage_path: str):
        """
        Configure connection to Data Warehouse via S3 protocol.

        :param service_name:
        :param endpoint_url:
        :param access_key:
        :param secret_access_key:
        :param bucket:
        :param local_storage_path:
        :return:
        """
        self.service_name_s3_t = service_name
        self.endpoint_url_s3_t = endpoint_url
        self.access_key_s3_t = access_key
        self.secret_access_key_s3_t = secret_access_key
        self.bucket_s3_t = bucket
        self.local_storage_path = local_storage_path

    def extract_from_data_lake(self):
        """
        Extract data from Data Lake to local storage.

        :return:
        """
        session = boto3.session.Session()
        s3_s = session.client(
            service_name=self.service_name_s3_s,
            endpoint_url=self.endpoint_url_s3_s,
            aws_access_key_id=self.access_key_s3_s,
            aws_secret_access_key=self.secret_access_key_s3_s
        )

        for key in s3_s.list_objects(Bucket=self.bucket_s3_s)['Contents']:
            s3_s.download_file(self.bucket_s3_s, key['Key'], f"{self.local_storage_path}{key['Key']}")

    def first_normal_form(self):
        """
        Reach first normal form.

        :return:
        """
        files = os.listdir(self.local_storage_path)

        for file in files:
            if '.csv' not in file:
                continue

            df = pd.read_csv(f"{self.local_storage_path}{file}")
            df.drop_duplicates()
            df.to_csv(f"{self.local_storage_path}{file}")

    def formatting_date(self):
        """
        Formatting data that is of date type.

        :return:
        """
        files = os.listdir(self.local_storage_path)

        for file in files:
            date_type_columns = []
            if '.csv' not in file:
                continue

            df = pd.read_csv(f"{self.local_storage_path}{file}")

            df_is_date = df.aggregate(lambda s: s.aggregate(is_date))

            df_id_date_value_count = df_is_date.aggregate(lambda s: s.groupby(s).count()).transpose().fillna(0)

            df_id_date_value_count.aggregate(
                lambda s: date_type_columns.append(s.name) if list(s)[0] < list(s)[1] else None,
                axis=1)

            for column in date_type_columns:
                df[column] = df[column].aggregate(to_timestamp)

            df.to_csv(f"{self.local_storage_path}{file}")

    def union_data_codec(self):
        """
        Changing the file codec.

        :return:
        """
        files = os.listdir(self.local_storage_path)
        for file in files:
            if '.csv' not in file:
                continue

            with codecs.open(f"{self.local_storage_path}{file}", "r", f"{self.default_codec}") as source_file:
                with codecs.open(f"{self.local_storage_path}/{self.default_codec}_{file}", "w", self.default_codec) as target_file:
                    while True:
                        contents = source_file.read(self.default_blocksize)
                        if not contents:
                            break
                        target_file.write(contents)

            os.remove(f"{self.local_storage_path}{file}")
            os.rename(f"{self.local_storage_path}{self.default_codec}_{file}", f"{self.local_storage_path}{file}")

    def index_data(self):
        """
        Index data.

        :return:
        """
        files = os.listdir(self.local_storage_path)

        for file in files:
            if '.csv' not in file:
                continue

            df = pd.read_csv(f"{self.local_storage_path}{file}")
            df.to_csv(f"{self.local_storage_path}{file}", index=True)

    def upload_to_data_warehouse(self):
        """
        Upload data from local storage to Data Warehouse.

        :return:
        """
        files = os.listdir(self.local_storage_path)

        session = boto3.session.Session()
        s3_t = session.client(
            service_name=self.service_name_s3_t,
            endpoint_url=self.endpoint_url_s3_t,
            aws_access_key_id=self.access_key_s3_t,
            aws_secret_access_key=self.secret_access_key_s3_t
        )
        for file in files:
            s3_t.upload_file(
                Filename=f"{self.local_storage_path}{file}",
                Bucket=self.bucket_s3_t,
                Key=file
            )

    def delete_local_data(self):
        """
        Delete local data.

        :return:
        """
        files = os.listdir(self.local_storage_path)

        for file in files:
            os.remove(f"{self.local_storage_path}{file}")

