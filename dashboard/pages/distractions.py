import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output, callback, dcc, html

from data import COLORS, TEMPLATE, df

dash.register_page(__name__, path="/distractions", title="Distractions", name="Distractions")

color_options = [
    {"label": "Stress Level", "value": "stress_level"},
    {"label": "Focus Score", "value": "focus_score"},
    {"label": "Sleep Hours", "value": "sleep_hours"},
]

layout = dbc.Container(
    [
        html.H3("The Distraction Tax", className="mt-3 mb-3"),
        html.P("What all that screen time actually costs in productivity."),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Scatter color variable"),
                        dcc.Dropdown(id="scatter-color", options=color_options, value="stress_level", clearable=False),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Label("Scatter sample size"),
                        dcc.Slider(
                            id="sample-slider",
                            min=500,
                            max=5000,
                            step=500,
                            value=3000,
                            marks={v: str(v) for v in range(500, 5001, 500)},
                        ),
                    ],
                    width=5,
                ),
            ],
            className="filter-row",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="distraction-scatter"))), width=12, className="card-margin"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="distraction-box"))), width=6, className="card-margin"),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="distraction-heatmap"))), width=6, className="card-margin"),
            ]
        ),
    ]
)


@callback(
    Output("distraction-scatter", "figure"),
    Output("distraction-box", "figure"),
    Output("distraction-heatmap", "figure"),
    Input("scatter-color", "value"),
    Input("sample-slider", "value"),
)
def update_distractions(color_var, sample_size):
    sample = df.sample(n=sample_size, random_state=42)

    pretty_color = color_var.replace("_", " ").title()
    fig_scatter = px.scatter(
        sample,
        x="total_distraction_hours",
        y="productivity_score",
        color=color_var,
        color_continuous_scale="RdYlGn_r",
        trendline="ols",
        opacity=0.5,
        template=TEMPLATE,
        labels={
            "total_distraction_hours": "Total Distraction Hours / Day",
            "productivity_score": "Productivity Score",
            color_var: pretty_color,
        },
        title=f"Distraction vs Productivity (colored by {pretty_color})",
    )
    fig_scatter.update_layout(margin={"t": 40, "b": 40})

    # Box plot
    fig_box = px.box(
        df,
        x="distraction_level",
        y="productivity_score",
        color="distraction_level",
        color_discrete_sequence=[COLORS["teal"], COLORS["yellow"], COLORS["peach"], COLORS["orange"]],
        template=TEMPLATE,
        title="Productivity by Distraction Level",
        labels={"distraction_level": "Distraction Level", "productivity_score": "Productivity Score"},
        category_orders={"distraction_level": ["Low (0-5h)", "Medium (5-10h)", "High (10-15h)", "Very High (15h+)"]},
    )
    fig_box.update_layout(showlegend=False, margin={"t": 40, "b": 40})

    # Heatmap
    phone_labels = ["0 - 2", "2 - 4", "4 - 6", "6 - 8", "8 - 10", "10 - 12"]
    social_labels = ["0 - 2", "2 - 4", "4 - 6", "6 - 8"]
    tmp = df.copy()
    tmp["phone_bin"] = pd.cut(
        tmp["phone_usage_hours"], bins=[0, 2, 4, 6, 8, 10, 12], labels=phone_labels, include_lowest=True
    )
    tmp["social_bin"] = pd.cut(
        tmp["social_media_hours"], bins=[0, 2, 4, 6, 8], labels=social_labels, include_lowest=True
    )
    heatmap_data = tmp.groupby(["phone_bin", "social_bin"], observed=False)["productivity_score"].mean().unstack()
    z_vals = heatmap_data.to_numpy().round(1)

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=z_vals,
            x=[str(c) for c in heatmap_data.columns],
            y=[str(r) for r in heatmap_data.index],
            colorscale="RdYlGn",
            text=z_vals,
            texttemplate="%{text:.1f}",
            textfont={"size": 12},
            colorbar={"title": "Mean<br>Productivity"},
        )
    )
    fig_heat.update_layout(
        template=TEMPLATE,
        title="Phone and Social Media Interaction",
        xaxis_title="Social Media (h/day)",
        yaxis_title="Phone Usage (h/day)",
        yaxis={"autorange": "reversed"},
        margin={"t": 40, "b": 40},
    )

    return fig_scatter, fig_box, fig_heat
