import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from app import app

stores = pd.read_table("all/stores.csv", sep=",")
transactions = pd.read_table("all/transactions.csv", sep=",")
df_grouped_sales = pd.read_table("all/new/df_grouped_sales.csv", sep=",")
store_sales_by_family = pd.read_table("all/new/store_sales_by_family.csv", sep=",")
list_of_store = stores.store_nbr.unique()

transactions_graph = transactions[transactions['store_nbr'] == 1]
sales_graph = df_grouped_sales[df_grouped_sales['store_nbr'] == 1]
store_sales_by_family_graph = store_sales_by_family[store_sales_by_family['store_nbr'] == 1]

layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Store checker'),
            dcc.Link('Sales performance', href='/apps/train', style={'margin-right': '35px'}),
            dcc.Link('Stores', href='/apps/stores', style={'margin-right': '35px'}),
            dcc.Link('Transactions', href='/apps/transactions', style={'margin-right': '35px'}),
            dcc.Link('Oil', href='/apps/oil', style={'margin-right': '35px'}),
            dcc.Link('Prediction', href='/apps/predict', style={'margin-right': '35px'}),
        ],className="container" , style={'color':'#fff',}),
    ], style={'background-color':'#2a3f5f', 'padding': '20px 0px'}),
    html.Div([
        
        html.Div([
        ],className="row",
        style={'margin-top': '20'}),

        html.H4('Select Store Number:'),
        html.Div([
            
            html.Div(
                dcc.Dropdown(
                    id='store_select',
                    options=[{'label': i, 'value': i} for i in list_of_store],
                    value='Pichincha'
                ),
            className="col-md-6"),
        ],className="row",
        style={'margin-top': '20'}),

        html.Div([
            html.Div(
                html.Div(id='store_info_div'),
            className="col-md-12"),
        ], style={'margin-top': '20'}),

        html.Div([
            
            html.Div(
                dcc.Graph(
                    id='store-transactions',
                    figure={
                        'data': [
                            go.Bar(
                                x=transactions_graph['date'],
                                y=transactions_graph['transactions']
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': ''},
                            yaxis={'title': ''},
                            hovermode='closest',
                            font=dict(color='#CCCCCC'),
                            titlefont=dict(color='#CCCCCC', size=13),
                            plot_bgcolor="#191A1A",
                            paper_bgcolor="#020202",
                            title = "Transactions by store"
                        )
                    }
                ),
            className="col-md-12"),
        ],className="row",
        style={'margin-top': '20'}),

        html.Div([
            
            html.Div(
                dcc.Graph(
                    id='store-sales',
                    figure={
                        'data': [
                            go.Bar(
                                x=sales_graph['date'],
                                y=sales_graph['unit_sales'],
                                marker = dict(
                                    color = 'yellow'
                                ),
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': ''},
                            yaxis={'title': ''},
                            hovermode='closest',
                            font=dict(color='#CCCCCC'),
                            titlefont=dict(color='#CCCCCC', size=13),
                            plot_bgcolor="#191A1A",
                            paper_bgcolor="#020202",
                            title = "Sales by store"
                        )
                    }
                ),
            className="col-md-12"),
        ],className="row",
        style={'margin-top': '20'}),

        html.Div([
            
            html.Div(
                dcc.Graph(
                    id='store_sales_family',
                    figure={
                        'data': [
                            go.Bar(
                                x=store_sales_by_family_graph['family'],
                                y=store_sales_by_family_graph['unit_sales'],
                                marker=dict(
                                    color='rgb(158,202,225)',
                                    line=dict(
                                        color='rgb(8,48,107)',
                                        width=1.5,
                                    )
                                ),
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': ''},
                            yaxis={'title': 'Unit Sales'},
                            hovermode='closest',
                            font=dict(color='#CCCCCC'),
                            titlefont=dict(color='#CCCCCC', size=13),
                            plot_bgcolor="#191A1A",
                            paper_bgcolor="#020202",
                            title = "Item family sales by store",
                        )
                    }
                ),
            className="col-md-12"),
        ],className="row",
        style={'margin-top': '20','margin-bottom': '40'}),
    
    ], className="container")
])

@app.callback(
    dash.dependencies.Output('store-transactions', 'figure'),
    [dash.dependencies.Input('store_select', 'value')])
def update_state_figure(selected_store):
    transactions_graph = transactions[transactions['store_nbr'] == selected_store]

    return {
        'data': [
            go.Bar(
                x=transactions_graph['date'],
                y=transactions_graph['transactions']
            )
        ],
        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': ''},
            hovermode='closest',
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size=13),
            plot_bgcolor="#191A1A",
            paper_bgcolor="#020202",
            title = "Transactions by store"
        )
    }

@app.callback(
    dash.dependencies.Output('store-sales', 'figure'),
    [dash.dependencies.Input('store_select', 'value')])
def update_sales_figure(selected_store):
    sales_graph = df_grouped_sales[df_grouped_sales['store_nbr'] == selected_store]

    return {
        'data': [
            go.Bar(
                x=sales_graph['date'],
                y=sales_graph['unit_sales'],
                marker = dict(
                    color = 'yellow'
                ),
            )
        ],
        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': ''},
            hovermode='closest',
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size=13),
            plot_bgcolor="#191A1A",
            paper_bgcolor="#020202",
            title = "Sales by store"
        )
    }

@app.callback(
    Output(component_id='store_info_div', component_property='children'),
    [Input(component_id='store_select', component_property='value')]
)
def update_output_div(input_value):
    store_info = stores[stores['store_nbr'] == input_value]
    
    return html.Div([
            html.H4('State: {}'.format(store_info.state.values[0])),
            html.H4('City: {}'.format(store_info.city.values[0])),
            html.H4('Type: {}'.format(store_info.type.values[0])),
            html.H4('Cluster: {}'.format(store_info.cluster.values[0])),
        ])