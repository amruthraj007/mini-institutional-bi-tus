# Data Generation Plan (Synthetic Raw Extracts)

## Outputs (written to data/raw/)
- students_raw.csv
- programmes_raw.csv
- enrolments_raw.csv
- academic_performance_raw.csv

## Parameters
- academic_years: 2020/21–2024/25 (5 years)
- n_programmes: 40
- total_students: ~12,000 (~2,400 new entrants/year)
- seed: fixed for reproducibility

## High-level flow
1. Generate programmes catalogue (faculty, NFQ, mode, campus, difficulty_factor)
2. Generate student master records (DOB, gender, entry_route, access_flag, etc.)
3. For each academic year:
   a. create new entrant cohort
   b. assign each new entrant to a programme
   c. generate performance for that year (gpa, attendance)
   d. decide retention into next year using probability model
   e. if retained, create next-year enrolment record (possibly transfer/repeat)
4. Write raw extracts (CSVs) with small intentional imperfections

## Validation checks
- unique students ≈ 12k
- retention Y1→Y2 overall ≈ 75–85%
- retention differs by GPA/attendance/risk
- programme-level variation visible