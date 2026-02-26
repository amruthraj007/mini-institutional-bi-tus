from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import numpy as np
import pandas as pd

# -----------------------------
# Config
# -----------------------------

@dataclass
class Config:
    seed: int = 42
    output_dir: Path = Path("data/raw")
    academic_years: tuple[str, ...] = ("2020/21", "2021/22", "2022/23", "2023/24", "2024/25")
    n_programmes: int = 40
    new_entrants_per_year: int = 2400
    transfer_rate: float = 0.05
    repeat_rate_if_low_gpa: float = 0.15
    missing_perf_rate: float = 0.015
    duplicate_enrolment_rate: float = 0.005


def set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Generators (to implement)
# -----------------------------

def generate_programmes(cfg: Config) -> pd.DataFrame:
    faculties = ["Business", "Engineering", "Science", "Arts", "Health", "Computing"]
    campuses = ["Athlone", "Moylish", "Thurles", "Clonmel", "Ennis"]
    nfq_levels = [6, 7, 8]

    # Mode distribution: 85% FT, 15% PT
    modes = np.random.choice(
        ["FT", "PT"],
        size=cfg.n_programmes,
        p=[0.85, 0.15],
    )

    # Spread programmes across faculties fairly evenly
    faculty_assignments = np.random.choice(faculties, size=cfg.n_programmes, replace=True)

    # NFQ levels with a realistic tilt (more level 8 programmes)
    level_assignments = np.random.choice(nfq_levels, size=cfg.n_programmes, p=[0.20, 0.25, 0.55])

    # Campuses distribution (roughly balanced)
    campus_assignments = np.random.choice(campuses, size=cfg.n_programmes, replace=True)

    # Difficulty factor drives retention differences later (lower = harder)
    difficulty = np.round(np.random.uniform(0.60, 0.90, size=cfg.n_programmes), 2)

    # Simple name generator per faculty
    name_bank = {
        "Business": ["Business Studies", "Accounting", "Marketing", "Finance", "HR Management", "Entrepreneurship"],
        "Engineering": ["Mechanical Engineering", "Civil Engineering", "Electrical Engineering", "Mechatronics", "Energy Systems"],
        "Science": ["Biotechnology", "Applied Science", "Pharmaceutical Science", "Environmental Science", "Sports Science"],
        "Arts": ["Digital Media", "Design", "Creative Arts", "Journalism", "Languages", "Social Studies"],
        "Health": ["Nursing", "Health Science", "Public Health", "Physiotherapy Studies", "Mental Health Studies"],
        "Computing": ["Computer Science", "Software Development", "Data Analytics", "Cybersecurity", "Cloud Computing"],
    }

    programme_rows = []
    for i in range(cfg.n_programmes):
        faculty = faculty_assignments[i]
        nfq = int(level_assignments[i])
        mode = modes[i]
        campus = campus_assignments[i]

        # Construct a programme id like PRG001, PRG002...
        programme_id = f"PRG{str(i+1).zfill(3)}"

        # Select a name and add an NFQ hint
        base_name = random.choice(name_bank[faculty])
        # A light naming pattern; keep it believable
        programme_name = f"Higher Cert in {base_name}" if nfq == 6 else \
                         f"Ordinary Degree in {base_name}" if nfq == 7 else \
                         f"Honours Degree in {base_name}"

        programme_rows.append(
            {
                "programme_id": programme_id,
                "programme_name": programme_name,
                "faculty": faculty,
                "nfq_level": nfq,
                "mode": mode,
                "campus": campus,
                # simulation-only helper (we won't show it in dashboards)
                "difficulty_factor": float(difficulty[i]),
            }
        )

    programmes_df = pd.DataFrame(programme_rows)

    # A touch of raw-ish imperfection (optional): inconsistent faculty casing (very low rate)
    # Keep it tiny so it doesn't become annoying to clean
    noisy_idx = programmes_df.sample(frac=0.02, random_state=cfg.seed).index
    programmes_df.loc[noisy_idx, "faculty"] = programmes_df.loc[noisy_idx, "faculty"].str.lower()

    return programmes_df


