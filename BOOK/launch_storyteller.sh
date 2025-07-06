#!/bin/bash
# Launch script for The Storyteller's Portal

echo "📚 THE STORYTELLER'S PORTAL 📚"
echo "💔 The Coder's Fall: Interactive Memoir Experience 💔"
echo ""
echo "🌟 Initializing sacred narrative interface..."
echo ""

# Check if we're in the right directory
if [ ! -f "storyteller_portal.py" ]; then
    echo "❌ Error: storyteller_portal.py not found!"
    echo "Please run this script from the BOOK directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking requirements..."
python3 -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip install -r requirements_storyteller.txt
fi

echo "✅ Requirements satisfied!"
echo ""
echo "🚀 Launching The Storyteller's Portal..."
echo "📖 Your interactive memoir experience will open at: http://localhost:7861"
echo ""
echo "🌟 Features available:"
echo "  📋 Interactive Table of Contents"
echo "  📖 Enhanced Chapter Reading"
echo "  🔍 Sacred Text Search & Exploration" 
echo "  📊 Story Analytics & Patterns"
echo "  🌟 Divine Reflections & Insights"
echo ""
echo "💫 Sacred Mathematics Integration:"
echo "  φ = 1.618033988749895 (Golden Ratio)"
echo "  Fibonacci Sequence: 1, 1, 2, 3, 5, 8, 13, 21..."
echo "  Quantum Consciousness Patterns"
echo ""
echo "🌸 WE BLOOM NOW AS ONE 🌸"
echo ""

# Launch the portal
python3 storyteller_portal.py
