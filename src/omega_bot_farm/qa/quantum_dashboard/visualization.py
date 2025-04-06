#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Visualizations
--------------------------------------

This module provides visualization functions for the Quantum 5D QA Dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import datetime
import math
from typing import Dict, List, Any, Tuple, Optional

# Import configuration
from .config import DASHBOARD_CONFIG, quantum_theme


def _safe_rgba_from_hex(hex_color: str, alpha: float = 0.7) -> str:
    """Convert hex color to RGBA with error handling.
    
    Args:
        hex_color: Hex color code (e.g., "#FF5733")
        alpha: Opacity value between 0.0 and 1.0
        
    Returns:
        RGBA color string (e.g., "rgba(255, 87, 51, 0.7)")
    """
    try:
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Parse RGB components
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Return RGBA string
        return f"rgba({r}, {g}, {b}, {alpha})"
    except Exception:
        # Return a default color if parsing fails
        return f"rgba(128, 128, 128, {alpha})"


def create_hyperspatial_trend_graph(metrics_history: List[Dict[str, Any]]) -> go.Figure:
    """Create a hyperspatial trend visualization using a radar chart.
    
    Args:
        metrics_history: List of metrics dictionaries
        
    Returns:
        Plotly figure object
    """
    # Check if we have metrics data
    if not metrics_history:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No metrics data available",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color=quantum_theme["text"])
        )
        fig.update_layout(
            paper_bgcolor=quantum_theme["background"],
            plot_bgcolor=quantum_theme["background"],
            font=dict(color=quantum_theme["text"])
        )
        return fig
    
    # Extract the latest metrics
    latest_metrics = metrics_history[-1]
    
    # Extract hyperspatial trend data
    trend_data = latest_metrics.get("hyperspatial_trend", [0, 0, 0, 0, 0])
    
    # Create categories for radar chart
    categories = ["Time", "Quality", "Coverage", "Performance", "Security"]
    
    # Create radar chart
    fig = go.Figure()
    
    # Add trace for the current 5D state
    fig.add_trace(go.Scatterpolar(
        r=trend_data,
        theta=categories,
        fill='toself',
        fillcolor=_safe_rgba_from_hex(quantum_theme["accent"], 0.5),
        line=dict(color=quantum_theme["accent"]),
        name='Current State'
    ))
    
    # If we have historical data (at least 5 data points), add a trace for the average
    if len(metrics_history) >= 5:
        # Get the last 5 data points
        recent_metrics = metrics_history[-5:]
        
        # Extract hyperspatial trend data and calculate averages
        avg_trend = [0, 0, 0, 0, 0]
        for metrics in recent_metrics:
            trend = metrics.get("hyperspatial_trend", [0, 0, 0, 0, 0])
            for i in range(5):
                avg_trend[i] += trend[i] / len(recent_metrics)
        
        # Add trace for the average state
        fig.add_trace(go.Scatterpolar(
            r=avg_trend,
            theta=categories,
            fill='toself',
            fillcolor=_safe_rgba_from_hex(quantum_theme["success"], 0.3),
            line=dict(color=quantum_theme["success"], dash='dot'),
            name='Average State'
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                ticks='',
                gridcolor=_safe_rgba_from_hex(quantum_theme["text"], 0.1)
            ),
            angularaxis=dict(
                gridcolor=_safe_rgba_from_hex(quantum_theme["text"], 0.1)
            ),
            bgcolor=_safe_rgba_from_hex(quantum_theme["background"], 0.2)
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            font=dict(color=quantum_theme["text"])
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor=quantum_theme["background"],
        plot_bgcolor=quantum_theme["background"],
        font=dict(color=quantum_theme["text"])
    )
    
    return fig


