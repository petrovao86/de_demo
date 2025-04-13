import sys
from pathlib import Path

import fire

from de_demo.api.cli import ApiCli
from de_demo.apps.events.cli import GeneratorCli as EventsGeneratorCli
from de_demo.dbt.cli import DbtCli
from de_demo.migrations.cli import MigrateCli
from de_demo.settings.main import Settings


class RunCli:
    """Запуск сервисов и утилит."""

    @property
    def api(self):
        return ApiCli()

    @property
    def dbt(self):
        return DbtCli()


class GenerateCli:
    """Запуск генераторов."""

    @property
    def events(self):
        return EventsGeneratorCli()


class Cli:
    """Клиент командной строки для de-demo.

    Args:
        settings (str): Путь до файла настроек.
        env_prefix (str): Префикс переменных окружения.
    """
    def __init__(
            self,
            settings: str = "./dd.yaml",
            env_prefix: str = "DD_"
    ):
        path = Path(settings)
        if path.exists() and path.is_file():
            if path.suffix == ".yaml":
                Settings._yaml_file = path
                self._settings = Settings(_env_prefix=env_prefix)
            elif path.suffix == ".toml":
                Settings._toml_file = path
                self._settings = Settings(_env_prefix=env_prefix)
            elif path.suffix == ".env":
                self._settings = Settings(_env_file=path, _env_prefix=env_prefix)
            else:
                raise ValueError(f"unknown settings file format {path}")
        else:
            self._settings = Settings(_env_prefix=env_prefix)

    @property
    def settings(self):
        return self._settings.model_dump_json(indent=4)

    @property
    def run(self):
        return RunCli()

    @property
    def migrate(self):
        return MigrateCli()

    @property
    def generate(self):
        return GenerateCli()


def run():
    try:
        fire.Fire(Cli)
    except Exception as e:
        print(e)
        sys.exit(1)
