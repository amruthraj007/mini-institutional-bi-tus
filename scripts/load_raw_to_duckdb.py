from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "duckdb" / "warehouse.duckdb"


def main() -> None:
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Raw data folder not found: {RAW_DIR}")

    con = duckdb.connect(str(DB_PATH))

    # Create a dedicated schema for raw tables (optional but nice)
    con.execute("create schema if not exists raw;")

    # Helper to load CSV into a DuckDB table
    def load_csv(table_name: str, csv_name: str) -> None:
        csv_path = RAW_DIR / csv_name
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing CSV: {csv_path}")

        print(f"Loading {csv_name} -> raw.{table_name}")
        con.execute(f"drop table if exists raw.{table_name};")
        con.execute(
            f"""
            create table raw.{table_name} as
            select *
            from read_csv_auto('{csv_path.as_posix()}', header=true);
            """
        )

    load_csv("students", "students_raw.csv")
    load_csv("programmes", "programmes_raw.csv")
    load_csv("enrolments", "enrolments_raw.csv")
    load_csv("academic_performance", "academic_performance_raw.csv")

    # Basic row counts
    print("\nRow counts in DuckDB:")
    for t in ["students", "programmes", "enrolments", "academic_performance"]:
        n = con.execute(f"select count(*) from raw.{t};").fetchone()[0]
        print(f"raw.{t}: {n:,}")

    con.close()
    print(f"\n✅ Loaded raw tables into DuckDB: {DB_PATH}")


if __name__ == "__main__":
    main()