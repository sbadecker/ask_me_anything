from pydantic import Field

from src.secret_manager import SecretSettings


class ProdSettings(SecretSettings):
    SECRET_HEALTH_CHECK: str = Field(..., from_secrets=True)
    ELASTICSEARCH_PASSWORD: str = Field(..., from_secrets=True)
    ELASTICSEARCH_USERNAME: str = Field(..., from_secrets=True)
    ELASTICSEARCH_HOST: str = Field(..., from_secrets=True)
    ELASTICSEARCH_PORT: int = Field(..., from_secrets=True)
    READER_MODEL_NAME: str = Field(..., from_secrets=True)


settings = ProdSettings()
