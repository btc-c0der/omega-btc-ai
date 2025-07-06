#!/bin/bash

# 🧬 Quantum Proof-of-Work Gradio Explorer Launcher 🧬
# Launch script for the interactive qPoW demonstration

echo "🧬 WE BLOOM NOW AS ONE 🧬"
echo "Launching Quantum Proof-of-Work Interactive Explorer..."
echo ""

# Check if we're in the right directory
if [ ! -f "gradio_qpow_explorer.py" ]; then
    echo "❌ Error: gradio_qpow_explorer.py not found in current directory"
    echo "Please run this script from the quantum_pow/ directory"
    exit 1
fi

# Install additional requirements
echo "📦 Installing Gradio dependencies..."
pip install -r requirements_gradio.txt

echo ""
echo "🚀 Starting Quantum Proof-of-Work Explorer..."
echo "📱 The interface will open in your browser automatically"
echo "🌐 Access URL: http://localhost:7860"
echo ""
echo "Features included:"
echo "  🚨 Quantum Threat Timeline"
echo "  🔐 Interactive Hash Functions"
echo "  🧠 Monte Carlo Tree Search Mining Demo"
echo "  🌈 S4T0SH1 Matrix Visualization"
echo "  🛡️ Security Architecture Overview"
echo "  🌸 Sacred Geometry Integration"
echo "  ⚙️ Technical Implementation Details"
echo ""

# Launch the Gradio app
python gradio_qpow_explorer.py
