from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from de_demo.warehouse.settings import ClickhouseDatabaseSettings


class ClickhouseMigrationsSettings(BaseSettings, validate_assignment=True):
    package: str = Field(default="de_demo.migrations.clickhouse", min_length=1)
    db: ClickhouseDatabaseSettings = ClickhouseDatabaseSettings()

    model_config = SettingsConfigDict(
        env_prefix='DD__MIGRATIONS__CLICKHOUSE__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


class MigrationSettings(BaseSettings):
    clickhouse: ClickhouseMigrationsSettings = ClickhouseMigrationsSettings()

    model_config = SettingsConfigDict(
        env_prefix='DD__MIGRATIONS__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
    )


settings = MigrationSettings()
