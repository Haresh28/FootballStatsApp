import dash
from dash import Dash, dcc, html, Input, Output ,dash_table ,ctx ,State      # pip install dash
import dash_bootstrap_components as dbc         # pip install dash_bootstrap_components
import os
from Utils import master_scrapper
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
import time
from tqdm import tqdm
import sys

def valuesetter():
    if not os.path.isfile("fbref.db"):
        master_scrapper()


valuesetter()
cache = diskcache.Cache('./cache')
lcm = DiskcacheLongCallbackManager(cache)
app = Dash(__name__, long_callback_manager=lcm,use_pages=True,external_stylesheets=[dbc.themes.VAPOR])

app.config.suppress_callback_exceptions = True
pbar = dbc.Progress(id='pbar',style={'margin-top': 15,"visibility": "hidden"})

timer_progress = dcc.Interval(id='timer_progress',interval=1000)

row_4 = dbc.Col([pbar,timer_progress], className='col-2')
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2",style={"color":"black"})
                    ],

                    href=page["path"],
                    active="exact",

                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=True,
            className="bg-light",
            style={"width":"100%","display":"flex","justify-content":"center"}

)


app.layout=html.Div(
    children=[
           html.Div(dbc.Row([dbc.Col(dbc.Button("Update",id="update",title="Load new data from net",style={"margin-left":"55px","margin-top":"10px","margin-bottom":"10px"}),className='col-2'),row_4
                                ,dbc.Col(html.H2("FOOTBALL STATISTICS APP",style={"margin-right":"55px","text-align":"center","width":"50%","font-family":"High Tower Text","font-weight":"bold"}))]))
        ,html.Div(id="hidden-div",style={"display":"none"}),html.Div(id="hidden-div2",style={"display":"none"}),html.Div([sidebar],className='col-4',style={"width":"100%","font-family":"High Tower Text"}),dash.page_container




    ],style={"display":"flex","flex-direction":"column"})
@app.callback(Output("hidden-div","children"),[Input('update', 'n_clicks')], prevent_initial_call=True)
def update_data(n_clicks):

    if ctx.triggered_id == "update":
        print("started")
        #master_scrapper()
        print("download completed")
        return "buttonset"
    else:
        return dash.exceptions.PreventUpdate


def time_consuming_function(number: float) -> float:
    for i in tqdm(range(20)):
        time.sleep(0.5)

    result = number ** 0.5

    return result


@app.callback(
    Output('pbar', 'value'),
    Output('pbar', 'label'),
    Input('timer_progress', 'n_intervals'),
    prevent_initial_call=True)
def callback_progress(n_intervals: int) -> (float, str):
    try:
        with open('progress.txt', 'r') as file:
            str_raw = file.read()
        last_line = list(filter(None, str_raw.split('\n')))[-1]
        #print("lastline",last_line)
        percent = float(last_line.split('%')[0])

    except:
        percent = 0

    finally:
        text = f'{percent:.0f}%'
        return percent, text
@app.long_callback(
    output=Output("hidden-div2","children"),
    inputs=[Input('hidden-div', 'children')],
    running=[(Output('update', 'disabled'), True, False),(
        Output("pbar", "style"),
        {"visibility": "visible"},
        {"visibility": "hidden"},
    ),

    ],
    prevent_initial_call=True
)
def callback_hidden(btn_name) :
    std_err_backup = sys.stderr
    file_prog = open('progress.txt', 'w')
    sys.stderr = file_prog


    print("download started")
    master_scrapper()
    print("download completed")
    result_str = "download completed"

    file_prog.close()
    sys.stderr = std_err_backup

    return result_str

if __name__ == "__main__":
    app.run_server(debug=True)





