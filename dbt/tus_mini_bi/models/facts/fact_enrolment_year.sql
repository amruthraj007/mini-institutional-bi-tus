{{ config(materialized='table') }}

with e as (

    select *
    from {{ ref('stg_enrolments') }}
    where registration_status = 'Registered'

),

-- Deduplicate any raw enrolment records to ensure we have one record per student per programmes and academic year  

e_dedup as (

    select *
    from (
        select 
            e.*, 
            row_number() over (
                partition by student_id, programme_id, academic_year
                order by entrant_flag desc, year_of_study desc
            ) as rn
        from e
    )
    where rn = 1
),

p as (

    select 
        student_id,
        academic_year,
        gpa,
        attendance_rate
    from {{ ref('stg_academic_performance') }}
),

prog as (

    select 
        programme_id,
        mode
    from {{ ref('dim_programme') }}
),

final as (

    select 
        e.student_id,
        e.programme_id,
        e.academic_year,
        e.year_of_study,
        e.entrant_flag,

        -- Credits derived from mode 
        case 
            when prog.mode = 'FT' then 60
            when prog.mode = 'PT' then 30
            else null
        end as credits_attempted,

        p.gpa,
        p.attendance_rate,

        -- Derived bands 
        case 
            when p.gpa is null then 'Unknown'
            when p.gpa < 2.0 then 'Low'
            when p.gpa < 3.2 then 'Medium'
            else 'High'
        end as gpa_band,

        case
           when p.attendance_rate is null then 'Unknown'
           when p.attendance_rate < 0.70 then 'Low'
           when p.attendance_rate < 0.9 then 'Medium'
           else 'High'
        end as attendance_band
    
    from e_dedup e
    left join prog
       on e.programme_id = prog.programme_id
    left join p
         on e.student_id = p.student_id
        and e.academic_year = p.academic_year

)

select * from final