from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
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
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Label("Enter FTP", style={"textAlign": "center", "marginTop": "10px", "fontWeight": "bold"}),  # Label for FTP
                                                dbc.Input(
                                                    id="input-ftp",
                                                    type="number",
                                                    placeholder="Enter FTP",
                                                    value=240,  # Default FTP value
                                                    style={
                                                        "textAlign": "center",
                                                        "marginTop": "10px",
                                                        "backgroundColor": "yellow",
                                                        },
                                                ),
                                            ],
                                            width=2,  # Set the same width for both columns
                                            className="d-flex justify-content-center"  # Centers the content horizontally within the column
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Label("Enter Max Heart Rate", style={"textAlign": "center", "marginTop": "10px", "fontWeight": "bold"}),  # Label for Max HR
                                                dbc.Input(
                                                    id="input-max-hr",
                                                    type="number",
                                                    placeholder="Enter Max Heart Rate",
                                                    value=186,  # Default Max Heart Rate value
                                                    style={
                                                        "textAlign": "center",
                                                        "marginTop": "10px",
                                                        "backgroundColor": "yellow",
                                                        },
                                                ),
                                            ],
                                            width=2,  # Set the same width for both columns
                                            className="d-flex justify-content-center"  # Centers the content horizontally within the column
                                        ),
                                    ],
                                    justify="center",  # Centers the columns in the row
                                    style={"marginTop": "30px"}  # Optional: Adds space above the row for visual balance
                                )
                            ]
                        ),
                        # dbc.Container(id="output-data-upload", fluid=True),
                        dcc.Loading(
                            id="loading",
                            type="dot",  # Choose spinner type: "circle", "dot", or "default"
                            style={"marginTop": "30px"},
                            children=dbc.Container(id="output-data-upload", fluid=True),
                        ),
                    ]
                ),
                width=12,  # Adjust width as needed
            ),
        )
    ],
    fluid=True,
    className="container-fluid",
)

# Callback to process the uploaded file
@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-fitfile", "contents"),
    State("upload-fitfile", "filename"),
    State("input-ftp", "value"),
    State("input-max-hr", "value")
)

def parse_fit_file(contents, filename, ftp, max_hr):
    if contents is None:
        return html.Div("Upload a .FIT file to see the corresponding graphs and analysis.", style={"textAlign": "center", "marginTop": "15px"})

    # Decode the uploaded file
    content_type, content_string = contents.split(",")
    decoded = io.BytesIO(base64.b64decode(content_string))
    
    try:
        # Pass user inputs (FTP and Max HR) to the processing function
        fig, fig_HR, fig_cadence, fig_all = process_fit_file(decoded, ftp, max_hr)

        # Display summary statistics
        return html.Div(
            [
                html.H4(
                    f"File successfully uploaded. Current settings: FTP = {ftp}, Max Heart Rate = {max_hr}.",
                    style={"textAlign": "center", "marginTop": "15px"},
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(figure=fig_all), width=12),  # Full width for all data graph
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(figure=fig), width=4),
                        dbc.Col(dcc.Graph(figure=fig_HR), width=4),  # Half-width for HR graph
                        dbc.Col(dcc.Graph(figure=fig_cadence), width=4),  # Half-width for cadence graph
                    ]
                ),
            ]
        )
    except Exception as e:
        return html.Div(f"An error occurred while processing the file: {str(e)}")

if __name__ == '__main__':
    app.run_server(debug=True)