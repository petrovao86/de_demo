{{
    config(
      order_by = '(date, user_id)',
      partition_by = 'toYYYYMM(date)',
      engine = 'MergeTree()',
      materialized = 'incremental',
      incremental_strategy = 'insert_overwrite',
    )
}}
WITH users_summary_by_day AS (
    SELECT
        toDate(dt) as date,
        user_id,
        min(dt) as first_seen_at,
        max(dt) as last_seen_at,

        min(if(event = 'view_page' AND target = 'product', dt, toDateTime(0) - 1)) as first_product_view_at,
        max(if(event = 'view_page' AND target = 'product', dt, toDateTime(0))) as last_product_view_at,
        sum(event = 'view_page' AND target = 'product') as product_view_cnt,
        sumIf(amount, event = 'view_page' AND target = 'product') as product_view_amount,

        min(if(event = 'add_to_cart', dt, toDateTime(0) - 1)) as first_add_to_cart_at,
        max(if(event = 'add_to_cart', dt, toDateTime(0)) ) as last_add_to_cart_at,
        sum(event = 'add_to_cart') as add_to_cart_cnt,
        sumIf(amount, event = 'add_to_cart') as add_to_cart_amount,

        min(if(event = 'checkout', dt, toDateTime(0) - 1)) as first_checkout_at,
        max(if(event = 'checkout', dt, toDateTime(0)) ) as last_checkout_at,
        sum(event = 'checkout') as checkout_cnt,
        sumIf(amount, event = 'checkout') as checkout_amount
    FROM {{ ref('stg_site_events') }}
    {% if is_incremental() %}
    WHERE dt >= toStartOfMonth((select max(date) from {{ this }})) - toIntervalMonth(1)
    {% endif %}
    GROUP BY date, user_id
)
select * from users_summary_by_day