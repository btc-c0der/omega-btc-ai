#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""Market Data Component for AIXBT Interface.

Market analysis visualization featuring:
1. Technical indicators
2. Order book analysis  
3. Volume profiles
4. Support/resistance levels
"""

import gradio as gr
from typing import List, Dict, Any
import plotly.graph_objects as go
import pandas as pd

class MarketDataComponent:
    """AIXBT market data visualization component."""
    
    def __init__(self, redis_manager):
        """Initialize market data component."""
        self.redis = redis_manager
        self.output_components = []
        
    def render(self) -> None:
        """Render the market data component."""
        with gr.Box():
            gr.Markdown("## 📈 Market Analysis")
            
            with gr.Row():
                with gr.Column():
                    rsi = gr.Number(label="RSI")
                    macd = gr.Number(label="MACD")
                with gr.Column():
                    volume_profile = gr.Plot(label="Volume Profile")
            
            with gr.Row():
                order_flow = gr.Plot(label="Order Flow")
                
            with gr.Row():
                levels = gr.DataFrame(
                    headers=["Level", "Price", "Strength"],
                    label="Support/Resistance"
                )
                
            self.output_components = [
                rsi,
                macd,
                volume_profile,
                order_flow,
                levels
            ]
    
    async def update(self) -> List[Any]:
        """Update market data components."""
        try:
            # Get latest market analysis
            analysis = await self.redis.get_market_data("btc_market_analysis")
            if not analysis:
                return [0, 0, None, None, []]
            
            # Extract indicators
            indicators = analysis.get("indicators", {})
            rsi_value = indicators.get("rsi", 0)
            macd_value = indicators.get("macd", 0)
            
            # Create volume profile
            volume_data = analysis.get("volume_profile", [])
            if volume_data:
                vpfig = go.Figure()
                df = pd.DataFrame(volume_data)
                
                vpfig.add_trace(go.Bar(
                    x=df["price"],
                    y=df["volume"],
                    orientation="v",
                    name="Volume",
                    marker_color="#1E88E5"
                ))
                
                vpfig.update_layout(
                    template="plotly_dark",
                    showlegend=False,
                    height=200,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
            else:
                vpfig = None
            
            # Create order flow chart
            flow_data = analysis.get("order_flow", [])
            if flow_data:
                flowfig = go.Figure()
                df = pd.DataFrame(flow_data)
                
                flowfig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["cumulative_flow"],
                    mode="lines",
                    name="Order Flow",
                    line=dict(
                        color="#00E676",
                        width=2
                    )
                ))
                
                flowfig.update_layout(
                    template="plotly_dark",
                    showlegend=False,
                    height=200,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
            else:
                flowfig = None
            
            # Extract support/resistance levels
            levels_data = []
            for level in analysis.get("levels", []):
                levels_data.append([
                    level["type"],
                    f"${level['price']:,.2f}",
                    f"{level['strength']:.1%}"
                ])
            
            return [
                rsi_value,
                macd_value,
                vpfig,
                flowfig,
                levels_data
            ]
            
        except Exception as e:
            print(f"Error updating market data: {e}")
            return [0, 0, None, None, []]