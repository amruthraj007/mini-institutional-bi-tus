{{ config(materialized='table') }}

with enrol as (

    select
        student_id,
        programme_id,
        academic_year,
        gpa_band,
        attendance_band
    from {{ ref('fact_enrolment_year') }}

),

student_dim as (

    select
        student_id,
        access_flag
    from {{ ref('dim_student') }}

),

scored as (

    select
        e.student_id,
        e.programme_id,
        e.academic_year,

        -- GPA component
        case
            when e.gpa_band = 'Low' then 2
            when e.gpa_band = 'Med' then 1
            when e.gpa_band = 'High' then 0
            else 1
        end as gpa_score,

        -- Attendance component
        case
            when e.attendance_band = 'Low' then 2
            when e.attendance_band = 'Med' then 1
            when e.attendance_band = 'High' then 0
            else 1
        end as attendance_score,

        -- Access widening participation component
        case
            when s.access_flag = 1 then 1
            else 0
        end as access_score

    from enrol e
    left join student_dim s
        on e.student_id = s.student_id

),

final as (

    select
        student_id,
        programme_id,
        academic_year,

        (gpa_score + attendance_score + access_score) as risk_score,

        case
            when (gpa_score + attendance_score + access_score) <= 1 then 'Low'
            when (gpa_score + attendance_score + access_score) = 2 then 'Medium'
            else 'High'
        end as risk_band,

        -- Keep components for explainability in dashboards
        gpa_score,
        attendance_score,
        access_score

    from scored

)

select * from final