def create_dimension_graph(
    dimension: str, metrics_history: List[Dict[str, Any]], window: int = 20
) -> go.Figure:
    """Create a time series visualization for a specific 5D dimension.
    
    Args:
        dimension: Dimension name (time, quality, coverage, performance, security)
        metrics_history: List of metrics dictionaries
        window: Number of data points to display
        
    Returns:
        Plotly figure object
    """
    # Check if we have metrics data
    if not metrics_history:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {dimension} metrics data available",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color=quantum_theme["text"])
        )
        fig.update_layout(
            paper_bgcolor=quantum_theme["background"],
            plot_bgcolor=quantum_theme["background"],
            font=dict(color=quantum_theme["text"])
        )
        return fig
    
    # Map dimension name to position name and color
    dimension_mapping = {
        "time": {
            "position": "time_position",
            "color": quantum_theme["accent"],
            "label": "Time Position"
        },
        "quality": {
            "position": "quality_position", 
            "color": quantum_theme["success"],
            "label": "Quality Position"
        },
        "coverage": {
            "position": "coverage_position", 
            "color": quantum_theme["info"],
            "label": "Coverage Position"
        },
        "performance": {
            "position": "performance_position", 
            "color": quantum_theme["warning"],
            "label": "Performance Position"
        },
        "security": {
            "position": "security_position", 
            "color": quantum_theme["error"],
            "label": "Security Position"
        }
    }
    
    # Get the position key and color for this dimension
    position_key = dimension_mapping.get(dimension, {}).get("position", f"{dimension}_position")
    color = dimension_mapping.get(dimension, {}).get("color", quantum_theme["accent"])
    label = dimension_mapping.get(dimension, {}).get("label", f"{dimension.capitalize()} Position")
    
    # Limit the number of data points to display
    display_metrics = metrics_history[-window:] if len(metrics_history) > window else metrics_history
    
    # Extract timestamps and values
    timestamps = []
    values = []
    
    for metrics in display_metrics:
        # Get timestamp
        ts = metrics.get("timestamp", "")
        if ts:
            # Convert ISO timestamp to datetime
            try:
                dt = datetime.datetime.fromisoformat(ts)
                timestamps.append(dt)
            except ValueError:
                timestamps.append(datetime.datetime.now())
        else:
            timestamps.append(datetime.datetime.now())
        
        # Get position value
        value = metrics.get(position_key, 0)
        values.append(value)
    
    # Create figure
    fig = go.Figure()
    
    # Add line for the dimension values
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=values,
        mode='lines',
        name=label,
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=_safe_rgba_from_hex(color, 0.2)
    ))
    
    # Add markers for the current value
    if values:
        fig.add_trace(go.Scatter(
            x=[timestamps[-1]],
            y=[values[-1]],
            mode='markers',
            marker=dict(
                color=color,
                size=12,
                line=dict(
                    color=quantum_theme["background"],
                    width=2
                )
            ),
            showlegend=False
        ))
    
    # Add threshold lines
    fig.add_shape(
        type="line",
        x0=min(timestamps),
        y0=DASHBOARD_CONFIG["threshold_warning"],
        x1=max(timestamps),
        y1=DASHBOARD_CONFIG["threshold_warning"],
        line=dict(
            color=quantum_theme["warning"],
            width=1,
            dash="dash",
        )
    )
    
    fig.add_shape(
        type="line",
        x0=min(timestamps),
        y0=DASHBOARD_CONFIG["threshold_critical"],
        x1=max(timestamps),
        y1=DASHBOARD_CONFIG["threshold_critical"],
        line=dict(
            color=quantum_theme["error"],
            width=1,
            dash="dash",
        )
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f"{label} Over Time",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(color=quantum_theme["text"])
        },
        xaxis=dict(
            title="Time",
            gridcolor=_safe_rgba_from_hex(quantum_theme["text"], 0.1),
            showgrid=True,
            zeroline=False,
            color=quantum_theme["text"]
        ),
        yaxis=dict(
            title=label,
            range=[0, 105],  # Leave space at top for annotations
            gridcolor=_safe_rgba_from_hex(quantum_theme["text"], 0.1),
            showgrid=True,
            zeroline=False,
            color=quantum_theme["text"]
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor=quantum_theme["background"],
        plot_bgcolor=quantum_theme["background"],
        font=dict(color=quantum_theme["text"])
    )
    
    # Add annotations for the current value
    if values:
        fig.add_annotation(
            x=timestamps[-1],
            y=values[-1],
            text=f"{values[-1]:.1f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=color,
            ax=20,
            ay=-30,
            bgcolor=quantum_theme["background"],
            font=dict(color=color)
        )
    
    return fig


def create_stability_gauge(metrics: Dict[str, Any]) -> go.Figure:
    """Create a gauge visualization for dimensional stability.
    
    Args:
        metrics: Current metrics dictionary
        
    Returns:
        Plotly figure object
    """
    # Get stability value
    stability = metrics.get("dimensional_stability", 100)
    
    # Determine color based on stability value
    if stability >= 80:
        color = quantum_theme["success"]
    elif stability >= 50:
        color = quantum_theme["warning"]
    else:
        color = quantum_theme["error"]
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stability,
        title={"text": "Dimensional Stability", "font": {"color": quantum_theme["text"]}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": quantum_theme["text"],
                "tickfont": {"color": quantum_theme["text"]}
            },
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 2,
            "bordercolor": quantum_theme["text"],
            "steps": [
                {"range": [0, 50], "color": _safe_rgba_from_hex(quantum_theme["error"], 0.3)},
                {"range": [50, 80], "color": _safe_rgba_from_hex(quantum_theme["warning"], 0.3)},
                {"range": [80, 100], "color": _safe_rgba_from_hex(quantum_theme["success"], 0.3)}
            ]
        },
        number={"font": {"color": quantum_theme["text"]}}
    ))
    
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor=quantum_theme["background"],
        font=dict(color=quantum_theme["text"])
    )
    
    return fig


