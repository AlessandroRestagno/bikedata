from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime
from fitparse import FitFile
import io
import base64

FTP = 240
max_heart_rate = 186
# Define the function to categorize zones based on power values
def assign_zone(power):
    if power <= 0.55 * FTP:
        return 'Zone 1 '
    elif power <= 0.75 * FTP:
        return 'Zone 2 '
    elif power <= 0.9 * FTP:
        return 'Zone 3 '
    elif power <= 1.05 * FTP:
        return 'Zone 4 '
    elif power <= 1.2 * FTP:
        return 'Zone 5 '
    else:
        return 'Zone 6 '
    
# Define the function to categorize zones based on Heart Rates (0-50-65-80-85-92-10)
def assign_heart_zone(heart_rate):
    if heart_rate <= 0.5*max_heart_rate:
        return 'Resting '
    elif heart_rate <= 0.65*max_heart_rate:
        return 'Zone 1 '
    elif heart_rate <= 0.8*max_heart_rate:
        return 'Zone 2 '
    elif heart_rate <= 0.85*max_heart_rate:
        return 'Zone 3 '
    elif heart_rate <= 0.92*max_heart_rate:
        return 'Zone 4 '
    else:
        return 'Zone 5 '
    
def assign_color(power):
    if power <= 0.55*FTP:
        return 'gray'
    elif power <= 0.75*FTP:
        return 'blue'
    elif power <= 0.9*FTP:
        return 'green'
    elif power <= 1.05*FTP:
        return 'yellow'
    elif power <= 1.2*FTP:
        return 'orange'
    else:
        return 'red'

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
        # Read the .fit file
        fit_file = FitFile(decoded)
        
        # Extract records
        records = []
        for record in fit_file.get_messages('record'):
            record_data = {}
            for data in record:
                record_data[data.name] = data.value
            records.append(record_data)
        
        # Create a DataFrame
        df = pd.DataFrame(records)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Define your Functional Threshold Power (FTP)
        FTP = 240

        # Define your maximum heart rate
        max_heart_rate = 186

        # Update the 'zone' column based on the 'power' column
        df['zone'] = df['power'].apply(assign_zone)

        # Count the occurrences of each zone (time spent in each zone)
        power_zones = ['Zone 1 ', 'Zone 2 ', 'Zone 3 ', 'Zone 4 ', 'Zone 5 ', 'Zone 6 ']
        zone_counts = df['zone'].value_counts().sort_index() / 60
        zone_counts = zone_counts.reindex(power_zones, fill_value=0)

        # Set up custom colors and text positions
        custom_colors = ["gray", "blue", "green", 'yellow', 'orange', 'red']
        position_text_inorout = ['inside'] * len(zone_counts)
        for i in range(len(zone_counts)):
            if zone_counts.iloc[i] < (max(zone_counts) / 8):
                position_text_inorout[i] = 'outside'

        # Create the bar chart
        fig = go.Figure(
            data=[
                go.Bar(
                    y=power_zones,
                    x=zone_counts,
                    name='zone',
                    orientation='h',
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5,
                    text=[str(datetime.timedelta(seconds=i * 60)) for i in zone_counts],
                    textposition=position_text_inorout,
                    marker_color=custom_colors
                )
            ],
            layout=dict(
                title={
                    'text': "Time Spent in Each Power Zone",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                },
                titlefont=dict(size=20, family="Roboto, monospace"),
                font=dict(size=16, family="Roboto, monospace"),
                barmode='stack',
                xaxis=dict(title='Minutes'),
                template='plotly_dark',
                barcornerradius=15
            ),
        )
        fig.update_yaxes(autorange="reversed")

        HR_zones_col = df['heart_rate'].dropna().apply(assign_heart_zone)
        HR_power_zones = ['Resting ', 'Zone 1 ', 'Zone 2 ', 'Zone 3 ', 'Zone 4 ', 'Zone 5 ']
        HR_zone_counts = HR_zones_col.value_counts().sort_index() / 60
        HR_zone_counts = HR_zone_counts.reindex(HR_power_zones,fill_value=0)

        # Set up a cool color palette and styling
        HR_custom_colors = ["blue","green",'yellow','orange','red']
        HR_position_text_inorout = ['inside','inside','inside','inside','inside']
        # We plot only from Z1 to Z5. We don't plot the resting time.
        for i in range(1,len(HR_zone_counts)):
            if HR_zone_counts.iloc[i] < (max(HR_zone_counts)/8):
                HR_position_text_inorout[i-1] = 'outside'

        # Create the histogram with enhanced styling
        fig_HR = go.Figure(
            data=[
                go.Bar(y=HR_power_zones[1:],
                    x=HR_zone_counts.iloc[1:],
                    name='zone',
                    orientation='h',
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5,
                    text=[str(datetime.timedelta(seconds = i*60)) for i in HR_zone_counts.iloc[1:]],
                    textposition=HR_position_text_inorout,
                    marker_color=HR_custom_colors
                )
            ],
            layout=dict(
                title={
                'text': "Time Spent in Each Heart Rate Zone",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                },
                titlefont=dict(size=20,family="Roboto, monospace",),
                font=dict(size=16,family="Roboto, monospace",),
                barmode='stack',
                xaxis=dict(title='Minutes'),
                template='plotly_dark',
                barcornerradius=15
            ),
        )
        fig_HR.update_yaxes(autorange="reversed")

        # Create the histogram with enhanced styling
        fig_cadence = go.Figure(data=[go.Histogram(x=df.cadence, histnorm='probability',marker_color='rgb(250,184,29)')],
            layout=dict(
                title={
                'text': "Cadence Distribution",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                },
                titlefont=dict(size=20,family="Roboto, monospace",),
                font=dict(size=16,family="Roboto, monospace",),
                barmode='stack',
                yaxis=dict(title='Frequency',showticklabels=False),
                template='plotly_dark',
                barcornerradius=15
            ),
        )
        #fig.update_yaxes(autorange="reversed")
        fig_cadence.update_xaxes(range=[30,150])

        # Create traces
        fig_all = go.Figure()
        fig_all.add_trace(go.Scatter(x=df.timestamp, y=df.power,
                            fill='tozeroy',
                            fillgradient=dict(
                                type="horizontal",
                                colorscale=df.power.apply(assign_color).values,
                            ),
                            mode='lines',
                            name='Power'))
        fig_all.add_trace(go.Scatter(x=df.timestamp, y=df.heart_rate,
                            mode='lines',
                            name='Heart Rate'))
        fig_all.add_trace(go.Scatter(x=df.timestamp, y=df.cadence,
                            mode='lines', name='Cadence'))
        fig_all.update_layout(title={
                                'text': 'Power, Heart Rate, and Cadence Over Time',
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                },
                        template='plotly_dark',
                        font=dict(size=16,family="Roboto, monospace",),
                        titlefont=dict(size=20,family="Roboto, monospace"),
                        xaxis = go.XAxis(showticklabels=False),
                        )                        

        # Display summary statistics as an example
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