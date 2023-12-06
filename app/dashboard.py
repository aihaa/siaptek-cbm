# Import necessary libraries
import dash
import numpy as np
# Import specific components and functions from other files
from left_panel import *
from utils import parse_contents, calculate_fft, get_ftaps

from dash import callback
from dash.dependencies import Input, Output, State
from dash import html, dcc
from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.graph_objects as go
# import plotly.io as pio
# import matplotlib.pyplot as plt
from scipy import signal 
# import pymysql
import psycopg2
from navbar import navbar
# from additional import offcanvas_left
from db_operations import *
import json

load_figure_template('LUX')

# Create a Dash app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
container_style = {'width': '50%', 'height': '50%', 'display': 'inline-block'}

#--------------------------------------------------(LAYOUT)------------------------------------------------------------------------

def mem_data(filename):
    try:
        data = execute_read_query("SELECT data FROM memory1 WHERE filename = %s", (filename, ))
        if isinstance(data, list):
            mem_data = {}
            for item in data:
                data = {f'object{i}': item for i, item in enumerate(data, start=1)} # <dict>
                mem_data = data['object1'][0]
                print("mem_data.keys():")
                print(mem_data.keys()) # dict_keys(['dims', 'attrs', 'coords', 'data_vars'])
            return {"filename": filename, "data": mem_data}  
        else:
            return {"filename": None, "data": None}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"filename": None, "data": None}

filename = 'y2016-m09-d20-03-31-36.nc'
memory1 = mem_data(filename)['data']['data_vars']['vib']["data"]
memory2 = mem_data(filename)['data']['data_vars']['tach']["data"]

# Now ensure that both vib_data and tach_data have exactly 1000 data points
desired_length = 1000

memory1 = memory1[:desired_length] if len(memory1) >= desired_length else memory1 + [None] * (desired_length - len(memory1))
memory2 = memory2[:desired_length] if len(memory2) >= desired_length else memory2 + [None] * (desired_length - len(memory2))


layout = html.Div(
    [
        dcc.Location(id='url', refresh=True, pathname='/dashboard'),
        html.H4("CONDITION-BASED MONITORING SYSTEM FOR ROTATING EQUIPMENT", style={"text-align": "center","margin": "20px"}),
        navbar,
        dcc.Interval(id="interval_component", interval=1*1000, n_intervals=0, max_intervals=50000),
        dcc.Store(id="memory1", data=memory1),
        dcc.Store(id="memory2", data=memory2),
        dcc.Store(id="fs", data=5000),
        dcc.Store(id="nfft", data=2048),
        dcc.Store(id="stored_data1"),
        dcc.Store(id="stored_data2"),
        html.Div(id="index_holder", style={"display": "none"}, children=0),
        html.Div(className="main",style={"justify-content":"center","align-items":"center","margin":"auto"},children=
            [               
            # content
            html.Div(className="parent-container",children=[
                html.Div(id="metadata"),
                html.Div(
                    style={'display': 'flex', 'flexWrap': 'wrap', 'height': '100vh'},
                    children=[
                        # Container 1 (Top-left)
                        html.Div(
                            style=container_style,  # Each div will take half of the page width and height
                            children=[
                                html.Div(className="card graph-container", children=[
                                        html.Div(className="card-body", children=[
                                            html.Div(className="row", children=[html.H5(className="card-title",children=["Time Domain"])]),
                                            html.Div(id="alert_1"),
                                            html.Div(className="row", children=[dcc.Graph(id="graph_1",style={'height':'250px'})])
                                        ])
                                    ]),
                            ]
                        ),
                        # Container 2 (Top-right)
                        html.Div(
                            style=container_style,
                            children=[
                                html.Div(className="card graph-container", children=[
                                        html.Div(className="card-body", children=[
                                            html.Div(className="row", children=[html.H5(className="card-title",children=["Time Domain"])]),
                                            html.Div(className="row", children=[dcc.Graph(id="graph_3",style={'height':'250px'})])
                                        ])
                                    ])
                            ]
                        ),
                        # Container 3 (Bottom-left)
                        html.Div(
                            style=container_style,
                            children=[
                                html.Div(className="card graph-container", children=[
                                        html.Div(className="card-body", children=[
                                            html.Div(className="row", children=[html.H5(className="card-title",children=["Frequency Plot"])]),
                                            html.Div(className="row", children=[dcc.Graph(id="graph_2",style={'height':'250px'})])
                                        ])
                                    ])
                            ]
                        ),
                        # Container 4 (Bottom-right)
                        html.Div(
                            style=container_style,
                            children=[
                                html.Div(className="card graph-container", children=[
                                        html.Div(className="card-body", children=[
                                            html.Div(className="row", children=[html.H5(className="card-title",children=["Frequency Plot"])]),
                                            html.Div(className="row", children=[dcc.Graph(id="graph_4",style={'height':'250px'})])
                                        ])
                                    ])
                            ]
                        ),
                    ]
                ),                
            ])
            ]
        )
    ]
)

