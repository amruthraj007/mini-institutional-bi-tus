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
    raise NotImplementedError


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
    main()