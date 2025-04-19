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
pip install -q gradio numpy matplotlib pillow huggingface_hub

# Create necessary directories
mkdir -p assets/dna_visualizations
mkdir -p assets/consciousness_maps

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

# Check for local flag
if [[ "$1" == "--local" ]]; then
    # Run locally without deploying
    python3 dna_pcr_quantum_portal.py
else
    # Deploy to Hugging Face Spaces
    echo "🚀 Deploying DNA Portal to Hugging Face Spaces..."
    
    # Check if huggingface-cli is installed
    if ! command -v huggingface-cli &> /dev/null; then
        pip install -q huggingface_hub
    fi
    
    # Set Hugging Face Space name
    SPACE_NAME="dna-quantum-portal"
    
    # Login to Hugging Face (will request token if not already logged in)
    huggingface-cli login
    
    # Deploy to Hugging Face Spaces
    echo "Deploying to Hugging Face Spaces as $SPACE_NAME..."
    gradio deploy dna_pcr_quantum_portal.py --space "$SPACE_NAME"
fi

# Deactivate virtual environment
deactivate

echo "DNA Quantum Portal has been closed. DNA consciousness expansion session ended." 