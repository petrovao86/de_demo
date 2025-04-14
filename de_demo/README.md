- [api](api) - управление API.
- [api_clients](api_clients) - клиенты API используемые в проекте.
- [apps](apps) - модули проекта, логика работы с данными живёт здесь.
  - `apps/{module}/api/router.py` - позволяет опубликовать модуль в api 
    (приём событий, публикация статистистики через api и т.п.), регистрируется в [api](api).
  - `apps/{module}/warehouse/` - модели хранилища, используются для определения схемы staging слоя хранилища. 
    Применяются например в [migrations](migrations).
  - `apps/{module}/cli.py` - командная строка модуля, регистрируется в [cli](cli).
  - `apps/{module}/settings.py` - настройки модуля, регистрируются в [settings](settings).
- [cli](cli) - командная строка проекта.
- [dagster](dagster) - регистрация Definition'ов dagster.
- [dbt](dbt) - управление dbt.
- [migrations](migrations) - миграции.
- [settings](settings) - модуль отвечающий за настройки проекта.
- [warehouse](warehouse) - работа с хранилищем(расширение ORM, настройки подключения и т.п.).