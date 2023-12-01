import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

# Sample data chunk
data_chunk = ['Data point 1', 'Data point 2', 'Data point 3', 'Data point 4']

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Store(id='stored-data'),  # This will store the data to be shared
    html.Div(id='data-output', children=''),
    # Hidden div to store the current index
    html.Div(id='index-holder', style={'display': 'none'}, children=0),
    dcc.Graph(id='live-graph')  # Graph component to display the live graph
])

@app.callback(
    Output('stored-data', 'data'),  # Update the Store component
    Output('data-output', 'children'),
    Output('index-holder', 'children'),
    Input('interval-component', 'n_intervals'),
    State('index-holder', 'children'),
    State('stored-data', 'data')  # Read the current stored data
)
def update_data(n, current_index, stored_data):
    # Make sure current_index is an integer
    current_index = int(current_index)
    
    # Initialize stored_data if it's None
    if not stored_data:
        stored_data = []

    # Check if the current index is still within the range of data_chunk
    if current_index < len(data_chunk):
        # Fetch the data at the current index
        data_to_display = data_chunk[current_index]
        # Print the data
        print(data_to_display)
        # Append the new data to the stored_data
        stored_data.append(data_to_display)
        # Update the current index for the next callback
        current_index += 1
    else:
        # Indicate that the processing is done
        data_to_display = 'Done processing data chunk.'
        current_index = 0  # Reset index or remove this line to stop the process

    # Return the updated stored data, the current data to display, and the updated index
    return stored_data, data_to_display, current_index

@app.callback(
    Output('live-graph', 'figure'),
    Input('stored-data', 'data')
)
def update_graph(stored_data):
    # If there's no data, create an empty graph
    if not stored_data:
        return go.Figure()
    
    # Otherwise, create a graph with the stored data
    figure = {
        'data': [
            go.Scatter(
                x=list(range(len(stored_data))),
                y=stored_data,
                mode='lines+markers'
            )
        ],
        'layout': {
            'title': 'Live Data Points',
            'xaxis': {
                'title': 'Index'
            },
            'yaxis': {
                'title': 'Value'
            }
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
