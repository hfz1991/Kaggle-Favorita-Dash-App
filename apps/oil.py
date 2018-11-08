import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from app import app

oil = pd.read_table("all/oil.csv", sep=",")

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
        html.H3('Oil', style={'margin-top':'20px'}),
        dcc.Graph(
            id='oil',
            figure={
                'data': [
                    go.Scatter(
                        x = oil['date'],
                        y = oil['dcoilwtico'],
                        mode = 'lines',
                        name = 'lines'
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Price'},
                    hovermode='closest'
                )
            }
        ),
    ], className="container")
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
