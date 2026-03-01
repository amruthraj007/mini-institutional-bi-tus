{{ config(materialized='table') }}

with base as (

    select 
        student_id,
        gender,
        date_of_birth,
        entry_route,
        access_flag,
        nationality_group,
        home_campus
    from {{ ref('stg_students') }}
),

final as (

    select 
        student_id,
        gender,

        -- We are deriving age band from date of birth, which is a common practice in educational analytics to protect student privacy while still allowing for age-related analysis
        case 
            when date_of_birth is null then 'Unknown'
            when date_diff('year', date_of_birth, current_date) < 20 then '<20'
            when date_diff('year', date_of_birth, current_date) between 20 and 24 then '20-24'
            when date_diff('year', date_of_birth, current_date) between 25 and 29 then '25-34'
            else '35+'
        end as age_band,

        entry_route,
        access_flag,
        nationality_group,
        home_campus
    from base 
)

select * from final