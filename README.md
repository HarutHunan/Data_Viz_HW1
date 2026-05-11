# Student Productivity & Distraction — Data Visualization Project

## Dashboard (Assignment 3)

The dashboard lives under [`dashboard/`](dashboard/). It is a multi-page Dash app that turns the Assignment 2 story into interactive views.

- [`dashboard/app.py`](dashboard/app.py): Navbar, shared layout container for active page, Bootstrap theme.
- [`dashboard/data.py`](dashboard/data.py): Loads `data/student_productivity_distraction_dataset_20000.csv`, adds derived columns (`total_distraction_hours`, sleep/exercise flags, distraction buckets, productivity tiers).
- Additional pages in [`dashboard/pages/`](dashboard/pages/): 
    * **Overview** (time budget, gender dropdown), 
    * **Distractions** (scatter + trendline, box plot, phone × social heatmap; color dropdown and sample slider),
    * **Drivers** (academic and lifestyle correlation bars, sleep × exercise box plot, stress dual-axis lines; outcome dropdown and stress range slider). Charts align with [`story.ipynb`](story.ipynb).
- [`dashboard/assets/styles.css`](dashboard/assets/styles.css): Light spacing helpers for cards.


From the repo root, after `uv sync`:

```bash
cd dashboard
uv run python app.py
```

Open **http://127.0.0.1:8050/** in your browser. Use the navbar to switch pages.

---

A data analysis project exploring the relationship between student habits, digital distractions, and academic outcomes. Using a dataset of 20,000 synthetic student records, this repository investigates how behavioral factors — study time, sleep, stress, social media, gaming, and more — influence productivity, focus, and final grades.

## Story Notebook (Assignment 2)

[`story.ipynb`](story.ipynb) builds on the EDA by narrowing down to the insights that actually matter and presenting them as a focused narrative with interactive Plotly visualizations. It covers time allocation, the cost of digital distractions, what drives productivity, and how lifestyle factors amplify or undermine study effort. This notebook is meant to serve as the foundation for the final dashboard.

## EDA (Assignment 1)

The initial exploration lives in [`EDA.ipynb`](EDA.ipynb), a structured notebook that walks through data quality checks, univariate and multivariate distributions, gender comparisons, correlation analysis, and a final summary of key findings and modelling ideas.

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
