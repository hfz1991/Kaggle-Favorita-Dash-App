import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output

from app import app

df_grouped_state_2017 = pd.read_table("all/new/grouped_state_2017.csv", sep=",")
df_grouped_state_2017 = df_grouped_state_2017.groupby('state').agg({'unit_sales':'sum'}).reset_index()
df_grouped_state_2017 = df_grouped_state_2017.sort_values(by='unit_sales', ascending=False)

df_grouped_city_2017 = pd.read_table("all/new/grouped_city_2017.csv", sep=",")
df_grouped_city_2017 = df_grouped_city_2017.sort_values(by='unit_sales', ascending=False)

df_stores_weekday_2017 = pd.read_table("all/new/stores_weekday_2017.csv", sep=",")
df_stores_weekday_2017 = df_stores_weekday_2017.pivot(index='weekday', columns='store_nbr', values='unit_sales')
df_stores_weekday_2017_norm = (df_stores_weekday_2017 - df_stores_weekday_2017.mean()) / (df_stores_weekday_2017.max() - df_stores_weekday_2017.min())

df_grouped_store_2017 = pd.read_table("all/new/df_grouped_store_2017.csv", sep=",")
graph_data = df_grouped_store_2017[df_grouped_store_2017['state'] == 'Pichincha']
graph_data = graph_data.sort_values(by='unit_sales', ascending=False)
list_of_state = df_grouped_store_2017.reset_index().state.unique()

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
        html.H3('Select year:', style={'margin-top':'20px'}),
        dcc.Slider(
            id='year-slider',
            min=2013,
            max=2017,
            marks={i: str(i) for i in range(2013, 2018)},
            value=2017,
        ),
        html.Div([
            html.Div(
                html.Label(''),
            className="col-md-12", style={'margin-bottom': '20'}),
            html.Div(
                dcc.Graph(
                    id='state-sales',
                    figure={
                        'data': [
                            go.Bar(
                                x=df_grouped_state_2017['state'],
                                y=df_grouped_state_2017['unit_sales']
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
                            title = "Sales by state"
                        )
                    }
                ),
            className="col-md-6"),
            html.Div(
                dcc.Graph(
                    id='city-sales',
                    figure={
                        'data': [
                            go.Bar(
                                x=df_grouped_city_2017['city'],
                                y=df_grouped_city_2017['unit_sales'],
                                marker = dict(
                                    color = 'purple'
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
                            title = "Sales by city"
                        )
                    }
                ),
            className="col-md-6")
        ],className="row"),
        html.Div([
            html.Div(
                dcc.Graph(
                    id='state-density',
                    figure={
                        'data': [
                            go.Heatmap(
                                z=list(df_stores_weekday_2017_norm.values),
                                x=list(df_stores_weekday_2017_norm),
                                y=['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Store number'},
                            yaxis={'title': 'Weekday'},
                            hovermode='closest',
                            font=dict(color='#CCCCCC'),
                            titlefont=dict(color='#CCCCCC', size=13),
                            plot_bgcolor="#191A1A",
                            paper_bgcolor="#020202",
                            title = "Sales intensity by store"
                        )
                    }
                ),
            className="col-md-12"),
        ],className="row",
        style={'margin-top': '20'}),

        html.Div([
            html.Div(
                dcc.Dropdown(
                    id='states-column',
                    options=[{'label': i, 'value': i} for i in list_of_state],
                    value='Pichincha'
                ),
            className="col-md-6"),
        ],className="row",
        style={'margin-top': '20'}),
        html.Div([
            html.Div(
                dcc.Graph(
                    id='store-sales-by-state',
                    figure={
                        'data': [
                            go.Bar(
                                x=graph_data['store_nbr'],
                                y=graph_data['unit_sales']
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
                            title = "Store sales by state"
                        )
                    }
                ),
            className="col-md-6"),
        ],className="row",
        style={'margin-top': '20'}),
    
    ], className="container") 
])



@app.callback(
    dash.dependencies.Output('state-sales', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_state_figure(selected_year):
    filename = "all/new/grouped_state_" + str(selected_year) + ".csv"
    df_grouped_state = pd.read_table(filename, sep=",")
    df_grouped_state = df_grouped_state.groupby('state').agg({'unit_sales':'sum'}).reset_index()
    df_grouped_state = df_grouped_state.sort_values(by='unit_sales', ascending=False)

    return {
        'data': [
            go.Bar(
                x=df_grouped_state['state'],
                y=df_grouped_state['unit_sales']
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
            title = "Sales by state"
        )
    }

@app.callback(
    dash.dependencies.Output('city-sales', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_city_figure(selected_year):
    filename = "all/new/grouped_city_" + str(selected_year) + ".csv"
    df_grouped_city = pd.read_table(filename, sep=",")
    df_grouped_city = df_grouped_city.sort_values(by='unit_sales', ascending=False)

    return {
        'data': [
            go.Bar(
                x=df_grouped_city['city'],
                y=df_grouped_city['unit_sales'],
                marker = dict(
                    color = 'purple'
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
            title = "Sales by city"
        )
    }

@app.callback(
    dash.dependencies.Output('state-density', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filename = "all/new/stores_weekday_" + str(selected_year) + ".csv"
    df_stores_weekday = pd.read_table(filename, sep=",")
    df_stores_weekday = df_stores_weekday.pivot(index='weekday', columns='store_nbr', values='unit_sales')
    df_stores_weekday_norm = (df_stores_weekday - df_stores_weekday.mean()) / (df_stores_weekday.max() - df_stores_weekday.min())

    return {
        'data': [
            go.Heatmap(
                z=list(df_stores_weekday_norm.values),
                x=list(df_stores_weekday_norm),
                y=['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Store number'},
            yaxis={'title': 'Weekday'},
            hovermode='closest',
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size=13),
            plot_bgcolor="#191A1A",
            paper_bgcolor="#020202",
            title = "Sales intensity by store"
        )
    }

@app.callback(
    dash.dependencies.Output('store-sales-by-state', 'figure'),
    [dash.dependencies.Input('states-column', 'value'), dash.dependencies.Input('year-slider', 'value')])
def update_sales_by_state_figure(selected_state, selected_year):
    filename = "all/new/df_grouped_store_" + str(selected_year) + ".csv"
    df_grouped_store = pd.read_table(filename, sep=",")
    graph_data = df_grouped_store[df_grouped_store['state'] == selected_state]
    graph_data = graph_data.sort_values(by='unit_sales', ascending=False)

    return {
        'data': [
            go.Bar(
                x=graph_data['store_nbr'],
                y=graph_data['unit_sales']
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Store number'},
            yaxis={'title': 'Sales'},
            hovermode='closest',
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size=13),
            plot_bgcolor="#191A1A",
            paper_bgcolor="#020202",
            title = "Store sales by state"
        )
    }

