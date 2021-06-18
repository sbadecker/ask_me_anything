import abc
import logging
from os import environ as env
import os
from typing import Any, Dict, Optional

from google.api_core.exceptions import NotFound as GoogleAPICoreExceptionNotFound
from google.cloud import secretmanager
from google.auth.exceptions import DefaultCredentialsError
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable

logger = logging.getLogger(__name__)

# A global client so we only establish one connection.
# You should always use get_secrets_client() to access this.
_client: Optional[secretmanager.SecretManagerServiceClient] = None

# Make sure the service account secrets are in the src directory
env["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     "gcloud_service_account_secret.json")
logger.info(f"Set google crential path to {env['GOOGLE_APPLICATION_CREDENTIALS']}.")


def get_secrets_client():
    global _client
    if not _client:
        try:
            _client = secretmanager.SecretManagerServiceClient()
        except DefaultCredentialsError:
            pass
    return _client


def _retrieve_secrets_from_google_secrets_manager(settings: BaseSettings) -> Dict[str, Any]:
    secrets: Dict[str, Optional[str]] = {}

    project_id = getattr(settings.__config__, "project_id", None)
    if not project_id:
        return secrets

    for field in settings.__fields__.values():
        if field.field_info.extra.get("from_secrets", False):
            env_name = field.name
            client = get_secrets_client()
            if client:
                secret_path = client.secret_path(project_id, env_name)
                secret_path += "/versions/latest"
                try:
                    resp = client.access_secret_version(name=secret_path)
                    secrets[field.alias] = resp.payload.data.decode("utf8")
                except GoogleAPICoreExceptionNotFound:
                    pass  # secret wasn't found, hopefully it's in the env

    return secrets


class SecretSettings(BaseSettings, abc.ABC):
    class Config:
        project_id = "linear-element-311408"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ):
            return env_settings, _retrieve_secrets_from_google_secrets_manager
