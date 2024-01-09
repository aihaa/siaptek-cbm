# Import necessary libraries
import dash
# import numpy as np
# Import specific components and functions from other files
# from left_panel import *
# from utils import parse_contents, calculate_fft, get_ftaps

from dash import callback, html, dcc
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt
# from scipy import signal
from db_operations import *
import psycopg2

import login_page
import registration_page
import dashboard
import historical_data

# Define external stylesheets for the app
external_stylesheets = [dbc.themes.LUX]

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='page-content')
])

@app.callback(
        Output('page-content','children'),
        Input('url','pathname'))
def display_page(pathname):
    if pathname == '/register':
        return registration_page.layout
    elif pathname == '/login':
        return login_page.layout
    
    elif pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/collection':
        return historical_data.layout
    else:
        return '404'
    
if __name__ == '__main__':
    app.run_server(host ='127.0.0.1', port = 33000, debug=False)



