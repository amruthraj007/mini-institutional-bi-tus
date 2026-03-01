{{ config(materialized='view') }}

with
enrol as (select * from {{ ref('fact_enrolment_year') }}),
ret as (select * from {{ ref('fact_retention_outcome') }}),
risk as (select * from {{ ref('fact_student_success_score') }}),
stu as (select * from {{ ref('dim_student') }}),
prog as (select * from {{ ref('dim_programme') }}),
yr as (select * from {{ ref('dim_academic_year') }})

select
    -- row counts
    (select count(*) from enrol) as enrol_rows,
    (select count(*) from ret) as retention_rows,
    (select count(*) from risk) as risk_rows,
    (select count(*) from stu) as student_dim_rows,
    (select count(*) from prog) as programme_dim_rows,
    (select count(*) from yr) as year_dim_rows,

    -- join coverage checks (should be near 100%)
    (select count(*) from enrol e left join stu s on e.student_id = s.student_id where s.student_id is null) as enrol_missing_student_dim,
    (select count(*) from enrol e left join prog p on e.programme_id = p.programme_id where p.programme_id is null) as enrol_missing_programme_dim,
    (select count(*) from enrol e left join yr y on e.academic_year = y.academic_year where y.academic_year is null) as enrol_missing_year_dim,

    -- retention fact coverage
    (select count(*) from enrol e left join ret r
        on e.student_id=r.student_id and e.programme_id=r.programme_id and e.academic_year=r.academic_year
     where r.student_id is null) as enrol_missing_retention_fact,

    -- risk fact coverage
    (select count(*) from enrol e left join risk k
        on e.student_id=k.student_id and e.programme_id=k.programme_id and e.academic_year=k.academic_year
     where k.student_id is null) as enrol_missing_risk_fact
