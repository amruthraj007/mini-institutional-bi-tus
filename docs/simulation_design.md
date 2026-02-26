Synthetic Institutional Dataset – Design Notes

This repository contains a synthetic undergraduate dataset designed to simulate realistic institutional behaviour across five academic years (2020/21–2024/25).

The purpose of this simulation is to generate data that behaves like a typical university extract — including enrolments, performance, and retention — without being randomly generated noise.

The design focuses on controlled realism rather than statistical complexity.

Scope

~12,000 unique students

~2,400 new entrants per year

~40 undergraduate programmes

NFQ Levels 6, 7, 8

6 faculties

5 academic years

Target overall Year 1 → Year 2 retention: 75–85%

Datasets Generated
students_raw.csv

Grain: One row per student

Contains demographic and entry attributes including:

Gender (intentionally inconsistent values)

Entry route

Access participation flag (~18%)

Nationality group

Home campus

Minor missing values are introduced to simulate real extracts.

programmes_raw.csv

Grain: One row per programme

Includes programme metadata and a hidden simulation variable:

difficulty_factor (0.60–0.90)

This variable influences GPA and retention probability to create programme-level variation. It is not intended for reporting use.

enrolments_raw.csv

Grain: Student × Programme × Academic Year

Captures:

Year of study

Registration status

Credits attempted

Entrant flag

Simulated behaviours include:

Normal progression

Dropout

Small transfer rate (~5%)

Small repeat rate

~0.5% duplicate records (intentional)

academic_performance_raw.csv

Grain: Student × Academic Year

Includes:

GPA (1.0–4.0 scale, centred ~2.8)

Attendance rate (positively correlated with GPA)

1–2% missing values are included intentionally.

Simulation Logic (High-Level)

Retention is simulated year-to-year using a bounded probability model.

Base probability is adjusted using:

GPA band

Attendance band

Access participation

Programme difficulty

Final retention probability is constrained between 5% and 98%.

The simulation is tuned to ensure:

Overall retention between 75–85%

Clear separation by GPA and attendance

Consistent programme-level variation

Small demographic gaps (3–8 percentage points)

Design Philosophy

This dataset is intentionally:

Correlated, not random

Slightly imperfect, not clean

Believable, not exaggerated

Small enough to run locally

The goal is to create data that feels institutionally realistic while remaining fully synthetic.