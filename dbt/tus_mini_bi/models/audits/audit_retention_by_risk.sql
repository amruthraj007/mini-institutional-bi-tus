{{ config(materialized='view') }}

with risk as (
    select * from {{ ref('fact_student_success_score') }}
),
ret as (
    select * from {{ ref('fact_retention_outcome') }}
),
enrol as (
    select student_id, programme_id, academic_year, entrant_flag
    from {{ ref('fact_enrolment_year') }}
)

select
    rsk.risk_band,
    count(*) as rows,
    avg(ret.retained_institution_next_year_flag) as retention_rate
from risk rsk
left join ret
    on rsk.student_id=ret.student_id and rsk.programme_id=ret.programme_id and rsk.academic_year=ret.academic_year
left join enrol e
    on rsk.student_id=e.student_id and rsk.programme_id=e.programme_id and rsk.academic_year=e.academic_year
where e.entrant_flag = 1
group by 1
order by
    case rsk.risk_band
        when 'Low' then 1
        when 'Medium' then 2
        else 3
    end