from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

import dash_daq as daq
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
from collections import deque
import random

url_base = '/dash/app3/'

# Data Definitions
X = deque(maxlen=40)
X.append(1)
Y = deque(maxlen=40)
Y.append(1)
led_state = "CLOSE"

plot_data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode= 'lines+markers',
        marker=dict(
            color='#73A839',
            line=dict(
                color='#73A839'
            ))
        )
graph_layout = go.Layout(
                title = "Air Temperature Data",
                xaxis=dict(
                    showline=False,
                    showgrid=True,
                    zeroline=False,
                    showticklabels=True,
                    linecolor= "#444444",
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Roboto',
                        size=15,
                        color= "#444444",
                        )
                    ),
                yaxis=dict(
                    showline=False,
                    showgrid=True,
                    zeroline=False,
                    showticklabels=True,
                    linecolor= "#444444",
                    linewidth=2,
                    tickfont=dict(
                        family='Roboto',
                        size=15,
                        color= "#444444",
                        )
                    ),
                autosize=True,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor = 'white'
                )

fig = go.Figure({'data': [plot_data],'layout' : graph_layout})

layout = html.Div(
    [	
        dbc.Row([
            dbc.Col(
                daq.PowerButton(
                    id='my-power-button',
                    label = "LED STATUS",
                    size = 60,
                    on=False,
                    color = "#73A839",
                    # style = {
                    #     'top': '1.5%',
                    #     'left':'20%',
                    #     'position':'absolute'
                    #     }
                    ),
            width = {"size": 2, "order": 1, "offset": 0}),
            dbc.Col(
                dbc.Button(
                    "Real Time On",
                    id = "button",
                    color = "success",
                    # style = {
                    #     'top': '6.8%',
                    #     'left':'8%',
                    #     'position':'absolute'
                    #     }
                    ),
            width = {"size": 2, "order": "first", "offset": 0}),
            dbc.Col(
                html.H1(
                    "Dature Project",
                    style = {
                        # 'textAlign': 'center',
                        # "margin-top": "2.5%",
                        # "font-size" : "3rem",
                        "color": "#73A839"
                    }
                ),
            width = {"size": 4, "order": 2, "offset": 0})
        ],justify="start",align="center"),
        dbc.Row(dbc.Col(dcc.Graph(id='live-graph', animate=False,style = {"margin-top":"2%"})),justify="start"),
        dcc.Interval(
            id='graph-update',
            interval=1000,
            n_intervals = 0
        )   
    ]
)

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, external_stylesheets=[dbc.themes.BOOTSTRAP])
    apply_layout_with_auth(app, layout)

    # power button for led turn on/off state
    @app.callback(Output('my-power-button', 'label'),
                [Input('my-power-button', 'on')])
    def update_led_state(on):
        global led_state
        led_state = "OPEN" if on else "CLOSE"
        return "LED "+led_state

    # Real Time ON/OFF Button Callback
    @app.callback(
        [Output('graph-update', 'disabled'),
        Output('button', 'children')],
        [Input('button', 'n_clicks')])
    def update_output(n_clicks):
        if n_clicks:
            return [True,"Real Time: OFF"] if (n_clicks % 2 == 0) else [False,"Real Time: ON"]
        else: 
            return [False,"Real Time: ON"]

    # Update Graph Callback
    @app.callback(Output('live-graph', 'figure'),
                [Input('graph-update', 'n_intervals')])
    def update_graph_scatter(n):
        global graph_layout
        data = go.Scatter(
                X.append(X[-1]+1),
                Y.append(random.uniform(20,40)),
                x=list(X),
                y=list(Y),
                name='Scatter',
                mode= 'lines+markers',
                marker=dict(
                    color='#73A839',
                    line=dict(
                    color='#73A839'
                    ))
                )
        return {'data': [data],'layout' : graph_layout}

    return app.server