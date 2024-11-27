import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from fitparse import FitFile

# FTP = 240
# max_heart_rate = 186

def process_fit_file(decoded, FTP=240, max_heart_rate=186):
    """
    Process the decoded .FIT file content and generate DataFrame and plots.
    """
    # Read the .FIT file
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

    # Update the 'zone' column based on the 'power' column
    # Define thresholds and zones
    power_thresholds = np.array([0.55, 0.75, 0.9, 1.05, 1.2]) * FTP
    power_zones = np.array(['Zone 1 ', 'Zone 2 ', 'Zone 3 ', 'Zone 4 ', 'Zone 5 ', 'Zone 6 '])

    # Use NumPy digitize for efficient zone assignment
    df['zone'] = power_zones[np.digitize(df['power'], power_thresholds)]
    # df['zone'] = df['power'].apply(assign_zone)

    # Power Zone Data
    power_zones = ['Zone 1 ', 'Zone 2 ', 'Zone 3 ', 'Zone 4 ', 'Zone 5 ', 'Zone 6 ']
    zone_counts = df['zone'].value_counts().sort_index() / 60
    zone_counts = zone_counts.reindex(power_zones, fill_value=0)

    # Bar Chart for Power Zones
    fig = generate_bar_chart(zone_counts, power_zones, "Time Spent in Each Power Zone", "Minutes")

    # Heart Rate Zones
    # Define the thresholds and zones
    max_heart_rate = 186  # Replace with your value
    heart_thresholds = np.array([0.5, 0.65, 0.8, 0.85, 0.92]) * max_heart_rate
    HR_zones = np.array(['Resting ', 'Zone 1 ', 'Zone 2 ', 'Zone 3 ', 'Zone 4 ', 'Zone 5 '])

    # Use NumPy digitize to assign zones
    df['HR_zone'] = HR_zones[np.digitize(df['heart_rate'], heart_thresholds)]
    #HR_zones_col = df['heart_rate'].dropna().apply(assign_heart_zone)
    HR_zone_counts = df['HR_zone'].value_counts().sort_index() / 60
    HR_zone_counts = HR_zone_counts.reindex(HR_zones,fill_value=0)

    fig_HR = generate_bar_chart(HR_zone_counts[1:], HR_zones[1:], "Time Spent in Each Heart Rate Zone", "Minutes")

    # Cadence Distribution
    fig_cadence = go.Figure(
        data=[go.Histogram(x=df.cadence, histnorm='probability', marker_color='rgb(250,184,29)')],
        layout=dict(
            title={"text": "Cadence Distribution", "y": 0.9, "x": 0.5, "xanchor": "center"},
            titlefont=dict(size=20, family="Roboto, monospace"),
            font=dict(size=16, family="Roboto, monospace"),
            barmode='stack',
            yaxis=dict(title='Frequency', showticklabels=False),
            template='plotly_dark',
            barcornerradius=15,
        ),
    )
    fig_cadence.update_xaxes(range=[30, 150])

    # Power, Heart Rate, and Cadence Over Time
    fig_all = generate_combined_chart(df,power_thresholds)

    return fig, fig_HR, fig_cadence, fig_all

def generate_bar_chart(zone_counts, zones, title, xaxis_label):
    """
    Generate a bar chart for given zone counts.
    """
    custom_colors = ["gray", "blue", "green", 'yellow', 'orange', 'red']
    position_text_inorout = ['inside'] * len(zone_counts)
    for i in range(len(zone_counts)):
        if zone_counts.iloc[i] < (max(zone_counts) / 8):
            position_text_inorout[i] = 'outside'
    
    fig = go.Figure(
        data=[
            go.Bar(
                y=zones,
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
            title={"text": title, "y": 0.9, "x": 0.5, "xanchor": "center"},
            titlefont=dict(size=20, family="Roboto, monospace"),
            font=dict(size=16, family="Roboto, monospace"),
            barmode='stack',
            xaxis=dict(title=xaxis_label),
            template='plotly_dark',
            barcornerradius=15,
        ),
    )
    fig.update_yaxes(autorange="reversed")
    return fig

def generate_combined_chart(df,power_thresholds):
    """
    Generate a combined chart for power, heart rate, and cadence over time.
    """
    color_mapping = np.array(['gray', 'blue', 'green', 'yellow', 'orange', 'red']) # For combined plot

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.timestamp, y=df.power,
                        fill='tozeroy',
                        fillgradient=dict(
                            type="horizontal",
                            colorscale=list(color_mapping[np.digitize(df['power'], power_thresholds)]),
                        ),
                        mode='lines',
                        name='Power'))
    fig.add_trace(go.Scatter(x=df.timestamp, y=df.heart_rate,
                        mode='lines',
                        name='Heart Rate'))
    fig.add_trace(go.Scatter(x=df.timestamp, y=df.cadence,
                        mode='lines', name='Cadence'))
    fig.update_layout(title={
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
    return fig