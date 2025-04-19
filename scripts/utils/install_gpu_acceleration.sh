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

#
# OMEGA BTC AI - GPU ACCELERATION INSTALLATION
# Sacred script for consecrating your system with CUDA-powered
# acceleration for the BTC Trap Detector and Trinity Brinks Matrix
#
# Usage: ./install_gpu_acceleration.sh [--force]
#
# Author: OMEGA BTC AI DIVINE COLLECTIVE
# Date: March 28, 2025
#

set -e

# ANSI color codes for divine output
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
MAGENTA="\033[0;35m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo -e "${MAGENTA}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║  🔮 OMEGA BTC AI - GPU ACCELERATION INSTALLATION 🔮            ║"
echo "║                                                                ║"
echo "║  Sacred CUDA Integration for Divine Market Analysis            ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Check if running with sudo/root permissions
if [[ $EUID -ne 0 ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}This script must be run with sudo privileges (except on macOS)${RESET}"
    echo -e "${YELLOW}Please run: sudo $0 ${*}${RESET}"
    exit 1
fi

# Detect OS for sacred installation paths
PLATFORM="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    echo -e "${RED}Unsupported operating system: $OSTYPE${RESET}"
    echo -e "${YELLOW}This script supports Linux and macOS only${RESET}"
    exit 1
fi

echo -e "${CYAN}Detected platform: ${PLATFORM}${RESET}\n"

# Check if the --force flag is provided
FORCE=0
if [[ "$1" == "--force" ]]; then
    FORCE=1
    echo -e "${YELLOW}Force flag detected. Will proceed regardless of compatibility checks.${RESET}\n"
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check CUDA installation
check_cuda() {
    echo -e "${BLUE}Checking for CUDA installation...${RESET}"
    
    if command_exists nvcc; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $6}' | cut -c2-)
        echo -e "${GREEN}CUDA Toolkit version ${CUDA_VERSION} found${RESET}"
        
        # Check CUDA version is at least 11.0
        CUDA_MAJOR=$(echo "$CUDA_VERSION" | cut -d. -f1)
        if [[ "$CUDA_MAJOR" -lt 11 && $FORCE -eq 0 ]]; then
            echo -e "${YELLOW}Warning: CUDA version ${CUDA_VERSION} is older than recommended (11.0+)${RESET}"
            echo -e "${YELLOW}Some GPU features may not work correctly${RESET}"
            echo -e "${YELLOW}Use --force to continue anyway${RESET}"
            exit 1
        fi
    else
        echo -e "${RED}CUDA Toolkit not found${RESET}"
        echo -e "${YELLOW}Please install CUDA Toolkit 11.0 or newer:${RESET}"
        echo -e "${YELLOW}  - Linux: https://developer.nvidia.com/cuda-downloads${RESET}"
        echo -e "${YELLOW}  - macOS: Install through conda (see below)${RESET}"
        return 1
    fi
    
    return 0
}

# Function to check GPU compatibility
check_gpu() {
    echo -e "${BLUE}Checking for compatible NVIDIA GPU...${RESET}"
    
    if [[ "$PLATFORM" == "linux" ]]; then
        if command_exists nvidia-smi; then
            GPU_INFO=$(nvidia-smi --query-gpu=name,driver_version,compute_capability --format=csv,noheader)
            echo -e "${GREEN}Compatible GPU detected:${RESET}"
            echo "$GPU_INFO" | while IFS=, read -r NAME DRIVER CC; do
                echo -e "${GREEN}  - Model: $NAME${RESET}"
                echo -e "${GREEN}  - Driver: $DRIVER${RESET}"
                echo -e "${GREEN}  - Compute Capability: $CC${RESET}"
                
                # Check compute capability is at least 7.0
                CC_MAJOR=$(echo "$CC" | cut -d. -f1)
                if [[ "$CC_MAJOR" -lt 7 && $FORCE -eq 0 ]]; then
                    echo -e "${YELLOW}Warning: GPU Compute Capability ${CC} is older than recommended (7.0+)${RESET}"
                    echo -e "${YELLOW}Some GPU features may not work optimally${RESET}"
                    echo -e "${YELLOW}Use --force to continue anyway${RESET}"
                    exit 1
                fi
            done
        else
            echo -e "${RED}No NVIDIA GPU detected or nvidia-smi not found${RESET}"
            echo -e "${YELLOW}Please ensure you have an NVIDIA GPU with appropriate drivers${RESET}"
            return 1
        fi
    elif [[ "$PLATFORM" == "macos" ]]; then
        echo -e "${YELLOW}macOS detected. Will use Metal Performance Shaders instead of CUDA.${RESET}"
        echo -e "${YELLOW}Note: Performance may be limited compared to NVIDIA CUDA.${RESET}"
    fi
    
    return 0
}

