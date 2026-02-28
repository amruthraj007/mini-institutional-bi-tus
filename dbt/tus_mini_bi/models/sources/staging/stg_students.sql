{{ config(materialized='view') }}

with src as (
    select *
    from {{ source('raw', 'students') }}
),
cleaned as (
    select
        cast(student_id as varchar) as student_id,
        case 
            when gender is null then 'Other/Unknown'
            when lower(trim(gender)) in ('m', 'male', 'male ') then 'Male'
            when lower(trim(gender)) in ('ma le', 'm ale', 'male') then 'Male' 
            when lower(trim(gender)) in ('f', 'female', 'female ') then 'Female'
            when lower(trim(gender)) in ('fem ale', 'female') then 'Female'
            when lower(trim(gender)) in ('other', 'unknown', 'not stated', 'other/unknown') then 'Other/Unknown'
            else 'Other/Unknown'
        end as gender,

        try_cast(date_of_birth as date) as date_of_birth,

        case
            when entry_route is null then 'Unknown'
            when lower(trim(entry_route)) = 'cao' then 'CAO'
            when lower(trim(entry_route)) in ('qqi/fet', 'qqi', 'fet', 'qqi-fet') then 'QQI/FET'
            when lower(trim(entry_route)) = 'mature' then 'Mature'
            when lower(trim(entry_route)) = 'international' then 'International'
            when lower(trim(entry_route)) = 'other' then 'Other'
            else 'Unknown'
        end as entry_route,

        try_cast(access_flag as integer) as access_flag,

        case
            when nationality_group is null then 'Unknown'
            when lower(trim(nationality_group)) in ('irish', 'ireland') then 'Irish'
            when lower(trim(nationality_group)) in ('eu', 'eea') then 'EU'
            when lower(trim(nationality_group)) in ('non-eu/eea', 'non-eu', 'non-eea') then 'Non-EU'
            else 'Unknown'
        end as nationality_group,

        case 
            when home_campus is null then 'Unknown'
            else trim(home_campus)
        end as home_campus

    from src
)

select * from cleaned