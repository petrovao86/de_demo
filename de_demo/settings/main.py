from pathlib import Path
from typing import ClassVar, Tuple, Type

from pydantic_settings import (
    BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource,
    YamlConfigSettingsSource
)

from de_demo.migrations.settings import ClickhouseMigrationsSettings, MigrationSettings
from de_demo.warehouse.settings import WarehouseSettings


class Settings(BaseSettings):
    warehouse: WarehouseSettings = WarehouseSettings()
    migrations: MigrationSettings = MigrationSettings(clickhouse=ClickhouseMigrationsSettings(db=warehouse.clickhouse))

    _yaml_file: ClassVar[Path] = None
    _toml_file: ClassVar[Path] = None

    model_config = SettingsConfigDict(
        env_prefix='DD__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        sources = (init_settings, env_settings, dotenv_settings, file_secret_settings)

        if cls._toml_file:
            sources = sources + (TomlConfigSettingsSource(settings_cls, toml_file=cls._toml_file),)

        if cls._yaml_file:
            sources = sources + (YamlConfigSettingsSource(settings_cls, yaml_file=cls._yaml_file),)

        return sources


settings = Settings()