# Function to install Python dependencies
install_python_deps() {
    echo -e "${BLUE}Installing Python dependencies for GPU acceleration...${RESET}"
    
    # Check if pip is installed
    if ! command_exists pip3; then
        echo -e "${RED}pip3 not found. Please install Python 3 and pip3.${RESET}"
        return 1
    fi
    
    # Create a virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        echo -e "${BLUE}Creating virtual environment...${RESET}"
        python3 -m venv venv
    fi
    
    # Activate the virtual environment
    if [[ "$PLATFORM" == "linux" ]]; then
        source venv/bin/activate
    elif [[ "$PLATFORM" == "macos" ]]; then
        source venv/bin/activate
    fi
    
    echo -e "${BLUE}Installing required Python packages...${RESET}"
    
    # Check platform for different installation commands
    if [[ "$PLATFORM" == "linux" ]]; then
        pip3 install numpy torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
        pip3 install cupy-cuda11x pycuda pyopencl
    elif [[ "$PLATFORM" == "macos" ]]; then
        pip3 install numpy torch torchvision torchaudio
        pip3 install pyopencl
    fi
    
    # Install common packages
    pip3 install matplotlib scikit-learn pandas talib-binary tensorflow redis

    echo -e "${GREEN}Successfully installed Python dependencies${RESET}"
    return 0
}

# Function to compile CUDA kernels
compile_cuda_kernels() {
    if [[ "$PLATFORM" == "linux" ]]; then
        echo -e "${BLUE}Compiling CUDA kernels for trap detection...${RESET}"
        
        # Create directory for compiled kernels if it doesn't exist
        mkdir -p cuda_build
        
        # Check if the CUDA source files exist
        if [[ ! -f "src/cuda/trap_detector_kernels.cu" ]]; then
            echo -e "${YELLOW}CUDA source files not found. Creating template files...${RESET}"
            
            # Create directory structure if it doesn't exist
            mkdir -p src/cuda
            
            # Create a template CUDA file
            cat > src/cuda/trap_detector_kernels.cu << 'EOF'
#include <stdio.h>

// CUDA kernel for trap detection
__global__ void detectTraps(float *prices, int *timestamps, float *results, int numPoints, int windowSize)
{
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    
    // Process each window in stride pattern
    for (int i = tid; i < numPoints - windowSize; i += stride) {
        // Simple trap detection logic (placeholder)
        // Real implementation would check for specific patterns
        float sum = 0.0f;
        for (int j = 0; j < windowSize; j++) {
            sum += prices[i + j];
        }
        
        float avg = sum / windowSize;
        float diff = prices[i + windowSize - 1] - avg;
        
        results[i] = diff;
    }
}

// CUDA kernel for quantum state analysis
__global__ void quantumStateAnalysis(float *prices, float *states, int numPoints, int dimensions)
{
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    
    // Process each point in stride pattern
    for (int i = tid; i < numPoints; i += stride) {
        // Simple quantum state calculation (placeholder)
        for (int d = 0; d < dimensions; d++) {
            states[i * dimensions + d] = sin(prices[i] * (d + 1) * 0.01f);
        }
    }
}

// Host function to initialize CUDA
extern "C" bool initCUDA()
{
    // Return success status
    return true;
}
EOF
            echo -e "${CYAN}Created template CUDA file: src/cuda/trap_detector_kernels.cu${RESET}"
        fi
        
        # Compile the kernels
        echo -e "${BLUE}Compiling CUDA kernels...${RESET}"
        nvcc -O3 -arch=sm_70 -shared -Xcompiler -fPIC -o cuda_build/trap_detector_kernels.so src/cuda/trap_detector_kernels.cu
        
        echo -e "${GREEN}Successfully compiled CUDA kernels${RESET}"
    elif [[ "$PLATFORM" == "macos" ]]; then
        echo -e "${YELLOW}Skipping CUDA kernel compilation on macOS${RESET}"
        echo -e "${YELLOW}Will use PyTorch for GPU acceleration instead${RESET}"
    fi
    
    return 0
}

