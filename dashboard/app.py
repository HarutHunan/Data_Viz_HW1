import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    assets_folder="assets",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

navbar = dbc.NavbarSimple(
    brand="Student Productivity Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"], active="exact"))
        for page in dash.page_registry.values()
    ],
)

app.layout = dbc.Container(
    [navbar, html.Br(), dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
