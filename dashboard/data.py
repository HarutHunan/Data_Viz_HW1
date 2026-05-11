from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "student_productivity_distraction_dataset_20000.csv"
TEMPLATE = "plotly_white"
COLORS = {
    "teal": "#2a9d8f",
    "dark": "#264653",
    "orange": "#e76f51",
    "yellow": "#e9c46a",
    "peach": "#f4a261",
}

df = pd.read_csv(DATA_PATH)

df["total_distraction_hours"] = (
    df["phone_usage_hours"] + df["social_media_hours"] + df["youtube_hours"] + df["gaming_hours"]
)
df["good_sleep"] = np.where(df["sleep_hours"] >= 7, "Sleep >= 7h", "Sleep < 7h")
df["exercises_regularly"] = np.where(df["exercise_minutes"] >= 60, "Exercise >= 60min", "Exercise < 60min")
df["distraction_level"] = pd.cut(
    df["total_distraction_hours"],
    bins=[0, 5, 10, 15, df["total_distraction_hours"].max()],
    labels=["Low (0-5h)", "Medium (5-10h)", "High (10-15h)", "Very High (15h+)"],
    include_lowest=True,
)
df["productivity_tier"] = pd.qcut(df["productivity_score"], q=4, labels=["Low", "Mid-Low", "Mid-High", "High"])
