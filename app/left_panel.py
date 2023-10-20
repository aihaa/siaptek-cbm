from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from constants import *

# Create an upload component that allows users to select a file
files_location = dcc.Upload(
    id="upload",
    children=[
        'Drag and Drop or ',
        html.A('Select a File')
    ],
    multiple=False,

    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    }
)

# Defines a function that creates an accordion component to display a list of files
def create_files_list(files):
    acc_files = []                      # Create an empty list to store the accordion items
    for i, file in enumerate(files):    # Iterate over each file in the provided list
        acc_files.append(               # Create an accordion item for each file and add it to the list
            dbc.AccordionItem(
                title=file              # Set the title of the accordion item as the file name
            )
        )
    accordion = html.Div(               # Create a HTML division element to contain the accordion component
        dbc.Accordion(
            acc_files,                  # Pass the list of accordion items to the Accordion component
            start_collapsed=True        # Set the accordion items to start in a collapsed state
        ),
    )
    return accordion


# Takes files and id_name (initial name of the file), to create a list of radio
def create_list_radio(files, id_name):
    radio_options = []                      # Create an empty list to store the radio item options
    for i, file in enumerate(files):        # Iterate over each file in the provided list
        radio_options.append(               # Create a radio item option for each file and add it to the list
            {"label": file, "value": file}  # Use the file name as both the label and value of the option
        )
    radio = dbc.RadioItems(                 # Create a RadioItems component from the Dash Bootstrap Components library
        options=radio_options,              # Set the options of the radio items to the list of radio item options
        value=files[0],                     # Set the initial value of the radio items to the first file in the list
        id=id_name
    )
    return radio


# To create a consistent layout for input fields throughout the application
#           Creates a row contain 2 columns: display name, display input field
def create_input_box(name, id_1, ph, value):
    return dbc.Row(
        [
            dbc.Col(html.Div(name)),                                    # Create a column containing a div with the provided name
            dbc.Col(dbc.Input(id=id_1, placeholder=ph, value=value)),   # Create a column containing an input field
            dbc.Row()                                                   # Create an empty row
        ]
    )


# To create a consistent layout for dropdown components throughout the application
#           Creates a row contain 2 columns: display name, display dropdown component
def create_drop_down(name, op_list, id_1, default_value=0):
    return dbc.Row(
        [
            dbc.Col(html.Div(name)),                                    # Create a column containing a div with the provided name
            dbc.Col(
                dcc.Dropdown(
                    id=id_1,                                            # Set the ID of the dropdown component
                    options=[dict(label=x, value=x) for x in op_list],  # Set the options of the dropdown component
                    value=op_list[default_value]                        # Set the initial selected value of the dropdown component
                )
            ),
            dbc.Row()                                                   # Create an empty row
        ]
    )


def create_checkbox(name, op_list, id_1, default_value=0, switch_flag=False):
    return dbc.Row(
        [
            dbc.Col(dcc.Markdown(f""" ** {name} ** """)),
            # dbc.Col(html.Div(name)),
            dbc.Col(
                dbc.Checklist(
                    id=id_1,
                    options=[dict(value=x) for x in op_list],
                    value=op_list[default_value],
                    switch=switch_flag
                )
            ),
            dbc.Row()
        ]
    )


# To provide a visually organizaed representation of file details in the system
file_details = html.Div(
    children=[
        # Create a heading for the file contents section
        html.H6("File contents"),                                                   
        # Create a div container for metadata with an ID and styling
        html.Div(
            id="metadata",
            children=[],
            style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
        ),

        # Create a heading for the data variables section
        html.H6("Data variables"),
        # Create a div container for the variable list with an ID and styling
        html.Div(
            id="variable_list",
            children=[],
            style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
        ),

        # # Create a heading for the variable contents section
        # html.H6("Variable contents"),
        # # Create a div container for the variable content with an ID and styling
        # html.Div(
        #     id="variable_content",
        #     children=[],
        #     style={"height": "24vh", "maxHeight": "24vh", "overflow": "scroll"},
        # ),
    ],
    id="File_contents",
    style={"marginTop": "2px", "marginBottom": "2px"}
)


# Contains input boxes for the sampling frequency and NFFT values
right_panel = html.Div(
    [
        create_input_box("Sampling Frequency: ", "fs", "50000", 50000),
        create_input_box("NFFT: ", "nfft", "2048", 2048),

        create_checkbox("Filter:", [0], "filter_apply", 0, True),
        create_drop_down("Window type", FILTERS, "filter_type", 11),
        create_input_box("Cut off 1", "fc_1", "0", 0),
        create_input_box("Cut off 2", "fc_2", "500", 500),
    ]
)

# Contains checkbox, dropdown menu, input boxes, and two graphs for filter-related options and visualizations
filter_panel = html.Div(
    [
        create_checkbox("Filter:", [0], "filter_apply", 0, True),
        create_drop_down("Window type", FILTERS, "filter_type", 11),
        create_input_box("Cut off 1", "fc_1", "0", 0),
        create_input_box("Cut off 2", "fc_2", "500", 500),
        # dcc.Graph(id="graph_3", style={"height": "29vh"}),
        # dcc.Graph(id="graph_4", style={"height": "29vh"})
    ],
)
