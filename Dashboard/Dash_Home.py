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

def create_things_table(data_fields,columns_fields,data_sensors,columns_sensors):
    return  [
        dbc.Row(html.H4("Registered Fields"),style={"margin-left":"47%"}),
        dbc.Row(html.Div([
                DataTable(
                    data=data_fields,
                    columns=columns_fields,
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
        ],style={"width":"100%","margin-left":"30%"})),
        dbc.Row(html.H4("Registered Sensors"),style={"margin-left":"47%"}),
        dbc.Row(html.Div([
                DataTable(
                    data=data_sensors,
                    columns=columns_sensors,
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
                df = df[["user_id","username","e-mail"]]
                columns=[{"name": i, "id": i} for i in df.columns]
                data= df.to_dict("records")
                return create_users_table(data,columns)
            else:
                user_data = User.find_by_username(current_user.username).jsonify_all()
                if user_data["field_info"]:
                    field_df = pd.DataFrame(user_data["field_info"])
                    field_df = field_df[["user_id","field_id","field_name"]]
                    field_columns = [{"name": i, "id": i} for i in field_df.columns]
                    field_data = field_df.to_dict("records")
                else:
                    field_data,field_columns = {},[]
                if user_data["sensor_info"]:
                    sensor_df = pd.DataFrame(user_data["sensor_info"])
                    sensor_df = sensor_df[["user_id","sensor_id","sensor_name","field_name","sensor_unique_id"]]
                    sensor_columns = [{"name": i, "id": i} for i in sensor_df.columns]
                    sensor_data = sensor_df.to_dict("records")
                else:
                    sensor_data,sensor_columns = {},[]
                return create_things_table(field_data,field_columns,sensor_data,sensor_columns)
        return None
    
    return app.server