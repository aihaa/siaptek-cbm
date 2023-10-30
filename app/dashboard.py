# Import necessary libraries
import dash
import numpy as np
# Import specific components and functions from other files
from left_panel import *
from utils import parse_contents, calculate_fft, get_ftaps

from dash import callback
from dash.dependencies import Input, Output, State
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
from additional import offcanvas_left

load_figure_template('LUX')

# Define external stylesheets for the app
#external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create a Dash app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


db_type = 'postgres'


# if db_type = 'mysql':
#     connection = pymysql.connect(
#         host = "localhost",
#         user = "root",
#         password = "17200bc10B1_",
#         database = "cbm_system"
#     )

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
        dcc.Location(id='url', refresh=True, pathname='/dashboard'),
        html.H4("CONDITION-BASED MONITORING SYSTEM FOR ROTATING EQUIPMENT", style={"text-align": "center","margin": "20px"}),
        # navbar
        navbar,
        # html.Div(id="navbar-collapse"),
        # main
        dcc.Store(id="memory1"),    # Store component for storing data
        dcc.Store(id="filter_mem"), # Store component for storing filter data
        dcc.Store(id="filt_x_mem"), # Store component for storing filtered data
        html.Div(className="main",style={"justify-content":"center","align-items":"center","margin":"auto"},children=
            [     
            # html.Div(className="row header d-grid gap-2 d-md-flex justify-content-md-center",style={'padding':'20px'},children=[
            #         html.Div(className="col-xl-5 w-30", children=[
            #             dbc.Card(dbc.CardBody([right_panel]))
            #         ]),
            #         html.Div(className="col-xl-6 w-30", children=[
            #             dbc.Card(dbc.CardBody([filter_panel]))
            #         ])
            #     ]),          
                # content
                html.Div(className="container-fluid",children=[
                    html.Div(className="header d-grid gap-2 d-md-flex justify-content-md-center",style={"padding":"10px"},children=[offcanvas_left]),
                    # row 1
                    html.Div(className="row",style={},children=[
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
                    
                ])
                # footer
            ]
        )
    ]
)


predefined_list = ['Variable A', 'Variable B']

# Purpose: Ensures that variable_list is always synchronized with the data stored in memory1
@callback(
    Output("variable_list", "children"),
    [Input("memory1", "data")],
)
def update_variable_list(mem_data):

    if mem_data is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_list])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate
    else:
        var_list = list(mem_data['data']['data_vars'].keys())

        var_buttons = create_list_radio(var_list, "var_list_radio")

        return var_buttons





# Purpose: To ensure that metadata is always synchronized with data stored in memoery1 
#               -- allows user to see summary of metadata associated with the variables they analyze
@callback(
    Output("metadata", "children"),
    [Input("memory1", "data")],
)
def update_metadata(mem_data):

    meta_head = pd.Series(mem_data['data']).head(5)
    print(meta_head)

    return str(meta_head)


predefined_data = {
    'data_vars': {
        'Variable A': {'type': 'categorical'},
        'Variable B': {'type': 'numeric'}
    },
    'metadata': {
        'description': 'Predefined dataset',
        'author': 'Aiman Fatihah',
    }
}

# Purpose: To ensure that variable_content is always synchronized with selected varible and data stored in memory1
#           -- allow user to see detailed information about the selected varible and explore its content
@callback(
    Output("variable_content", "children"),
    [
    Input("var_list_radio", "value"),
     Input("memory1", "data")]
)
def update_variable_content(radio_value, mem_data):

    if mem_data is None and radio_value is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate
    else: 
        head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

        return str(head_dict)



