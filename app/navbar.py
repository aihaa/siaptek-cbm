
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
import pymysql


# def navbar():
    #--------------------------------------------------()------------------------------------------------------------------------
    # @callback(
    #     dash.dependencies.Output('output-div','children'),
    #     [dash.dependencies.Input('nonexistent-input','value')]
    # )
    # def update_output(value):
    #     try:
    #         return f"Input Value: {value}"
    #     except Exception as e:
    #         error_message = "An error occured: " + str(e)
    #         return error_message

    #--------------------------------------------------(NAVBAR)------------------------------------------------------------------------


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

nav = dbc.Nav(className="",children=
    [
        dbc.NavItem(dbc.NavLink("Dashboard", className="", href="/dashboard")),
        dbc.NavItem(dbc.NavLink("Collection", href="/historical_data")),
        # dbc.NavItem(dbc.NavLink("Another link", href="#")),
        # dbc.NavItem(dbc.NavLink("Disabled", disabled=True, href="#")),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Alerts & Notification", href="#"), dbc.DropdownMenuItem("Sign Out",href="/login_page")],
            label="Settings",
            nav=True,
        ),
    ]
)

navbar = dbc.Navbar( className="" ,children=
    dbc.Container( className="", children=
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src="#", height="30px")),
                        dbc.Col(dbc.NavbarBrand("SIAPTEK", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/dashboard",
                style={"textDecoration": "none"},
            ),
            nav,
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)



# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open", allow_duplicate=True),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
    prevent_initial_call=True
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
    

    # return navbar

