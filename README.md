# Демо сервиса сбора и обработки событий
Пример сервиса аналитики, отвечающего за приём и обработку событий.
____
## Описание
- [Структура проекта](#структура-проекта)
- [Инициализация проекта](#инициализация-проекта)
- [Схема данных](#схема-данных)
- - [События сайта](#cобытия-сайта)
- [Мониторинг](#мониторинг)

## Структура проекта
Код в [de_demo](de_demo), контейнеризация в [docker](docker), тесты в [tests](tests).

## Инициализация проекта
Можно стартануть в [docker](docker) или локально.

Для запуска проекта локально, необходимо:
- Установить python 3.12([загрузки](https://www.python.org/downloads/)) 
- Установить poetry([инструкция](https://python-poetry.org/docs/#installing-with-the-official-installer))
  - TLDR: `curl -sSL https://install.python-poetry.org | python3 -`
- В корне проекта `poetry env use python3.12` и `poetry install --no-root`
- Далее см. [утилиту командной строки](#утилита-командной-строки), [тесты](#тесты)


## Схема данных
Для работы с хранилищем используется библиотека [infi-clickhouse-orm](https://github.com/Infinidat/infi.clickhouse_orm).

Схема staging слоя определяется [миграциями](de_demo/migrations/clickhouse). 
Миграции можно запускать при помощи [соответствующей утилиты командной строки](#миграции).

### События сайта
Представлены двумя [таблицами](de_demo/apps/events/warehouse), которые развертываются 
миграцией [0001_create_events.py](de_demo/migrations/clickhouse/0001_create_events.py).

## Мониторинг
Логин `admin`, пароль `admin`.
Адрес http://127.0.0.1:13000/d/q9Or1W0Nz/dashboard?orgId=1&refresh=5s
