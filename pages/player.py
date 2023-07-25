import dash
from dash import  dcc, html, Input, Output    # pip install dash
import dash_bootstrap_components as dbc
from .utils import  *
import sqlite3


#fetching player names
con = sqlite3.connect("fbref.db")
cur = con.cursor()
cur.execute("select DISTINCT(pid),markstatsplayer from ( select a.pid,p.markstatsplayer  from astats as a ,playerkey as p where a.min>1000 and trim(p.fbrefplayer)=trim(a.player));")
records = cur.fetchall()
records=[x[1] for x in records]
cur.close()

dash.register_page(__name__,order=2)

layout=html.Div([html.Div(
    dbc.Row([ dbc.Col([
        dcc.Dropdown(records, id='demo-dropdown',value="Lionel Messi", placeholder="Select a player",className="drop",style={"background-color":"#ea39B8","color":"black","font-family":"Rockwell"}),
        ],width=12)]),style={"margin-bottom":"20px","margin-top":"20px","width":"25%","margin-left":"auto","margin-right":"auto"}) ,#1st row

    html.Div(dbc.Row([
        dbc.Col([html.Div("Category:",style={"font-weight":"bold","padding-right":"100px","text-align":"right","margin-bottom":"10px","color":"#F5EFE7","font-family":"Rockwell"})]),
        dbc.Col([html.Div("Similar Players:",style={"font-weight":"bold","padding-left":"50px","text-align":"left","color":"#F5EFE7","font-family":"Rockwell"})])
                        ])),

    html.Div(children=[dbc.Row(children=[html.Div(children=[dbc.Col(children=[dcc.Markdown(id='sim-players1')])],style={"text-align":"right","width":"45%","padding-right":"1.5%","font-family":"Rockwell"}),

        html.Div(children=[dbc.Col(children=[dcc.Markdown(id='sim-players2')]),dbc.Col(children=[html.Div(dcc.Markdown(id='sim-players3'))]),html.Div(dbc.Col(children=[dcc.Markdown(id='sim-players4')]))],
                 style={"width":"25%","text-align":"center","font-family":"Rockwell"}),

        ])]),



    html.Div(children=[dbc.Row([dbc.Col([dcc.Graph(id='player-style')],className='col-6')],className='row-10')],style={"width":"60%","margin-left":"auto","margin-right":"auto","margin-bottom":"10px"}),
    html.Div(children=[dbc.Row([dbc.Col([dcc.Graph(id='plot1')],className='col-6')],className='row-10')],style={"width":"60%","margin-left":"auto","margin-right":"auto","margin-bottom":"10px"}),
    html.Div(children=[dbc.Row([dbc.Col([dcc.Graph(id='plot2')],className='col-6')],className='row-10')],style={"width":"60%","margin-left":"auto","margin-right":"auto","margin-bottom":"10px"}),



])

@dash.callback([Output('sim-players1', 'children'),Output('sim-players2', 'children'),Output('sim-players3', 'children'),Output('sim-players4', 'children'),Output('player-style', 'figure'),Output('plot1', 'figure'),Output('plot2', 'figure')],
               [Input('demo-dropdown', 'value')])
def update_graph(value):
    if value not in records:
        print(value)
        raise dash.exceptions.PreventUpdate
    else:
        con = sqlite3.connect('fbref.db')
        c = con.cursor()
        #extracting player id and position from name
        c.execute(
            "select pid,position from astats where playedfull >10 and player=(select fbrefplayer from playerkey where markstatsplayer=  '{}')".format(
                value))
        rec = c.fetchall()[0]
        playerid = rec[0]
        position = rec[1]

        print(playerid, position)

        data,titles=graph_matcher(c,playerid,position)

        fig2=plotone(c,playerid,position)
        fig3=plottwo(c,playerid,position)
        # category def
        categories = ["Poacher/No.9-Tier 1", "Attacking-Fullback-Tier 2", "Ball Playing Centre Back -Tier 2",
                      "No.10-Tier 2", "Solid and Physical Centre Back-Tier 1", "Ball Playing Centre Back -Tier 1",
                      "No.8-Tier 2", "Defensive Midfielder-Tier 1", "Poacher/No.9-Tier 2", "Winger-Tier 1",
                      "Attacking-Fullback-Tier 1", "Orchestrator-Tier 1", "Defensive Midfielder-Tier 2",
                      "No.8-Tier 1", "Winger-Tier 2", "Solid and Physical Centre Back-Tier 2", "Complete Forward",
                      "Orchestrator-Tier 2", "Conventional FullBack", "No.10-Tier 1", "Goalkeeper"]

        # picking similar players
        similarplayers = []
        if position != 'GK':
            c.execute("select cluster from clusterinfo where pid= {} ".format(playerid))
            clusterid = c.fetchall()[0][0]

            c.execute(
                "select sFirst,sSecond,sThird from similarplayers where pid=  '{}'".format(playerid))

            rec = c.fetchall()[0]
            print(rec)
            for x in rec:
                c.execute(
                    "select player from astats where pid=  '{}'".format(x))
                temp = c.fetchall()[0][0]
                print("similar players", temp)
                similarplayers.append(temp)
        else:
            clusterid = len(categories) - 1
            c.execute("select player from totgk where pid<> {}  order by random() Limit 3;".format(playerid))
            rec = c.fetchall()
            for x in rec:
                print("similar players", x[0])
                similarplayers.append(x[0])

        c.close()
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=titles,name='',
            fill='toself',fillcolor='#eb4034',line=dict(color="#781f19"),
        ))

        fig.update_layout(
            margin=dict(l=20, r=20, t=25, b=35),
            title={
                'text': 'Player Wheel', 'x': 0.07, 'y': 0.97,
            }, font=fontdict,
            width=1000, height=700,
            polar=dict(
                radialaxis=dict(
                    visible=True
                ),
            ), template='plotly_dark',
            showlegend=False
        )
        fig.update_layout(
            polar={"radialaxis": {"tickvals": [i for i in range(0, 101, 20)], 'range': [0, 100]}})

        fig2.update_layout(
            margin=dict(l=20, r=5, t=30, b=25),
            title={
                'x': 0.07, 'y': 0.97,
            }, font=fontdict,
            width=1000, height=500, template='plotly_dark',

        )
        fig3.update_layout(
            margin=dict(l=20, r=5, t=25, b=25),
            title={
                'x': 0.07, 'y': 0.97,
            }, font=fontdict,
            width=1000, height=500, template='plotly_dark',

        )
        return categories[clusterid],similarplayers[0],similarplayers[1],similarplayers[2],fig,fig2,fig3














