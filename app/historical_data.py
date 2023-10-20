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
from navbar import navbar
from additional import offcanvas_left, files_option, offcanvas_left_2
from utils import retrieve_files

load_figure_template('LUX')

# Define external stylesheets for the app
#external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create a Dash app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "17200bc10B1_",
    database = "cbm_system"
)

cursor = connection.cursor()




#--------------------------------------------------(LAYOUT)------------------------------------------------------------------------

# Define the layout of the app
layout = html.Div(
    [
        dcc.Location(id='url', refresh=True, pathname='/historical_data'),
        html.H4("CONDITION-BASED MONITORING SYSTEM FOR ROTATING EQUIPMENT", style={"text-align": "center","margin": "20px"}),
        # navbar
        navbar,
        # html.Div(id="navbar-collapse"),
        # main
        dcc.Store(id="memory2"),    # Store component for storing data
        # dcc.Store(id="filter_mem"), # Store component for storing filter data
        # dcc.Store(id="filt_x_mem"), # Store component for storing filtered data
        # dcc.Store(id="metadata2"),
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
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"},children=[files_option]),
                    html.Div(className="header d-md-flex justify-content-md-center",style={"padding":"10px"},children=[offcanvas_left_2]),
                    # html.Div(id="metadata2"),
                    # html.Div(id="file_dropdown")
                    # html.H5(id="print_file",children=[])
                    # row 1
                    # html.Div(className="row",style={},children=[
                    #     # col 1
                    #     html.Div(className="col-xl-6 d-flex", style={}, children=[
                    #         html.Div(className="w-100", children=[
                    #             # graph 1
                    #             html.Div(className="row",style={'padding-bottom':'20px'}, children=[
                    #                 html.Div(className="", children=[
                    #                     html.Div(className="card", children=[
                    #                         html.Div(className="card-body", children=[
                    #                             html.Div(className="row", children=[html.H5(className="card-title",children=["Time Domain"])]),
                    #                             html.Div(className="row", children=[dcc.Graph(id="graph_1",style={'height':'250px'})])
                    #                         ])
                    #                     ]),
                    #                     html.Div(className="card")
                    #                 ]),
                    #             ]),
                    #             # graph 2
                    #             html.Div(className="row", children=[
                    #                 html.Div(className="", children=[
                    #                     html.Div(className="card", children=[
                    #                         html.Div(className="card-body", children=[
                    #                             html.Div(className="row", children=[html.H5(className="card-title",children=["Frequency Plot"])]),
                    #                             html.Div(className="row", children=[dcc.Graph(id="graph_2",style={'height':'250px'})])
                    #                         ])
                    #                     ])
                    #                 ])
                    #             ]),
                    #         ])
                    #     ]),
                    #     # col 2
                    #     html.Div(className="col-xl-6", children=[
                    #         html.Div(className="card", children=[
                    #             html.Div(className="card-body", children=[
                    #                 html.Div(className="row", children=[html.H5(className="card-title", children=["Spectrogram"])]),
                    #                 html.Div(className="row", children=[dcc.Graph(id="graph_spec",style={'height':'575px'})])
                    #             ])
                    #         ])
                    #     ])
                    # ]),
                    
                ])
                # footer
            ]
        )
    ]
)


# @callback(
#     Output("memory2", "data"),
#     # Output("print_file","children"),
#     [
#     Input("file_dropdown", "value"),
#     # Input({'type': 'dropdown-item', 'index': ALL}, 'n_clicks')
#      ]
# )
# for i, _ in enumerate(files_option):
#     callback(
#         Output('memory2', 'data',allow_duplicate=True),
#         Input({'type': 'dropdown-item', 'index': i}, 'n_clicks')
#     )(lambda n_clicks, index=i: update_memory(n_clicks, index))
#     prevent_initial_call='initial_duplicate'  

# def update_memory(selected_file):
#     # Retrieve the data for the selected file from the database
#     cursor = connection.cursor()
#     cursor.execute("SELECT data FROM memory1 WHERE filename = %s", (selected_file,))
#     result = cursor.fetchone()
#     # cursor.close()


#     output_dict = dict({'filenames': selected_file, 'data': result})
#     # selected_file = ""

#     return output_dict


import json

@callback(
    Output("memory2", "data"),
    # Output("print_file","children"),
    [
    Input("file_dropdown", "value"),
    # Input({'type': 'dropdown-item', 'index': ALL}, 'n_clicks')
     ]
)

def update_memory(selected_file):
    # Check if the 'memory1' table exists
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES LIKE 'memory1'")
    table_exists = len(cursor.fetchall()) > 0

    if table_exists:
        # Retrieve the data for the selected file from the database
        cursor.execute("SELECT data FROM memory1 WHERE filename = %s", (selected_file,))
        data = cursor.fetchone()
    else:
        data = None

    cursor.close()

    if data is not None:
        # # data = data[0].replace("'", "\"")  # Replace single quotes with double quotes
        # data = json.loads(data)  # Convert the string to a dictionary
        # file_content = data.split("dtype: object")[0].strip()

        # file_dict = ast.literal_eval(data)
        # Replace single quotes with double quotes to make it a valid JSON string
        # string_data = data.replace("'", "\"")

        # # Use json.loads() to parse the string as a JSON object
        # file_dict = json.loads(string_data)

        # ----------------- PALING BERJAYA ----------- setakat ni with error lol
        # Convert the string to a tuple using eval()
        # tuple_data = ast.literal_eval(data)

        # # Convert the tuple to a dictionary using json.loads()
        # file_dict = json.loads(json.dumps(tuple_data))

        output_dict = {'filenames': selected_file, 'data': data}

    return output_dict



