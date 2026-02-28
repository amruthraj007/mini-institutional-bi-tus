{{ config(materialized='view') }}

with src as (
    select * from {{ source('raw', 'enrolments') }}
),

cleaned as (
    select
        cast(student_id as varchar) as student_id,
        cast(programme_id as varchar) as programme_id,
        cast(academic_year as varchar) as academic_year,
        try_cast(year_of_study as integer) as year_of_study,

        case
            when registration_status is null then 'Unknown'
            when lower(trim(registration_status)) = 'registered' then 'Registered'
            when lower(trim(registration_status)) = 'withdrawn' then 'Withdrawn'
            when lower(trim(registration_status)) = 'deferred' then 'Deferred'
            else 'Unknown'
        end as registration_status,

        try_cast(entrant_flag as integer) as entrant_flag

    from src
)

select * from cleaned