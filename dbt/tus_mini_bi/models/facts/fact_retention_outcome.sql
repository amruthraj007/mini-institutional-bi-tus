{{ config(materialized='table') }}

with base as (

    select
        student_id,
        programme_id,
        academic_year,
        year_of_study
    from {{ ref('fact_enrolment_year') }}

),

-- Create a mapping from academic_year to next academic_year
year_map as (

    select
        academic_year as year_n,
        lead(academic_year) over (order by year_index) as year_n1
    from {{ ref('dim_academic_year') }}

),

n as (

    select
        b.*,
        ym.year_n1 as next_academic_year
    from base b
    left join year_map ym
        on b.academic_year = ym.year_n

),

next_year_any as (

    select distinct
        student_id,
        academic_year
    from base

),

next_year_same_prog as (

    select distinct
        student_id,
        programme_id,
        academic_year
    from base

),

final as (

    select
        n.student_id,
        n.programme_id,
        n.academic_year,

        case
            when n.next_academic_year is null then null
            when exists (
                select 1
                from next_year_any a
                where a.student_id = n.student_id
                  and a.academic_year = n.next_academic_year
            ) then 1 else 0
        end as retained_institution_next_year_flag,

        case
            when n.next_academic_year is null then null
            when exists (
                select 1
                from next_year_same_prog sp
                where sp.student_id = n.student_id
                  and sp.programme_id = n.programme_id
                  and sp.academic_year = n.next_academic_year
            ) then 1 else 0
        end as retained_same_programme_next_year_flag

    from n

)

select * from final