# def update_memory(selected_file):
#     # Check if the 'memory1' table exists
#     cursor = connection.cursor()
#     cursor.execute("SHOW TABLES LIKE 'memory1'")
#     # table_exists = cursor.fetchone() is not None
#     table_exists = len(cursor.fetchall()) > 0

#     if table_exists:
#         # Retrieve the data for the selected file from the database
#         cursor.execute("SELECT data FROM memory1 WHERE filename = %s", (selected_file,))
#         data = cursor.fetchone()
#     else:
#         data = None

#     cursor.close()


#     data = data[0].replace("'", "\"")
#     # data is in str --> convert to json
#     data = json.loads(data)

#     output_dict = dict({'filenames': selected_file, 'data': data})

#     return output_dict


# @callback(
#     Output("metadata2", "children"),
#     [Input("memory2", "data")],
#     # prevent_initial_call=True
# )
# def update_metadata(mem_data):

#     meta_head = pd.Series(mem_data['data']).head(5)
#     print(meta_head)

#     return str(meta_head)


# predefined_list = ['Variable A', 'Variable B']

# # Purpose: Ensures that variable_list is always synchronized with the data stored in memory2
# @callback(
#     Output("variable_list2", "children"),
#     [Input("memory2", "data")],
# )
# def update_variable_list(mem_data):

#     if mem_data is None:
#         # suggestion = html.Ul([html.Li(var) for var in predefined_list])
#         # return html.Div([suggestion])
#         raise dash.exceptions.PreventUpdate
#     else:
#         var_list = list(mem_data['data']['data_vars'].keys())

#         var_buttons = create_list_radio(var_list, "var_list_radio")

#         return var_buttons
    


# # predefined_data = {
# #     'data_vars': {
# #         'Variable A': {'type': 'categorical'},
# #         'Variable B': {'type': 'numeric'}
# #     },
# #     'metadata': {
# #         'description': 'Predefined dataset',
# #         'author': 'Aiman Fatihah',
# #     }
# # }

# # Purpose: To ensure that variable_content is always synchronized with selected varible and data stored in memory2
# #           -- allow user to see detailed information about the selected varible and explore its content
# @callback(
#     Output("variable_list2", "children", allow_duplicate=True),
#     [
#     Input("var_list_radio", "value"),
#      Input("memory2", "data")],
#      prevent_initial_call=True
# )
# def update_variable_content(radio_value, mem_data):

#     if mem_data is None and radio_value is None:
#         # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
#         # return html.Div([suggestion])
#         raise dash.exceptions.PreventUpdate
#     else: 
#         head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

#         return str(head_dict)
    

# @callback(
#     Output("variable_content2", "children"),
#     [
#     Input("var_list_radio", "value"),
#      Input("memory2", "data")]
# )
# def update_variable_content(radio_value, mem_data):

#     if mem_data is None and radio_value is None:
#         # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
#         # return html.Div([suggestion])
#         raise dash.exceptions.PreventUpdate
#     else: 
#         head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

#         return str(head_dict)
    

# @callback(
#     Output("graph_1", "figure", allow_duplicate=True),
#     Output("filt_x_mem", "data", allow_duplicate=True),
#     [Input("memory2", "data"),
#     Input("var_list_radio", "value"),
#     Input("fs", "value"),
#     Input("filter_apply", "value"),
#     Input("filter_mem", "data")],
#     prevent_initial_call=True
# )
# def update_td_plot(mem_data, selected_var, fs, fil_val, fil_taps):
#     if mem_data is None and selected_var is None or fil_val is None or fil_taps is None:
#         # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
#         # return html.Div([suggestion])
#         raise dash.exceptions.PreventUpdate
#     else:
#         fs = int(fs)

#         # extract data narrowed to var_list_radio option
#         var_data = mem_data['data']['data_vars'][selected_var]["data"]
#         df = pd.DataFrame(
#             data=var_data,
#             index=np.linspace(0, 
#                             len(var_data)/fs, 
#                             len(var_data)),
#             columns=[selected_var]
#         )

#         # Create a Figure object to plot the raw measurement
#         fig = go.Figure(
#             layout={"xaxis":{"title":"time"}}
#         )
#         fig.add_trace(
#             go.Scatter(
#             name="Raw Measurement",
#             x=df.index,
#             y=df[selected_var],
#             mode="lines",
#             line=dict(
#                 color="blue"
#             )
#             )
#         )
#         fig.update_layout
#         print(fil_val,fil_taps)



#         # check if a filter is applied
#         if type(fil_val) is list and len(fil_val) > 0:

