"""Fictional demonstration profile (clearly labelled as demo data)."""
from __future__ import annotations

import csv
from pathlib import Path

import database as db
from recommendations import refresh_saved_recommendations

SAMPLE_CSV = Path(__file__).resolve().parent / "data" / "sample_skills.csv"

DEMO_PROFILE = {
    "display_name": "Demo Student (fictional)",
    "education_level": "Undergraduate (in progress)",
    "field_of_study": "Mathematics",
    "technical_skills": ["Python", "Excel", "Pandas"],
    "soft_skills": ["Communication", "Critical thinking"],
    "career_interests": ["Data Analyst", "Machine Learning Engineer"],
    "career_goal": "Start a career in data and AI after graduation (fictional example).",
    "learning_areas": ["Data analysis", "Machine learning"],
}


def read_sample_scores(path=SAMPLE_CSV) -> dict[str, int]:
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["skill"]: int(row["score"]) for row in csv.DictReader(fh)}


def load_demo_profile(db_path=None) -> int:
    pid = db.create_profile(DEMO_PROFILE, is_demo=True, db_path=db_path)
    db.save_assessment(pid, read_sample_scores(), db_path)
    refresh_saved_recommendations(pid, db_path)
    return pid
