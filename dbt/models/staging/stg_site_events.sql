{{
    config(
      order_by = '(dt, event, target)',
      partition_by = 'toYYYYMM(dt)',
      engine = 'MergeTree()',
      materialized = 'incremental',
      incremental_strategy = 'insert_overwrite',
    )
}}
WITH site_events AS (
    SELECT
        dt,
        multiIf(
            name='view', concat(name, '_', obj),
            name='click' and obj='button', obj_id,
            name='click', concat(name, '_', obj),
            concat(name, '_',obj,'_', obj_id)
        ) as event,
        obj_id as target,
        user_id,
        url,
        name,
        obj,
        obj_id,
        product_id,
        amount,
        exp
    FROM {{ source('default', 'events_file') }}
    {% if is_incremental() %}
    WHERE dt >= toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1)
    {% else %}
    WHERE dt >= toStartOfYear(now())
    {% endif %}
)
select * from site_events
