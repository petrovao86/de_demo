from infi.clickhouse_orm import migrations

operations = [
    migrations.RunSQL("""
        CREATE VIEW events_file AS
        SELECT
            dt,
            name,
            user_id,
            url,
            obj,
            obj_id,
            product_id,
            amount,
            exp
        FROM file('events.xz', 'CSVWithNames', 'dt DateTime, name LowCardinality(String), user_id UInt64, url String, obj LowCardinality(String), obj_id String, product_id UInt64, amount Float32, exp Map(String, String)', 'xz')
        WHERE dt <= now()
    """)
]