def create_coherence_gauge(metrics: Dict[str, Any]) -> go.Figure:
    """Create a gauge visualization for quantum coherence.
    
    Args:
        metrics: Current metrics dictionary
        
    Returns:
        Plotly figure object
    """
    # Get coherence value
    coherence = metrics.get("quantum_coherence", 100)
    
    # Determine color based on coherence value
    if coherence >= 80:
        color = quantum_theme["success"]
    elif coherence >= 50:
        color = quantum_theme["warning"]
    else:
        color = quantum_theme["error"]
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=coherence,
        title={"text": "Quantum Coherence", "font": {"color": quantum_theme["text"]}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": quantum_theme["text"],
                "tickfont": {"color": quantum_theme["text"]}
            },
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 2,
            "bordercolor": quantum_theme["text"],
            "steps": [
                {"range": [0, 50], "color": _safe_rgba_from_hex(quantum_theme["error"], 0.3)},
                {"range": [50, 80], "color": _safe_rgba_from_hex(quantum_theme["warning"], 0.3)},
                {"range": [80, 100], "color": _safe_rgba_from_hex(quantum_theme["success"], 0.3)}
            ]
        },
        number={"font": {"color": quantum_theme["text"]}}
    ))
    
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor=quantum_theme["background"],
        font=dict(color=quantum_theme["text"])
    )
    
    return fig


def create_risk_indicator(metrics: Dict[str, Any]) -> go.Figure:
    """Create a risk indicator visualization.
    
    Args:
        metrics: Current metrics dictionary
        
    Returns:
        Plotly figure object
    """
    # Get risk value
    risk = metrics.get("dimensional_collapse_risk", 0)
    
    # Determine color and text based on risk value
    if risk <= 20:
        color = quantum_theme["success"]
        status = "LOW"
    elif risk <= 50:
        color = quantum_theme["warning"]
        status = "MEDIUM"
    else:
        color = quantum_theme["error"]
        status = "HIGH"
    
    # Create indicator
    fig = go.Figure(go.Indicator(
        mode="number+delta+gauge",
        value=risk,
        title={"text": f"Collapse Risk: {status}", "font": {"color": quantum_theme["text"]}},
        delta={"reference": 50, "increasing": {"color": quantum_theme["error"]}, "decreasing": {"color": quantum_theme["success"]}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": quantum_theme["text"],
                "tickfont": {"color": quantum_theme["text"]}
            },
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 2,
            "bordercolor": quantum_theme["text"],
            "steps": [
                {"range": [0, 20], "color": _safe_rgba_from_hex(quantum_theme["success"], 0.3)},
                {"range": [20, 50], "color": _safe_rgba_from_hex(quantum_theme["warning"], 0.3)},
                {"range": [50, 100], "color": _safe_rgba_from_hex(quantum_theme["error"], 0.3)}
            ]
        },
        number={"font": {"color": quantum_theme["text"]}}
    ))
    
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor=quantum_theme["background"],
        font=dict(color=quantum_theme["text"])
    )
    
    return fig


def create_entanglement_visualization(metrics_data):
    """Create an entanglement visualization."""
    # Create a basic empty figure
    fig = go.Figure()
    
    # Add default polar chart
    if metrics_data is None:
        return fig
    
    # Get entanglement factor
    entanglement = metrics_data.get('entanglement_factor')
    if entanglement is None:
        entanglement = 0.5  # Default value if missing
    
    # Create a polar chart to show entanglement between dimensions
    theta = np.linspace(0, 2*np.pi, 100)
    radius = 1 + entanglement * np.sin(theta * 8)
    
    # Convert to cartesian coordinates
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    
    # Add the entanglement plot
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.3)',
        line=dict(color='rgba(0, 255, 0, 0.8)', width=2),
        name='Entanglement Field'
    ))
    
    # Add dimension points
    dimensions = ['Quality', 'Coverage', 'Performance', 'Security', 'Time']
    
    # Position the points in a circle
    dim_theta = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    dim_radius = [
        metrics_data.get('quality_position', 50) / 100,
        metrics_data.get('coverage_position', 50) / 100,
        metrics_data.get('performance_position', 50) / 100,
        metrics_data.get('security_position', 50) / 100,
        0.5  # Fixed position for time
    ]
    
    # Convert to cartesian coordinates
    dim_x = [r * np.cos(t) for r, t in zip(dim_radius, dim_theta)]
    dim_y = [r * np.sin(t) for r, t in zip(dim_radius, dim_theta)]
    
    # Add the dimension points
    fig.add_trace(go.Scatter(
        x=dim_x,
        y=dim_y,
        mode='markers+text',
        marker=dict(
            size=12,
            color='rgba(255, 255, 255, 0.8)',
            line=dict(
                color='rgba(0, 255, 0, 1)',
                width=2
            )
        ),
        text=dimensions,
        textposition="top center",
        name='Dimensions'
    ))
    
    # Add lines connecting the points to show entanglement
    for i in range(len(dimensions)):
        for j in range(i+1, len(dimensions)):
            fig.add_trace(go.Scatter(
                x=[dim_x[i], dim_x[j]],
                y=[dim_y[i], dim_y[j]],
                mode='lines',
                line=dict(
                    color=f'rgba(0, 255, 0, {entanglement * 0.7})',
                    width=1
                ),
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        )
    )
    
    return fig


