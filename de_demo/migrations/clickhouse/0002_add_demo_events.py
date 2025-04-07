from infi.clickhouse_orm import migrations

operations = [
    migrations.RunSQL("""
        INSERT INTO default.events (dt, name, user_id, url, obj, obj_id, product_id, amount, exp)
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
        FROM file('events.xz', 'CSV', 'dt DateTime, name LowCardinality(String), user_id UInt64, url String, obj LowCardinality(String), obj_id String, product_id UInt64, amount Float32, exp Map(String, String)', 'xz')
        WHERE dt <= now()
    """)
]
