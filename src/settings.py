from pydantic import Field

from secret_manager import SecretSettings


class ProdSettings(SecretSettings):
    SECRET_HEALTH_CHECK: str = Field(..., from_secrets=True)


settings = ProdSettings()
