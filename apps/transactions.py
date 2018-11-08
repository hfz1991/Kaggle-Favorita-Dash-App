import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from app import app

transactions = pd.read_table("all/transactions.csv", sep=",")
transactions = transactions.groupby('date').agg({'transactions':'sum'})
transactions = transactions.reset_index()
transactions.columns = ['ds','y']

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
        html.H3('Transactions', style={'margin-top':'20px'}),
        dcc.Graph(
            id='transactions',
            figure={
                'data': [
                    go.Scatter(
                        x = transactions['ds'],
                        y = transactions['y'],
                        mode = 'lines',
                        name = 'lines'
                    )
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Transactions'},
                    hovermode='closest'
                )
            }
        ),
    ], className="container")
])
