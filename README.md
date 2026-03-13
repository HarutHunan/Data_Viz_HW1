# Student Productivity & Distraction — Exploratory Data Analysis

A data analysis project exploring the relationship between student habits, digital distractions, and academic outcomes. Using a dataset of 20,000 synthetic student records, this repository investigates how behavioral factors — study time, sleep, stress, social media, gaming, and more — influence productivity, focus, and final grades.

The core analysis lives in [`EDA.ipynb`](EDA.ipynb), a structured notebook that walks through data quality checks, univariate and multivariate distributions, gender comparisons, correlation analysis, and a final summary of key findings and modelling ideas.

Find the original data [here](https://www.kaggle.com/datasets/algozee/student-productivity-and-behavior-dataset-20k)

---

## Dataset

**File:** `data/student_productivity_distraction_dataset_20000.csv`  
**Records:** 20,000 students × 18 features

| Feature | Description |
|---|---|
| `student_id` | Unique identifier |
| `age` | Student age (17–29) |
| `gender` | Female / Male / Other |
| `study_hours_per_day` | Daily study hours |
| `sleep_hours` | Nightly sleep hours |
| `phone_usage_hours` | Total daily phone screen time |
| `social_media_hours` | Hours spent on social media |
| `youtube_hours` | Hours spent on YouTube |
| `gaming_hours` | Hours spent gaming |
| `breaks_per_day` | Number of study breaks taken |
| `coffee_intake_mg` | Daily caffeine intake (mg) |
| `exercise_minutes` | Daily exercise duration (minutes) |
| `assignments_completed` | Number of assignments submitted |
| `attendance_percentage` | Class attendance rate (%) |
| `stress_level` | Self-reported stress (1–10) |
| `focus_score` | Self-reported focus score |
| `final_grade` | Final academic grade |
| `productivity_score` | Computed productivity score (target variable) |

---

## Environment Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Python 3.12+ is required.

### Linux / macOS

Install uv (if not already installed).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repository and navigate into it.
```
git clone <repo-url>
cd dataviz
```

Create a virtual environment and activate.
```
uv venv --python=3.12
source .venv/bin/activate
```

Install dev dependencies (includes Jupyter kernel and linter)
```
uv sync
uv sync --group dev
```

### Windows (PowerShell)

Install uv.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Activate the virtual environment.

```powershell
.venv\Scripts\Activate.ps1
```
