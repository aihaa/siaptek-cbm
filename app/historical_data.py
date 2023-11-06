# Import necessary libraries
import dash
import numpy as np
# Import specific components and functions from other files
# from left_panel import *
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
from navbar import navbar
from additional import file_option
import psycopg2
from db_operations import *
import json
from left_panel import right_panel

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
        dcc.Store(id="filter_mem_2"), # Store component for storing filter data
        dcc.Store(id="filt_x_mem_2"), # Store component for storing filtered data        html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"}, children=[file_option]),
        html.Div(className="main",style={"justify-content":"center","align-items":"center","margin":"auto"},children=
            [               
            # content
            html.Div(className="container-fluid",children=[
                html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"}, children=[file_option]),
                html.Div(className="header d-md-flex justify-content-md-center",style={ "transform": "scale(0.8)"},children=[right_panel]),
                # row 1
                html.Div(className="row",style={},children=[
                    # col 1
                    html.Div(className="col-xl-6 d-flex", style={}, children=[
                        html.Div(className="w-100", children=[
                            # graph 1
                            html.Div(className="row",style={'padding-bottom':'10px'}, children=[
                                html.Div(className="", children=[
                                    html.Div(className="card", children=[
                                        html.Div(className="card-body", children=[
                                            html.Div(className="row", children=[html.H5(className="card-title",children=["Time Domain"])]),
                                            html.Div(className="row", children=[dcc.Graph(id="graph2_1",style={'height':'250px'})])
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
                                            html.Div(className="row", children=[dcc.Graph(id="graph2_2",style={'max-height':'250px'})])
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
                                html.Div(className="row", children=[dcc.Graph(id="graph_spec2",style={'height':'600px'})])
                            ])
                        ])
                    ])
                ]),
                
            ])
            # footer
            ]
        )
    ]
)


@callback(
    Output("memory2", "data"), ## IMPORTANT! store files_dropdown value into memory2 dcc.store --> to be used globally.. cannot ask system to print it!!
    Input("file_dropdown", "value"),
)
def update_memory_hd(filename):
    data = execute_read_query("SELECT data FROM memory1 WHERE filename = %s", (filename, ))

    if isinstance(data, list):

        mem_data = {}
        for item in data:
            data = {f'object{i}': item for i, item in enumerate(data, start=1)} # <dict>

            mem_data = data['object1'][0]

            print(mem_data.keys()) # dict_keys(['dims', 'attrs', 'coords', 'data_vars'])


        return {"filename": filename, "data": mem_data}  

    else:
        return {"filename": None, "data": None}


@callback(
    Output("metadata2", "children"),
    [Input("memory2", "data")],
)
def update_metadata2(mem_data):
    print("mem_data['data']:")
    print(type(mem_data['data']))
    meta_head = pd.Series(mem_data['data']) # if without data, <list> ; with data <dict>
    print(meta_head)

    return str(meta_head)

# @callback(
#     Output("variable_content2", "children"),
#     [Input("var_list_radio", "value"),
#     Input("memory2", "data")]
# )
# def update_variable_content2(radio_value, mem_data):

#     print("mem_Data['data'] :")
#     print(type(mem_data['data']))
#     print("mem_Data['data'][vib]['data_vars] :")
#     print(type(mem_data['data']["vib"]['data_vars']))
#     if mem_data is None and radio_value is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         # if isinstance(mem_data['data'], dict) and 'data_vars' in mem_data['data']:
#         #     head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()
#         # else:
#         #     raise TypeError("mem_data['data'] is not a dictionary or does not contain the key 'data_vars'")

#         head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

#     return str(head_dict)



# Purpose: To select file type and adjust the cutoff frequency and visualize them corresponding to the filter taps and frequency response
@callback(
        Output("filter_mem_2", "data"),
        [Input("filter_type", "value"),
        Input("nfft", "value"),
        Input("fs", "value"),
        Input("fc_1", "value"),
        Input("fc_2", "value")])
def plot_filter(filter_type_2, n_fft, fs, fc_1, fc_2):
    fs = float(fs)
    fc_1 = int(fc_1)
    fc_2 = int(fc_2)
    n_fft = int(n_fft)

    # Get the filter taps based on the selected filter type, n_fft, and cutoff frequencies
    y = get_ftaps(filter_type_2, n_fft + 1, fc_1, fc_2, fs)
    print(y)

    # Store the filter taps in filter_mem_2_data
    filter_mem_2_data = {
        "taps": y
    }
    return filter_mem_2_data



@callback(
    Output("graph2_1", "figure"),
    Output("filt_x_mem_2", "data"),
    [Input("memory2", "data"),
    Input("fs", "value"),
    Input("filter_apply", "value"),
    Input("filter_mem_2", "data")]
)
def update_td_plot(mem_data, fs, fil_val, fil_taps):
    if mem_data is None or fil_val is None or fil_taps is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate
    else:

        fs = int(fs)

        print(mem_data['data']['data_vars']['vib'].keys())
        print(mem_data['data']['attrs'])
        print(mem_data['data']['data_vars']['vib'].keys())
        print(mem_data['data']['data_vars']['vib']['dims']) # ['vibDim']
        print(mem_data['data']['data_vars']['vib']['attrs']) # {'Fs': 51200, 'unit': 'm/s2', 'unitscale': 98.10000000000001}
        print(mem_data['data']['data_vars']['vib']['attrs']['unit'])

        # extract data narrowed to var_list_radio option
        var_data = mem_data['data']['data_vars']['vib']["data"]
        df = pd.DataFrame(
            data=var_data,
            index=np.linspace(0, 
                            len(var_data)/fs, 
                            len(var_data)),
            columns=["vib"]
        )

        # Create a Figure object to plot the raw measurement
        fig = go.Figure(
            layout={
                "xaxis": {"title": "Time (s)"},  # Assuming time is in seconds
                "yaxis": {"title": "Vibration (m/s)"}  # Include the unit in the y-axis title
            }
            
        )
        fig.add_trace(
            go.Scatter(
            name="Raw Measurement",
            x=df.index,
            y=df["vib"],
            mode="lines",
            line=dict(
                color="blue"
            )
            )
        )
        fig.update_layout
        print(fil_val,fil_taps)



        # check if a filter is applied
        if type(fil_val) is list and len(fil_val) > 0:

            filtered = signal.lfilter(
                fil_taps["taps"],
                1.0,
                df["vib"]
            )
            delay = 0.5*(len(fil_taps["taps"]) - 1) / fs
            print(f"delay--{delay}")


            indices = df.index[:-int((len(fil_taps["taps"]) - 1) / 2)]
            # create filtered df with appropriate indexing and column name
            df_filt = pd.DataFrame(
                data= filtered[int( (len(fil_taps["taps"]) - 1) /2 ):],
                index= df.index[: -int( (len(fil_taps["taps"]) - 1) /2)],
                columns=["filtered"]
            )
            print(df_filt.head(10))


            # update the figure after filter is applied
            fig.add_trace(
                go.Scatter(
                name='Filtered',
                x=df_filt.index,
                y=df_filt["filtered"],
                mode="lines",
                line=dict(
                    color="red"
                )
                )
            )

            filt_x = {
                "filtered": filtered[int((len(fil_taps["taps"]) - 1) / 2):], 
                "index": indices
            }
        else:
            # no filter is applied
                        filt_x = {
                            "filtered":None,
                            "index":None
                        }
        # update the figure after filter is disabled
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            ),
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="left",
                x=0
            )
        )

            

        return fig, filt_x




# Purpose: Allow users to select a variable, adjust the sampling frequency and FFT size,
#                       and visualize the time-domain plot and spectrogram plot for selected variable
@callback(
    Output('graph2_2', 'figure'),
    Output("graph_spec2", "figure"),
    [Input("memory2", "data"),
     Input("fs", "value"),
     Input("nfft", "value"),
     Input('graph2_1', 'relayoutData'),
     Input("filt_x_mem_2", "data")
     ])
def update_fd_plot(mem_data, fs, nfft, relayoutData, filt_x):
    if mem_data is None:

        raise dash.exceptions.PreventUpdate

    else:
        fs = int(fs)
        nfft = int(nfft)
        var_data = mem_data['data']['data_vars']['vib']["data"]
        # df = pd.DataFrame(
        #     data=var_data,
        #     index=np.linspace(0, len(var_data) / fs, len(var_data)),
        #     columns=['vib']
        # )

        # Check if a range selection has been made on the x-axis of graph_1
        if 'xaxis.range[0]' in relayoutData:
            start = int(relayoutData["xaxis.range[0]"] * fs)
            end = int(relayoutData["xaxis.range[1]"] * fs)
        else:
            start = 0
            end = fs

        # Calculate the FFT (Fast Fourier Transform) of the selected variable data within the specified range
        fft_df = calculate_fft(np.array(var_data[start:end]), nfft, fs)

        # Create a Figure object to plot the frequency spectrum
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                name='Frequency spectrum',
                x=fft_df["Frequency"],
                y=fft_df["Amplitude"],
                mode="lines",
                line=dict(
                    color="blue"
                )
            )
        )

        # Calculate the spectrogram of the selected variable data within the specified range
        freqs, t, Pxx = signal.spectrogram(np.array(var_data[start:end]),fs=fs,nfft=fs, window=signal.get_window("hamming", fs, fftbins=True))

        # Check if there is filtered data available
        if filt_x["filtered"] is not None:
            # Calculate the FFT of the filtered data within the specified range
            fft_filt = calculate_fft(np.array(filt_x["filtered"][start:end]), nfft, fs)

            # Add the filtered frequency spectrum to the Figure object for plotting
            fig.add_trace(
                go.Scatter(
                    name='Frequency spectrum (Filtered)',
                    x=fft_filt["Frequency"],
                    y=fft_filt["Amplitude"],
                    mode="lines",
                    line=dict(
                        color="red"
                    )
                )
            )

            # Calculate the spectrogram of the filtered data within the specified range
            freqs, t, Pxx = signal.spectrogram(np.array(filt_x["filtered"][start:end]), fs=fs, nfft=fs, window=signal.get_window("hamming", fs, fftbins=True))

        # Customize the layout of the Figure object
        fig.update_layout(xaxis_rangeslider_visible=False,
                        margin=dict(l=10, r=10, t=20, b=20),
                        legend=dict(yanchor="top", y=1, xanchor="left", x=0))

       # Add x-axis and y-axis labels
        fig.update_xaxes(title_text='Frequency (Hz)') 
        fig.update_yaxes(title_text='Amplitude (m/s²)')     

        # Create a heatmap Figure object for the spectrogram
        trace = [go.Heatmap(
            x=t,
            y=freqs,
            z=10 * np.log10(Pxx),
            colorscale='Jet',
        )]
        layout = go.Layout(
            yaxis=dict(title='Frequency'),  # x-axis label
            xaxis=dict(title='Time'),  # y-axis label
        )
        fig2 = go.Figure(data=trace, layout=layout)

        return fig, fig2