#             filtered = signal.lfilter(
#                 fil_taps["taps"],
#                 1.0,
#                 df[selected_var]
#             )
#             delay = 0.5*(len(fil_taps["taps"]) - 1) / fs
#             print(f"delay--{delay}")


#             indices = df.index[:-int((len(fil_taps["taps"]) - 1) / 2)]
#             # create filtered df with appropriate indexing and column name
#             df_filt = pd.DataFrame(
#                 data= filtered[int( (len(fil_taps["taps"]) - 1) /2 ):],
#                 index= df.index[: -int( (len(fil_taps["taps"]) - 1) /2)],
#                 columns=["filtered"]
#             )
#             print(df_filt.head(10))


#             # update the figure after filter is applied
#             fig.add_trace(
#                 go.Scatter(
#                 name='Filtered',
#                 x=df_filt.index,
#                 y=df_filt["filtered"],
#                 mode="lines",
#                 line=dict(
#                     color="red"
#                 )
#                 )
#             )

#             filt_x = {
#                 "filtered": filtered[int((len(fil_taps["taps"]) - 1) / 2):], 
#                 "index": indices
#             }
#         else:
#             # no filter is applied
#                         filt_x = {
#                             "filtered":None,
#                             "index":None
#                         }
#         # update the figure after filter is disabled
#         fig.update_layout(
#             xaxis_rangeslider_visible=False,
#             margin=dict(
#                 l=10,
#                 r=10,
#                 t=20,
#                 b=20
#             ),
#             legend=dict(
#                 yanchor="top",
#                 y=1,
#                 xanchor="left",
#                 x=0
#             )
#         )

            

#         return fig, filt_x



# ------------------------------------------------------------------------------------------------
# predefined_list = ['Variable A', 'Variable B']

import ast

# Purpose: Ensures that variable_list is always synchronized with the data stored in memory2
@callback(
    Output("variable_list2", "children"),
    [Input("memory2", "data")],
)
def update_variable_list2(mem_data):

    if mem_data is None:
        raise dash.exceptions.PreventUpdate
    else:
        # data = json.loads()
        # file_contents = 
        var_list = list(mem_data['data']['data_vars'].keys())
        var_buttons = create_list_radio(var_list, "var_list_radio2")
        return var_buttons





# Purpose: To ensure that metadata is always synchronized with data stored in memoery1 
#               -- allows user to see summary of metadata associated with the variables they analyze
@callback(
    Output("metadata2", "children"),
    [Input("memory2", "data")],
)
def update_metadata(mem_data):

    meta_head = pd.Series(mem_data['data']).head(5)
    print(meta_head)

    return str(meta_head)


# predefined_data = {
#     'data_vars': {
#         'Variable A': {'type': 'categorical'},
#         'Variable B': {'type': 'numeric'}
#     },
#     'metadata': {
#         'description': 'Predefined dataset',
#         'author': 'Aiman Fatihah',
#     }
# }

# Purpose: To ensure that variable_content is always synchronized with selected varible and data stored in memory2
#           -- allow user to see detailed information about the selected varible and explore its content
@callback(
    Output("variable_content2", "children"),
    [
    Input("var_list_radio2", "value"),
     Input("memory2", "data")]
)
def update_variable_content2(radio_value, mem_data):

    if mem_data is None and radio_value is None:
        # suggestion = html.Ul([html.Li(var) for var in predefined_data['data_vars'].keys()])
        # return html.Div([suggestion])
        raise dash.exceptions.PreventUpdate
    else: 
        head_dict = pd.Series(mem_data['data']['data_vars'][radio_value]).head()

        return str(head_dict)



# # Purpose: allows user to upload a file, stores the content in system's memory (memory2), and displays the selected file
# @callback(
#     Output("memory2", "data"),
#     Output("selected_file", "children"),
#     [Input("upload", "contents"), 
#      Input("upload", "filename")],
# )
# def update_memory(contents, filename):
#     if not contents:
#         raise PreventUpdate
    
#     file_contents = parse_contents(contents, filename).to_dict()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS memory2 (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     filename VARCHAR(255),
#     data LONGTEXT
#     )
#     """)

#     # # Store filename and data in MySQL database
#     # sql = "INSERT INTO memory2 (filename, data) VALUES (%s, %s) IF NOT EXISTS {filename}"
#     # val = (filename, str(file_contents))  # Store the data as JSON string
#     # cursor.execute(sql, val)
#     # connection.commit()

#     # Check if the filename already exists
#     cursor.execute("SELECT filename FROM memory2 WHERE filename = %s", (filename,))
#     result = cursor.fetchone()

#     if result:
#         # File already exists, update the data
#         sql = "UPDATE memory2 SET data = %s WHERE filename = %s"
#         val = (str(file_contents), filename)
#     else:
#         # File doesn't exist, insert the data
#         sql = "INSERT INTO memory2 (filename, data) VALUES (%s, %s)"
#         val = (filename, str(file_contents))

#     # cursor.close()
#     # connection.close()


#     return dict({'filenames': filename, 'data': file_contents}), f"File: {filename}"


