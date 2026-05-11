import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from data import COLORS, TEMPLATE, df

dash.register_page(__name__, path="/", title="Overview", name="Overview")

gender_options = [{"label": "All", "value": "All"}] + [{"label": g, "value": g} for g in sorted(df["gender"].unique())]


def make_kpi_card(title, value, color=COLORS["teal"]):
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(title, className="kpi-label"),
                html.P(value, className="kpi-value", style={"color": color}),
            ]
        ),
        className="kpi-card card-margin",
    )


layout = dbc.Container(
    [
        html.H3("The Time Budget", className="mt-3 mb-3"),
        html.P("How students split their day between study, rest, and screen time."),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Filter by gender"),
                        dcc.Dropdown(id="gender-filter", options=gender_options, value="All", clearable=False),
                    ],
                    width=3,
                ),
            ],
            className="filter-row",
        ),
        dbc.Row(
            [
                dbc.Col(make_kpi_card("Students", f"{len(df):,}"), width=3, id="kpi-students-col"),
                dbc.Col(id="kpi-study-col", width=3),
                dbc.Col(id="kpi-distraction-col", width=3),
                dbc.Col(id="kpi-productivity-col", width=3),
            ],
            className="mb-3",
            id="kpi-row",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="sunburst-chart"))), width=5),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="histogram-chart"))), width=7),
            ]
        ),
    ]
)


@callback(
    Output("kpi-study-col", "children"),
    Output("kpi-distraction-col", "children"),
    Output("kpi-productivity-col", "children"),
    Output("kpi-students-col", "children"),
    Output("sunburst-chart", "figure"),
    Output("histogram-chart", "figure"),
    Input("gender-filter", "value"),
)
def update_overview(gender):
    filtered = df if gender == "All" else df[df["gender"] == gender]

    kpi_students = make_kpi_card("Students", f"{len(filtered):,}", COLORS["dark"])
    kpi_study = make_kpi_card("Avg Study h/day", f"{filtered['study_hours_per_day'].mean():.1f}", COLORS["teal"])
    kpi_distraction = make_kpi_card(
        "Avg Distraction h/day", f"{filtered['total_distraction_hours'].mean():.1f}", COLORS["orange"]
    )
    kpi_productivity = make_kpi_card("Avg Productivity", f"{filtered['productivity_score'].mean():.1f}", COLORS["teal"])

    # Sunburst
    time_data = {
        "Study": filtered["study_hours_per_day"].mean(),
        "Sleep": filtered["sleep_hours"].mean(),
        "Phone": (filtered["phone_usage_hours"] - filtered["social_media_hours"]).clip(lower=0).mean(),
        "Social Media": filtered["social_media_hours"].mean(),
        "YouTube": filtered["youtube_hours"].mean(),
        "Gaming": filtered["gaming_hours"].mean(),
    }
    time_df = {
        "Activity": list(time_data.keys()),
        "Hours": list(time_data.values()),
        "Category": ["Productive", "Rest", "Distraction", "Distraction", "Distraction", "Distraction"],
    }
    fig_sun = px.sunburst(
        time_df,
        path=["Category", "Activity"],
        values="Hours",
        color="Category",
        color_discrete_map={"Productive": COLORS["teal"], "Rest": COLORS["dark"], "Distraction": COLORS["orange"]},
        template=TEMPLATE,
        title="Where Does the Day Go?",
    )
    fig_sun.update_traces(
        textinfo="label+value+percent parent", texttemplate="%{label}<br>%{value:.1f}h (%{percentParent:.0%})"
    )
    fig_sun.update_layout(margin={"t": 40, "b": 10, "l": 10, "r": 10})

    # Histogram
    fig_hist = go.Figure()
    fig_hist.add_trace(
        go.Histogram(
            x=filtered["study_hours_per_day"],
            name="Study Hours",
            marker_color=COLORS["teal"],
            opacity=0.7,
            nbinsx=40,
        )
    )
    fig_hist.add_trace(
        go.Histogram(
            x=filtered["total_distraction_hours"],
            name="Distraction Hours",
            marker_color=COLORS["orange"],
            opacity=0.7,
            nbinsx=40,
        )
    )
    fig_hist.update_layout(
        barmode="overlay",
        template=TEMPLATE,
        title="Study vs Distraction Distributions",
        xaxis_title="Hours per Day",
        yaxis_title="Students",
        legend={"yanchor": "top", "y": 0.95, "xanchor": "right", "x": 0.95},
        margin={"t": 40, "b": 40},
    )
    mean_study = filtered["study_hours_per_day"].mean()
    mean_dist = filtered["total_distraction_hours"].mean()
    fig_hist.add_vline(
        x=mean_study,
        line_dash="dash",
        line_color=COLORS["teal"],
        annotation_text=f"Mean: {mean_study:.1f}h",
        annotation_position="top left",
    )
    fig_hist.add_vline(
        x=mean_dist,
        line_dash="dash",
        line_color=COLORS["orange"],
        annotation_text=f"Mean: {mean_dist:.1f}h",
        annotation_position="top right",
    )

    return kpi_study, kpi_distraction, kpi_productivity, kpi_students, fig_sun, fig_hist