def generate_students(cfg: Config, total_students: int) -> pd.DataFrame:
    campuses = ["Athlone", "Moylish", "Thurles", "Clonmel", "Ennis"]

    # Entry route distribution (approx)
    entry_routes = ["CAO", "QQI/FET", "Mature", "International", "Other"]
    entry_probs = [0.65, 0.15, 0.10, 0.07, 0.03]

    # Nationality distribution (approx)
    nationality_groups = ["Irish", "EU", "Non-EU"]
    nationality_probs = [0.82, 0.10, 0.08]

    # Access / disadvantage flag
    access_prob = 0.18

    # We'll generate DOBs so dbt can convert to age bands.
    # For UG populations: mostly 18–24, plus some mature students.
    # We'll simulate by sampling age at first observed year, then convert to DOB.
    # Use a simple mixture: 85% typical UG, 15% mature.
    is_mature = np.random.choice([0, 1], size=total_students, p=[0.85, 0.15])

    # Choose "age" at baseline year 2020 (approx), then compute DOB year.
    # Typical UG: 18–24, Mature: 25–55
    ages = []
    for m in is_mature:
        if m == 0:
            ages.append(int(np.random.choice(range(18, 25))))
        else:
            ages.append(int(np.random.choice(range(25, 56))))
    ages = np.array(ages)

    # Convert ages to DOBs by subtracting from a reference year.
    # We'll use 2020-10-01 (typical academic start) as anchor.
    # DOB day/month randomised.
    ref_year = 2020
    dob_years = ref_year - ages
    dob_months = np.random.randint(1, 13, size=total_students)
    dob_days = np.random.randint(1, 29, size=total_students)  # avoid month-length issues

    date_of_birth = [
        f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
        for y, m, d in zip(dob_years, dob_months, dob_days)
    ]

    # Gender (raw-ish): generate clean then introduce noise
    # Base distribution: 48/48/4
    base_gender = np.random.choice(
        ["Male", "Female", "Other/Unknown"],
        size=total_students,
        p=[0.48, 0.48, 0.04],
    )

    # Introduce raw category noise for gender (small %)
    gender = base_gender.astype(object).copy()
    noise_idx = np.random.choice(np.arange(total_students), size=int(total_students * 0.06), replace=False)
    for i in noise_idx:
        if gender[i] == "Male":
            gender[i] = np.random.choice(["male", "M", "MALE"])
        elif gender[i] == "Female":
            gender[i] = np.random.choice(["female", "F", "FEMALE"])
        else:
            gender[i] = np.random.choice(["Unknown", "Other", "Not Stated"])

    # Entry route, with slight imperfection noise
    entry_route = np.random.choice(entry_routes, size=total_students, p=entry_probs).astype(object)
    # A tiny amount of casing inconsistency
    route_noise_idx = np.random.choice(np.arange(total_students), size=int(total_students * 0.02), replace=False)
    for i in route_noise_idx:
        entry_route[i] = str(entry_route[i]).lower()

    # Access flag
    access_flag = np.random.choice([0, 1], size=total_students, p=[1 - access_prob, access_prob])

    # Nationality
    nationality_group = np.random.choice(nationality_groups, size=total_students, p=nationality_probs)

    # Home campus
    home_campus = np.random.choice(campuses, size=total_students, replace=True)

    # Create pseudonymised student ids
    # e.g., STU000001 ... STU012000
    student_ids = [f"STU{str(i+1).zfill(6)}" for i in range(total_students)]

    students_df = pd.DataFrame(
        {
            "student_id": student_ids,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "entry_route": entry_route,
            "access_flag": access_flag,
            "nationality_group": nationality_group,
            "home_campus": home_campus,
        }
    )

    # Add a small amount of missingness (raw-ish)
    # e.g., 1% missing entry_route, 1% missing gender
    miss_entry_idx = students_df.sample(frac=0.01, random_state=cfg.seed).index
    students_df.loc[miss_entry_idx, "entry_route"] = None

    miss_gender_idx = students_df.sample(frac=0.01, random_state=cfg.seed + 1).index
    students_df.loc[miss_gender_idx, "gender"] = None

    return students_df


