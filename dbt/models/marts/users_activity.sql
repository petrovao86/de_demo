{{ config(materialized = 'view') }}
select
	date,
	uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN CURRENT ROW AND CURRENT ROW) as dau,
	uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN 7 PRECEDING AND CURRENT ROW) as wau,
	uniqMerge(dauState) OVER (ORDER BY date RANGE BETWEEN 30 PRECEDING AND CURRENT ROW) as mau
FROM {{ ref('int_site_events_to_users_activity_by_day') }}
