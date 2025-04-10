{{ config(materialized = 'view') }}
with dau_state as (
     SELECT
        date,
        uniqState(user_id) as dauState
     FROM {{ ref('int_site_events_to_users_activity_by_day') }}
     GROUP BY date
)
SELECT
    date,
    uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN CURRENT ROW AND CURRENT ROW)  AS dau,
    uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN 7 PRECEDING AND CURRENT ROW)  AS wau,
    uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN 30 PRECEDING AND CURRENT ROW) AS mau
FROM dau_state