"""
dash.register_page(__name__)
leagueopts=['Premier League','LaLiga','Bundesliga','Ligue1','Serie A','All']
con = sqlite3.connect("fbref.db")
cur = con.cursor()
cur.execute("select * from lstanding where country='{}'".format('eng ENG'))
records = cur.fetchall()
rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
df = pd.DataFrame(rec, columns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                'xgd'])

layout=html.Div(
    [
html.Div(
    dbc.Row([ html.Div([], className = 'col-5'),dbc.Col([
        dcc.Dropdown(leagueopts, id='demo-dropdown', placeholder="Select a league",style={'color': 'black'}),
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
        style_data=dict(backgroundColor="purple", height='auto', whitespace='normal')
    ))  # 2nd row

         ]
)

@dash.callback([Output('table1','data'),Output('table1','columns')],[Input('demo-dropdown', 'value')],prevent_initial_call=True)
def update_table(value):
    leaguematcher = {'Premier League': 'eng ENG', 'LaLiga': 'es ESP', 'Bundesliga': 'de GER', 'Ligue1': 'fr FRA',
                     'Serie A': 'it ITA'}
    con = sqlite3.connect("fbref.db")
    cur = con.cursor()
    if value!='All':

        cur.execute("select * from lstanding where country='{}'".format(leaguematcher[value]))
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec, columns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                        'xgd'])

        return df.to_dict('records'),[{"name": i, "id": i}
                     for i in df.columns]
    else:
        cur.execute("select * from lstanding ")
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:2] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec,
                          columns=['rnk', 'squad','country', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                   'xgd'])

        return df.to_dict('records'), [{"name": i, "id": i}
                                       for i in df.columns]

layout =html.Div(
    [html.Div([html.Div([dbc.Col(className='col-2')],className='col-2'),dcc.Tabs(id="tab-styled-props",value='Premier League',children=[
        dcc.Tab(value='Premier League',label='Premier league'),
        dcc.Tab(value='LaLiga',label='La liga'),
        dcc.Tab(value='Bundesliga',label='Bundesliga'),
        dcc.Tab(value='Ligue1',label='Ligue 1'),
        dcc.Tab(value='Serie A',label='Serie A'),dcc.Tab(value='All',label='All')],colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }

    ),dcc.Store(storage_type='session',id='clubstore')],className='col-8')
     , dcc.Link(
             html.Div(id='tabs-content-props'),
            id="ticker-search2-link",
            href="/",
        ),]

)

@dash.callback(
    Output("ticker-search2-link", "href"),
    Input('tabs-content-props', "active_cell"),
    prevent_initial_call=True,
)
def search(ticker):

    if ticker is None or ticker == "":
        return dash.no_update
    print("ticker", ticker)
    return "/team"

@dash.callback(Output('clubstore','data'),[Input('','')])
def store_value(value):
    return value

@dash.callback(Output('tabs-content-props','children'),[Input('tab-styled-props', 'value')])
def update_table(value):
    leaguematcher = {'Premier League': 'eng ENG', 'LaLiga': 'es ESP', 'Bundesliga': 'de GER', 'Ligue1': 'fr FRA',
                     'Serie A': 'it ITA'}
    con = sqlite3.connect("fbref.db")
    cur = con.cursor()

    if value!='All':

        cur.execute("select * from lstanding where country='{}'".format(leaguematcher[value]))
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:1] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec, columns=['rnk', 'squad', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                        'xgd'])



    else:
        cur.execute("select * from lstanding ")
        records = cur.fetchall()
        rec = [list(x[2:3] + x[0:2] + x[3:11] + x[12:15]) for x in records]
        df = pd.DataFrame(rec,
                          columns=['rnk', 'squad','country', 'mp', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'pts', 'xg', 'xga',
                                   'xgd'])

    return [html.Div([dash_table.DataTable(
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
            style_data=dict(backgroundColor="purple", height='auto', whitespace='normal')
        )])]
"""