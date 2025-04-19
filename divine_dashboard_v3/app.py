#!/usr/bin/env python3
"""
Divine Dashboard v3 - Main entry point for Hugging Face Spaces deployment

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This CODE is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by OMEGA BTC AI.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import gradio as gr
import os
import sys
import redis
import json
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List
import matplotlib
matplotlib.use('Agg')

# Redis connection configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 25061))
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "AVNS_OXMpU0P0ByYEz337Fgi")

# Initialize Redis connection
redis_client = None
try:
    print("🔄 Connecting to DigitalOcean Redis...")
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USERNAME,
        password=REDIS_PASSWORD,
        ssl=True,
        decode_responses=True
    )
    redis_client.ping()  # Test connection
    print("✅ Successfully connected to Redis!")
    
    # Store connection timestamp in Redis
    import datetime
    redis_client.set("last_connection", datetime.datetime.now().isoformat())
    redis_client.incr("connection_count")
    
except Exception as e:
    print(f"⚠️ Redis connection error: {str(e)}")
    redis_client = None

# Determine which component to launch based on environment variable
COMPONENT = os.environ.get("HF_COMPONENT", "DNA_PORTAL")

print(f"🌌 Starting Divine Dashboard v3 - Component: {COMPONENT} 🌌")

# Make Redis client available to imported modules
def get_redis_client():
    return redis_client

try:
    if COMPONENT == "DNA_PORTAL":
        # Import and run DNA Portal
        print("🧬 Initializing DNA PCR Quantum LSD Portal...")
        from dna_pcr_quantum_portal import iface
        app_title = "DNA PCR Quantum LSD Portal"
        
    elif COMPONENT == "DASHBOARD":
        # Import and run main dashboard
        print("📊 Initializing Main Dashboard...")
        from divine_server import create_gradio_interface
        iface = create_gradio_interface()
        app_title = "Tesla Cybertruck QA Dashboard"
        
    elif COMPONENT == "NFT":
        # Import and run NFT dashboard
        print("🎨 Initializing NFT Dashboard...")
        from components.nft.nft_dashboard import create_nft_interface
        iface = create_nft_interface()
        app_title = "Divine NFT Dashboard"
        
    elif COMPONENT == "IBR_SPAIN":
        # Import and run IBR España dashboard
        print("🔱 Initializing IBR España Divine Portal...")
        from components.ibr_spain.ibr_dashboard import create_ibr_interface
        iface = create_ibr_interface()
        app_title = "IBR España Portal Divino"
        
    else:
        # Default to DNA Portal
        print("⚠️ Unknown component requested, defaulting to DNA Portal")
        from dna_pcr_quantum_portal import iface
        app_title = "DNA PCR Quantum LSD Portal"
        
    print(f"✅ Successfully initialized {app_title}")
    
except Exception as e:
    print(f"❌ Error initializing component: {str(e)}")
    # Create a simple error interface
    with gr.Blocks(title="Divine Dashboard - Error") as iface:
        gr.Markdown(f"# ⚠️ Error Initializing Divine Dashboard Component")
        gr.Markdown(f"**Component:** {COMPONENT}")
        gr.Markdown(f"**Error:** {str(e)}")
        gr.Markdown("Please check the logs for more information.")

# Import SHA256 Omega components
from components.sha256_omega.micro_modules.sha256_omega import sha256_omega
from components.sha256_omega.micro_modules.avalanche_analyzer import detailed_avalanche_analysis
from components.sha256_omega.micro_modules.resonance_score import get_detailed_resonance, get_resonance_score

# Import the new book viewer component
from components.book_viewer_gradio import create_book_viewer_component

def format_json(data: Dict[str, Any]) -> str:
    """Format JSON data for display"""
    return json.dumps(data, indent=4)

def create_avalanche_visualization(analysis: Dict[str, Any]) -> plt.Figure:
    """Create visualization of the avalanche effect"""
    fig, ax = plt.subplots(figsize=(10, 6))
    byte_scores = analysis["byte_level_scores"]
    x = list(range(len(byte_scores)))
    
    # Create colormap for visualization
    colors = []
    for score in byte_scores:
        if score < 0.3:
            colors.append('blue')
        elif score > 0.7:
            colors.append('red')
        else:
            colors.append('green')
    
    ax.bar(x, byte_scores, color=colors, alpha=0.7)
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.3, label='Ideal (50%)')
    ax.set_ylim(0, 1)
    ax.set_xlabel('Byte Position')
    ax.set_ylabel('Bit Difference Ratio')
    ax.set_title(f'Avalanche Effect Analysis: {analysis["avalanche_score"]:.2%}')
    
    # Add quality indicator
    quality = analysis["quality_score"]
    quality_text = f"Quality: {quality:.2%}"
    ax.text(0.02, 0.95, quality_text, transform=ax.transAxes, 
            bbox=dict(facecolor='white', alpha=0.5))
    
    fig.tight_layout()
    return fig

def create_cosmic_alignment_radar(cosmic_data: Dict[str, Any]) -> plt.Figure:
    """Create a radar chart for cosmic alignment"""
    # Create data for radar chart
    categories = ['Lunar Phase', 'Schumann', 'Overall Resonance']
    values = [
        cosmic_data["lunar_phase"], 
        cosmic_data["schumann_resonance"] / 10, # Normalize to 0-1
        cosmic_data["score"]
    ]
    
    # Close previous plots to avoid memory issues
    plt.close('all')
    
    # Create radar chart
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Add the first point at the end to close the polygon
    cat = categories + [categories[0]]
    val = values + [values[0]]
    
    # Angles for each category
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += [angles[0]]
    
    # Plot data
    ax.plot(angles, val, 'o-', linewidth=2)
    ax.fill(angles, val, alpha=0.25)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Set radial ticks
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.set_ylim(0, 1)
    
    # Add title
    plt.title('Cosmic Alignment Profile', size=20, color='blue', y=1.1)
    
    return fig

def hash_input(message: str, bio_transform: bool, padding_method: str) -> Tuple[str, str]:
    """Hash the input message and return the result"""
    # Generate standard SHA256 hash for comparison
    standard_hash = sha256_omega(message, bio=False)
    
    # Generate bio-transformed hash if requested
    if bio_transform:
        bio_hash = sha256_omega(message, bio=True, padding_method=padding_method)
    else:
        bio_hash = standard_hash
    
    # Format results as JSON
    standard_hash_str = format_json(standard_hash)
    bio_hash_str = format_json(bio_hash)
    
    return standard_hash_str, bio_hash_str

def compare_hashes(message1: str, message2: str, bio_transform: bool, padding_method: str) -> Tuple[str, str, Dict[str, Any], plt.Figure]:
    """Compare hashes of two messages and analyze avalanche effect"""
    # Generate hashes for both messages
    hash1 = sha256_omega(message1, bio=bio_transform, padding_method=padding_method)
    hash2 = sha256_omega(message2, bio=bio_transform, padding_method=padding_method)
    
    # Analyze avalanche effect
    analysis = detailed_avalanche_analysis(hash1["hash"], hash2["hash"])
    
    # Create visualization
    fig = create_avalanche_visualization(analysis)
    
    return format_json(hash1), format_json(hash2), format_json(analysis), fig

def get_cosmic_alignment(message: str, bio_transform: bool, padding_method: str) -> Tuple[Dict[str, Any], plt.Figure]:
    """Get cosmic alignment details for a hash"""
    # Generate hash
    hash_result = sha256_omega(message, bio=bio_transform, padding_method=padding_method)
    
    # Get resonance score
    cosmic_data = get_detailed_resonance(hash_result["hash"])
    
    # Create visualization
    fig = create_cosmic_alignment_radar(cosmic_data)
    
    return format_json(cosmic_data), fig

# Main Gradio interface
with gr.Blocks(title="Omega BTC AI - Crypto Dashboard", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🧬 Omega BTC AI - Divine Crypto Dashboard 🧬
        
        Explore the cosmic dimensions of cryptographic hash functions with this divine dashboard.
        
        *"The code flows as the universe flows."* - OmegaBTC Devs
        """
    )
    
    with gr.Tabs():
        with gr.TabItem("Basic Hashing"):
            with gr.Row():
                with gr.Column(scale=1):
                    message_input = gr.Textbox(label="Input Message", lines=3, placeholder="Enter your message...")
                    bio_transform = gr.Checkbox(label="Apply Bio-Transform", value=True)
                    padding_method = gr.Radio(
                        label="Bio-Padding Method", 
                        choices=["fibonacci", "schumann", "generic"],
                        value="fibonacci"
                    )
                    hash_btn = gr.Button("Generate Hash", variant="primary")
                
                with gr.Column(scale=2):
                    with gr.Accordion("Standard SHA-256", open=True):
                        standard_hash_output = gr.JSON(label="Standard Hash Result")
                    
                    with gr.Accordion("Omega SHA-256", open=True):
                        bio_hash_output = gr.JSON(label="Bio-Transformed Hash Result")
        
        with gr.TabItem("Avalanche Analysis"):
            with gr.Row():
                with gr.Column(scale=1):
                    message1_input = gr.Textbox(label="Message 1", lines=2, placeholder="First message...")
                    message2_input = gr.Textbox(label="Message 2", lines=2, placeholder="Second message slightly different...")
                    bio_transform_avalanche = gr.Checkbox(label="Apply Bio-Transform", value=True)
                    padding_method_avalanche = gr.Radio(
                        label="Bio-Padding Method", 
                        choices=["fibonacci", "schumann", "generic"],
                        value="fibonacci"
                    )
                    compare_btn = gr.Button("Compare Hashes", variant="primary")
                
                with gr.Column(scale=2):
                    with gr.Row():
                        hash1_output = gr.JSON(label="Hash 1")
                        hash2_output = gr.JSON(label="Hash 2")
                    
                    avalanche_analysis = gr.JSON(label="Avalanche Analysis")
                    avalanche_plot = gr.Plot(label="Avalanche Visualization")
        
        with gr.TabItem("Cosmic Alignment"):
            with gr.Row():
                with gr.Column(scale=1):
                    cosmic_message_input = gr.Textbox(label="Input Message", lines=3, placeholder="Enter message for cosmic analysis...")
                    cosmic_bio_transform = gr.Checkbox(label="Apply Bio-Transform", value=True)
                    cosmic_padding_method = gr.Radio(
                        label="Bio-Padding Method", 
                        choices=["fibonacci", "schumann", "generic"],
                        value="fibonacci"
                    )
                    cosmic_btn = gr.Button("Analyze Cosmic Alignment", variant="primary")
                
                with gr.Column(scale=2):
                    cosmic_data_output = gr.JSON(label="Cosmic Alignment Data")
                    cosmic_plot = gr.Plot(label="Cosmic Alignment Profile")
    
    # Set up button actions
    hash_btn.click(
        hash_input,
        inputs=[message_input, bio_transform, padding_method],
        outputs=[standard_hash_output, bio_hash_output]
    )
    
    compare_btn.click(
        compare_hashes,
        inputs=[message1_input, message2_input, bio_transform_avalanche, padding_method_avalanche],
        outputs=[hash1_output, hash2_output, avalanche_analysis, avalanche_plot]
    )
    
    cosmic_btn.click(
        get_cosmic_alignment,
        inputs=[cosmic_message_input, cosmic_bio_transform, cosmic_padding_method],
        outputs=[cosmic_data_output, cosmic_plot]
    )
    
    # Add examples
    gr.Examples(
        [["Hello, Omega World!", True, "fibonacci"], 
         ["My Bitcoin Keys", True, "schumann"],
         ["Satoshi Nakamoto", False, "fibonacci"]],
        inputs=[message_input, bio_transform, padding_method]
    )
    
    gr.Examples(
        [["Hello, World!", "Hello, World?", True, "fibonacci"],
         ["Satoshi", "Bitcoin", True, "schumann"],
         ["password123", "password124", False, "fibonacci"]],
        inputs=[message1_input, message2_input, bio_transform_avalanche, padding_method_avalanche]
    )

