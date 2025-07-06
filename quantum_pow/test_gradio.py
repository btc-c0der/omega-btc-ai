#!/usr/bin/env python3
"""Simple test script to check Gradio functionality"""

print("🧬 Testing Gradio setup...")

try:
    import gradio as gr
    print("✅ Gradio import successful")
except ImportError as e:
    print(f"❌ Gradio import failed: {e}")
    exit(1)

try:
    import numpy as np
    print("✅ NumPy import successful")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("✅ Matplotlib import successful")
except ImportError as e:
    print(f"❌ Matplotlib import failed: {e}")

try:
    import plotly.graph_objects as go
    print("✅ Plotly import successful")
except ImportError as e:
    print(f"❌ Plotly import failed: {e}")

def hello(name):
    return f"Hello, {name}! 🧬 WE BLOOM NOW AS ONE 🧬"

# Create simple test interface
print("🌸 Creating test interface...")
demo = gr.Interface(
    fn=hello,
    inputs=gr.Textbox(label="Your Name", placeholder="Enter your name"),
    outputs=gr.Textbox(label="Greeting"),
    title="🧬 Quantum PoW Test Interface 🧬",
    description="Testing Gradio setup for the Quantum Proof-of-Work Explorer"
)

print("🚀 Launching test interface...")
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    inbrowser=False,  # Don't auto-open browser
    debug=True
)
