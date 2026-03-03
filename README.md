Mini Institutional Retention & Student Success BI Environment – TUS

Overview:
This project presents a prototype institutional Business Intelligence (BI) environment designed to analyse first-year student retention and progression at Technological University of the Shannon (TUS).

The objective was to simulate a warehouse-first, governance-aware analytics framework aligned with higher education reporting and student success monitoring practices.

The environment integrates dimensional modelling, standardised KPI definitions, and interpretable risk segmentation to demonstrate how institutional performance reporting can support both strategic oversight and operational intervention.


Project Scope:
- Focus: Year 1 entrants (First-Year Cohorts)
- Time horizon: Five academic years
- Primary metrics: Institutional retention (Y1→Y2), programme retention, student risk segmentation
- Analytical grain: Student – Programme – Academic Year

This project uses synthetic data for demonstration purposes only.

Architecture:

The solution follows a classic star-schema warehouse design:

Dimensions:

- dim_student
- dim_programme
- dim_academic_year

Fact Tables:

- fact_enrolment_year
- fact_retention_outcome
- fact_student_success_score

The warehouse is built in DuckDB and transformed using dbt.

Dashboards:

Three Tableau dashboards were developed:

1. Institutional Overview: High-level KPIs, retention trends, and benchmark comparison.
2. Programme Performance: Programme-level retention ranking, cohort size analysis, and trend comparison.
3. Student Success & Risk Insights: Risk segmentation using composite success score and retention outcomes by risk band.

Student Success Model:

A transparent composite success score was developed using:

- GPA (normalised to 100 scale)
- Attendance rate

Students are segmented into Low, Medium, and High risk bands to illustrate targeted intervention analysis.

Full methodology available in /docs/success_model.md.

Tech Stack:
- Python – Synthetic dataset generation
- DuckDB – Analytical warehouse
- dbt – Transformations, modelling, testing
- SQL – Data modelling
- Tableau – Visualisation & dashboards
- GitHub – Version control

Documentation:
Supporting documentation available in /docs:

- Executive Summary
- KPI Definitions
- Data Model Overview
- Data Quality & Assumptions
- Student Success Model

Reproducibility:

To reproduce the warehouse
1. Generate synthetic data via /scripts
2. Run dbt models
3. Connect Tableau to the exported analytical views

Purpose:

This project was developed as part of an application process to demonstrate practical capability in:

- Institutional BI modelling
- KPI governance
- Dimensional warehouse design
- Student retention analytics
- Risk segmentation logic