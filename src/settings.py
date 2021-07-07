from pydantic import Field

from src.secret_manager import SecretSettings


class ProdSettings(SecretSettings):
    SECRET_HEALTH_CHECK: str = Field(..., from_secrets=True)
    READER_MODEL_NAME: str = Field(..., from_secrets=True)
    DOCUMENT_EMBEDDINGS_BUCKET_NAME: str = Field(..., from_secrets=True)
    DOCUMENT_EMBEDDINGS_FILE_NAME: str = Field(..., from_secrets=True)
    DPR_PASSAGE_ENCODER_NAME: str = Field(..., from_secrets=True)
    DPR_QUERY_ENCODER_NAME: str = Field(..., from_secrets=True)
    DB_NAME: str = Field(..., from_secrets=True)
    DB_HOST: str = Field(..., from_secrets=True)
    DB_USER: str = Field(..., from_secrets=True)
    DB_PASSWORD: str = Field(..., from_secrets=True)
    CLOUD_SQL_CONNECTION_NAME: str = Field(..., from_secrets=True)
    USE_UNIX_SOCKET: bool = Field(..., from_secrets=False)


settings = ProdSettings()
