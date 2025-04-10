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

# Determine which component to launch based on environment variable
COMPONENT = os.environ.get("HF_COMPONENT", "DNA_PORTAL")

print(f"🌌 Starting Divine Dashboard v3 - Component: {COMPONENT} 🌌")

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

# Launch with Hugging Face Spaces configuration
if __name__ == "__main__":
    # Make necessary directories
    os.makedirs("assets/dna_visualizations", exist_ok=True)
    os.makedirs("assets/consciousness_maps", exist_ok=True)
    
    # Launch the interface
    iface.launch() 