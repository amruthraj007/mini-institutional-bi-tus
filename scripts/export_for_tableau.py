import duckdb
import pandas as pd
import os

DB_PATH = "duckdb/warehouse.duckdb"
EXPORT_DIR = "data/tableau_exports_excel"

os.makedirs(EXPORT_DIR, exist_ok=True)

tables = [
    "fact_enrolment_year",
    "fact_retention_outcome",
    "fact_student_success_score",
    "dim_student",
    "dim_programme",
    "dim_academic_year"
]

con = duckdb.connect(DB_PATH)

for table in tables:
    print(f"Exporting {table}...")
    df = con.execute(f"SELECT * FROM main.{table}").df()
    output_path = os.path.join(EXPORT_DIR, f"{table}.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Saved to {output_path}")

con.close()

print("All tables exported successfully.")