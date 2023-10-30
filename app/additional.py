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
import navbar
from utils import retrieve_files
#-------------------------------------------------------(OFFCANVAS LEFT)---------------------------------------------------------------------------

offcanvas_left = html.Div(
    [
        dbc.Button("Upload & Filter",class_name="btn btn-primary btn-sm", id="open-offcanvas-start", n_clicks=0),
        dbc.Offcanvas(
            html.Div(
                    id="left_panel",
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    files_location,                 # Component for file location input
                                    html.Div(id="selected_file"),   # Container for selected file display
                                    file_details,                   # Component for displaying file details
                                ]
                            )
                        ),
                        dbc.Card(dbc.CardBody([right_panel])),
                    ],
                    style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top', 'marginRight': '4px',
                            'marginLeft': '', 'height': '100%'}
                ),
            id="offcanvas-start",
            title="File Upload & Filter",
            is_open=False,
            # allow_duplicate=True
        ),
        dbc.Tooltip(
            ""
            "Upload .csv/.xlsx/.nc files for visualization and analyzation purposes.",
            target="open-offcanvas-start",
            placement="left"
        )
    ]
)


@callback(
    [Output("offcanvas-start", "is_open", allow_duplicate=True)],
    [Input("open-offcanvas-start", "n_clicks")],
    [State("offcanvas-start", "is_open")],
    prevent_initial_call='initial_duplicate'
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return [not is_open]
    return [is_open]



# ------------------------------------------------------------------------------------------
files_option = html.Div([
    dcc.Dropdown(id="file_dropdown", className="btn btn-sm",style={'width':'400px'}, options=[{'label': filename, 'value': filename} for filename in retrieve_files()],
                placeholder='Select a File'),
    # dcc.Dropdown(
    #     id='file-dropdown',
    #     style={'width': '400px'},
    #     options=[
    #         {'label': filename, 'value': filename, 'id': f'dropdown-item-{i}'}
    #         for i, filename in enumerate(retrieve_files())
    #     ],
    #     placeholder='Select a File'
    # )
])

# ------------------------------------------------------------------------------------------
offcanvas_left_2 = html.Div(
    [
        dbc.Button("File Description",class_name="btn btn-primary btn-sm", id="open-offcanvas-start", n_clicks=0),
        dbc.Offcanvas(
            html.Div(
                    id="left_panel",
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # files_location,                 # Component for file location input
                                    # html.Div(id="selected_file"),   # Container for selected file display
                                    html.Div(
                                        children=[
                                            # Create a heading for the file contents section
                                            html.H6("File contents"),                                                   
                                            # Create a div container for metadata with an ID and styling
                                            html.Div(
                                                id="metadata2",
                                                children=[],
                                                style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
                                            ),

                                            # Create a heading for the data variables section
                                            html.H6("Data variables"),
                                            # Create a div container for the variable list with an ID and styling
                                            html.Div(
                                                id="variable_list2",
                                                children=[],
                                                style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
                                            ),

                                            # Create a heading for the variable contents section
                                            html.H6("Variable contents"),
                                            # Create a div container for the variable content with an ID and styling
                                            html.Div(
                                                id="variable_content2",
                                                children=[],
                                                style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
                                            ),
                                        ],
                                        id="File_contents",
                                        style={"marginTop": "2px", "marginBottom": "2px"}
                                    ),                   # Component for displaying file details
                                ]
                            )
                        ),
                        dbc.Card(dbc.CardBody([right_panel])),
                    ],
                    style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top',
                             'height': '100%'}
                ),
            id="offcanvas-start",
            title="File Description",
            is_open=False,
            # allow_duplicate=True
        ),
        # dbc.Tooltip(
        #     ""
        #     "Upload .csv/.xlsx/.nc files for visualization and analyzation purposes.",
        #     target="open-offcanvas-start",
        #     placement="left"
        # )
    ]
)