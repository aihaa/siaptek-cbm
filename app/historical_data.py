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
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
from scipy import signal 
# import pymysql
from navbar import navbar
from additional import offcanvas_left, file_option, offcanvas_left_2
from utils import retrieve_files
import psycopg2
from db_operations import *

load_figure_template('LUX')

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

#--------------------------------------------------(LAYOUT)------------------------------------------------------------------------

# Define the layout of the app
layout = html.Div(
    [
        dcc.Location(id='url', refresh=True, pathname='/historical_data'),
        html.H4("CONDITION-BASED MONITORING SYSTEM FOR ROTATING EQUIPMENT", style={"text-align": "center","margin": "20px"}),
        navbar,
        dcc.Store(id="memory2"),    # Store component for storing data
        dcc.Store(id="memory3"),
        html.Div(className="main",style={"justify-content":"center","align-items":"center","margin":"auto"},children=
            [              
                # content
                html.Div(className="container-fluid",children=[
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"}, children=[file_option]),
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"},children=[offcanvas_left_2]),                    
                     # col 1
                        html.Div(className="col-xl-6 d-flex", style={}, children=[
                            html.Div(className="w-100", children=[
                                # graph 1
                                html.Div(className="row",style={'padding-bottom':'20px'}, children=[
                                    html.Div(className="", children=[
                                        html.Div(className="card", children=[
                                            html.Div(className="card-body", children=[
                                                html.Div(className="row", children=[html.H5(className="card-title",children=["Time Domain"])]),
                                                html.Div(className="row", children=[dcc.Graph(id="graph_1",style={'height':'250px'})])
                                            ])
                                        ]),
                                        html.Div(className="card")
                                    ]),
                                ]),
                                # graph 2
                                html.Div(className="row", children=[
                                    html.Div(className="", children=[
                                        html.Div(className="card", children=[
                                            html.Div(className="card-body", children=[
                                                html.Div(className="row", children=[html.H5(className="card-title",children=["Frequency Plot"])]),
                                                html.Div(className="row", children=[dcc.Graph(id="graph_2",style={'height':'250px'})])
                                            ])
                                        ])
                                    ])
                                ]),
                            ])
                        ]),
                        # col 2
                        html.Div(className="col-xl-6", children=[
                            html.Div(className="card", children=[
                                html.Div(className="card-body", children=[
                                    html.Div(className="row", children=[html.H5(className="card-title", children=["Spectrogram"])]),
                                    html.Div(className="row", children=[dcc.Graph(id="graph_spec",style={'height':'575px'})])
                                ])
                            ])
                        ])
                    ]),
                
                # footer
            ]
        )
    ]
)


# '''
# 1. when choose 'file_options' --> file name will be setup
# 2. when filename has been set (act as input), --> data visualzation will be triggered (will be automatically shown)
# '''

# predefined_list = ['Variable A', 'Variable B']

@callback(
    Output("memory2", "data"), ## IMPORTANT! store files_dropdown value into memory2 dcc.store --> to be used globally.. cannot ask system to print it!!
    Input("file_dropdown", "value"),
)
def update_memory_hd(filename):

    data = execute_read_query("SELECT data FROM memory2 WHERE filename = %s", (filename, ))
    # print(data)
    # print(filename)
    return {"filename": filename, "data": data}   # print --> {'filename': 'y2016-m09-d20-04-06-52.nc'}



# ### HOW TO USE OR HOW TO USE FILENAME
# @callback(
#     Output("memory3", "data"),
#     Input("memory2", "data")
# )
# def hiii(data):
#     filename = data["filename"]
#     print(filename)
#     return {"filename": filename}

# @callback(
#     Output("variable_list", "children"),
#     [Input("memory2", "data")]
# )
# def update_variable_ilst(mem_data):

#     if mem_data is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         var_list = list(mem_data['data']['data_vars'].keys())
#         var_buttons = create_list_radio(var_list, "var_list_radio")

#     return var_buttons

# @callback(
#     Output("metadata", "children"),
#     [Input("memory2", "data")],
# )
# def update_metadata(mem_data):
#     meta_head = pd.Series(mem_data['data']).head(5)
#     print(meta_data)

#     return str(meta_data)

# @callback(
#     Output("variable_content", "children"),
#     [Input("var_list_radio", "value"),
#     Input("memory2", "data")]
# )
# def update_variable_content(radio_value, mem_data):
#     if mem_data is None and radio_value is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

#     return str(head_dict)





