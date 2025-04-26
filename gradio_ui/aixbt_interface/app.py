#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""AIXBT Gradio Interface.

Web interface for AIXBT market analysis and trading, featuring:
1. Real-time price monitoring
2. Market maker trap detection 
3. Neural matrix visualization
4. Multi-timeframe analysis
5. Trading signals integration
"""

import os
import gradio as gr
from components.redis_manager import AIXBTRedisManager
from components.price_feed import PriceFeedComponent
from components.trap_meter import TrapMeterComponent
from components.market_data import MarketDataComponent
from components.neural_matrix import NeuralMatrixComponent
from components.visualization import VisualizationComponent

def create_interface():
    """Create the AIXBT Gradio interface."""
    
    # Initialize components
    redis_manager = AIXBTRedisManager()
    price_feed = PriceFeedComponent(redis_manager)
    trap_meter = TrapMeterComponent(redis_manager)
    market_data = MarketDataComponent(redis_manager)
    neural_matrix = NeuralMatrixComponent(redis_manager)
    visualizer = VisualizationComponent(redis_manager)
    
    # Create interface
    with gr.Blocks(theme="dark") as interface:
        gr.Markdown("# 🧬 AIXBT Neural Analysis Interface")
        
        with gr.Row():
            with gr.Column():
                price_feed.render()
                trap_meter.render()
            with gr.Column():
                market_data.render()
                neural_matrix.render()
        
        with gr.Row():
            visualizer.render()
            
        # Schedule component updates
        interface.load(price_feed.update, None, price_feed.output_components)
        interface.load(trap_meter.update, None, trap_meter.output_components)
        interface.load(market_data.update, None, market_data.output_components)
        interface.load(neural_matrix.update, None, neural_matrix.output_components)
        interface.load(visualizer.update, None, visualizer.output_components)
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860)),
        share=True,
        debug=True
    )