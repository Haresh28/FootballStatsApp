import dash
from dash import Dash, dcc, html, Input, Output ,dash_table        # pip install dash
import dash_bootstrap_components as dbc         # pip install dash_bootstrap_components
import plotly.express as px
import pandas as pd
import sqlite3

dash.register_page(__name__,path='/',order=1)
#fetching league names
leagueopts=['Premier League','LaLiga','Bundesliga','Ligue1','Serie A','All']
con = sqlite3.connect("fbref.db")
cur = con.cursor()
cur.execute("select * from lstanding where country='{}'".format('eng ENG'))
records = cur.fetchall()
rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
df = pd.DataFrame(rec, columns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                'xgd'])

layout=html.Div(
    children=[

        html.Div(children=[html.H3("Hello Footy Fam!! Welcome to this app",style={"margin":"15px","text-align":"center","font-family":"Rockwell"}),html.P(" Use advanced football statistics to learn more about "
            "the style of play of your favourite players and clubs, using amazing graphics and charts.",style={"text-align":"center","font-size":"20px","font-family":"Rockwell"})]),
html.Div(
    dbc.Row([ html.Div([], className = 'col-5'),dbc.Col([
        dcc.Dropdown(leagueopts, id='demo-dropdown', placeholder="Select a league",style={'color': 'black',"margin-top":"15px","font-family":"Rockwell","background-color":"#ea39b8"}),
        ],width=2)]) ),
     html.Hr(),
    html.Div(dash_table.DataTable(
        id='table1',
        columns=[{"name": i, "id": i}
                 for i in df.columns],
        data=df.to_dict('records'), editable=False, filter_action='native', sort_action='native', sort_mode='multi',
        column_selectable=False,
        row_selectable=False, row_deletable=False, selected_rows=[],
        style_cell_conditional=[
            {'if': {'column_id': c}, 'textAlign': 'left'

             } for c in ['squad']
        ],
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="black"),
        style_data=dict(backgroundColor="purple", height='auto', whitespace='normal',family="Rockwell")
    ))  # 2nd row

         ]
)


@dash.callback([Output('table1','data'),Output('table1','columns')],[Input('demo-dropdown', 'value')],prevent_initial_call=True)
def update_table(value):
    leaguematcher = {'Premier League': 'eng ENG', 'LaLiga': 'es ESP', 'Bundesliga': 'de GER', 'Ligue1': 'fr FRA',
                     'Serie A': 'it ITA'}
    con = sqlite3.connect("fbref.db")
    cur = con.cursor()
    constcolumns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                        'xgd']
    if value != 'All':

        cur.execute("select * from lstanding where country='{}'".format(leaguematcher[value]))
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec,
                          columns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                   'xgd'])

        return df.to_dict('records'), [{"name": i, "id": i}
                                       for i in df.columns]
    else:
        cur.execute("select * from lstanding ")
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:2] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec,
                          columns=['rnk', 'squad', 'country', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts',
                                   'xg', 'xga',
                                   'xgd'])

        return df.to_dict('records'), [{"name": i, "id": i}
                                       for i in df.columns]

    '''
    if value not in leaguematcher.keys():
        print("false value:",value)
        raise dash.exceptions.PreventUpdate
    elif value!='All':

        cur.execute("select * from lstanding where country='{}'".format(leaguematcher[value]))
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec, columns=constcolumns)

        return df.to_dict('records'),[{"name": i, "id": i}
                     for i in df.columns]
    else:
        cur.execute("select * from lstanding ")
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:2] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec,
                          columns=constcolumns[0:2]+['country'] +constcolumns[2:])

        return df.to_dict('records'), [{"name": i, "id": i}
                                       for i in df.columns]
'''

