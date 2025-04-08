from pydantic import AnyHttpUrl, EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from de_demo.warehouse.settings import ClickhouseDatabaseSettings


class MetabaseMigrationsSettings(BaseSettings, validate_assignment=True):
    addr: AnyHttpUrl = "http://127.0.0.1:13001/"
    user: str = Field(default="test", min_length=1)
    email: str = "test@test.test"
    passwd: SecretStr = "1!!test!!1"
    locale: str = "en"
    site_name: str = "test"
    db_engine: str = "clickhouse"
    db_name: str = "ch"
    db: ClickhouseDatabaseSettings = ClickhouseDatabaseSettings()

    model_config = SettingsConfigDict(
        env_prefix='DD__MIGRATIONS__METABASE__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


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
    metabase: MetabaseMigrationsSettings = MetabaseMigrationsSettings()

    model_config = SettingsConfigDict(
        env_prefix='DD__MIGRATIONS__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
    )


settings = MigrationSettings()
