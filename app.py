from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from callbacks import register_callbacks 

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

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)