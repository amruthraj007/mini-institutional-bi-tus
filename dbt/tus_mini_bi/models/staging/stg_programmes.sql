{{ config(materialized='view') }}

with src as (
    select * from {{ source('raw', 'programmes') }}
),

cleaned as (
    select
        cast(programme_id as varchar) as programme_id,
        trim(programme_name) as programme_name,

        -- faculty may have lowercase noise from simulation
        case
            when faculty is null then 'Unknown'
            else
                -- title-case simple normalisation for known faculties
                case lower(trim(faculty))
                    when 'business' then 'Business'
                    when 'engineering' then 'Engineering'
                    when 'science' then 'Science'
                    when 'arts' then 'Arts'
                    when 'health' then 'Health'
                    when 'computing' then 'Computing'
                    else trim(faculty)
                end
        end as faculty,

        try_cast(nfq_level as integer) as nfq_level,

        case
            when mode is null then 'Unknown'
            when upper(trim(mode)) in ('FT', 'FULL-TIME', 'FULL TIME') then 'FT'
            when upper(trim(mode)) in ('PT', 'PART-TIME', 'PART TIME') then 'PT'
            else 'Unknown'
        end as mode,

        case
            when campus is null then 'Unknown'
            else trim(campus)
        end as campus

    from src
)

select * from cleaned