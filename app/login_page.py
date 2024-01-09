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

# execute_create_query("""
# CREATE TABLE IF NOT EXISTS tbl_users (
# id SERIAL PRIMARY KEY,
# username VARCHAR(255) NOT NULL,
# password VARCHAR(255)
# )
# """)



email_input = html.Div(
    className="form-group d-flex",
    children=[
        dcc.Input(id="username-input", type="text", placeholder="Username"),
    ]
)

password_input = html.Div(
    className="form-group",
    children=[
        dcc.Input(id="password-input", type="password", placeholder="Password")
    ]
)

# --------------------------------------------------(LAYOUT)--------------------------------------------------


layout = html.Div(
    className="main h-100 w-100", children=[
            dcc.Location(id='url-login', refresh=False, pathname="/login"),
                html.Div(className="row h-100", children=[
                    html.Div(className="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100", children=[
                        html.Div(className="d-table-cell align-middle", children=[
                            html.Div(className="text-center mt-4", children=[
                                html.H2(className="h2", children=["Login"])
                            ]),
                            dbc.Form(className="card", children=[
                                html.Div(className="card-body", children=[
                                    html.Div(className="m-sm-4 d-flex justify-content-center", children=[
                                        dbc.Form(children=[
                                            html.Div(className="mb-3", children=[email_input]),
                                            html.Div(className="mb-3", children=[password_input]),
                                            html.Div(className="d-flex justify-content-center", style={'padding':'20px'},
                                                    children=[html.Button("Login", id="login-button", className="text-center mb-3 btn btn-primary", n_clicks=0)]),
                                            html.Div(className="d-flex justift-content-center", 
                                                     children=[dcc.Link('Register here', href='/register')]
                                                     ),
                                            html.Div(id="login-status", className="d-flex justify-content-center")
                                        ])
                                    ])
                                ])
                            ])
                        ]),
                    ])
                ])
            ,
            
        ]
    )


@callback(
    [Output('url-login', 'pathname'),
     Output("login-status", "children")],
    [Input("login-button", "n_clicks")],
    [State("username-input", "value"),
     State("password-input", "value")]
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        print(f"n_clicks value: {n_clicks}")
        try:
            # Input validation
            if not username or not password:
                print("Username or password is invalid")
                return ('/login', 'Please fill all fields')

            try:
                # Database query
                query = "SELECT * FROM tbl_users WHERE username = %s AND password = %s"
                result = execute_read_query(query, (username, password))
                if not result:
                    print("Wrong password")
                    return ('/login', 'Invalid username or password')
                # else:
                
                print("Success login")
                return ('/dashboard', 'Logged in')

            except psycopg2.DatabaseError as e:
                print(f"Database error: {e}")
                return ('/login', 'Database error occurred, please try again later')
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ('/login', 'An unexpected error occurred, please try again')
    
    raise dash.exceptions.PreventUpdate
