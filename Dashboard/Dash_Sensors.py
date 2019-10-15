from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime as dt
from datetime import timedelta as td


url_base = '/dash/sensors/'


layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(html.H1("Sensor Name",id ="sensor_title"))
    ],align="start"),
    dbc.Row([
        dbc.Col(
            dbc.Label([
                "Sensor ID",
                dcc.Dropdown(
                    id="sensor_dropdown",
                    placeholder="sensor-id"
                    )
            ],style = {"width":"72%"}),
            width = {"size": 2, "order": 1, "offset": 0}),
        dbc.Col(
            dbc.Label([
                "Graph Datepicker",
                dcc.DatePickerRange(
                    id = "datepicker",
                    display_format='DD / MM / YYYY',
                    start_date_placeholder_text='dd/mm/yyyy'
                    )
            ]),
            width = {"size": 4, "order": 2, "offset": 0}),
        dbc.Col(
            dbc.Row([
                dbc.Col(
                    dbc.Label([
                        "Last Data",
                        dbc.Input(
                            id="#_data",
                            placeholder="# of data",
                            debounce=True, 
                            type = "number",
                            value = 20,
                            min = 0
                        ) 
                    ]),width = {"size": 4, "order": 1, "offset": 0}
                ),
                dbc.Col(
                    dbc.Label([
                        "Refresh Rate",
                        dbc.Input(
                            id="refresh_rate",
                            placeholder= "miliseconds",
                            debounce=True, 
                            type = "number",
                            value = 2000,
                            min = 0,
                            step = 100
                        ) 
                    ]),width = {"size": 4, "order": 2, "offset": 0}
                ),
                dbc.Col(
                    dbc.Button("Refresh",id="btn_refresh_rate",color = "info"),
                    width = {"size": 4, "order": 3, "offset": 0}
                )
            ],justify="start",align="center"),
            width = {"size": 6, "order": 3, "offset": 0})
    ],justify="start",align="center"),
    dbc.Row([
        dbc.Col(dcc.Graph(id = "temp_graph")),dbc.Col(dcc.Graph(id = "moist_graph"))
    ]),
    dcc.Interval(
            id='graph-update',
            interval=2000,
            n_intervals = 0
    )
])

def create_graph(data_dict):
    temp_data = go.Scatter(
        x= data_dict["dates"],
        y= data_dict["temps"],
        name='Scatter',
        mode= 'lines+markers',
        marker=dict(
            color='#17a2b8',
            line=dict(
                color='#17a2b8'
            ))
        )
    moist_data = go.Scatter(
        x= data_dict["dates"],
        y= data_dict["moists"],
        name='Scatter',
        mode= 'lines+markers',
        marker=dict(
            color='#17a2b8',
            line=dict(
                color='#17a2b8'
            ))
        )
    # graph_layout =  go.Layout(
    #         title = title,
    #         autosize= False,
    #         showlegend=False
    #         )
    # graph_layout =  go.Layout(
    #         title = "title",
    #         autosize= False,
    #         showlegend=False
    #         )
    return [{'data': [temp_data],'layout' : go.Layout(title="Temperature Data")},
                {'data': [moist_data],'layout' : go.Layout(title="Moisture Data")}]


def Add_Dash(server):
    from app.base.models import User, SensorInformationModel
    from app.base.sensormodels import SensorModel
    from flask_login import current_user

    app = Dash(server=server, url_base_pathname=url_base,external_stylesheets=[dbc.themes.BOOTSTRAP])
    apply_layout_with_auth(app, layout)

    @app.callback(
            [Output('sensor_dropdown', 'options'),Output('sensor_dropdown', 'value')],
            [Input('url', 'pathname')])
    def callback_fun(pathname):
        if pathname == "/dash/sensors/":
            if current_user.username == "admin":
                sensor_data = SensorInformationModel.find_all_unique_ids()
                options=[{'label':opt, 'value':opt} for opt in sensor_data]
                return options, "Sensor Name"
            else:
                user = User.find_by_username(username=current_user.username)
                sensor_data = SensorInformationModel.find_unique_ids_by_user_id(user.id)
                options=[{'label':opt, 'value':opt} for opt in sensor_data]
                return options, "Sensor Name"
        else:
            return [{}], "Sensor Name"

    @app.callback(
            Output('sensor_title', 'children'),
            [
                Input('sensor_dropdown', 'value')
            ]
        )
    def change_value(value):
        try:
            user_id , sensor_id = value.split("_")
            sensor_info = SensorInformationModel.find_by_user_id_and_sensor_id(user_id,sensor_id)
            return sensor_info.json()["sensor_name"]
        except:
            return "Sensor Name"


    # Real Time ON/OFF Button Callback
    @app.callback(
        [Output('graph-update', 'disabled'),
        Output('btn_refresh_rate', 'children')],
        [Input('btn_refresh_rate', 'n_clicks')])
    def update_output(n_clicks):
        if n_clicks:
            return [True,"Refresh: OFF"] if (n_clicks % 2 == 0) else [False,"Refresh: ON"]
        else: 
            return [False,"Refresh: ON"]

    @app.callback(Output('graph-update',"interval"),
                    [Input("refresh_rate","value")])
    def change_refresh_rate(interval):
        return interval if interval > 0 else 2000
    
    @app.callback([Output('temp_graph', 'figure'),Output('moist_graph', 'figure')],
                [
                    Input('graph-update', 'disabled'),
                    Input('graph-update', 'n_intervals'),
                    Input('sensor_dropdown', 'value'),
                    Input('#_data', 'value'),
                    Input('datepicker', 'start_date'),
                    Input('datepicker', 'end_date')
                ])
    def update_graph_scatter(update, n_interval, sensor_id, n,start_date, end_date):
        if not update:
            try:    
                sensor_data = SensorModel.find_last_n_data_by_id(sensor_id, n=n)
            except TypeError:
                sensor_data = SensorModel.find_last_n_data_by_id(sensor_id, n=20)
            data_dict =   {     
                "dates":[data["date"] for data in sensor_data],
                "moists":[data["moisture"] for data in sensor_data],
                "temps":[data["temperature"] for data in sensor_data]
                }
            return create_graph(data_dict)
        else:
            try:
                start_dt = dt.strptime(start_date,'%Y-%m-%d')
                end_dt = dt.strptime(end_date,'%Y-%m-%d')
                print(start_dt, end_dt)  
                sensor_data = SensorModel.find_last_n_data_by_id_and_date(sensor_id, n=n,end = end_dt,start = start_dt)
            except TypeError:
                sensor_data = SensorModel.find_last_n_data_by_id(sensor_id, n=20)
            data_dict =   {     
                "dates":[data["date"] for data in sensor_data],
                "moists":[data["moisture"] for data in sensor_data],
                "temps":[data["temperature"] for data in sensor_data]
                }
            return create_graph(data_dict)
            

    return app.server