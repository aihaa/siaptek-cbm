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

username_reg_input = html.Div(
    className="form-group d-flex",
    children=[
        dcc.Input(id="reg-username-input", type="text", placeholder="Username"),
    ]
)

password_reg_input = html.Div(
    className="form-group",
    children=[
        dcc.Input(id="reg-password-input", type="password", placeholder="Password"),
    ]
)

confirm_password_input = html.Div(
    className="form-group",
    children=[
        html.Div(
            className="form floating mb-3",
            children=[
                dcc.Input(id="confirm-password-input", type="password", placeholder="Confirm Password")
            ]
        )   
    ]
)

layout = html.Div(
    className="main h-100 w-100", children=[
        dcc.Location(id='url-reg', refresh=True, pathname="/register"),
        html.Div(className="row h-100", children=[
            html.Div(className="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100", children=[
                html.Div(className="d-table-cell align-middle", children=[
                    html.Div(className="text-center mt-4", children=[
                        html.H2(className="h2", children=["Register"])
                    ]),
                    dbc.Form(className="card", children=[
                        html.Div(className="card-body", children=[
                            html.Div(className="m-sm-4 d-flex justify-content-center", children=[
                                html.Form(children=[
                                    html.Div(className="mb-3", children=[username_reg_input]),
                                    html.Div(className="mb-3", children=[password_reg_input]),
                                    html.Div(className="mb-3", children=[confirm_password_input]),
                                    html.Div(className="d-flex justify-content-center", style={'padding':'20px'},
                                            children=[html.Button("Register", id="register-button", className="text-center mb-3 btn btn-primary", n_clicks=0)]),
                                ])
                            ])
                        ])
                    ])
                ]),
                
            ])
        ]),
        html.Div(id="registration-status")
    ]
)

@callback(
    [Output('url-reg', 'pathname'),
     Output("registration-status", "children")],
     [Input("register-button", "n_clicks")],
     [State("reg-username-input", "value"),
      State("reg-password-input", "value"),
      State("confirm-password-input", "value")]
)
def register(n_clicks, username, password, confirm_password):
    if n_clicks > 0:
        if password != confirm_password:
            return ('/register', 'Passwords do not match')
        
        # Check if username is already exists
        user_check_query = "SELECT * FROM tbl_users WHERE username = %s"
        result = execute_read_query(user_check_query, (username,))
        if result:
            return ('/register', 'Username already exists')
        
        # Insert new user
        insert_query = "INSERT INTO tbl_users (username, password) VALUES (%s,%s)"
        execute_create_query(insert_query, (username, password))
        return ('/login', 'Registration successful, please login')
    
    raise dash.exceptions.PreventUpdate