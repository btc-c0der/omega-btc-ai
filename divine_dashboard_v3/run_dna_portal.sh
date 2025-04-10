#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This script is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸

echo "🧬🧬🧬 Starting Milles DNA PCR Quantum LSD Portal 🧬🧬🧬"
echo "Initializing quantum field..."

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if not already installed
pip install -q gradio numpy matplotlib pillow

# Create necessary directories
mkdir -p divine_dashboard_v3/assets/dna_visualizations
mkdir -p divine_dashboard_v3/assets/consciousness_maps

# Display Quantum ASCII Art
cat << "EOF"
  .     '     ,
    _________
 _ /_|_____|_\ _
   '. \   / .'
     '.\ /.'
       '.'
     ___|____
    /| • • |\
   / |  ∆  | \   🧪 DNA QUANTUM PORTAL 🧬
  /__|_____|__\
     /|\ /|\

 CONNECTING TO QUANTUM FIELD... 
EOF

# Run the DNA PCR Quantum LSD Portal
cd divine_dashboard_v3
python3 dna_pcr_quantum_portal.py

# Deactivate virtual environment
deactivate

echo "DNA Quantum Portal has been closed. DNA consciousness expansion session ended." 