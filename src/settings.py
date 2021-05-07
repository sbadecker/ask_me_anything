from pydantic import Field
from secrets import SecretSettings


class ProdSettings(SecretSettings):
    SECRET_HEALTH_CHECK: str = Field(..., from_secrets=True)


settings = ProdSettings()
