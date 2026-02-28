{{ config(materialized='view') }}

with src as (
    select * from {{ source('raw', 'academic_performance') }}
),

cleaned as (
    select
        cast(student_id as varchar) as student_id,
        cast(academic_year as varchar) as academic_year,
        try_cast(gpa as double) as gpa,
        try_cast(attendance_rate as double) as attendance_rate
    from src
)

select * from cleaned