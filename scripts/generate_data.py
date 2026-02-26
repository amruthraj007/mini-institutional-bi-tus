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
    raise NotImplementedError


def simulate_enrolments_and_performance(
    cfg: Config,
    students_df: pd.DataFrame,
    programmes_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (enrolments_raw, academic_performance_raw)."""
    raise NotImplementedError


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
    cfg = Config()
    set_seeds(cfg.seed)
    df = generate_programmes(cfg)
    print(df.head())