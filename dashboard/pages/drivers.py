import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html
from plotly.subplots import make_subplots

from data import COLORS, TEMPLATE, df

dash.register_page(__name__, path="/drivers", title="Drivers", name="Drivers")

outcome_options = [
    {"label": "Productivity Score", "value": "productivity_score"},
    {"label": "Focus Score", "value": "focus_score"},
]

layout = dbc.Container(
    [
        html.H3("Productivity Drivers", className="mt-3 mb-3"),
        html.P("What pushes productivity up — study effort and lifestyle factors."),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Outcome variable"),
                        dcc.Dropdown(
                            id="outcome-select", options=outcome_options, value="productivity_score", clearable=False
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Label("Stress level range"),
                        dcc.RangeSlider(
                            id="stress-slider",
                            min=1,
                            max=10,
                            step=1,
                            value=[1, 10],
                            marks={i: str(i) for i in range(1, 11)},
                        ),
                    ],
                    width=5,
                ),
            ],
            className="filter-row",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="academic-corr"))), width=6, className="card-margin"),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="lifestyle-corr"))), width=6, className="card-margin"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="sleep-exercise-box"))), width=6, className="card-margin"),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="stress-lines"))), width=6, className="card-margin"),
            ]
        ),
    ]
)


@callback(
    Output("academic-corr", "figure"),
    Output("lifestyle-corr", "figure"),
    Output("sleep-exercise-box", "figure"),
    Output("stress-lines", "figure"),
    Input("outcome-select", "value"),
    Input("stress-slider", "value"),
)
def update_drivers(outcome, stress_range):
    filtered = df[(df["stress_level"] >= stress_range[0]) & (df["stress_level"] <= stress_range[1])]
    outcome_label = outcome.replace("_", " ").title()

    # Academic correlations
    academic_vars = ["study_hours_per_day", "focus_score", "assignments_completed", "attendance_percentage"]
    acad_corrs = filtered[academic_vars].corrwith(filtered[outcome]).sort_values()
    fig_acad = px.bar(
        x=acad_corrs.values,
        y=[v.replace("_", " ").title() for v in acad_corrs.index],
        orientation="h",
        template=TEMPLATE,
        title=f"Academic Drivers of {outcome_label}",
        labels={"x": "Correlation (r)", "y": ""},
        text=[f"{v:.2f}" for v in acad_corrs.values],
    )
    fig_acad.update_traces(marker_color=[COLORS["orange"] if v < 0.2 else COLORS["teal"] for v in acad_corrs.values])
    fig_acad.update_layout(margin={"t": 40, "b": 30}, yaxis={"tickfont": {"size": 12}})

    # Lifestyle correlations
    lifestyle_vars = ["sleep_hours", "exercise_minutes", "stress_level", "coffee_intake_mg"]
    life_corrs = filtered[lifestyle_vars].corrwith(filtered[outcome]).sort_values()
    life_labels = [
        v.replace("_", " ").replace("mg", "(mg)").replace("minutes", "(min)").replace("hours", "(h)").title()
        for v in life_corrs.index
    ]
    fig_life = px.bar(
        x=life_corrs.values,
        y=life_labels,
        orientation="h",
        template=TEMPLATE,
        title=f"Lifestyle Drivers of {outcome_label}",
        labels={"x": "Correlation (r)", "y": ""},
        text=[f"{v:+.2f}" for v in life_corrs.values],
    )
    fig_life.update_traces(marker_color=[COLORS["orange"] if v < 0 else COLORS["teal"] for v in life_corrs.values])
    fig_life.update_layout(margin={"t": 40, "b": 30}, yaxis={"tickfont": {"size": 12}})

    # Sleep x Exercise box
    fig_box = px.box(
        filtered,
        x="good_sleep",
        y=outcome,
        color="exercises_regularly",
        color_discrete_map={"Exercise >= 60min": COLORS["teal"], "Exercise < 60min": COLORS["orange"]},
        template=TEMPLATE,
        title=f"Sleep + Exercise Effect on {outcome_label}",
        labels={"good_sleep": "Sleep Category", outcome: outcome_label, "exercises_regularly": "Exercise"},
        category_orders={
            "good_sleep": ["Sleep < 7h", "Sleep >= 7h"],
            "exercises_regularly": ["Exercise < 60min", "Exercise >= 60min"],
        },
    )
    fig_box.update_layout(
        boxmode="group", margin={"t": 40, "b": 40}, legend={"yanchor": "top", "y": 0.95, "xanchor": "right", "x": 0.98}
    )

    # Stress lines (dual axis)
    stress_agg = filtered.groupby("stress_level", as_index=False).agg(
        mean_focus=("focus_score", "mean"),
        mean_productivity=("productivity_score", "mean"),
    )
    fig_stress = make_subplots(specs=[[{"secondary_y": True}]])
    fig_stress.add_trace(
        go.Scatter(
            x=stress_agg["stress_level"],
            y=stress_agg["mean_productivity"],
            mode="lines+markers",
            name="Productivity",
            line={"color": COLORS["teal"], "width": 3},
            marker={"size": 7},
        ),
        secondary_y=False,
    )
    fig_stress.add_trace(
        go.Scatter(
            x=stress_agg["stress_level"],
            y=stress_agg["mean_focus"],
            mode="lines+markers",
            name="Focus",
            line={"color": COLORS["yellow"], "width": 3, "dash": "dot"},
            marker={"size": 7},
        ),
        secondary_y=True,
    )
    fig_stress.update_layout(
        template=TEMPLATE,
        title="Stress vs Focus & Productivity",
        xaxis_title="Stress Level",
        margin={"t": 40, "b": 40},
        legend={"yanchor": "top", "y": 0.95, "xanchor": "right", "x": 0.95},
    )
    fig_stress.update_yaxes(title_text="Mean Productivity", secondary_y=False)
    fig_stress.update_yaxes(title_text="Mean Focus", secondary_y=True)

    return fig_acad, fig_life, fig_box, fig_stress
