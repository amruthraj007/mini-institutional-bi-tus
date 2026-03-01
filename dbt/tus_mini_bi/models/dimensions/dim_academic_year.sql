{{ config(materialized='table') }}

with years as (

    select distinct academic_year
    from {{ ref('stg_enrolments') }}
    where academic_year is not null
),

parsed as (

    select
        academic_year,
        try_cast(substr(academic_year, 1, 4) as integer) as start_year,
        try_cast('20' || substr(academic_year, 6, 2) as integer) as end_year
    from years
),

final as (
    select 
        academic_year, 
        start_year,
        end_year,
        dense_rank() over (order by start_year) as year_index
    from parsed

)

select * from final