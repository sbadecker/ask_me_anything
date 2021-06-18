import logging

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
