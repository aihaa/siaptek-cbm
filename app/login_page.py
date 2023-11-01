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
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy import signal
from db_operations import *
import psycopg2

execute_create_query("""
CREATE TABLE IF NOT EXISTS tbl_users (
id SERIAL PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255)
)
""")



email_input = html.Div(
    className="form-group d-flex",
    children=[
        html.Div(
            className='form-floating mb-3',
            children=[
            # html.Label("Username: "),
            dcc.Input(id="username-input", type="text", placeholder="Username"),
    ])]
)

password_input = html.Div(
    className="form-group",
    children=[
        html.Div(
            className="form floating mb-3",
            children=[
                # html.Label("Password: ", className="form-label mt-4"),
                dcc.Input(id="password-input", type="password", placeholder="Password")
            ]
        )
    ]
)

# --------------------------------------------------(LAYOUT)--------------------------------------------------


layout = html.Div(className="main h-100 w-100", children=[
            dcc.Location(id='url', refresh=True, pathname='/login_page'),
            html.Div(className="container h-100", children=[
                html.Div(className="row h-100", children=[
                    html.Div(className="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100", children=[
                        html.Div(className="d-table-cell align-middle", children=[
                            html.Div(className="text-center mt-4", children=[
                                html.H2(className="h2", children=["Login"])
                            ]),
                            dbc.Form(className="card", children=[
                                html.Div(className="card-body", children=[
                                    html.Div(className="m-sm-4 d-flex justify-content-center", children=[
                                        html.Form(children=[
                                            html.Div(className="mb-3", children=[email_input]),
                                            html.Div(className="mb-3", children=[password_input]),
                                            html.Div(className="d-flex justify-content-center", style={'padding':'20px'},
                                                    children=[html.Button("Login", id="login-button", className="text-center mb-3 btn btn-primary" , n_clicks=0)]),
                                            
                                        ])
                                    ])
                                ])
                            ])
                        ])
                    ])
                ])
            ]),
            html.Div(id="login-status")
        ])


@callback(
    [Output('url', 'pathname'),
     Output("login-status","children")],
    [Input("login-button", "n_clicks")],
    [State("username-input","value"),
     State("password-input","value")]
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        query = """
        SELECT * FROM tbl_users
        WHERE username = %s AND password = %s
        """
        execute_read_query(query,(username,password))
        result = cursor.fetchone()

        if result:
            return ('/dashboard',print("success login"))
        else:
            return ('/login_page',print("fail login"))
        
    raise dash.exceptions.PreventUpdate