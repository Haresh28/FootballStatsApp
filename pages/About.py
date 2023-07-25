import dash
from dash import Dash, dcc, html, Input, Output        # pip install dash
import dash_bootstrap_components as dbc

dash.register_page(__name__,order=4)

layout=html.Div(children=[
    dbc.Row(html.Div("Why are Roles needed?",style={"font-size":"25px","color":"#F5EFE7","margin":"25px 0px 15px 15px",
                                                    "font-weight":"bold"})),
    dbc.Row(html.P(''' Position is a higher-level abstraction of roles within a team . Players in the same position can often have different roles , which can be influenced by the playing style of their team . Comparing the abilities of players across different roles can be unfair since some roles may not require certain attributes that others do .
                        To address this issue , we not only divide players based on their roles but also consider their quality . This approach allows us to assess a player's performance in comparison to others at their level , accounting for the specific demands of their role and the attributes relevant to their position . By doing so, we can make a more accurate evaluation of a player's abilities and contributions within their respective position and role .
''',style={"margin":"25px 0px 15px 15px","font-size":"20px","width":"95%","text-align":"justify"})),
    dbc.Row(html.Div("CHARTS ",
                     style={"font-size": "25px", "color": "#F5EFE7", "margin": "25px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.Div("1. Distribution of player's valuation :",
                     style={"font-size": "22px", "color": "#F5EFE7", "margin": "15px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.P(''' The players' values are categorized based on their positions. The red line represents the average value of these positions across the league standings relative to the selected team. For example, if the chosen team is in 7th place, the values are averaged over the teams placed from 6th to 10th.
''',style={"margin":"5px 0px 15px 15px","font-size":"20px","width":"95%","text-align":"justify"})),
    dbc.Row(html.Div("2. Zone Domination : ",
                     style={"font-size": "22px", "color": "#F5EFE7", "margin": "15px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.P(''' The pitch is divided into five parts, and the amount of possession in each part, along with the side that dominated each part, is highlighted.
''',style={"margin":"5px 0px 15px 15px","font-size":"20px","width":"95%","text-align":"justify"})),
    dbc.Row(html.Div("3. Attacking Style : ",
                     style={"font-size": "22px", "color": "#F5EFE7", "margin": "15px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.P(''' The data shows the attacking style of the teams in their respective leagues. "Passes per sequence" indicates the average number of passes made per attacking sequence.
''',style={"margin":"5px 0px 15px 15px","font-size":"20px","width":"95%","text-align":"justify"})),
    dbc.Row(html.Div("4. Squad Wheel : ",
                     style={"font-size": "22px", "color": "#F5EFE7", "margin": "15px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.P(''' The squad wheel is a helpful tool in understanding the overall playstyle of the team.The club percentile rank is determined by comparing the performance of a club against other clubs in the top 5 leagues. 
    It indicates how a particular club's performance stacks up relative to its counterparts in those leagues.
''', style={"margin": "5px 0px 15px 15px", "font-size": "20px", "width": "95%", "text-align": "justify"})),
    dbc.Row(html.Div("5. Player Wheel : ",
                     style={"font-size": "22px", "color": "#F5EFE7", "margin": "15px 0px 15px 15px",
                            "font-weight": "bold"})),
    dbc.Row(html.P(''' The player wheel is a useful tool for distinguishing the qualities of players who play in the same position as the chosen player. Each position demands a different set of attributes, 
    and the player wheel showcases these unique characteristics to help compare and contrast players effectively. It allows for a comprehensive assessment of players based on the specific requirements and demands of their respective positions.
''',style={"margin":"5px 0px 15px 15px","font-size":"20px","width":"95%","text-align":"justify"})),
],style={"font-family":"Rockwell"})
