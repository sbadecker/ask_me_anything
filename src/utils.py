import logging
import os

import sqlalchemy
from google.cloud import storage
from src.settings import settings

logger = logging.getLogger(__name__)


def download_blob(bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    logger.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def get_sql_url(host: str = settings.DB_HOST, db_name: str = settings.DB_NAME, user: str = settings.DB_USER,
                password: str = settings.DB_PASSWORD) -> str:
    sql_url = f"postgresql://{host}/{db_name}?user={user}&password={password}"
    return sql_url


def get_unix_socket_sql_url(db_name: str = settings.DB_NAME, user: str = settings.DB_USER,
                            password: str = settings.DB_PASSWORD,
                            cloud_sql_connection_name: str = settings.CLOUD_SQL_CONNECTION_NAME) -> str:
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    sql_url = sqlalchemy.engine.url.URL.create(
        drivername="postgresql+pg8000",
        username=user,
        password=password,
        database=db_name,
        query={
            "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                db_socket_dir,
                cloud_sql_connection_name)
        })
    return str(sql_url)
