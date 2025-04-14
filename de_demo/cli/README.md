Модуль реализует утилиту командной строки проекта, утилита зарегистрирована в [pyproject.toml](../../pyproject.toml).

Команды и группы команд регистрируются здесь. 
Пример регистрации см. в [de_demo.api.cli:ApiCli](../api/cli.py) или [de_demo.migrations.cli:MigrateCli](../migrations/cli.py)

Доступные команды:
- `generate` - запуск генераторов данных.
  - `events` - генерация событий.
- `metabase` - управление объектами Metabase.
  - `create_card` - создать карточку в metabase из json-файла конфигурации.
  - `dump_card` - вывести json-конфигурацию карточки metabase.
- `migrate` - запуск миграций.
  - `clickhouse` - миграция БД ClickHouse.
  - `metabase` - создание пользователя, подключение базы ClickHouse, развёртывание отчётов Metabase.
- `run` - запуск сервисов.
  - `api` - запуск API.
  - `dbt` - запуск dbt.
- `settings` - текущие настройки.
