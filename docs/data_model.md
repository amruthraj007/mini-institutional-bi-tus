Data Model Overview:

Architecture:

This project implements a prototype institutional Business Intelligence environment using a star schema data warehouse architecture built in DuckDB and transformed using dbt.

The design separates fact and dimension tables to ensure scalability, clarity, and analytical flexibility.

Primary Analytical Grain:

Student – Programme – Academic Year

This grain supports:

- Institutional retention metrics
- Programme-level performance analysis
- Student-level risk segmentation

Dimension Tables:

dim_student:Contains demographic and cohort attributes, including:

- student_id
- access_flag
- gender

dim_programme

Contains programme-level descriptors:

- programme_id
- programme_name
- faculty
- NFQ_level
- mode

dim_academic_year: Contains academic year reference data.

Fact Tables:

fact_enrolment_year: Annual student enrolment records.

fact_retention_outcome: Derived Year 1 retention outcomes (institutional and programme-level).

fact_student_success_score: Student-level success score and risk classification.

Tools Used:
1. DuckDB - Analytical warehouse
2. dbt - Transformations, modelling, testing
3. Python - Synthetic dataset generation
4. Tableau - Data visualisation and dashboards
5. GitHub - Version control