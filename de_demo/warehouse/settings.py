from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClickhouseDatabaseSettings(BaseSettings, validate_assignment=True):
    addr: AnyHttpUrl = "http://127.0.0.1:18123"
    name: str = Field(default="default", min_length=1)
    user: str = Field(default="user", min_length=1)
    passwd: SecretStr = "pass"

    model_config = SettingsConfigDict(
        env_prefix='DD__WAREHOUSE__CLICKHOUSE__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


class WarehouseSettings(BaseSettings):
    clickhouse: ClickhouseDatabaseSettings = ClickhouseDatabaseSettings()

    model_config = SettingsConfigDict(
        env_prefix='DD__WAREHOUSE__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


settings = WarehouseSettings()
