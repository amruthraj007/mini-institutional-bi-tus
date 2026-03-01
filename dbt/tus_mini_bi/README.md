Mini Institutional BI Environment
Student Retention & Success Analytics Prototype

Executive Summary:

This project is a prototype institutional Business Intelligence (BI) environment designed to simulate how a university could monitor student retention, progression, and student success in a structured, governed way.

The goal was to build more than just dashboards. The objective was to demonstrate how raw institutional data can be transformed into a decision-ready analytical environment using a classic star schema warehouse design, validated KPI logic, and a transparent student success model.

The result is a reproducible, end-to-end workflow that covers:

- Synthetic institutional data simulation

- Data loading into a warehouse (DuckDB)

- Structured transformation using dbt

- Star schema modelling (dimensions + facts)

- Retention and progression metrics

- A transparent student risk scoring model

- Validation via audit models

- Dashboard-ready outputs

This project reflects how a modern institutional BI function can support leadership, academic management, and student support services with trusted, well-defined metrics.

What This Project Demonstrates:

This prototype showcases:

- Classic Star Schema warehouse design

- Governed KPI definitions (retention, progression, entrants)

- Student success modelling using transparent scoring logic

- Data validation through structured audit checks

- Reproducible data pipeline (Python → DuckDB → dbt → BI)

- Dashboard-ready analytical outputs

The focus is not just technical implementation, but structured analytical thinking aligned with institutional decision-making.

Architecture Overview:

The project follows a layered approach commonly used in BI environments:

Raw Data → Staging Layer → Star Schema → Dashboards

Raw Layer:

Synthetic extracts simulate institutional systems:

1. Students
2. Programmes
3. Enrolments
4. Academic performance

Staging Layer (stg_*):

- Standardises and cleans source data
- Preserves source grain
- Applies basic quality controls

Star Schema (Analytical Layer):
Dimensions

1. dim_student
2. dim_programme
3. dim_academic_year

Fact Tables

1. fact_enrolment_year
2. fact_retention_outcome
3. fact_student_success_score

All fact tables are built at the grain:

student_id – programme_id – academic_year

Institutional KPIs Implemented

The environment supports:

- New Entrants (Year 1 headcount)
- Institutional Retention Rate (Year 1 → Year 2)
- Same-Programme Retention Rate
- Retention Trend (5 academic years)
- Retention by Faculty / Programme
- Retention by Demographic Group
- Programme Ranking by Retention
- Student Risk Distribution (Low / Medium / High)
- Retention by Risk Band

KPI logic is implemented in dbt to ensure definitions are consistent and governed.

Student Success Model:

A transparent student risk scoring model is included to simulate an early-alert style success framework.

Inputs:

- GPA band
- Attendance band
- Access (widening participation) flag

Method:

A simple points-based scoring system assigns risk scores based on academic and engagement indicators.

Risk bands:

- Low
- Medium
- High

Validation confirms a clear retention gradient:

- Low Risk → Highest Retention
- Medium Risk → Moderate Retention
- High Risk → Lowest Retention

This demonstrates a sample modelling logic integration into a governed BI environment but not using complex machine learning pipelines.

Data Validation & Quality Controls:

To ensure reliability, the project includes audit models that:

- Confirm star schema row alignment
- Detect missing dimension joins
- Validate retention logic
- Confirm risk segmentation behaves logically

Example validation commands:

dbt run -s audit_star_schema
dbt run -s audit_business_metrics
dbt run -s audit_retention_by_risk

Tech Stack:

- DuckDB –  Analytical warehouse
- dbt – Transformations, modelling, testing
- Python – Data simulation and loading
- Tableau – Dashboard layer
- Git/GitHub – Version control

The environment is fully reproducible.

How to Run the Project
1️. Create Python Environment

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

2️. Generate Synthetic Data

python scripts/generate_synthetic_data.py

3️. Load Data into DuckDB

python scripts/load_raw_to_duckdb.py

4️. Run dbt Models

cd dbt/tus_mini_bi
dbt run
dbt test

Dashboard Layer:

Dashboards are built using the star schema tables directly.

Central fact:

- fact_enrolment_year

Related tables:

- fact_retention_outcome

- fact_student_success_score

- dim_student

- dim_programme

- dim_academic_year

The dashboards include:

1. Executive Overview (Retention Trends & KPIs)

2. Programme Performance Analysis

3. Risk & Segmentation Insights

Repository Structure:
mini-institutional-bi/
│
├── data/
├── duckdb/
├── scripts/
├── docs/
├── dbt/
│   └── tus_mini_bi/
│       ├── models/
│       │   ├── staging/
│       │   ├── dimensions/
│       │   ├── facts/
│       │   └── audits/
│       └── dbt_project.yml
└── README.md

Future Enhancements

Potential extensions include:

- Enrolment projection models

- Resource allocation analysis

- Space optimisation modelling

- Workforce analytics

- Predictive retention modelling

Purpose:

This project was developed as a portfolio demonstration of institutional BI capabilities, modelling best practices, and analytics design aligned with higher education reporting and strategic planning needs.

It aims to reflect how a structured BI function can move from raw operational data to governed, decision-ready insights.