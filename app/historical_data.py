# Import necessary libraries
import dash
import numpy as np
# Import specific components and functions from other files
from left_panel import *
from utils import parse_contents, calculate_fft, get_ftaps

from dash import callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
from scipy import signal 
# import pymysql
from navbar import navbar
from additional import offcanvas_left, files_option, offcanvas_left_2
from utils import retrieve_files
import psycopg2

load_figure_template('LUX')

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


db_type = 'postgres'

if db_type == 'postgres':
    connection = psycopg2.connect(
        host = "localhost",
        user = "postgres",
        password = "17200bc10b1_",
        database = "postgres"
    )
else:
    print ("Invalid database type")

cursor = connection.cursor()




#--------------------------------------------------(LAYOUT)------------------------------------------------------------------------

# Define the layout of the app
layout = html.Div(
    [
        dcc.Location(id='url', refresh=True, pathname='/historical_data'),
        html.H4("CONDITION-BASED MONITORING SYSTEM FOR ROTATING EQUIPMENT", style={"text-align": "center","margin": "20px"}),
        navbar,
        dcc.Store(id="memory2"),    # Store component for storing data
        html.Div(className="main",style={"justify-content":"center","align-items":"center","margin":"auto"},children=
            [              
                # content
                html.Div(className="container-fluid",children=[
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"},children=[files_option]),
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"},children=[offcanvas_left_2]),                    
                ])
                # footer
            ]
        )
    ]
)

