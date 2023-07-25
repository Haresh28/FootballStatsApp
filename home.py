from dash import Dash, dcc, html, Input, Output         # pip install dash
import dash_bootstrap_components as dbc         # pip install dash_bootstrap_components
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
app.layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(html.H2("FOOTBALL STATISTICS"),id='title',width={"size":4,"offset":4},md=6)
        ),
        dbc.Row(children=[
            dbc.Col(children=[dbc.Nav([dbc.NavLink("Team Stats",href="#")])],width={"size":2,"offset":4}),
            dbc.Col(children=[dbc.Nav([dbc.NavLink("Player Stats", href="#")])],width={"size":2,"offset":0})

        ],
        )
     ]


)
if __name__ == "__main__":
    app.run_server(debug=True)