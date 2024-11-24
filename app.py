import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import datetime
from fitparse import FitFile

# Load the .fit file
fit_file = FitFile('yhflr5YcfJD8zHqa4czOkiDQK2vhM60nRbFaCeFQ.fit')  # Replace with your file path

fields = set()

# Extract all record messages from the .fit file
records = []
for record in fit_file.get_messages('record'):
    record_data = {}
    for data in record:
        record_data[data.name] = data.value
        fields.add(data.name)
    records.append(record_data)

# Load the records into a DataFrame
df = pd.DataFrame(records)

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define your Functional Threshold Power (FTP)
FTP = 240

# Define your maximum heart rate
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

# Initialize the Dash app
app = dash.Dash(__name__)

# Expose the server for Gunicorn
server = app.server

app.layout = html.Div([
    html.H1("Power Zone Analysis", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)