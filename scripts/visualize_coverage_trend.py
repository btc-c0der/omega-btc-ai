#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Trend Visualizer
----------------------------------------------

This script generates visualizations for coverage trends using plotly.
"""

import os
import json
import logging
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_trend_visualizer')

def load_coverage_history():
    """Load coverage history from JSON file."""
    try:
        with open('coverage_history.json', 'r') as f:
            data = json.load(f)
            return data.get('history', {})
    except FileNotFoundError:
        logger.error('Coverage history file not found')
        return None
    except json.JSONDecodeError:
        logger.error('Invalid JSON in coverage history file')
        return None

def prepare_trend_data(history):
    """Prepare data for trend visualization."""
    entries = history.get('entries', [])
    
    dates = []
    coverage_values = []
    harmony_values = []
    balance_values = []
    resonance_values = []
    
    for entry in entries:
        dates.append(datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00')))
        coverage_values.append(entry['coverage'])
        divine_metrics = entry.get('divine_metrics', {})
        harmony_values.append(divine_metrics.get('harmony', 0) * 100)
        balance_values.append(divine_metrics.get('balance', 0) * 100)
        resonance_values.append(divine_metrics.get('resonance', 0) * 100)
    
    return {
        'dates': dates,
        'coverage': coverage_values,
        'harmony': harmony_values,
        'balance': balance_values,
        'resonance': resonance_values
    }

def create_trend_visualization(data):
    """Create trend visualization using plotly."""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Coverage Trend', 'Divine Metrics Trend'),
        vertical_spacing=0.15
    )
    
    # Coverage trend
    fig.add_trace(
        go.Scatter(
            x=data['dates'],
            y=data['coverage'],
            name='Coverage',
            line=dict(color='#4CAF50', width=3),
            mode='lines+markers'
        ),
        row=1, col=1
    )
    
    # Divine metrics trend
    fig.add_trace(
        go.Scatter(
            x=data['dates'],
            y=data['harmony'],
            name='Harmony',
            line=dict(color='#2196F3', width=2),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data['dates'],
            y=data['balance'],
            name='Balance',
            line=dict(color='#9C27B0', width=2),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data['dates'],
            y=data['resonance'],
            name='Resonance',
            line=dict(color='#FF9800', width=2),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title='AIXBT Divine Monitor Coverage Trends',
        template='plotly_dark',
        showlegend=True,
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial',
            size=12,
            color='white'
        )
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(255,255,255,0.1)',
        zeroline=False,
        range=[0, 100]
    )
    
    return fig

def save_visualization(fig, output_dir='coverage_reports'):
    """Save visualization to HTML and PNG files."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Save HTML
        html_path = os.path.join(output_dir, 'coverage_trend.html')
        fig.write_html(html_path)
        logger.info(f'Saved HTML visualization to {html_path}')
        
        # Save PNG
        png_path = os.path.join(output_dir, 'coverage_trend.png')
        fig.write_image(png_path)
        logger.info(f'Saved PNG visualization to {png_path}')
        
        return True
    except Exception as e:
        logger.error(f'Error saving visualization: {e}')
        return False

def main():
    """Main function to generate coverage trend visualization."""
    logger.info('Starting coverage trend visualization')
    
    # Load coverage history
    history = load_coverage_history()
    if history is None:
        return
    
    # Prepare data
    data = prepare_trend_data(history)
    
    # Create visualization
    fig = create_trend_visualization(data)
    
    # Save visualization
    if save_visualization(fig):
        logger.info('Coverage trend visualization completed')
    else:
        logger.error('Failed to save visualization')

if __name__ == '__main__':
    main() 