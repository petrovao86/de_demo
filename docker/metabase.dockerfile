FROM metabase/metabase:v0.54.x
ADD https://github.com/ClickHouse/metabase-clickhouse-driver/releases/download/1.53.3/clickhouse.metabase-driver.jar /plugins/
RUN chmod 744 /plugins/clickhouse.metabase-driver.jar
