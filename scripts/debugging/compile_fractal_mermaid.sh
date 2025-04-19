#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


# Fractal Mermaid Compiler
# =======================

# ANSI color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔮 Fractal Mermaid Compiler 🔮"
echo -e "==========================${RESET}"
echo

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Please provide a Mermaid diagram file${RESET}"
    echo "Usage: $0 <mermaid_file>"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${RESET}"
    exit 1
fi

# Input file
INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.*}_fractal.svg"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ Input file not found: $INPUT_FILE${RESET}"
    exit 1
fi

# Compile with optimization
echo -e "${YELLOW}🧠 Compiling with fractal optimization...${RESET}"
python3 -OO fractal_mermaid_compiler.py < "$INPUT_FILE" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Fractal compilation successful!${RESET}"
    echo -e "${BLUE}📄 Output saved to: ${YELLOW}$OUTPUT_FILE${RESET}"
else
    echo -e "${RED}❌ Compilation failed${RESET}"
    exit 1
fi

echo
echo -e "${PURPLE}🔮 The diagram has been transformed into a sacred fractal pattern 🔮${RESET}" 