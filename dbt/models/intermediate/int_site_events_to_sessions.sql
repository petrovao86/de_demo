{{
    config(
      order_by = '(dt, event, target, url, user_id)',
      partition_by = 'toYYYYMM(dt)',
      engine = 'MergeTree()',
      materialized = 'incremental',
      incremental_strategy = 'insert_overwrite',
    )
}}
{% set session_timeout = 1800 %}

{% if is_incremental() %}
WITH last_events AS (
    select
        user_id,
        max(prev_dt) as last_prev_dt
    from {{ this }}
    where dt<toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1)
    and dt >= toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1) - toIntervalSecond({{ session_timeout }})
    group by user_id
),
{% else %}
WITH
{% endif %}
sessions AS (
    select
        dt,
        user_id,
        event,
        {% if is_incremental() %}
        if((last_value(dt) OVER (PARTITION BY user_id ORDER BY dt ROWS between 1 preceding and 1 preceding) as raw_prev_dt) = toDateTime(0), le.last_prev_dt, raw_prev_dt)  as prev_dt,
        {% else %}
        last_value(dt) OVER (PARTITION BY user_id ORDER BY dt ROWS between 1 preceding and 1 preceding) as prev_dt,
        {% endif %}
        url,
        target,
        product_id,
        amount
    FROM {{ ref('stg_site_events') }}
    {% if is_incremental() %}
    LEFT JOIN last_events AS le ON {{ ref('stg_site_events') }}.user_id = le.user_id
    WHERE dt >= toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1)
    {% endif %}
)
select
    dt,
    event,
    target,
    user_id,
    url,
    prev_dt,
    cityHash64(
        user_id,
        min(dt) OVER (PARTITION BY user_id),
        sum(dt - prev_dt > {{ session_timeout }}) OVER (PARTITION BY user_id ORDER BY dt ROWS between unbounded preceding and current row)
    ) as session_id,
    product_id,
    amount
from sessions
