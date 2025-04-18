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

WITH events_prev_dt AS (
    select
        dt,
        user_id,
        event,
        last_value(dt) OVER (PARTITION BY user_id ORDER BY dt ROWS between 1 preceding and 1 preceding) as prev_dt,
        url,
        target,
        product_id,
        amount
    FROM {{ ref('stg_site_events') }}
    {% if is_incremental() %}
    WHERE dt >= toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1)
    {% endif %}
),
{% if is_incremental() %}
last_events AS (
    select
        user_id,
        max(session_started_at) as last_session_started_at,
        max(user_session_id) as last_user_session_id,
        max(dt) as last_prev_dt
    from {{ this }}
    where dt<toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1)
    and dt >= toStartOfMonth((select max(dt) from {{ this }})) - toIntervalMonth(1) - toIntervalSecond({{ session_timeout }})
    group by user_id
),
{% endif %}
sessions as (
    select
        dt,
        {% if is_incremental() %}
        if(prev_dt = toDateTime(0), le.last_prev_dt, prev_dt)
        {% else %}
        prev_dt
        {% endif %} as session_prev_dt,
        {% if is_incremental() %}
        sum(
            dt - session_prev_dt > {{ session_timeout }}
        ) OVER (PARTITION BY user_id ORDER BY dt ROWS between unbounded preceding and current row)
        + le.last_user_session_id
        {% else %}
        sum(
            dt - session_prev_dt > {{ session_timeout }}
        ) OVER (PARTITION BY user_id ORDER BY dt ROWS between unbounded preceding and current row)
        {% endif %} as user_session_id,
        event,
        target,
        user_id,
        url,
        product_id,
        amount
    from events_prev_dt
    {% if is_incremental() %}
    LEFT JOIN last_events AS le ON events_prev_dt.user_id = le.user_id
    {% endif %}
)
select
    dt,
    session_prev_dt as prev_dt,
    user_session_id,
    {% if is_incremental() %}
    if(
        le.last_session_started_at>toDateTime(0),
        le.last_session_started_at,
        min(dt) OVER (PARTITION BY (user_id, user_session_id))
    )
    {% else %}
    min(dt) OVER (PARTITION BY (user_id, user_session_id))
    {% endif %} as session_started_at,
    event,
    target,
    user_id,
    url,
    product_id,
    amount
from sessions
{% if is_incremental() %}
LEFT JOIN last_events AS le ON sessions.user_id = le.user_id
{% endif %}