# Purpose: To ensure that metadata is always synchronized with data stored in memoery1 
#               -- allows user to see summary of metadata associated with the variables they analyze
# @callback(
#     Output("metadata", "children"),
#     [Input("memory1", "data")],
# )
# def update_metadata(mem_data):

#     meta_head = pd.Series(mem_data['data']).head(5)
#     print(meta_head)

#     return str(meta_head)


@callback(
    Output("stored_data1","data"),
    Output("stored_data2","data"),
    Output("index_holder", "children"),
    Input("interval_component", "n_intervals"),
    State("memory1", "data"),
    State("memory2", "data"),
    State("index_holder", "children"),
    State("stored_data1", "data"),
    State("stored_data2","data"),
)
def update_data(n, memory1, memory2, current_index, stored_data1, stored_data2):
    if not stored_data1:
        stored_data1 = []
    if not stored_data2:
        stored_data2 = []

    if memory1 and memory2:
        current_index = int(current_index)
        min_length = min(len(memory1), len(memory2))
        if current_index < min_length:
            stored_data1.append(memory1[current_index])
            stored_data2.append(memory2[current_index])
            current_index += 1
        else:
            current_index = 0

    return stored_data1, stored_data2, current_index


'''
Allow users to:
1. select variable (vib/tach)
2. adjust filter settings
3. visualize raw measurement (graph_1) & filtered data
'''

@callback(
    Output("graph_1", "figure"),
    Output("graph_3", "figure"),
    [Input("stored_data1", "data"),
    Input("stored_data2", "data"),
    State("fs", "data"),]
)
def update_td_plot(stored_data1, stored_data2, fs):
    if stored_data1 is None and stored_data2 is None:
        raise dash.exceptions.PreventUpdate
    else:
        fs = int(fs)

        df1 = pd.DataFrame(
            data = stored_data1,
            index=np.linspace(0, len(stored_data1) / fs, len(stored_data1)),
            columns=['vib']
        )
        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(
                name="Vibration Measurement",
                x=df1.index,
                y=df1['vib'],
                mode="lines",
                line=dict(color="blue")
            )
        )
        fig1.update_layout(title="Vibration Data", xaxis_title="Time (s)", yaxis_title="Vibration (m/s²)")

        df2 = pd.DataFrame(
            data=stored_data2,
            index=np.linspace(0, len(stored_data2) / fs, len(stored_data2)),
            columns=['tach']
        )
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                name="Tachometer Measurement",
                x=df2.index,
                y=df2['tach'],
                mode="lines",
                line=dict(color="blue")
            )
        )
        fig2.update_layout(title="Tachometer Data", xaxis_title="Time (s)", yaxis_title="Tachometer (BRM)")

        return fig1, fig2


THRESHOLD=0.0015
@callback(
    Output('alert_1', 'children'),
    Output('alert_1', 'style'),
    [Input('stored_data1', 'data')]
)
def alerts_1(dataPoint):
    if dataPoint[-1]>THRESHOLD:
        return "ALERT!!", {"background-color":"red", "color":"white"}
    else:
        return "Normal", {"background-color":"green", "color":"white"}


# Purpose: Allow users to select a variable, adjust the sampling frequency and FFT size,
#                       and visualize the time-domain plot and spectrogram plot for selected variable
@callback(
    Output('graph_2', 'figure'),
    Output('graph_4', 'figure'),
    [Input('graph_1', 'relayoutData'),
     Input('graph_3', 'relayoutData'),
    Input("stored_data1", "data"),
    Input("stored_data2", "data"),
     State("fs", "data"),
     State("nfft", "data"),
     ])
def update_fd_plot(relayoutData1, relayoutData2, stored_data1, stored_data2, fs, nfft):
    if stored_data1 is None and stored_data2 is None:
        raise dash.exceptions.PreventUpdate

    else:
        fs = int(fs)
        nfft = int(nfft)

        def create_fft_figure(data, fs, nfft, relayoutData):
            if relayoutData and 'xaxis.range[0]' in relayoutData:
                start = int(float(relayoutData["xaxis.range[0]"]) * fs)
                end = int(float(relayoutData["xaxis.range[1]"]) * fs)
            else:
                start = 0
                end = len(data)

            fft_df = calculate_fft(np.array(data[start:end]), nfft, fs)
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    name='Frequency Spectrum',
                    x=fft_df["Frequency"],
                    y=fft_df["Amplitude"],
                    mode="lines",
                    line=dict(color="blue")
                )
            )
            fig.update_layout(title="Frequency Domain Data", xaxis_title="Frequency (Hz)", yaxis_title="Amplitude")
            return fig

        fig1 = create_fft_figure(stored_data1, fs, nfft, relayoutData1)
        fig2 = create_fft_figure(stored_data2, fs, nfft, relayoutData2)

        return fig1, fig2