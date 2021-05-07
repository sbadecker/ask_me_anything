from secrets import SecretSettings

from pydantic import Field


class ProdSettings(SecretSettings):
    SECRET_HEALTH_CHECK: str = Field(..., from_secrets=True)


settings = ProdSettings()
