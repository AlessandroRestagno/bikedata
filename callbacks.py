from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import io
import base64
from data_processing import process_fit_file


def register_callbacks(app):
    @app.callback(
        Output("output-data-upload", "children"),
        Input("upload-fitfile", "contents"),
        State("upload-fitfile", "filename"),
        State("input-ftp", "value"),
        State("input-max-hr", "value"),
    )
    def parse_fit_file(contents, filename, ftp, max_hr):
        if contents is None:
            return html.Div(
                "Upload a .FIT file to see the corresponding graphs and analysis.",
                style={"textAlign": "center", "marginTop": "15px"},
            )

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
                        f"File '{filename}' uploaded successfully. FTP: {ftp} and Max HR: {max_hr}.",
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
