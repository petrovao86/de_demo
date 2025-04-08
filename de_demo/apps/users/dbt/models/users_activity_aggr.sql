{{
    config(
      order_by = 'date',
      partition_by = 'toYYYYMM(date)',
      engine = 'MergeTree()',
      materialized = 'incremental',
      incremental_strategy = 'insert_overwrite',
    )
}}
WITH users_activity AS (
    SELECT
        toDate(dt) as date,
        uniqState(user_id) as dauState
    FROM {{ source('default', 'events') }}
    {% if is_incremental() %}
    WHERE dt >= toStartOfMonth((select max(date) from {{ this }})) - toIntervalMonth(1)
    {% endif %}
    GROUP BY date
)
select * from users_activity
