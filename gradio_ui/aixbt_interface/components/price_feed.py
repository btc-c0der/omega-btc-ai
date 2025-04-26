#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""Price Feed Component for AIXBT Interface.

Real-time price monitoring component that displays:
1. Current BTC price and changes
2. Price movement visualization
3. Volume analysis
4. Market momentum indicators
"""

import gradio as gr
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

class PriceFeedComponent:
    """AIXBT price feed visualization component."""
    
    def __init__(self, redis_manager):
        """Initialize price feed component."""
        self.redis = redis_manager
        self.output_components = []
        
    def render(self) -> None:
        """Render the price feed component."""
        with gr.Box():
            gr.Markdown("## 📊 BTC Price Feed")
            
            with gr.Row():
                price_display = gr.Number(label="Current Price (USDT)")
                change_display = gr.Number(label="24h Change (%)")
                volume_display = gr.Number(label="24h Volume (BTC)")
            
            with gr.Row():
                chart = gr.Plot(label="Price Movement")
                
            self.output_components = [
                price_display,
                change_display,
                volume_display,
                chart
            ]
    
    async def update(self) -> List[Any]:
        """Update price feed components."""
        try:
            # Get latest market data
            market_data = await self.redis.get_market_data("btc_market_data")
            if not market_data:
                return [0, 0, 0, None]
            
            # Extract data
            price = float(market_data.get("price", 0))
            change = float(market_data.get("change_24h", 0))
            volume = float(market_data.get("volume_24h", 0))
            
            # Get price history for chart
            history = await self.redis.get_market_data("btc_price_history")
            if not history:
                history = []
            
            # Create price chart
            df = pd.DataFrame(history)
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df.get("timestamp", []),
                y=df.get("price", []),
                mode="lines",
                name="BTC/USDT",
                line=dict(color="#F7931A", width=2)
            ))
            
            fig.update_layout(
                template="plotly_dark",
                showlegend=True,
                height=400,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            return [price, change, volume, fig]
            
        except Exception as e:
            print(f"Error updating price feed: {e}")
            return [0, 0, 0, None]