Здесь лежат миграции схемы данных хранилища. 
Их можно запускать при помощи командной строки: 
```shell
de-demo migrate clickhouse
```
При запуске проекта в [docker compose](../../../docker) запускаются автоматом после запуска ClickHouse.
См. сервис `migrator` в [docker-compose.warehouse.yml](../../../docker/docker-compose.warehouse.yml).