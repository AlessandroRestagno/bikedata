from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
from fitparse import FitFile
import io
import base64
from data_processing import process_fit_file

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose the server for Gunicorn
server = app.server

# Define layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1(
                            "Upload and Analyze Your .FIT File",
                            style={"textAlign": "center", "marginTop": "50px"},
                        ),
                        dcc.Upload(
                            id="upload-fitfile",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select a .FIT File")]
                            ),
                            className="upload-container",  # Apply the custom CSS class
                            multiple=False,  # Only one file at a time
                        ),
                        # html.Div(id="output-data-upload"),
                        dbc.Container(id="output-data-upload", fluid=True),
                    ]
                ),
                width=12  # Adjust width as needed
            ),
        )
    ],
    fluid=True,
    className="container-fluid",
    #className="d-flex justify-content-center align-items-center vh-100",
)

# Callback to process the uploaded file
@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-fitfile", "contents"),
    State("upload-fitfile", "filename")
)
def parse_fit_file(contents, filename):
    if contents is None:
        return html.Div("Please upload a .FIT file to analyze.",style={"textAlign": "center", "marginTop": "15px"})

    # Decode the uploaded file
    content_type, content_string = contents.split(",")
    decoded = io.BytesIO(base64.b64decode(content_string))
    
    try:
        fig, fig_HR, fig_cadence, fig_all = process_fit_file(decoded)               

        # Display summary statistics
        return html.Div([
            html.H4(f"File '{filename}' uploaded successfully.",style={"textAlign": "center", "marginTop": "15px"}),
            # html.P(f"Number of records: {len(df)}"),
            # html.P(f"Columns: {', '.join(df.columns)}"),
            # Graphs
            dbc.Row(
                dbc.Col(dcc.Graph(figure=fig_all), width=12)  # Full width for all data graph
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=fig), width=4),
                    dbc.Col(dcc.Graph(figure=fig_HR), width=4),  # Half-width for HR graph
                    dbc.Col(dcc.Graph(figure=fig_cadence), width=4),  # Half-width for cadence graph
                ]
            ),
            ])
    except Exception as e:
        return html.Div(f"An error occurred while processing the file: {str(e)}")

if __name__ == '__main__':
    app.run_server(debug=True)