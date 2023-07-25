import dash
from dash import  dcc, html, Input, Output        # pip install dash
import dash_bootstrap_components as dbc
from .utils import *
import sqlite3
import numpy as np
import plotly.express as px
import plotly.graph_objects as go






con = sqlite3.connect("fbref.db")
cur = con.cursor()
cur.execute("select squad from lstanding  order by country ")
records = cur.fetchall()
pl = [x[0] for x in records[18:38]]
laliga = [x[0] for x in records[38:58]]
bundesliga = [x[0] for x in records[0:18]]
seriea = [x[0] for x in records[78:98]]
ligue1 = [x[0] for x in records[58:78]]

cur.close()




dash.register_page(__name__,order=3)
layout=html.Div(
    [html.Div(
    dbc.Row([ dbc.Col([
        dcc.Dropdown(pl+laliga+seriea+bundesliga+ligue1, id='demo-dropdown',value=pl[0], placeholder="Select a club",style={'color': 'black',"font-family":"Rockwell","background-color":"#ea39b8"}),
        ],width=4)]),style={"margin-top":"20px","margin-bottom":"20px","width":"60%","margin-left":"auto","amrgin-right":"auto"}) ,#1st row

    html.Div(children=[dbc.Row([dbc.Col([dcc.Graph(id='player-usage')],className='col-6'),dbc.Col([dcc.Graph(id='squad-val')],className='col-6')])],style={"padding":"10px"}),#2nd row

    html.Div(dbc.Row([dbc.Col([dcc.Graph(id='zonedomination')],className='col-6'),dbc.Col([dcc.Graph(id='attstyle')],className='col-6')]),style={"padding":"10px"}),#3rd row
html.Div(dbc.Row([dbc.Col([dcc.Graph(id='squad-wheel')],className='col-6',width=12)]),style={"padding":"10px","margin":"auto"})

]
)

