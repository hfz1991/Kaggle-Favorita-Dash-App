from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import train, stores, predict, oil, transactions, appIndex


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/train':
         return train.layout
    elif pathname == '/apps/stores':
         return stores.layout
    elif pathname == '/apps/predict':
         return predict.layout
    elif pathname == '/apps/oil':
         return oil.layout
    elif pathname == '/apps/transactions':
         return transactions.layout
    else:
        return appIndex.layout

if __name__ == '__main__':
    app.run_server(debug=True)
