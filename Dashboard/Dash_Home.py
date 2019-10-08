from dash import Dash
from dash_table import DataTable
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd
from app.extensions import db


url_base = '/dash/home/'

def create_users_table(data,columns):
    return  [
        dbc.Row(html.H4("Registered Users"),style={"margin-left":"47%"}),
        dbc.Row(html.Div([
                DataTable(
                    data=data,
                    columns=columns,
                    css= [
                        {
                            'selector': 'td.cell--selected, td.focused', 
                            'rule': 'background-color: #FFFF !important;'
                        },
                        {
                            'selector': 'table', 
                            'rule': "width: 50% !important; "
                        }
                    ],
                    style_table={'minWidth': '100px'}
                )
        ],style={"width":"100%","margin-left":"30%"}))
    ]


layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Col([
        html.Div(id="info_table")
    ])
])

def Add_Dash(server):
    from app.base.models import User
    from flask_login import current_user

    app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('info_table', 'children'),
            [Input('url', 'pathname')])
    def callback_fun(pathname):
        if pathname == "/dash/home/":
            if current_user.username == "admin":
                df = pd.DataFrame([user.json() for user in User.find_all()])
                df = df[["id","username","e-mail"]]
                columns=[{"name": i, "id": i} for i in df.columns]
                data= df.to_dict("records")
                return create_users_table(data,columns)
            else:
                return dbc.Row(html.H4("You are not authorized to see registered Users"),style={"margin-left":"38%"})   
        return None
    
    return app.server