@dash.callback(
   [ Output('squad-wheel', 'figure'),Output('player-usage', 'figure'),Output('squad-val', 'figure'),Output('zonedomination', 'figure'),Output('attstyle', 'figure')],
    [Input('demo-dropdown', 'value')]
)
def update_graph(value):
    con = sqlite3.connect('fbref.db')
    c = con.cursor()

    if value not in pl+laliga+seriea+ligue1+bundesliga:
        print("false value",value)
        raise dash.exceptions.PreventUpdate

    else:
        graphcmd = "select age,mtplayed,min,player from astats where squad = '{}' ".format(value[1:])
        c.execute(graphcmd)
        r = c.fetchall()
        xval = []
        yval = []
        textval = []
        for x in r:
            if x[0] == '':
                continue

            xval.append(x[0])
            textval.append(x[3].split(' ')[-1])
            yval.append(
                int((int(x[2].replace(',', '')) / (x[1] * 90)) * 100 if type(x[2]) is str else (x[2] / (
                            x[1] * 90)) * 100))

        fig = go.Figure(layout_showlegend=False)
        fig.add_trace(go.Bar(
            x=[27],
            y=[100],
            marker_color='#eb4034', opacity=0.5, hoverinfo="none", name=" ",
            width=6
        ))
        fig.add_trace(go.Scatter(
            x=xval,
            y=yval, text=textval, hovertemplate='<b>%{text}<b>' + '<br><i>Age</i>: %{x}' +
                                                '<br>Mins: %{y}%<br>', marker_symbol='circle', mode='markers+text',
            name=" ", textfont=dict(
                family="Belanosimo",
                size=15,
                color="#ffcc00"
            ),
            textposition="bottom center"

        ))

        fig.add_annotation(x=20, y=15, text='YOUTH', align='center', valign='middle', opacity=0.3, font=dict(
            family="chela",
            size=30,
            color="lightyellow"
        ))
        fig.add_annotation(x=28, y=15, text='PRIME', align='center', valign='middle', opacity=0.3, font=dict(
            family="chela",
            size=30,
            color="lightyellow"
        ))
        fig.add_annotation(x=35, y=15, text='EXPERIENCED', align='center', valign='middle', opacity=0.3,
                           font=dict(
                               family="chela",
                               size=30,
                               color="lightyellow"
                           ))
        fig.update_layout(margin=dict(l=15, r=1, t=30, b=1),
                          title={
                              'text': 'Player Usage', 'x': 0.05,'y':0.98
                          }, template='plotly_dark',

                          xaxis_title='PLAYER AGE',
                          yaxis_title='PERCENTAGE OF MIN PLAYED', showlegend=False,
                          font=fontdict
                          )
        fig.update_xaxes(showgrid=False, linewidth=2, linecolor='black', mirror=True, range=[16, 40])
        fig.update_yaxes(showgrid=False, linewidth=2, linecolor='black', mirror=True, range=[0, 100])
        # squad val chart figure 2-----------
        fig2 = go.Figure()
        columns = ["Gk", "Defenders", "Midfielders", "Forwards", "Total"]

        graphcmd = "select * from transferstats where squad = '{}' ".format(value)
        c.execute(graphcmd)
        r = c.fetchall()

        gk = r[0][10]
        defe = r[0][7]
        forw = r[0][4]
        tot = r[0][-2]
        fig2.add_trace(go.Bar(x=columns, y=[gk, defe, tot - (gk + defe + forw), forw, tot], name=value, opacity=0.5,
                              hovertemplate='<b>{}<b>'.format(value[1:]) + '<br>%{x}: $%{y}'))
        leaguernk = r[0][0]

        if leaguernk > 0 and leaguernk < 6:
            leaguerankrange = [0, 6]
        elif leaguernk > 5 and leaguernk < 11:
            leaguerankrange = [5, 11]
        elif leaguernk > 11 and leaguernk < 16:
            leaguerankrange = [10, 16]
        elif r[0][2] == 'de GER':
            leaguerankrange = [15, 19]
        else:
            leaguerankrange = [15, 21]
        c.execute(
            "select avg(gkval),avg(defval),avg(attval),avg(totval) from transferstats where league= '{}' and leaguernk > {} and leaguernk < {} ".format(
                r[0][2], leaguerankrange[0], leaguerankrange[1]))
        liner = c.fetchall()
        gk = liner[0][0]
        defe = liner[0][1]
        forw = liner[0][2]
        tot = liner[0][3]
        fig2.add_trace(
            go.Scatter(x=columns, y=[liner[0][0], liner[0][1], tot - (gk + defe + forw), liner[0][2], liner[0][3]],
                       name="Avg valuation of clubs in  relative league standings", hovertemplate='<b>%{x}:<b> $%{y}', textfont=dict(family="Belanosimo")))
        fig2.update_layout(margin=dict(l=15, r=1, t=30, b=1),
                           legend=legenddict,
                           title={
                               'text': "Distribution of Player Valuation ( ${} millions )".format(r[0][13]),
                               'y': 0.98,
                               'x': 0.4,
                               'xanchor': 'center',
                               'yanchor': 'top'},

                           yaxis_title="Money  in millions", showlegend=True, template='plotly_dark',
                           font=fontdict
                           )

        # possesion percentage chart figure 3--------
        fig3 = go.Figure(data=[], layout={

            'xaxis': {
                'range': [-2, 122],
                'showticklabels': False,
                'showgrid': False,
                'zeroline': False,
            },

            'yaxis': {
                'range': [-2, 82],
                'showticklabels': True,
                'showgrid': False,
                'zeroline': False,
            },

            'shapes': [
                # Pitch
                {'type': 'rect', 'x0': 0, 'y0': 0, 'x1': 120, 'y1': 80},
                # Left Penalty
                {'type': 'rect', 'x0': 0, 'y0': 22.3, 'x1': 0 + 14.6, 'y1': 22.3 + 35.3},
                # Right Penalty
                {'type': 'rect', 'x0': 105.4, 'y0': 22.3, 'x1': 105.4 + 14.6, 'y1': 22.3 + 35.3},
                # Midline
                {'type': 'line', 'x0': 60, 'y0': 0, 'x1': 60, 'y1': 80},
                # Left Six Yard
                {'type': 'rect', 'x0': 0, 'y0': 32, 'x1': 0 + 4.9, 'y1': 32 + 16},
                # Right Six Yard
                {'type': 'rect', 'x0': 115.1, 'y0': 32, 'x1': 115.1 + 4.9, 'y1': 32 + 16},
                # Center Circle
                {'type': 'circle', 'xref': 'x', 'yref': 'y', 'x0': 60 - 8.1, 'y0': 40 - 8.1, 'x1': 60 + 8.1,
                 'y1': 40 + 8.1},
                # Center Spot
                {'type': 'circle', 'xref': 'x', 'yref': 'y', 'x0': 60 - 0.71, 'y0': 40 - 0.71, 'x1': 60 + 0.71,
                 'y1': 40 + 0.71},
                # Left Pen Spot
                {'type': 'circle', 'xref': 'x', 'yref': 'y', 'x0': 110.3 - 0.71, 'y0': 40 - 0.71,
                 'x1': 110.3 + 0.71, 'y1': 40 + 0.71},
                # Right Pen Spot
                {'type': 'circle', 'xref': 'x', 'yref': 'y', 'x0': 9.7 - 0.71, 'y0': 40 - 0.71, 'x1': 9.7 + 0.71,
                 'y1': 40 + 0.71},
            ]
        }
                         )
        graphcmd = "select *  from zonedomination where squad = '{}' ".format(value[1:])
        c.execute(graphcmd)
        r = c.fetchall()[0]



        x = np.array([9, 29, 53, 67, 89, 111])
        y = np.array([9, 29, 53, 67, 89, 111])

        z = np.array([r[1] - r[7], r[2] - r[8], r[3] - r[9], r[3] - r[9], r[4] - r[10], r[5] - r[11]])

        mtest = z > 0
        mtest2 = z <= 0
        j = 0
        for i in range(6):
            if i == 3:
                y[i] = y[i - 1]
            else:
                y[i] = round((r[j + 1] / (r[j + 1] + r[j + 7])) * 100, 1) if mtest[j] else round(
                    (r[j + 7] / (r[j + 1] + r[j + 7])) * 100, 1)
                j = j + 1

        tx = [10, 30, 60, 90, 110]

        tlabel = ['Def pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att pen']
        fig3.add_trace(
            go.Bar(x=x[mtest], y=y[mtest], opacity=0.5, name=value, width=14, hovertemplate='<b>%{y}<b>', legendrank=1))
        fig3.add_trace(
            go.Bar(x=x[mtest2], y=y[mtest2], opacity=0.5, name='Opponents', width=14, hovertemplate='<b>%{y}<b>',
                   legendrank=2))



        for i in range(5):
            fig3.add_annotation(x=tx[i], y=64, text=str(round(((r[i + 1] / r[6])) * 100, 1)), align='center',
                                valign='top',

                                font=dict(size=15, color='greenyellow', family='fantasy'))
            fig3.add_annotation(x=tx[i], y=3, text=tlabel[i], align='center',

                                font=dict(size=18, color='#ffcc00', family='Belanosimo'), showarrow=False)

        fig3.update_layout(margin=dict(l=15, r=1, t=30, b=1), template='plotly_dark',
                           legend=legenddict,
                           title={
                               'text': 'Zone Domination :Total ' + str(round((r[6] / (r[6] + r[12])) * 100, 1)) + '%',
                               'x': 0.1, 'y': 0.98,
                           }, xaxis=dict(
                tickmode='array',
                tickvals=tx,
                ticktext=tlabel
            ),
                           font=fontdict
                           )

        # attstyle chart figure 4------
        graphcmd = "select m.directness,summedup,ls.mp,sq from (select squad as sq,sum(x) as summedup from (select a.league,a.squad,t.scapasslive as x from gca as t ,astats as a where t.pid=a.pid ) group by squad having trim(league)=(select trim(aa.league) from astats  as aa where trim(aa.squad)= trim('{}') )),lstanding as ls,markstats as m, squadkey as k where trim(ls.squad)=trim(sq)and trim(ls.squad) = trim(k.fbrefsquad)and trim(m.squad) = trim(k.markstatssquad)  ;".format( value)
        c.execute(graphcmd)
        r = c.fetchall()
        print(r)
        xval = []
        yval = []
        squadstats = [int(r[0][1] / r[0][2]), int(r[0][0]), r[0][3]]

        fullform = []
        for x in r:
            if x[0] == '':
                continue
            if x[3] == value:
                squadstats = [int(x[1] / x[2]), int(x[0]), x[3]]
            xval.append(int(x[1] / x[2]))
            fullform.append(x[3])

            yval.append(int(x[0]))
        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(x=xval, y=yval, text=fullform, name=" ", hovertemplate='<b>%{text}<b>', marker_symbol='circle',
                       mode='markers+text', textfont=dict(
                    family="Belanosimo",
                    size=12,
                    color="orange"
                ),
                       textposition="bottom center"))
        # highlighting the club
        fig4.add_trace(
            go.Scatter(x=[squadstats[0]], y=[squadstats[1]], text=[squadstats[2]], name=" ",
                       hovertemplate='<b>%{text}<b>', marker_symbol='circle',
                       mode='markers+text', textfont=dict(
                    family="Belanosimo",
                    size=12,
                    color="orange"
                ),
                       textposition="bottom center"))

        fig4.update_layout(margin=dict(l=15, r=1, t=30, b=1), template='plotly_dark',
                           title={
                               'text': 'Attacking Style', 'x': 0.1, 'y': 0.98},
                           xaxis_title='PPS',
                           yaxis_title='DIRECTNESS', showlegend=False,
                           font=fontdict
                           )
        fig4.update_xaxes(showgrid=False, linewidth=2, linecolor='black', mirror=True)
        fig4.update_yaxes(showgrid=False, linewidth=2, linecolor='black', mirror=True)

        # pizza plot figue 5-------
        params = ["Buildup", "Field Tilt", "Directness",
                  "Progressive\nPasses", "Switches", "Dribbling",
                  "Set pieces", "Chance Creation", "Chance Conversion",
                  "Start Distance", "Defensive\nActions", "Highpress"

                  ]

        values = squadwheelhelper(c, value)

        # values for corresponding parameters

        slice_colors = ["#1A78CF"] * 3 + ["#FF9300"] * 3 + ["#ff4000"] * 3 + ['#00ff40'] * 3


        fig5 = go.Figure(go.Barpolar(
            r=values,
            theta=params,
            # width=[4 for x in params ],
            marker_color=slice_colors, name='',
            marker_line_color="black",
            marker_line_width=.5, hovertemplate='<b>%{theta}<b><br>%{r}%',
            opacity=0.8, legendgroup="aTT"
        ))

        fig5.update_layout(legend_title="categories",
                           template='plotly_dark', margin=dict(l=15, r=1, t=30, b=30),
                           title={'x': 0.1,'y':0.98,
                                  'text': 'Squad Wheel'},
                           font=fontdict,
                           polar=dict(
                               radialaxis=dict(range=[0, 100], showticklabels=True, ticks=''),
                               angularaxis=dict(showticklabels=True, ticks='')
                           ),

                           )

        return fig, fig2, fig3, fig4, fig5


