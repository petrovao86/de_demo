{{ config(materialized = 'view') }}
select
    session_id,
    min(dt) as started_at,
    max(dt) - min(dt) as duration
FROM {{ ref('int_site_events_to_sessions') }}
GROUP by session_id
