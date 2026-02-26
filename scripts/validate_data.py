import pandas as pd

RAW = "data/raw"


def main() -> None:
    students = pd.read_csv(f"{RAW}/students_raw.csv")
    programmes = pd.read_csv(f"{RAW}/programmes_raw.csv")
    enrol = pd.read_csv(f"{RAW}/enrolments_raw.csv")
    perf = pd.read_csv(f"{RAW}/academic_performance_raw.csv")

    print("=== Row counts ===")
    print(f"students:   {len(students):,}")
    print(f"programmes: {len(programmes):,}")
    print(f"enrolments: {len(enrol):,}")
    print(f"performance:{len(perf):,}")

    print("\n=== Basic checks ===")
    print("Unique students in enrolments:", enrol["student_id"].nunique())
    print("Years in enrolments:", sorted(enrol["academic_year"].unique().tolist()))
    print("Years in performance:", sorted(perf["academic_year"].unique().tolist()))

    # Year 1 cohort per year
    y1 = enrol[(enrol["year_of_study"] == 1) & (enrol["registration_status"] == "Registered")]
    print("\n=== Year-1 cohort size by year ===")
    print(y1.groupby("academic_year")["student_id"].nunique().sort_index())

    # Institutional retention for Year1 -> next year
    years = sorted(enrol["academic_year"].unique().tolist())
    print("\n=== Approx Y1 -> next-year institutional retention (by cohort year) ===")
    for i in range(len(years) - 1):
        y = years[i]
        y_next = years[i + 1]
        cohort = y1[y1["academic_year"] == y][["student_id"]].drop_duplicates()
        next_year = enrol[(enrol["academic_year"] == y_next) & (enrol["registration_status"] == "Registered")][["student_id"]].drop_duplicates()

        retained = cohort.merge(next_year, on="student_id", how="inner")
        rate = len(retained) / max(1, len(cohort))
        print(f"{y} -> {y_next}: {rate:.1%}  (cohort={len(cohort):,})")

    # Retention by GPA band (use Year1 records only)
    print("\n=== Year-1 cohort: retention by GPA band (overall, approx) ===")
    # Determine retention for first year in each cohort by checking if student appears next year
    records = []
    for i in range(len(years) - 1):
        y = years[i]
        y_next = years[i + 1]

        cohort_y = y1[y1["academic_year"] == y][["student_id", "gpa_band"]].drop_duplicates()
        next_year_students = set(
            enrol[(enrol["academic_year"] == y_next) & (enrol["registration_status"] == "Registered")]["student_id"].unique()
        )
        cohort_y["retained_next_year"] = cohort_y["student_id"].apply(lambda s: 1 if s in next_year_students else 0)
        cohort_y["cohort_year"] = y
        records.append(cohort_y)

    if records:
        tmp = pd.concat(records, ignore_index=True)
        print(tmp.groupby("gpa_band")["retained_next_year"].mean().sort_index().apply(lambda x: f"{x:.1%}"))

    # Programme variation check (top/bottom by retention for one cohort year)
    if len(years) >= 2:
        y = years[0]
        y_next = years[1]
        cohort_prog = y1[y1["academic_year"] == y][["student_id", "programme_id"]].drop_duplicates()
        next_year_students = set(
            enrol[(enrol["academic_year"] == y_next) & (enrol["registration_status"] == "Registered")]["student_id"].unique()
        )
        cohort_prog["retained_next_year"] = cohort_prog["student_id"].apply(lambda s: 1 if s in next_year_students else 0)

        prog_ret = cohort_prog.groupby("programme_id")["retained_next_year"].mean().sort_values(ascending=False)
        print(f"\n=== Programme retention variation ({y} cohort, institutional retention) ===")
        print("Top 5 programmes:")
        print(prog_ret.head(5).apply(lambda x: f"{x:.1%}"))
        print("\nBottom 5 programmes:")
        print(prog_ret.tail(5).apply(lambda x: f"{x:.1%}"))

    print("\n✅ Validation complete.")


if __name__ == "__main__":
    main()