# Purpose: allows user to upload a file, stores the content in system's memory (memory1), and displays the selected file
@callback(
    Output("memory1", "data"),
    Output("selected_file", "children"),
    [Input("upload", "contents"), 
     Input("upload", "filename")],
)
def update_memory(contents, filename):
    if not contents:
        raise PreventUpdate
    
    file_contents = parse_contents(contents, filename).to_dict()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory1 (
        id SERIAL PRIMARY KEY, 
        filename VARCHAR(255), 
        data TEXT
    )
    """)

    # # Store filename and data in MySQL database
    # sql = "INSERT INTO memory1 (filename, data) VALUES (%s, %s) IF NOT EXISTS {filename}"
    # val = (filename, str(file_contents))  # Store the data as JSON string
    # cursor.execute(sql, val)
    # connection.commit()

    # Check if the filename already exists
    cursor.execute("SELECT filename FROM memory1 WHERE filename = %s", (filename,))
    result = cursor.fetchone()

    if result:
        # File already exists, update the data
        sql = "UPDATE memory1 SET data = %s WHERE filename = %s"
        val = (str(file_contents), filename)
        cursor.execute(sql, val)
    else:
        # File doesn't exist, insert the data
        sql = "INSERT INTO memory1 (filename, data) VALUES (%s, %s)"
        val = (filename, str(file_contents))
        cursor.execute(sql, val)

    # cursor.close()
    # connection.close()


    return dict({'filenames': filename, 'data': file_contents}), f"File: {filename}"





#-------------------------------------------------------------------------------------------
# @callback(
#         Output("output","children"),
#         Input("memory1","data")
# )
# def convert_and_store_to_mysql(mem_data):

#     filename = mem_data['filenames']
#     data = mem_data['data']

#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {filename} (data TEXT)")

#     cursor.execute(f"INSERT INTO {filename} (data) VALUES (%s)", (data, ))

#     # connection.commit()
#     # cursor.close()
#     # connection.close()
    
#     return "Data stored in MySQL successfully"

    
#-------------------------------------------------------------------------------------------


'''
Allow users to:
1. select variable (vib/tach)
2. adjust filter settings
3. visualize raw measurement (graph_1) & filtered data
'''

@callback(
    Output("graph_1", "figure"),
    Output("filt_x_mem", "data"),
    [Input("memory1", "data"),
    Input("var_list_radio", "value"),
    Input("fs", "value"),
    Input("filter_apply", "value"),
    Input("filter_mem", "data")]
)
def update_td_plot(mem_data, selected_var, fs, fil_val, fil_taps):
    if mem_data is None and selected_var is None or fil_val is None or fil_taps is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate
    else:
        fs = int(fs)

        # extract data narrowed to var_list_radio option
        var_data = mem_data['data']['data_vars'][selected_var]["data"]
        df = pd.DataFrame(
            data=var_data,
            index=np.linspace(0, 
                            len(var_data)/fs, 
                            len(var_data)),
            columns=[selected_var]
        )

        # Create a Figure object to plot the raw measurement
        fig = go.Figure(
            layout={"xaxis":{"title":"time"}}
        )
        fig.add_trace(
            go.Scatter(
            name="Raw Measurement",
            x=df.index,
            y=df[selected_var],
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
                df[selected_var]
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
    Output('graph_2', 'figure'),
    Output("graph_spec", "figure"),
    [Input("memory1", "data"),
     Input("var_list_radio", "value"),
     Input("fs", "value"),
     Input("nfft", "value"),
     Input('graph_1', 'relayoutData'),
     Input("filt_x_mem", "data")
     ])
def update_fd_plot(mem_data, selected_var, fs, nfft, relayoutData, filt_x):
    if mem_data is None and selected_var is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate

    else:
        fs = int(fs)
        nfft = int(nfft)
        var_data = mem_data['data']['data_vars'][selected_var]["data"]
        # df = pd.DataFrame(
        #     data=var_data,
        #     index=np.linspace(0, len(var_data) / fs, len(var_data)),
        #     columns=[selected_var]
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




# Purpose: To select file type and adjust the cutoff frequency and visualize them corresponding to the filter taps and frequency response
@callback(
        Output("filter_mem", "data"),
        [Input("filter_type", "value"),
        Input("nfft", "value"),
        Input("fs", "value"),
        Input("fc_1", "value"),
        Input("fc_2", "value")])
def plot_filter(filter_type, n_fft, fs, fc_1, fc_2):
    fs = float(fs)
    fc_1 = int(fc_1)
    fc_2 = int(fc_2)
    n_fft = int(n_fft)

    # Get the filter taps based on the selected filter type, n_fft, and cutoff frequencies
    y = get_ftaps(filter_type, n_fft + 1, fc_1, fc_2, fs)
    print(y)

    # Create a Figure object to plot the filter tap
    # fig = go.Figure()
    # fig.add_trace(
    #     go.Scatter(
    #         name="Filter taps",
    #         y=y,
    #         mode="lines+markers",
    #         line=dict(
    #             color="blue"
    #         )
    #     )
    # )

    # Customize the layout of the Figure object
    # fig.update_layout(xaxis_rangeslider_visible=False,
    #                   margin=dict(l=5, r=5, t=5, b=5),
    #                   xaxis=go.XAxis(showticklabels=False),
    #                   legend=dict(yanchor="top", y=1, xanchor="left", x=0))

    # # Calculate the frequency response of the filter taps
    # w, h = signal.freqz(y, worN=int(fs / 2))

    # # Create another Figure object to plot the frequency response
    # fig2 = go.Figure()
    # fig2.add_trace(
    #     go.Scatter(
    #         name="Filter taps",
    #         x=(w / np.pi) * (fs / 2),
    #         y=20 * np.log10(abs(h)),
    #         mode="lines",
    #         line=dict(
    #             color="blue"
    #         )
    #     )
    # )

    # # Customize the layout of the Figure object
    # fig2.update_layout(xaxis_rangeslider_visible=False,
    #                    margin=dict(l=5, r=5, t=5, b=5),
    #                    xaxis=go.XAxis(title='Frequency'),
    #                    yaxis=go.XAxis(title='Magnitude (dB)')
    #                    )

    # Store the filter taps in filter_mem_data
    filter_mem_data = {
        "taps": y
    }
    return filter_mem_data


if connection:
    print("Connected dashboard to the server...")

connection.commit()

# cursor.close()
connection.close()