from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings, validate_assignment=True):
    host: str = Field(default="127.0.0.1", min_length=1)
    port: PositiveInt = 18000
    log_level: str = Field(default="info")
    access_log: bool = False
    workers: PositiveInt = 1
    enable_metrics: bool = True

    model_config = SettingsConfigDict(
        env_prefix='DD__API__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


settings = ApiSettings()
