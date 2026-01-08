
-- models/gold/dim_location.sql
-- Gold layer: Dimension Location

{{ config(
    materialized='table',
    schema='gold',
    tags=['gold', 'dimension'],
    unique_id='location_id',
    meta={'owner': 'analytics'}
) }}

WITH jobs AS (
    SELECT DISTINCT
        location_cleaned as location_raw
    FROM {{ ref('int_job_title_normalization') }}
    WHERE location_cleaned IS NOT NULL
),

location_parsed AS (
    SELECT
        location_raw,
        -- Extract city (before comma)
        CASE 
            WHEN POSITION(',' IN location_raw) > 0 
            THEN TRIM(SUBSTRING(location_raw, 1, POSITION(',' IN location_raw) - 1))
            ELSE location_raw
        END as city,
        
        -- Extract country (after comma)
        CASE 
            WHEN POSITION(',' IN location_raw) > 0 
            THEN TRIM(SUBSTRING(location_raw, POSITION(',' IN location_raw) + 1))
            ELSE 'Not Specified'
        END as country,
        
        -- Detect if remote
        CASE 
            WHEN location_raw LIKE '%remote%' 
            THEN 'Remote'
            ELSE 'On-site'
        END as work_location_type
    FROM jobs
),

ranked_locations AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY location_raw) as location_id,
        location_raw,
        city,
        country,
        work_location_type,
        NOW() as created_at
    FROM location_parsed
)

SELECT
    location_id,
    location_raw,
    city,
    country,
    work_location_type,
    created_at
FROM ranked_locations
ORDER BY location_id