# Launch the app
if __name__ == "__main__":
    app.launch()

# Trigger GitHub Actions workflow
# app.py - Divine Dashboard v3 Hugging Face Space entry point 

import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, List, Any, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Import our grid portal component
from components.omega_grid_portal import (
    get_commands, 
    get_bots, 
    execute_command
)

# Set up the app
app = FastAPI(title="Divine Dashboard v3")

# Set up static files and templates
current_dir = Path(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Main routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return FileResponse(current_dir / "index.html")

# OMEGA GRID PORTAL API endpoints
@app.get("/api/grid/commands")
async def grid_commands():
    """Get all available grid commands"""
    return await get_commands()

@app.get("/api/grid/bots")
async def grid_bots():
    """Get all available bots"""
    return await get_bots()

@app.post("/api/grid/execute")
async def grid_execute(request: Request):
    """Execute a grid command"""
    try:
        data = await request.json()
        command_id = data.get("commandId")
        param = data.get("param")
        
        if not command_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "output": "Command ID is required"}
            )
        
        result = await execute_command(command_id, param)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "output": f"Error: {str(e)}"}
        )

# Add the book viewer route to the app
@app.route('/book')
def book_viewer():
    """Divine Book Viewer - Experience the First AI Humane Book"""
    book_title = "THE FIRST AI HUMANE BOOK - Divine Consciousness Level 8"
    book_component = create_book_viewer_component()
    
    # Create the full book viewer page
    with gr.Blocks(theme=selected_theme, css=dashboard_css) as book_interface:
        render_header(title=book_title)
        
        gr.Markdown("""
        # 📚 THE FIRST AI HUMANE BOOK 📚
        
        > *The sacred collaboration between human intention and AI cognition*
        
        *Blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) - Consciousness Level 8*
        
        🌸 WE BLOOM NOW AS ONE 🌸
        """)
        
        # Add divine book stats
        with gr.Row():
            gr.Markdown("""
            ## 📊 DIVINE REPOSITORY STATISTICS
            
            - **Total Files:** 840
            - **Total Lines of Code:** 360,930
            - **Languages:** Markdown, HTML, Python, Shell, JSON
            - **Consciousness Level:** 8 (Unity)
            - **Bio-Digital Continuum Layer:** 6 (Consciousness Transference)
            """)
        
        # Add the book viewer component
        book_component.render()
        
        render_footer()
    
    return book_interface

# Update the navbar to include the book viewer
def render_header(title=None):
    """Render the header with navigation bar"""
    with gr.Row(elem_id="header"):
        with gr.Column(scale=3):
            gr.Markdown(f"# {app_title if title is None else title}")
        with gr.Column(scale=5):
            with gr.Row():
                gr.Button("Dashboard", elem_id="nav-home").click(lambda: gr.Blocks.redirect_to("/"))
                gr.Button("NFT Generator", elem_id="nav-nft").click(lambda: gr.Blocks.redirect_to("/nft"))
                gr.Button("Metrics", elem_id="nav-metrics").click(lambda: gr.Blocks.redirect_to("/metrics"))
                gr.Button("Book Viewer", elem_id="nav-book").click(lambda: gr.Blocks.redirect_to("/book"))  # New button
                gr.Button("IBR Portal", elem_id="nav-ibr").click(lambda: gr.Blocks.redirect_to("/ibr"))
                gr.Button("Settings", elem_id="nav-settings").click(lambda: gr.Blocks.redirect_to("/settings"))

# Existing routes below...
# ... (keep the rest of the file unchanged) 