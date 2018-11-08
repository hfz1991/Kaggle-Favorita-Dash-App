import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from app import app

forecast = pd.read_table("all/new/forecast/forecast.csv", sep=",")

layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Sales performance'),
            dcc.Link('Sales performance', href='/apps/train', style={'margin-right': '35px'}),
            dcc.Link('Stores', href='/apps/stores', style={'margin-right': '35px'}),
            dcc.Link('Transactions', href='/apps/transactions', style={'margin-right': '35px'}),
            dcc.Link('Oil', href='/apps/oil', style={'margin-right': '35px'}),
            dcc.Link('Prediction', href='/apps/predict', style={'margin-right': '35px'}),
        ],className="container" , style={'color':'#fff',}),
    ], style={'background-color':'#2a3f5f', 'padding': '20px 0px'}),
    html.Div([
        html.H3('Prediction', style={'margin-top':'20px'}),
        
        html.Div([
            html.Img(
                src='/static/forecast.png',
                style={
                    'width': '60%',
                    'position' : 'relative',
                    'padding-top' : 30,
                    'padding-right' : 0
                })
        ]),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='predict',
                    options=[{'label': i, 'value': i} for i in forecast.ds],
                    value=''
                ),
            ], className="col-md-6", style={'margin-top': '30'}),
            html.Div([
                html.Div(
                    html.Div(id='result_div'),
                className="col-md-6"),
            ], style={'margin-top': '20'}),
        ],className="row"),

    ], className="container")
])


@app.callback(
    Output(component_id='result_div', component_property='children'),
    [Input(component_id='predict', component_property='value')]
)
def update_output_div(input_value):
    forecast_info = forecast[forecast['ds'] == input_value]
    
    return html.Div([
            html.H4('Result: {}'.format(forecast_info.yhat_lower.values[0])),
        ])