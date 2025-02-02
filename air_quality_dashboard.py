import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output
import numpy as np
from datetime import datetime, timedelta
import os
import traceback

def load_and_process_sensor_data(file_path):
    """
    Load and process sensor data from CSV file with specific handling for the data format
    """
    print("\n=== Loading Air Quality Data ===")
    
    try:
        # Read CSV with specific parameters for the format
        df = pd.read_csv(file_path, 
                        dtype={'sensor_id': str, 'location': str},  # Ensure these are treated as strings
                        )
        
        print(f"Initial data load: {len(df)} rows")
        
        # Clean the data
        # Remove any single quotes from string columns
        string_columns = ['sensor_id', 'sensor_type', 'location', 'value_type']
        for col in string_columns:
            df[col] = df[col].str.strip("'")
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Convert air_quality_index to numeric
        df['air_quality_index'] = pd.to_numeric(df['air_quality_index'].str.strip("'"), errors='coerce')
        
        # Filter for only air quality measurements
        df = df[df['value_type'].isin(['P0', 'P1', 'P2'])]
        
        # Calculate average air quality index for each timestamp and location
        df_grouped = df.groupby(['timestamp', 'location', 'sensor_id'])['air_quality_index'].mean().reset_index()
        
        print(f"\nProcessed data summary:")
        print(f"Number of records: {len(df_grouped)}")
        print(f"Date range: {df_grouped['timestamp'].min()} to {df_grouped['timestamp'].max()}")
        print(f"Locations: {', '.join(df_grouped['location'].unique())}")
        
        return df_grouped
        
    except Exception as e:
        print(f"\nError processing data: {str(e)}")
        return create_sample_data()

def create_sample_data():
    """Create sample data if processing fails"""
    print("\nCreating sample data...")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    locations = ['Location A', 'Location B', 'Location C']
    
    all_dates = []
    all_locations = []
    all_aqi = []
    all_sensors = []
    
    for loc in locations:
        for date in dates:
            all_dates.append(date)
            all_locations.append(loc)
            all_aqi.append(np.random.randint(0, 200))
            all_sensors.append(f"SENSOR_{np.random.randint(1, 5)}")
    
    df = pd.DataFrame({
        'timestamp': all_dates,
        'location': all_locations,
        'air_quality_index': all_aqi,
        'sensor_id': all_sensors
    })
    
    return df

def load_research_findings(findings_file, correlations_file):
    """Load and process research findings and health correlations data"""
    findings_df = pd.read_csv(findings_file)
    correlations_df = pd.read_csv(correlations_file)
    
    # Process findings data
    findings_by_category = findings_df.groupby('category')['detail'].count().reset_index()
    
    # Process correlations data
    correlations_df['value'] = pd.to_numeric(correlations_df['value'], errors='coerce')
    
    return findings_df, correlations_df, findings_by_category

# Initialize the Dash app
app = Dash(__name__)

# Load the data
sensor_data = load_and_process_sensor_data('sensor_reading.csv')

