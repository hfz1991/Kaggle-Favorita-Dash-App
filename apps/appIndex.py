from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from app import app

layout = html.Div([
    html.H3('App Index'),
    dcc.Link('Train', href='/apps/train'),
    html.Div(''),
    dcc.Link('Stores', href='/apps/stores'),
    html.Div(''),
    dcc.Link('Items', href='/apps/items'),
    html.Div(''),
    dcc.Link('Transactions', href='/apps/transactions'),
    html.Div(''),
    dcc.Link('Oil', href='/apps/oil'),
], className="container")
