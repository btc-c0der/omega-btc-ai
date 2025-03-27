#!/usr/bin/env python3
"""
Market Maker Trap Event Visualizer

This script creates detailed visualizations of market maker trap events 
from InfluxDB data to help identify patterns and correlations.
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dotenv import load_dotenv
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient

# Load environment variables
load_dotenv()

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "w4JzUNsut5GjPBB72ts_U3D5r6ojYkWGUTTHZdMOjVXmJqX8Wnuyp3EYLRzi9H5BLwM9hAEltSFdEF-ZDwSjOg==")
ORG = os.getenv("INFLUX_ORG", "omega")
BUCKET = os.getenv("INFLUX_BUCKET", "mm_traps")

# Time range for data analysis
TIME_RANGE = "-30d"  # Last 30 days

def connect_to_influxdb():
    """Connect to InfluxDB and return client."""
    try:
        client = InfluxDBClient(
            url=INFLUX_URL,
            token=INFLUX_TOKEN,
            org=ORG
        )
        health = client.health()
        if health.status == "pass":
            print("✅ Connected to InfluxDB")
            return client
        else:
            print(f"❌ InfluxDB health check failed: {health.message}")
            return None
    except Exception as e:
        print(f"❌ Error connecting to InfluxDB: {e}")
        return None

def query_mm_trap_events(client):
    """Query market maker trap events from InfluxDB."""
    query_api = client.query_api()
    
    query = f'''
    from(bucket: "{BUCKET}")
        |> range(start: {TIME_RANGE})
        |> filter(fn: (r) => r._measurement == "mm_traps" or r._measurement == "trap_events")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    try:
        result = query_api.query_data_frame(query)
        # Handle different return types (single dataframe or list of dataframes)
        if isinstance(result, list) and result:
            print(f"Received {len(result)} dataframes from InfluxDB query")
            result = pd.concat(result)
        
        if not result.empty:
            print(f"\n📊 Found {len(result)} market maker trap events")
            print(f"Trap types: {result['type'].value_counts().to_dict()}")
            
            if 'confidence' in result.columns:
                print(f"Average confidence: {result['confidence'].mean():.2f}")
                print(f"High confidence events (>0.7): {len(result[result['confidence'] > 0.7])}")
                
            # Ensure time column is datetime
            result['_time'] = pd.to_datetime(result['_time'])
            
            # Sort by time for better analysis
            result = result.sort_values('_time')
            
            return result
        else:
            print("No market maker trap events found")
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error querying trap events: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def visualize_trap_distribution(trap_data):
    """Create visualization of trap events distribution over time."""
    if trap_data.empty:
        return
    
    # Create daily counts of trap events by type
    trap_data['date'] = trap_data['_time'].dt.date
    daily_counts = trap_data.groupby(['date', 'type']).size().reset_index(name='count')
    
    # Plot daily trap event counts
    fig = px.bar(
        daily_counts, 
        x='date', 
        y='count', 
        color='type',
        title='Daily Market Maker Trap Events by Type',
        labels={'date': 'Date', 'count': 'Number of Events', 'type': 'Trap Type'}
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Events',
        legend_title='Trap Type',
        height=600,
        barmode='stack'
    )
    
    # Save figure
    fig.write_html('trap_distribution.html')
    print("📊 Trap distribution visualization saved to trap_distribution.html")

def visualize_price_with_traps(trap_data):
    """Create visualization of BTC price with trap events highlighted."""
    if trap_data.empty or 'btc_price' not in trap_data.columns:
        print("Cannot create price visualization: missing btc_price column")
        return
    
    # Create figure with two subplots: price and confidence
    fig = make_subplots(
        rows=2, 
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('BTC Price with Trap Events', 'Trap Confidence')
    )
    
    # Add price line
    fig.add_trace(
        go.Scatter(
            x=trap_data['_time'],
            y=trap_data['btc_price'],
            mode='lines',
            name='BTC Price',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )
    
    # Add trap events as markers, colored by type
    if 'type' in trap_data.columns:
        for trap_type in trap_data['type'].unique():
            trap_subset = trap_data[trap_data['type'] == trap_type]
            
            # Skip types with very few events for clarity
            if len(trap_subset) < 5:
                continue
                
            fig.add_trace(
                go.Scatter(
                    x=trap_subset['_time'],
                    y=trap_subset['btc_price'],
                    mode='markers',
                    name=trap_type,
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
    
    # Add confidence scatter plot
    if 'confidence' in trap_data.columns:
        for trap_type in trap_data['type'].unique():
            trap_subset = trap_data[trap_data['type'] == trap_type]
            
            # Skip types with very few events for clarity
            if len(trap_subset) < 5:
                continue
                
            fig.add_trace(
                go.Scatter(
                    x=trap_subset['_time'],
                    y=trap_subset['confidence'],
                    mode='markers',
                    name=f"{trap_type} Confidence",
                    marker=dict(size=6, opacity=0.7)
                ),
                row=2, col=1
            )
    
    # Improve layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='BTC Price (USDT)',
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Update y-axis titles
    fig.update_yaxes(title_text="BTC Price (USDT)", row=1, col=1)
    fig.update_yaxes(title_text="Confidence", row=2, col=1)
    
    # Save figure
    fig.write_html('price_with_traps.html')
    print("📈 Price with traps visualization saved to price_with_traps.html")

def visualize_confidence_heatmap(trap_data):
    """Create a heatmap of trap confidence by hour of day and day of week."""
    if trap_data.empty or 'confidence' not in trap_data.columns:
        return
    
    # Extract time components
    trap_data['hour'] = trap_data['_time'].dt.hour
    trap_data['day_of_week'] = trap_data['_time'].dt.day_name()
    
    # Define day order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create pivot table for heatmap
    heatmap_data = trap_data.pivot_table(
        values='confidence',
        index='day_of_week',
        columns='hour',
        aggfunc='mean'
    ).reindex(days_order)
    
    # Create heatmap
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Avg Confidence"),
        x=list(range(24)),
        y=days_order,
        color_continuous_scale="Viridis",
        title="Trap Confidence by Hour and Day"
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
        height=600,
        width=900
    )
    
    # Save figure
    fig.write_html('confidence_heatmap.html')
    print("🔥 Confidence heatmap saved to confidence_heatmap.html")

def visualize_price_change_histogram(trap_data):
    """Create histogram of price changes during trap events."""
    if trap_data.empty or 'price_change' not in trap_data.columns:
        return
    
    # Create histogram for each trap type
    fig = px.histogram(
        trap_data,
        x='price_change',
        color='type',
        barmode='overlay',
        opacity=0.7,
        nbins=50,
        title='Distribution of Price Changes by Trap Type',
        labels={'price_change': 'Price Change (%)', 'count': 'Number of Events', 'type': 'Trap Type'}
    )
    
    # Add vertical line at zero
    fig.add_vline(x=0, line_dash="dash", line_color="black")
    
    # Improve layout
    fig.update_layout(
        xaxis_title='Price Change (%)',
        yaxis_title='Number of Events',
        height=600
    )
    
    # Save figure
    fig.write_html('price_change_histogram.html')
    print("📊 Price change histogram saved to price_change_histogram.html")

def main():
    """Main function to visualize trap events."""
    client = connect_to_influxdb()
    if not client:
        return
    
    try:
        # Query trap events data
        trap_data = query_mm_trap_events(client)
        
        if not trap_data.empty:
            # Create visualizations
            visualize_trap_distribution(trap_data)
            visualize_price_with_traps(trap_data)
            visualize_confidence_heatmap(trap_data)
            visualize_price_change_histogram(trap_data)
        
        print("\n✅ Visualization complete!")
    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close client
        client.close()

if __name__ == "__main__":
    main() 