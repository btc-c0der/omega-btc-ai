#!/usr/bin/env python3
"""
AIXBT Visualization Module
-----------------------

Functions for creating various token analytics visualizations, including:
- Basic PnL projection
- Multi-leverage comparison
- OMEGA Trap Zone™ overlay
- Fibonacci vortex patterns
- Escape visualization
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Tuple, Optional

from .config import DASHBOARD_CONFIG

def create_basic_pnl_projection(
    price_range: Optional[Tuple[float, float]] = None
) -> go.Figure:
    """
    Create a basic PnL projection figure for AIXBT token.
    
    Args:
        price_range: Optional price range to display (min, max)
        
    Returns:
        Plotly figure object
    """
    # Extract configuration
    token_config = DASHBOARD_CONFIG["token"]
    theme = DASHBOARD_CONFIG["theme"]
    
    # Set price range or use default
    if price_range is None:
        price_range = (0.01, token_config["price_target"])
    
    # Generate price points
    prices = np.linspace(price_range[0], price_range[1], 500)
    
    # Calculate PnL at each price
    pnl = (prices - token_config["entry_price"]) * token_config["token_quantity"] * token_config["leverage"]
    
    # Create figure
    fig = go.Figure()
    
    # Add PnL curve
    fig.add_trace(
        go.Scatter(
            x=prices,
            y=pnl,
            mode="lines",
            line=dict(color=theme["gold"], width=3),
            name="Projected PnL"
        )
    )
    
    # Add reference lines
    fig.add_vline(
        x=token_config["entry_price"],
        line=dict(color="gray", dash="dash"),
        annotation_text=f"Entry @ {token_config['entry_price']:.5f}"
    )
    
    fig.add_vline(
        x=token_config["current_price"],
        line=dict(color=theme["error"], dash="dash"),
        annotation_text=f"Mark @ {token_config['current_price']:.5f}"
    )
    
    fig.add_vline(
        x=token_config["price_target"],
        line=dict(color=theme["success"], dash="dash"),
        annotation_text=f"Target @ ${token_config['price_target']:.2f}"
    )
    
    # Add zero line
    fig.add_hline(
        y=0,
        line=dict(color="black", width=0.5)
    )
    
    # Update layout
    fig.update_layout(
        title=f"🧬 AIXBT {token_config['leverage']}x Leverage PnL Projection to ${token_config['price_target']:.2f} 🧬",
        xaxis_title="Token Price (USD)",
        yaxis_title="Profit / Loss (USD)",
        template="plotly_dark",
        paper_bgcolor=theme["background"],
        plot_bgcolor=theme["background"],
        font=dict(color=theme["text"]),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_multi_leverage_pnl(
    leverage_profiles: Optional[List[int]] = None
) -> go.Figure:
    """
    Create a multi-leverage PnL comparison with breakeven and liquidation levels.
    
    Args:
        leverage_profiles: Optional list of leverage values to display
        
    Returns:
        Plotly figure object
    """
    # Extract configuration
    token_config = DASHBOARD_CONFIG["token"]
    theme = DASHBOARD_CONFIG["theme"]
    liquidation_price = DASHBOARD_CONFIG["liquidation_price"]
    breakeven_price = DASHBOARD_CONFIG["breakeven_price"]
    
    # Set leverage profiles or use default
    if leverage_profiles is None:
        leverage_profiles = [1, 2, 3, 4, 5]
    
    # Generate price points
    prices = np.linspace(0.01, token_config["price_target"] * 1.2, 1000)
    
    # Create figure
    fig = go.Figure()
    
    # Add PnL curves for each leverage
    for lev in leverage_profiles:
        pnl = (prices - token_config["entry_price"]) * token_config["token_quantity"] * lev
        is_current = (lev == token_config["leverage"])
        
        fig.add_trace(
            go.Scatter(
                x=prices,
                y=pnl,
                mode="lines",
                line=dict(
                    color=theme["gold"] if is_current else theme["accent4"],
                    width=3 if is_current else 1.5,
                    dash=None if is_current else "dash"
                ),
                name=f"{lev}x Leverage"
            )
        )
    
    # Add reference lines
    fig.add_vline(
        x=token_config["entry_price"],
        line=dict(color="gray", dash="dot"),
        annotation_text=f"Entry @ {token_config['entry_price']:.4f}"
    )
    
    fig.add_vline(
        x=token_config["current_price"],
        line=dict(color=theme["error"], dash="dash"),
        annotation_text=f"Mark @ {token_config['current_price']:.4f}"
    )
    
    fig.add_vline(
        x=token_config["price_target"],
        line=dict(color=theme["success"], dash="dash"),
        annotation_text=f"Target @ ${token_config['price_target']:.2f}"
    )
    
    fig.add_vline(
        x=breakeven_price,
        line=dict(color=theme["warning"], dash="dashdot"),
        annotation_text=f"Breakeven @ ${breakeven_price:.4f}"
    )
    
    fig.add_vline(
        x=liquidation_price,
        line=dict(color="black", width=2),
        annotation_text=f"Liquidation @ ${liquidation_price:.4f}"
    )
    
    # Add zero line
    fig.add_hline(
        y=0,
        line=dict(color="black", width=0.7)
    )
    
    # Update layout
    fig.update_layout(
        title="📊 AIXBT Multi-Leverage PnL Projection + Breakeven/Fees + Liquidation",
        xaxis_title="Token Price (USD)",
        yaxis_title="Profit / Loss (USD)",
        template="plotly_dark",
        paper_bgcolor=theme["background"],
        plot_bgcolor=theme["background"],
        font=dict(color=theme["text"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Use symlog scale for better visibility near zero
    fig.update_yaxes(type="symlog", zeroline=True, zerolinecolor="white", zerolinewidth=0.5)
    
    return fig

def create_omega_trap_zone_pnl() -> go.Figure:
    """
    Create a PnL chart with OMEGA Trap Zone™ overlay.
    
    Returns:
        Plotly figure object with the trap zone visualization
    """
    # Extract configuration
    token_config = DASHBOARD_CONFIG["token"]
    theme = DASHBOARD_CONFIG["theme"]
    trap_config = DASHBOARD_CONFIG["trap"]
    liquidation_price = DASHBOARD_CONFIG["liquidation_price"]
    breakeven_price = DASHBOARD_CONFIG["breakeven_price"]
    leverage_profiles = [1, 2, 3, 4, 5]
    
    # Generate price points
    prices = np.linspace(0.01, token_config["price_target"] * 1.2, 1000)
    
    # Create figure
    fig = go.Figure()
    
    # Add PnL curves for each leverage
    for lev in leverage_profiles:
        pnl = (prices - token_config["entry_price"]) * token_config["token_quantity"] * lev
        is_current = (lev == token_config["leverage"])
        
        fig.add_trace(
            go.Scatter(
                x=prices,
                y=pnl,
                mode="lines",
                line=dict(
                    color=theme["gold"] if is_current else theme["accent4"],
                    width=3 if is_current else 1.5,
                    dash=None if is_current else "dash"
                ),
                name=f"{lev}x Leverage"
            )
        )
    
    # Add trap zone as a shaded region
    fig.add_vrect(
        x0=trap_config["trap_start"],
        x1=trap_config["trap_end"],
        fillcolor="red",
        opacity=0.2,
        line_width=0,
        annotation_text="OMEGA TRAP ZONE™ 🔻",
        annotation_position="top left"
    )
    
    # Add reference lines
    fig.add_vline(
        x=token_config["entry_price"],
        line=dict(color="gray", dash="dot"),
        annotation_text=f"Entry @ {token_config['entry_price']:.4f}"
    )
    
    fig.add_vline(
        x=token_config["current_price"],
        line=dict(color=theme["error"], dash="dash"),
        annotation_text=f"Mark @ {token_config['current_price']:.4f}"
    )
    
    fig.add_vline(
        x=token_config["price_target"],
        line=dict(color=theme["success"], dash="dash"),
        annotation_text=f"Target @ ${token_config['price_target']:.2f}"
    )
    
    fig.add_vline(
        x=breakeven_price,
        line=dict(color=theme["warning"], dash="dashdot"),
        annotation_text=f"Breakeven @ ${breakeven_price:.4f}"
    )
    
    fig.add_vline(
        x=liquidation_price,
        line=dict(color="black", width=2),
        annotation_text=f"Liquidation @ ${liquidation_price:.4f}"
    )
    
    # Add zero line
    fig.add_hline(
        y=0,
        line=dict(color="black", width=0.7)
    )
    
    # Update layout
    fig.update_layout(
        title="🔻 AIXBT PnL Simulation with OMEGA TRAP ZONE OVERLAY™",
        xaxis_title="Token Price (USD)",
        yaxis_title="Profit / Loss (USD)",
        template="plotly_dark",
        paper_bgcolor=theme["background"],
        plot_bgcolor=theme["background"],
        font=dict(color=theme["text"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Use symlog scale for better visibility near zero
    fig.update_yaxes(type="symlog", zeroline=True, zerolinecolor="white", zerolinewidth=0.5)
    
    return fig

def create_fibonacci_vortex_pnl() -> go.Figure:
    """
    Create a PnL chart with Fibonacci vortex overlay on top of OMEGA Trap Zone™.
    
    Returns:
        Plotly figure with Fibonacci vortex visualization
    """
    # Start with trap zone PnL chart
    fig = create_omega_trap_zone_pnl()
    
    # Extract configuration
    token_config = DASHBOARD_CONFIG["token"]
    theme = DASHBOARD_CONFIG["theme"]
    fib_levels = DASHBOARD_CONFIG["fibonacci"]
    
    # Calculate Fibonacci price levels scaled to entry->target range
    price_range = token_config["price_target"] - token_config["entry_price"]
    fib_prices = [token_config["entry_price"] + price_range * level for level in fib_levels]
    
    # Add Fibonacci vortex lines
    for i, price in enumerate(fib_prices):
        # Skip levels outside our chart range
        if price < 0 or price > token_config["price_target"] * 1.2:
            continue
            
        fig.add_vline(
            x=price,
            line=dict(color="purple", dash="dot", width=1),
            annotation_text=f"Φ {fib_levels[i]:.3f}",
            annotation_position="top"
        )
    
    # Update title
    fig.update_layout(
        title="🌀 AIXBT PnL with OMEGA TRAP ZONE + Fibonacci Vortex Overlay 🌀"
    )
    
    return fig

def create_escape_visualization() -> go.Figure:
    """
    Create a visualization of the escape strategy from the OMEGA Trap Zone™.
    
    Returns:
        Plotly figure with escape path visualization
    """
    # Extract configuration
    token_config = DASHBOARD_CONFIG["token"]
    theme = DASHBOARD_CONFIG["theme"]
    escape_path = DASHBOARD_CONFIG["escape_path"]
    liquidation_price = DASHBOARD_CONFIG["liquidation_price"]
    trap_config = DASHBOARD_CONFIG["trap"]
    
    # Create a figure with two subplots
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("PnL Projection", "OMEGA Escape Path")
    )
    
    # Generate price points
    prices = np.linspace(liquidation_price * 0.9, token_config["price_target"] * 0.3, 500)
    
    # PnL curve for main leverage
    pnl = (prices - token_config["entry_price"]) * token_config["token_quantity"] * token_config["leverage"]
    
    # Add PnL curve to top subplot
    fig.add_trace(
        go.Scatter(
            x=prices,
            y=pnl,
            mode="lines",
            line=dict(color=theme["gold"], width=3),
            name=f"{token_config['leverage']}x Leverage"
        ),
        row=1, col=1
    )
    
    # Add trap zone as a shaded region to both subplots
    fig.add_vrect(
        x0=trap_config["trap_start"],
        x1=trap_config["trap_end"],
        fillcolor="red",
        opacity=0.2,
        line_width=0,
        annotation_text="OMEGA TRAP ZONE™",
        annotation_position="top left",
        row=1, col=1
    )
    
    fig.add_vrect(
        x0=trap_config["trap_start"],
        x1=trap_config["trap_end"],
        fillcolor="red",
        opacity=0.2,
        line_width=0,
        row=2, col=1
    )
    
    # Add escape triangle in the bottom subplot
    escape_prices = [item["price"] for item in escape_path]
    escape_labels = [item["label"] for item in escape_path]
    
    # Create escape path visualization
    for i, (price, label) in enumerate(zip(escape_prices, escape_labels)):
        fig.add_trace(
            go.Scatter(
                x=[price],
                y=[i],
                mode="markers+text",
                marker=dict(
                    symbol="circle",
                    size=15,
                    color=theme["accent2"] if "ENTRY" in label else theme["accent1"],
                    line=dict(width=2, color=theme["text"])
                ),
                text=label,
                textposition="middle right",
                name=label
            ),
            row=2, col=1
        )
    
    # Add connecting line through escape points
    fig.add_trace(
        go.Scatter(
            x=escape_prices,
            y=list(range(len(escape_prices))),
            mode="lines",
            line=dict(color=theme["accent2"], width=2, dash="dot"),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Add current price marker
    fig.add_vline(
        x=token_config["current_price"],
        line=dict(color=theme["error"], dash="dash"),
        annotation_text=f"Current @ {token_config['current_price']:.4f}",
        row="all", col=1
    )
    
    # Add liquidation line
    fig.add_vline(
        x=liquidation_price,
        line=dict(color="black", width=2),
        annotation_text=f"Liquidation @ {liquidation_price:.4f}",
        row="all", col=1
    )
    
    # Add zero line to PnL subplot
    fig.add_hline(
        y=0,
        line=dict(color="white", width=0.5),
        row=1, col=1
    )
    
    # Update layout
    fig.update_layout(
        title="☀️ AIXBT PnL ESCAPE ZONE FORECAST ☀️",
        template="plotly_dark",
        paper_bgcolor=theme["background"],
        plot_bgcolor=theme["background"],
        font=dict(color=theme["text"]),
        showlegend=False,
        height=800
    )
    
    # Update y-axis for escape path subplot
    fig.update_yaxes(
        title="Escape Steps",
        showticklabels=False,
        range=[-0.5, len(escape_path) - 0.5],
        row=2, col=1
    )
    
    # Update x-axis
    fig.update_xaxes(
        title="Token Price (USD)",
        row=2, col=1
    )
    
    # Update y-axis for PnL subplot
    fig.update_yaxes(
        title="Profit / Loss (USD)",
        type="symlog",
        row=1, col=1
    )
    
    return fig 