# Create the layout
app.layout = html.Div([
    # Add CSS styles using a style dictionary
    html.Div([
        html.H1("Air Quality Dashboard", style={'textAlign': 'center'}),
        
        dcc.Tabs(
            id='dashboard-tabs',
            children=[
                dcc.Tab(label='Air Quality Monitoring', children=[
                    # Filters section
                    html.Div([
                        html.Div([
                            html.Label('Select Location'),
                            dcc.Dropdown(
                                id='location-dropdown',
                                options=[{'label': f'Location {loc}', 'value': loc} 
                                        for loc in sensor_data['location'].unique()],
                                value=[sensor_data['location'].unique()[0]],
                                multi=True
                            )
                        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
                        
                        html.Div([
                            html.Label('Date Range'),
                            dcc.DatePickerRange(
                                id='date-range',
                                start_date=sensor_data['timestamp'].min(),
                                end_date=sensor_data['timestamp'].max(),
                                display_format='YYYY-MM-DD'
                            )
                        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'})
                    ]),
                    
                    # Graphs section
                    html.Div([
                        dcc.Graph(id='air-quality-graph'),
                        dcc.Graph(id='trends-graph')
                    ]),
                    
                    # Statistics section
                    html.Div(id='statistics-section', style={'padding': '20px'})
                ]),
                
                dcc.Tab(label='Research Findings', children=[
                    html.Div([
                        html.H2("Research Findings Summary", style={'textAlign': 'center'}),
                        
                        # Findings Distribution Chart
                        html.Div([
                            dcc.Graph(id='findings-distribution'),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        # Health Correlations Chart
                        html.Div([
                            dcc.Graph(id='health-correlations'),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        # Key Findings Section
                        html.Div([
                            html.H3("Key Findings"),
                            html.Div(id='key-findings-content'),
                        ], style={'padding': '20px'}),
                        
                        # Recommendations Section
                        html.Div([
                            html.H3("Recommendations"),
                            html.Div(id='recommendations-content'),
                        ], style={'padding': '20px'})
                    ], style={
                        'margin': '20px 0',
                        'padding': '20px',
                        'borderRadius': '5px',
                        'backgroundColor': 'white',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                    })
                ])
            ],
            style={
                'margin': '20px 0',
                'fontFamily': 'Arial, sans-serif'
            }
        )
    ], style={
        # Global styles
        'fontFamily': 'Arial, sans-serif',
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px'
    })
])

# Define component-specific styles as dictionaries
section_style = {
    'margin': '20px 0',
    'padding': '20px',
    'borderRadius': '5px',
    'backgroundColor': 'white',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

heading_style = {
    'color': '#2c3e50',
    'marginBottom': '15px'
}

list_style = {
    'listStyleType': 'none',
    'paddingLeft': '0'
}

list_item_style = {
    'margin': '8px 0',
    'paddingLeft': '20px',
    'position': 'relative',
    'borderLeft': '3px solid #3498db'
}

@app.callback(
    [Output('air-quality-graph', 'figure'),
     Output('trends-graph', 'figure'),
     Output('statistics-section', 'children')],
    [Input('location-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_figures(selected_locations, start_date, end_date):
    filtered_df = sensor_data.copy()
    
    if selected_locations:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_locations)]
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['timestamp'] >= start_date) &
            (filtered_df['timestamp'] <= end_date)
        ]
    
    # Create air quality graph
    air_quality_fig = px.line(
        filtered_df,
        x='timestamp',
        y='air_quality_index',
        color='location',
        title='Air Quality Index Over Time'
    )
    
    # Create daily trends graph
    filtered_df['date'] = filtered_df['timestamp'].dt.date
    daily_avg = filtered_df.groupby(['location', 'date'])['air_quality_index'].mean().reset_index()
    trends_fig = px.bar(
        daily_avg,
        x='date',
        y='air_quality_index',
        color='location',
        title='Daily Average Air Quality Index'
    )
    
    # Calculate statistics
    stats = []
    for loc in selected_locations:
        loc_data = filtered_df[filtered_df['location'] == loc]
        stats.append(html.Div([
            html.H3(f"Statistics for Location {loc}"),
            html.P(f"Average AQI: {loc_data['air_quality_index'].mean():.2f}"),
            html.P(f"Maximum AQI: {loc_data['air_quality_index'].max():.2f}"),
            html.P(f"Minimum AQI: {loc_data['air_quality_index'].min():.2f}"),
            html.P(f"Number of readings: {len(loc_data)}")
        ]))
    
    return air_quality_fig, trends_fig, html.Div(stats)

@app.callback(
    [Output('findings-distribution', 'figure'),
     Output('health-correlations', 'figure'),
     Output('key-findings-content', 'children')],
    [Input('dashboard-tabs', 'value')]
)
def update_research_findings(tab):
    print("\n=== Updating Research Findings ===")
    try:
        # Load and process data
        correlations_df = pd.read_csv('health_correlations.csv')
        print(f"Loaded correlations data shape: {correlations_df.shape}")
        
        correlations_df['value'] = pd.to_numeric(correlations_df['value'], errors='coerce')
        print(f"Number of valid numeric values: {correlations_df['value'].notna().sum()}")
        
        # Create health metrics visualization
        valid_data = correlations_df[correlations_df['value'].notna()]
        print(f"Data for health metrics visualization: {len(valid_data)} rows")
        
        health_metrics = px.bar(
            valid_data,
            x='parameter',
            y='value',
            color='parameter',
            title='Health Impact Metrics',
            labels={'value': 'Measured Value', 'parameter': 'Health Parameter'},
            template='plotly_white'
        )
        
        # Create trends visualization
        trends_data = correlations_df[correlations_df['parameter'].isin(['PM2.5 Levels', 'Health Implications'])]
        print(f"Data for trends visualization: {len(trends_data)} rows")
        
        trends_viz = px.scatter(
            trends_data[trends_data['value'].notna()],  # Only use rows with valid values
            x='parameter',
            y='value',
            size=[20] * len(trends_data[trends_data['value'].notna()]),  # Match size array to filtered data
            title='Health Correlations Overview'
        )
        
        # Generate key findings content
        key_findings = create_health_correlations_page()
        
        return health_metrics, trends_viz, key_findings
        
    except Exception as e:
        print(f"\nError in update_research_findings: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return px.bar(), px.bar(), html.Div("Error loading research findings")

def create_health_correlations_page():
    print("\n=== Creating Health Correlations Page ===")
    
    try:
        # Log PM2.5 data processing
        pm25_data = correlations_df[correlations_df['parameter'] == 'PM2.5 Levels']
        print(f"PM2.5 data shape: {pm25_data.shape}")
        print(f"PM2.5 columns: {pm25_data.columns.tolist()}")
        
        # Log health implications data processing
        health_data = correlations_df[
            (correlations_df['parameter'] == 'Health Implications') & 
            (correlations_df['value'].notna())
        ]
        print(f"Health implications data shape: {health_data.shape}")
        print(f"Number of valid values: {len(health_data)}")
        
        return html.Div([
            html.H2("Health Impact Analysis", style={'textAlign': 'center'}),
            
            # PM2.5 Levels Section
            html.Div([
                html.H3("PM2.5 Concentration Measurements"),
                dcc.Graph(
                    figure=px.bar(
                        data_frame=pm25_data,
                        x='detail',
                        y='value',
                        title='PM2.5 Concentration Measurements',
                        labels={'value': 'Concentration (μg/m³)', 'detail': 'Measurement Type'}
                    )
                )
            ], className='section'),
            
            # Health Risk Metrics
            html.Div([
                html.H3("Health Risk Metrics"),
                dcc.Graph(
                    figure=px.scatter(
                        data_frame=health_data,
                        x='detail',
                        y='value',
                        title='Health Risk Indicators',
                        labels={'value': 'Risk Ratio/Odds Ratio', 'detail': 'Health Outcome'},
                        size=[20] * len(health_data),  # Fix: Match size array length to filtered data
                    )
                )
            ], className='section'),
            
            # Key Findings Grid
            html.Div([
                html.H3("Key Findings"),
                html.Div([
                    create_finding_card("Pollution Sources", [
                        "Traffic-related emissions",
                        "Indoor air pollution (vapors, dusts, smoke)",
                        "Waste management practices"
                    ]),
                    create_finding_card("Vulnerable Groups", [
                        "Children with developing lungs",
                        "Preterm/low birth weight infants",
                        "Residents with limited healthcare access"
                    ]),
                    create_finding_card("Study Limitations", [
                        "Cross-sectional design",
                        "Limited longitudinal data",
                        "Indirect waste pollution inference"
                    ])
                ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '20px'})
            ], className='section')
        ])
    except Exception as e:
        print(f"\nError in create_health_correlations_page: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return html.Div("Error loading health correlations page")

def create_finding_card(title, points):
    return html.Div([
        html.H4(title, style=heading_style),
        html.Ul([
            html.Li(point, style=list_item_style) for point in points
        ], style=list_style)
    ], style=section_style)

if __name__ == '__main__':
    print("\n=== Air Quality Dashboard Initialization ===")
    # Load sensor data
    sensor_data = load_and_process_sensor_data('sensor_reading.csv')
    # Load research findings
    findings_df, correlations_df, findings_by_category = load_research_findings(
        'research_findings.csv', 'health_correlations.csv'
    )
    print("\nServer starting at http://127.0.0.1:8050/")
    print("\nPress Ctrl+C to quit")
    app.run_server(debug=True)