def simulate_enrolments_and_performance(
    cfg: Config,
    students_df: pd.DataFrame,
    programmes_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Simulates multi-year enrolments and annual performance.
    Returns:
      enrolments_raw: grain ~ student-programme-academic_year (with minor raw-ish duplicates/noise)
      academic_performance_raw: grain ~ student-academic_year
    """
    # Helper lookups
    prog = programmes_df.set_index("programme_id")
    programme_ids = programmes_df["programme_id"].tolist()

    # Track each student's "current" state across years
    # We'll create new entrants each year, then simulate continuation.
    student_state = {}  # student_id -> dict(programme_id, year_of_study, active)

    enrolment_rows: list[dict] = []
    perf_rows: list[dict] = []

    # Determine yearly cohorts
    years = list(cfg.academic_years)
    n_years = len(years)
    new_per_year = cfg.new_entrants_per_year

    # Shuffle student list so assignment across years is random
    all_students = students_df["student_id"].tolist()
    random.shuffle(all_students)

    # Slice students into new entrant cohorts per year
    cohorts = {
        years[i]: all_students[i * new_per_year : (i + 1) * new_per_year]
        for i in range(n_years)
    }

    # Convenience: access flag lookup
    access_lookup = students_df.set_index("student_id")["access_flag"].to_dict()

    def sample_programme_for_new_entrant() -> str:
        # You can bias this later if you want (e.g., by faculty), but keep it simple for now
        return random.choice(programme_ids)

    def gpa_attendance_for_student_year(student_id: str, programme_id: str) -> tuple[float, float]:
        """
        Generate a GPA and attendance rate influenced by programme difficulty and access flag.
        """
        difficulty = float(prog.loc[programme_id, "difficulty_factor"])  # 0.60..0.90
        access = int(access_lookup.get(student_id, 0))

        # Base GPA centered ~2.85 with noise
        # Harder programmes reduce GPA slightly (lower difficulty -> lower GPA)
        # Access flag gives a modest downward shift
        base = 2.85
        difficulty_shift = (difficulty - 0.75) * 1.2  # difficulty 0.75 as midpoint
        access_shift = -0.10 if access == 1 else 0.0

        gpa = np.random.normal(loc=base + difficulty_shift + access_shift, scale=0.45)
        gpa = float(np.clip(gpa, 1.0, 4.0))

        # Attendance correlated with GPA (simple linear relationship + noise)
        attendance = 55 + (gpa * 12.5) + np.random.normal(0, 8)
        attendance = float(np.clip(attendance, 30, 100))

        return gpa, attendance

    def retention_probability(student_id: str, programme_id: str, gpa: float, attendance: float) -> float:
        """
        Compute probability of being retained into next academic year.
        """
        difficulty = float(prog.loc[programme_id, "difficulty_factor"])
        access = int(access_lookup.get(student_id, 0))

        p = 0.82

        # GPA adjustments
        if gpa < 2.0:
            p -= 0.18
        elif gpa < 2.8:
            p -= 0.07
        elif gpa >= 3.2:
            p += 0.03

        # Attendance adjustments
        if attendance < 70:
            p -= 0.10
        elif attendance >= 90:
            p += 0.02

        # Access adjustment
        if access == 1:
            p -= 0.04

        # Programme difficulty multiplier
        p = p * difficulty

        return float(np.clip(p, 0.05, 0.98))

    def gpa_band(gpa: float) -> str:
        if gpa < 2.0:
            return "Low"
        if gpa < 3.2:
            return "Med"
        return "High"

    def attendance_band(att: float) -> str:
        if att < 70:
            return "Low"
        if att < 90:
            return "Med"
        return "High"

    # ---- Simulation loop by academic year ----
    for i, yr in enumerate(years):
        # 1) Add new entrants for this year
        for student_id in cohorts[yr]:
            programme_id = sample_programme_for_new_entrant()
            student_state[student_id] = {
                "programme_id": programme_id,
                "year_of_study": 1,
                "active": True,
            }

        # 2) For active students, generate enrolment + performance
        active_students = [sid for sid, st in student_state.items() if st["active"]]

        for student_id in active_students:
            st = student_state[student_id]
            programme_id = st["programme_id"]
            yos = st["year_of_study"]

            # Registration status (mostly Registered)
            reg_status = "Registered"

            # Generate performance
            gpa, att = gpa_attendance_for_student_year(student_id, programme_id)

            # Add row to performance extract (student-year grain)
            perf_rows.append(
                {
                    "student_id": student_id,
                    "academic_year": yr,
                    "gpa": round(gpa, 2),
                    "attendance_rate": round(att, 1),
                }
            )

            # Credits attempted based on mode
            mode = str(prog.loc[programme_id, "mode"])
            credits_attempted = 60 if mode == "FT" else 30

            enrolment_rows.append(
                {
                    "student_id": student_id,
                    "programme_id": programme_id,
                    "academic_year": yr,
                    "year_of_study": yos,
                    "registration_status": reg_status,
                    "credits_attempted": credits_attempted,
                    "entrant_flag": 1 if yos == 1 else 0,
                    "gpa_band": gpa_band(gpa),
                    "attendance_band": attendance_band(att),
                }
            )

            # 3) Decide retention into next year (unless last year)
            if i < n_years - 1:
                p_ret = retention_probability(student_id, programme_id, gpa, att)
                retained = np.random.rand() < p_ret

                if not retained:
                    # mark inactive for next year; also optionally mark withdrawn at end
                    student_state[student_id]["active"] = False
                else:
                    # Retained: possibly transfer or repeat
                    next_programme = programme_id
                    # Transfer (small %)
                    if np.random.rand() < cfg.transfer_rate:
                        # transfer within same faculty (more realistic)
                        faculty = prog.loc[programme_id, "faculty"]
                        same_faculty = programmes_df[programmes_df["faculty"].astype(str).str.lower() == str(faculty).lower()]
                        if len(same_faculty) > 0:
                            next_programme = random.choice(same_faculty["programme_id"].tolist())

                    # Repeat rule for low GPA
                    next_yos = yos + 1
                    if gpa < 1.8 and np.random.rand() < cfg.repeat_rate_if_low_gpa:
                        next_yos = yos  # repeats

                    student_state[student_id]["programme_id"] = next_programme
                    student_state[student_id]["year_of_study"] = next_yos

    enrolments_df = pd.DataFrame(enrolment_rows)
    performance_df = pd.DataFrame(perf_rows)

    # ---- Introduce small raw-ish imperfections ----

    # 1) Missing performance values (1–2%)
    if cfg.missing_perf_rate > 0:
        miss_n = int(len(performance_df) * cfg.missing_perf_rate)
        if miss_n > 0:
            miss_idx = performance_df.sample(n=miss_n, random_state=cfg.seed).index
            # randomly choose whether GPA or attendance is missing
            for idx in miss_idx:
                if np.random.rand() < 0.5:
                    performance_df.loc[idx, "gpa"] = None
                else:
                    performance_df.loc[idx, "attendance_rate"] = None

    # 2) Duplicate enrolment rows (very small %)
    if cfg.duplicate_enrolment_rate > 0:
        dup_n = int(len(enrolments_df) * cfg.duplicate_enrolment_rate)
        if dup_n > 0:
            dup_rows = enrolments_df.sample(n=dup_n, random_state=cfg.seed + 10)
            enrolments_df = pd.concat([enrolments_df, dup_rows], ignore_index=True)

    # 3) Add a small amount of status noise: some "Withdrawn" rows
    # (keep minimal so it's easy to handle)
    w_n = max(1, int(len(enrolments_df) * 0.01))
    w_idx = enrolments_df.sample(n=w_n, random_state=cfg.seed + 20).index
    enrolments_df.loc[w_idx, "registration_status"] = "Withdrawn"

    return enrolments_df, performance_df


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    cfg = Config()
    set_seeds(cfg.seed)
    ensure_output_dir(cfg.output_dir)

    total_students = cfg.new_entrants_per_year * len(cfg.academic_years)

    programmes = generate_programmes(cfg)
    students = generate_students(cfg, total_students=total_students)
    enrolments_raw, performance_raw = simulate_enrolments_and_performance(cfg, students, programmes)

    # Write outputs
    programmes.to_csv(cfg.output_dir / "programmes_raw.csv", index=False)
    students.to_csv(cfg.output_dir / "students_raw.csv", index=False)
    enrolments_raw.to_csv(cfg.output_dir / "enrolments_raw.csv", index=False)
    performance_raw.to_csv(cfg.output_dir / "academic_performance_raw.csv", index=False)

    print("✅ Synthetic raw extracts written to data/raw/")


if __name__ == "__main__":
    main()