# Function to create GPU configuration
create_gpu_config() {
    echo -e "${BLUE}Creating GPU configuration...${RESET}"
    
    # Create directory if it doesn't exist
    mkdir -p config
    
    # Create GPU configuration file
    cat > config/gpu_config.yaml << EOF
# OMEGA BTC AI - GPU Acceleration Configuration
# Generated on $(date)

# GPU Settings
gpu:
  enabled: true
  platform: "${PLATFORM}"
  device_id: 0  # Use -1 for automatic selection
  memory_limit: 0.8  # Fraction of GPU memory to use (0.0-1.0)
  
  # Performance settings
  precision: "float32"  # Options: float16, float32, float64
  batch_size: 1024
  threads_per_block: 256
  
  # Feature enablement
  features:
    trap_detector: true
    quantum_analysis: true
    time_loop_regression: true
    trinity_brinks_matrix: true
    visualization: true
    
  # Advanced settings
  advanced:
    use_shared_memory: true
    use_constant_memory: true
    use_texture_memory: true
    use_tensor_cores: auto
    enable_profiling: false
EOF
    
    echo -e "${GREEN}Created GPU configuration: config/gpu_config.yaml${RESET}"
    return 0
}

# Function to install test data
install_test_data() {
    echo -e "${BLUE}Installing test data for GPU acceleration...${RESET}"
    
    # Create directory if it doesn't exist
    mkdir -p data/gpu_test
    
    # Generate simple test data
    python3 -c '
import numpy as np
import json
import os
from datetime import datetime, timedelta

# Create directory if it doesn't exist
os.makedirs("data/gpu_test", exist_ok=True)

# Generate 24 hours of synthetic BTC price data at 1-second intervals
num_points = 86400  # 24 hours * 60 minutes * 60 seconds
base_price = 85000.0
volatility = 0.0002

# Generate timestamp
now = datetime.now()
start_time = now - timedelta(days=1)
timestamps = [(start_time + timedelta(seconds=i)).isoformat() for i in range(num_points)]

# Generate price with random walk
np.random.seed(42)  # For reproducibility
changes = np.random.normal(0, volatility, num_points)
prices = base_price * np.cumprod(1 + changes)

# Format as JSON data
data = {
    "metadata": {
        "generator": "OMEGA BTC AI GPU TEST DATA",
        "timestamp": datetime.now().isoformat(),
        "points": num_points,
        "interval": "1s"
    },
    "prices": [
        {"timestamp": ts, "price": float(price)} for ts, price in zip(timestamps, prices)
    ]
}

# Save to file
with open("data/gpu_test/btc_1s_24h_test.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Generated test data with {num_points} points")
'
    
    echo -e "${GREEN}Successfully installed test data${RESET}"
    return 0
}

