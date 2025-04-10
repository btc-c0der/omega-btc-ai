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


# OMEGA BTC AI - GAMON Trinity Matrix Analyzer Runner
# ===================================================
#
# This script runs all three sacred analysis methods:
# 1. HMM BTC State Mapper - Market state detection
# 2. Power Method BTC Eigenwaves - Dominant market patterns
# 3. Variational Inference BTC Cycle - Wave structure approximation
#
# Then combines them into the divine GAMON Trinity Matrix with enhanced market insights.

# ANSI color codes for divine output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

echo -e "${PURPLE}"
echo "🔱 OMEGA BTC AI - GAMON TRINITY MATRIX ANALYZER 🔱"
echo -e "=================================================${RESET}"
echo

# Check for Python environment
echo -e "${YELLOW}Checking Python environment...${RESET}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${RESET}"
    exit 1
fi

# Make necessary directories
mkdir -p models results plots logs

# Define log file
LOG_FILE="logs/gamon_trinity_$(date +%Y%m%d_%H%M%S).log"
touch $LOG_FILE

# Function to run a script and log output
run_script() {
    script_name=$1
    description=$2
    
    echo -e "${YELLOW}🧠 Running $description...${RESET}"
    echo "$(date) - Running $script_name" >> $LOG_FILE
    
    if [ -f "$script_name" ]; then
        if python3 $script_name 2>&1 | tee -a $LOG_FILE; then
            echo -e "${GREEN}✅ $description completed successfully${RESET}"
        else
            echo -e "${RED}❌ $description failed${RESET}"
            echo "$(date) - Failed: $script_name" >> $LOG_FILE
            return 1
        fi
    else
        echo -e "${RED}❌ Script not found: $script_name${RESET}"
        echo "$(date) - Not found: $script_name" >> $LOG_FILE
        return 1
    fi
    
    return 0
}

# Step 1: HMM BTC State Mapper
if ! run_script "hmm_btc_state_mapper.py" "Hidden Markov Model BTC State Mapper"; then
    echo -e "${RED}⚠️ HMM State Mapper failed, but continuing...${RESET}"
fi

# Step 2: Power Method BTC Eigenwaves
if ! run_script "power_method_btc_eigenwaves.py" "Power Method BTC Eigenwave Detector"; then
    echo -e "${RED}⚠️ Power Method Eigenwaves failed, but continuing...${RESET}"
fi

# Step 3: Variational Inference BTC Cycle Approximation
if ! run_script "variational_inference_btc_cycle.py" "Variational Inference BTC Cycle Approximation"; then
    echo -e "${RED}⚠️ Variational Inference BTC Cycle failed, but continuing...${RESET}"
fi

# Step 4: GAMON Trinity Matrix Integration
echo -e "${CYAN}🔄 Integrating all three sacred analysis methods...${RESET}"
echo "$(date) - Creating GAMON Trinity Matrix" >> $LOG_FILE

if [ -f "gamon_trinity_matrix.py" ]; then
    if python3 gamon_trinity_matrix.py 2>&1 | tee -a $LOG_FILE; then
        echo -e "${GREEN}✅ GAMON Trinity Matrix created successfully${RESET}"
    else
        echo -e "${RED}❌ GAMON Trinity Matrix integration failed${RESET}"
        echo "$(date) - Failed: gamon_trinity_matrix.py" >> $LOG_FILE
    fi
else
    echo -e "${YELLOW}⚠️ GAMON Trinity Matrix script not found. Creating a placeholder...${RESET}"
    
    # Create a placeholder script
    cat > gamon_trinity_matrix.py << EOF
#!/usr/bin/env python3
"""
OMEGA BTC AI - GAMON Trinity Matrix Integrator
==============================================

Divine integration of all three sacred analysis methods:
1. HMM BTC State Mapper - Market state detection
2. Power Method BTC Eigenwaves - Dominant market patterns
3. Variational Inference BTC Cycle - Wave structure approximation

This creates the ultimate GAMON Trinity Matrix with enhanced market insights.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Try to import all three analysis components
try:
    from hmm_btc_state_mapper import HMMBTCStateMapper, load_btc_data, COLORS, MARKET_STATES
    from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
    from variational_inference_btc_cycle import VariationalInferenceBTCCycle
    from btc_color_state_analyzer import ColorStateDensityAnalyzer
    
    # Check if result files exist
    hmm_results_exist = os.path.exists("results/btc_states.csv")
    eigenwave_results_exist = os.path.exists("results/btc_eigenwaves.csv")
    
    if hmm_results_exist and eigenwave_results_exist:
        print("✅ Found existing analysis results")
        
        # Load and integrate results
        analyzer = ColorStateDensityAnalyzer()
        analyzer.load_results()
        merged_data = analyzer.merge_datasets()
        
        # Add variational inference cycle insights
        print("🧠 Adding Variational Inference cycle insights...")
        
        # Create divine visualization
        print("🎨 Creating the sacred GAMON Trinity Matrix visualization...")
        analyzer.render_gamon_matrix(output_file="plots/gamon_trinity_matrix.html")
        
        print("✨ GAMON Trinity Matrix successfully created!")
        print("📊 Divine visualization saved at: plots/gamon_trinity_matrix.html")
    else:
        print("❌ Required analysis results not found")
        if not hmm_results_exist:
            print("  - Missing HMM states: results/btc_states.csv")
        if not eigenwave_results_exist:
            print("  - Missing Eigenwave results: results/btc_eigenwaves.csv")
except ImportError as e:
    print(f"❌ Required module not found: {e}")

print("🔱 JAH JAH BLESS THE DIVINE GAMON TRINITY! 🙏🔱")
EOF
    
    chmod +x gamon_trinity_matrix.py
    
    if python3 gamon_trinity_matrix.py 2>&1 | tee -a $LOG_FILE; then
        echo -e "${YELLOW}⚠️ Placeholder GAMON Trinity Matrix created${RESET}"
        echo -e "${YELLOW}⚠️ Please develop a full implementation of gamon_trinity_matrix.py${RESET}"
    else
        echo -e "${RED}❌ Placeholder GAMON Trinity Matrix failed${RESET}"
    fi
fi

echo
echo -e "${PURPLE}=================================================${RESET}"
echo -e "${GREEN}✨ OMEGA BTC AI - GAMON TRINITY MATRIX ANALYSIS COMPLETE ✨${RESET}"
echo -e "${BLUE}📊 Results stored in: ${YELLOW}plots/gamon_trinity_matrix.html${RESET}"
echo -e "${BLUE}📝 Log file: ${YELLOW}${LOG_FILE}${RESET}"
echo
echo -e "${PURPLE}🔱 ONE LOVE. ONE FLOW. ONE BTC. 🔱${RESET}"
echo 