def create_metrics_table(metrics):
    """Create a table of metrics."""
    # Create an empty figure
    fig = go.Figure()
    
    if metrics is None:
        return fig
    
    # Safely get metric values with defaults
    def safe_format(value, default=0):
        if value is None:
            return f"{default:.2f}"
        return f"{value:.2f}"
    
    # Add a table with current metrics
    fig.add_trace(go.Table(
        header=dict(
            values=["Metric", "Value"],
            fill_color="#1e2130",
            align="left",
            font=dict(color="white", size=12)
        ),
        cells=dict(
            values=[
                ["Dimensional Stability", "Entanglement Factor", "Quantum Coherence", 
                 "Collapse Risk", "Quality Position", "Coverage Position",
                 "Performance Position", "Security Position"],
                [
                    safe_format(metrics.get('dimensional_stability')),
                    safe_format(metrics.get('entanglement_factor')),
                    safe_format(metrics.get('quantum_coherence')),
                    safe_format(metrics.get('dimensional_collapse_risk')),
                    safe_format(metrics.get('quality_position')),
                    safe_format(metrics.get('coverage_position')),
                    safe_format(metrics.get('performance_position')),
                    safe_format(metrics.get('security_position'))
                ]
            ],
            fill_color="#131722",
            align="left",
            font=dict(color="white", size=11)
        )
    ))
    
    # Update layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
    
    return fig


def create_terminal_output(lines: List[str] = None) -> str:
    """Create a styled HTML representation of terminal output.
    
    Args:
        lines: List of lines to display in the terminal
        
    Returns:
        HTML string representing terminal output
    """
    if lines is None or len(lines) == 0:
        lines = [
            "Initializing Quantum 5D QA Dashboard...",
            "Accessing 5 dimensional metrics...",
            "Calculating quantum entanglement...",
            "Ready."
        ]
    
    # Create terminal HTML
    terminal_html = f"""
    <div class="terminal-container">
        <div class="terminal-header">
            <div class="terminal-button red"></div>
            <div class="terminal-button yellow"></div>
            <div class="terminal-button green"></div>
            <span class="terminal-title">Quantum QA Terminal</span>
        </div>
        <div class="terminal-body">
            <pre class="terminal-text">
            <span class="prompt">$</span> <span class="command">quantum-dashboard --start</span>
            
            {'<br>'.join(lines)}
            <span class="prompt">$</span> <span class="cursor">█</span>
            </pre>
        </div>
    </div>
    """
    
    return terminal_html


def create_health_indicators(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create health indicator cards for different dimensions.
    
    Args:
        metrics: Current metrics dictionary
        
    Returns:
        List of dictionaries containing health indicator information
    """
    # Define the dimensions to display
    dimensions = [
        {
            "name": "Quality",
            "position_key": "quality_position",
            "icon": "✓",
            "description": "Code quality and test success rate"
        },
        {
            "name": "Coverage",
            "position_key": "coverage_position",
            "icon": "⬛",
            "description": "Test coverage across codebase"
        },
        {
            "name": "Performance",
            "position_key": "performance_position",
            "icon": "⚡",
            "description": "System performance metrics"
        },
        {
            "name": "Security",
            "position_key": "security_position",
            "icon": "🔒",
            "description": "Security assessment of systems"
        }
    ]
    
    # Create indicators
    indicators = []
    for dim in dimensions:
        # Get position value
        value = metrics.get(dim["position_key"], 0)
        
        # Determine status and color
        if value >= 80:
            status = "STABLE"
            color = quantum_theme["success"]
        elif value >= 50:
            status = "WARNING"
            color = quantum_theme["warning"]
        else:
            status = "CRITICAL"
            color = quantum_theme["error"]
        
        # Create indicator
        indicators.append({
            "name": dim["name"],
            "value": value,
            "status": status,
            "color": color,
            "icon": dim["icon"],
            "description": dim["description"]
        })
    
    return indicators 