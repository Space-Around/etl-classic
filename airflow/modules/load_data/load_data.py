import os
import uuid
import boto3


class LoadData:
    """
    Manage load data to Data Lake throw S3 protocol.

    Attributes:
    service_name_s3         S3 service name
    endpoint_url_s3         Endpoint URL to S3 service
    access_key_s3           Access key
    secret_access_key_s3    Secret access key
    bucket_s3               Bucket name
    path_to_projects        Path to Python project folders
    extension               Files extension's to be uploaded
    """
    def __init__(self):
        self.service_name_s3: str = ''
        self.endpoint_url_s3: str = ''
        self.access_key_s3: str = ''
        self.secret_access_key_s3: str = ''
        self.bucket_s3: str = ''
        self.path_to_projects: str = ''
        self.extension: list = []

    def configure(self, service_name: str, endpoint_url: str, access_key: str, secret_access_key: str, bucket: str,
                  path_to_projects: str, extension: list):
        """
        Configure for S3 connection.

        :param service_name: Service name
        :param endpoint_url:  Endpoint URL
        :param access_key:  Access key
        :param secret_access_key: Secret access key
        :param bucket: S3 bucket name in storage
        :param path_to_projects: Path to folders with data
        :param extension: Extension of files that necessary to upload
        :return:
        """
        self.service_name_s3 = service_name
        self.endpoint_url_s3 = endpoint_url
        self.access_key_s3 = access_key
        self.secret_access_key_s3 = secret_access_key
        self.bucket_s3 = bucket
        self.path_to_projects = path_to_projects
        self.extension = extension

    def get_files(self, project_folders: list):
        """
        Get files.

        :param project_folders: list of Python project folders name
        :return: list of files
        """
        scrubbers_data_files: list = []

        for project_folder in project_folders:
            try:
                files = os.listdir(f'{self.path_to_projects}/{project_folder}')
                for file in files:
                    if any([e in file for e in self.extension]):
                        scrubbers_data_files.append({project_folder: file})
            except Exception:
                pass
        return scrubbers_data_files

    def delete_files(self, project_folders: list):
        """
        Delete data files of Python projects.

        :param project_folders: list of Python project folders name
        :return:
        """
        for project_folder in project_folders:
            try:
                files = os.listdir(f'{self.path_to_projects}/{project_folder}')
                for file in files:
                    if any([e in file for e in self.extension]):
                        os.remove(f'{self.path_to_projects}/{project_folder}')
            except Exception:
                pass

    def extract_load(self, dags: list):
        """
        Collect data from scrubber and load to Data Lake throw S3 protocol.

        :param dags: list of dags required to upload
        :return:
        """
        scrubbers_data_mapping: list = self.get_files(dags)

        session = boto3.session.Session()
        s3 = session.client(
            service_name=self.service_name_s3,
            endpoint_url=self.endpoint_url_s3,
            aws_access_key_id=self.access_key_s3,
            aws_secret_access_key=self.secret_access_key_s3
        )

        for scrubber_data_mapping in scrubbers_data_mapping:
            project_name = list(scrubber_data_mapping.keys())[0]
            file_name = scrubber_data_mapping[project_name]

            id = str(uuid.uuid4())

            filename, file_extension = os.path.splitext(f'{self.path_to_projects}/{project_name}/{file_name}')

            os.rename(f'{self.path_to_projects}/{project_name}/{file_name}', f'{self.path_to_projects}/{project_name}/{id}_{project_name}{file_extension}')

            try:
                s3.upload_file(
                    Filename=f'{self.path_to_projects}/{project_name}/{id}_{project_name}{file_extension}',
                    Bucket=self.bucket_s3,
                    Key=f"{id}_{project_name}{file_extension}"
                )

                os.remove(f'{self.path_to_projects}/{project_name}/{id}_{project_name}{file_extension}')
            except Exception as err:
                print(err)

        self.delete_files(dags)
