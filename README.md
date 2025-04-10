# Демо сервиса сбора и обработки событий
Пример сервиса аналитики, отвечающего за приём и обработку событий.
____
## Описание
- [Демонстрационные данные](#демонстрационные-данные)
- [Архитектура решения](#архитектура-решения)
- [Схема данных](#схема-данных)
  - [События сайта](#cобытия-сайта)
  - [Пользовательская активность](#пользовательская-активность)
- [Структура проекта](#структура-проекта)
- [Инициализация проекта](#инициализация-проекта)
- [BI](#bi)
- [dbt](#dbt)
- [API](#api)
- [Мониторинг](#мониторинг)

## Демонстрационные данные
Исторником данных является воображаемый интернет-магазин с 4мя товарами по которому перемещаются 
пользователи:
![Сайт](docs/images/de_demo_site.svg)

## Архитектура решения
Действия пользователей принимаются в [api](#api), и батчами пишутся в [clickhouse](#cобытия-сайта).
Дальнейшая обработка данных происходит при помощи [dbt](#dbt), результаты отображаются в [BI](#bi).
![Pipeline](docs/images/de_demo_arch_gen_2_scheduler_dbt.svg)

## Схема данных
Для работы с хранилищем используется библиотека [infi-clickhouse-orm](https://github.com/Infinidat/infi.clickhouse_orm).

Схема staging слоя определяется [миграциями](de_demo/migrations/clickhouse).

### События сайта
Представлены двумя [таблицами](de_demo/apps/events/warehouse), которые развертываются 
миграцией [0001_create_events.py](de_demo/migrations/clickhouse/0001_create_events.py).

### Пользовательская активность
Расчёт [метрик пользовательской активности](de_demo/apps/users/dbt/models) производится при помощи [dbt](#dbt).
В [intermediate слой](dbt/models/intermediate/int_site_events_to_users_activity_by_day.sql) 
при помощи [-State](https://clickhouse.com/docs/sql-reference/aggregate-functions/combinators#-state) 
комбинатора инкрементально пишутся агрегаты по дням, 
витрина представлена [вьюхой](dbt/models/marts/users_activity.sql) 
агрегирующей промежуточные данные за требуемое кол-во дней оконными функциями.


## Структура проекта
* Код в [de_demo](de_demo) 
* Контейнеризация в [docker](docker)
* Тесты в [tests](tests)

## Инициализация проекта
Можно стартануть в [docker](docker) или локально.

Для запуска проекта локально, необходимо:
- Установить python 3.12([загрузки](https://www.python.org/downloads/)) 
- Установить poetry([инструкция](https://python-poetry.org/docs/#installing-with-the-official-installer))
  - TLDR: `curl -sSL https://install.python-poetry.org | python3 -`
- В корне проекта `poetry env use python3.12` и `poetry install --no-root --all-extras`
- Далее см. [утилиту командной строки](#утилита-командной-строки), [тесты](#тесты)



## BI
В рамках проекта развёрнут BI на базе [metabase](https://www.metabase.com/).
Логин `test@test.test`, пароль `1!!test!!1`.

Адрес http://127.0.0.1:13001/

## dbt
Запуск dbt `de-demo run dbt`.  Файл настроек проекта [dbt_project.yml](dbt/dbt_project.yml).

## API
При запуске в docker, стартует автоматом. 

Запуск API руками `de-demo run api`.
> ! Для запуска api нужен запущенный clickhouse: 
> 
> `docker compose -f ./docker/docker-compose.warehouse.yml -p de_demo up --build -d`

Сервис приёма событий написан на python с использованием фреймворка FastAPI.

Документация API:
 - Swagger: http://127.0.0.1:18000/docs
 - Redoc: http://127.0.0.1:18000/redoc

Код endpoint'а событий сайта находится [тут](de_demo/apps/events/api).

## Мониторинг
Логин `admin`, пароль `admin`.

Адрес http://127.0.0.1:13000/d/q9Or1W0Nz/dashboard?orgId=1&refresh=5s
