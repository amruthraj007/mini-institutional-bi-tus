{{ config(materialized='table') }}

select 
    programme_id,
    programme_name,
    faculty,
    nfq_level,
    mode,
    campus
from {{ ref('stg_programmes') }}