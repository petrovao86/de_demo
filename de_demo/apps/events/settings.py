from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from de_demo.warehouse.settings import ClickhouseDatabaseSettings


class EventsSettings(BaseSettings, validate_assignment=True):
    db: ClickhouseDatabaseSettings = ClickhouseDatabaseSettings()
    api_buffer_size: int = Field(default=100000, ge=1)
    api_queue_time: float = Field(default=10.0, gt=0.0)
    api_batch_size: int = Field(default=10000, ge=1)

    model_config = SettingsConfigDict(
        env_prefix='DD__APPS__EVENTS__',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )


settings = EventsSettings()
