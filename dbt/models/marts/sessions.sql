{{ config(materialized = 'view') }}
select
    cityHash64(
        user_id,
        session_started_at,
        user_session_id
    ) as session_id,
    min(dt) as started_at,
    max(dt) - min(dt) as duration
FROM {{ ref('int_site_events_to_user_sessions') }}
GROUP by session_id