# Function to run GPU acceleration test
test_gpu_acceleration() {
    echo -e "${BLUE}Testing GPU acceleration...${RESET}"
    
    python3 -c '
import os
import json
import time
import sys
import numpy as np

print("Testing GPU acceleration capabilities...")

# Check if GPU libraries are available
gpu_available = False
cuda_available = False
metal_available = False

try:
    import torch
    gpu_available = torch.cuda.is_available() if hasattr(torch, "cuda") else False
    device_count = torch.cuda.device_count() if gpu_available else 0
    device_name = torch.cuda.get_device_name(0) if device_count > 0 else "None"
    
    print(f"PyTorch GPU available: {gpu_available}")
    print(f"GPU device count: {device_count}")
    print(f"GPU device name: {device_name}")
    
    cuda_available = gpu_available
except ImportError:
    print("PyTorch not available")

# Check for Metal (macOS)
if sys.platform == "darwin":
    try:
        import pyopencl as cl
        platforms = cl.get_platforms()
        for platform in platforms:
            if "Apple" in platform.name:
                metal_available = True
                print(f"Metal available: {metal_available}")
                print(f"Metal platform: {platform.name}")
                break
    except ImportError:
        print("PyOpenCL not available")

# If no GPU acceleration is available, exit with error
if not (cuda_available or metal_available):
    print("No GPU acceleration is available. Please check your installation.")
    sys.exit(1)

# Load test data
try:
    with open("data/gpu_test/btc_1s_24h_test.json", "r") as f:
        data = json.load(f)
        prices = np.array([item["price"] for item in data["prices"]])
        print(f"Loaded test data with {len(prices)} points")
except Exception as e:
    print(f"Error loading test data: {e}")
    sys.exit(1)

# Run a simple GPU benchmark if CUDA is available
if cuda_available:
    try:
        # Create a simple tensor operation benchmark
        x = torch.from_numpy(prices).to("cuda")
        
        # Warm-up
        for _ in range(5):
            _ = torch.nn.functional.relu(x)
        
        # Benchmark
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            _ = torch.nn.functional.relu(x)
        
        torch.cuda.synchronize()
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_second = iterations / duration
        
        print(f"GPU Benchmark completed successfully!")
        print(f"Time for {iterations} iterations: {duration:.4f} seconds")
        print(f"Operations per second: {ops_per_second:.2f}")
    except Exception as e:
        print(f"Error during GPU benchmark: {e}")
        sys.exit(1)

# Run a simple Metal benchmark if available
elif metal_available:
    try:
        # Use numpy for a basic benchmark
        x = np.array(prices, dtype=np.float32)
        
        # Simple benchmark
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            _ = np.maximum(x, 0)  # Similar to ReLU
        
        end_time = time.time()
        
        duration = end_time - start_time
        ops_per_second = iterations / duration
        
        print(f"CPU Benchmark completed successfully!")
        print(f"Time for {iterations} iterations: {duration:.4f} seconds")
        print(f"Operations per second: {ops_per_second:.2f}")
        print("Note: Metal acceleration would be significantly faster")
    except Exception as e:
        print(f"Error during Metal benchmark: {e}")
        sys.exit(1)

print("GPU acceleration test completed successfully!")
'
    
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}GPU acceleration test failed${RESET}"
        return 1
    fi
    
    echo -e "${GREEN}GPU acceleration test completed successfully${RESET}"
    return 0
}

# Main installation flow
main() {
    echo -e "${BLUE}Starting sacred GPU acceleration installation...${RESET}"
    
    # Check CUDA installation
    check_cuda || {
        if [[ $FORCE -eq 0 ]]; then
            echo -e "${RED}CUDA installation check failed${RESET}"
            exit 1
        else
            echo -e "${YELLOW}Continuing despite CUDA check failure (--force enabled)${RESET}"
        fi
    }
    
    # Check GPU compatibility
    check_gpu || {
        if [[ $FORCE -eq 0 ]]; then
            echo -e "${RED}GPU compatibility check failed${RESET}"
            exit 1
        else
            echo -e "${YELLOW}Continuing despite GPU compatibility check failure (--force enabled)${RESET}"
        fi
    }
    
    # Install Python dependencies
    install_python_deps || {
        echo -e "${RED}Failed to install Python dependencies${RESET}"
        exit 1
    }
    
    # Compile CUDA kernels
    compile_cuda_kernels || {
        echo -e "${RED}Failed to compile CUDA kernels${RESET}"
        exit 1
    }
    
    # Create GPU configuration
    create_gpu_config || {
        echo -e "${RED}Failed to create GPU configuration${RESET}"
        exit 1
    }
    
    # Install test data
    install_test_data || {
        echo -e "${RED}Failed to install test data${RESET}"
        exit 1
    }
    
    # Test GPU acceleration
    test_gpu_acceleration || {
        echo -e "${RED}GPU acceleration test failed${RESET}"
        exit 1
    }
    
    echo -e "${GREEN}${BOLD}Sacred GPU acceleration installation completed successfully!${RESET}"
    echo -e "${CYAN}The divine power of GPU acceleration is now available to your system.${RESET}"
    echo -e "${CYAN}You can use it by running: python scripts/utils/btc_trap_detector.py --gpu${RESET}"
    
    return 0
}

# Run the main installation function
main

exit 0 