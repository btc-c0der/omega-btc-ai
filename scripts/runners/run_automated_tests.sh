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


# 🔱 OMEGA BTC AI - Automated Test Runner 🔱
# This script orchestrates the execution of all automated tests

# Divine color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Divine test categories
declare -A TEST_CATEGORIES=(
    ["core"]="Core service functionality tests"
    ["monitoring"]="Monitoring and metrics tests"
    ["security"]="Security and protection tests"
    ["state"]="State management tests"
    ["divine"]="Divine feature tests"
    ["integration"]="Integration and communication tests"
    ["performance"]="Performance and load tests"
    ["recovery"]="Recovery and resilience tests"
)

# Function to display divine banner
display_banner() {
    echo -e "${BLUE}"
    echo "🔱 OMEGA BTC AI - AUTOMATED TEST SUITE 🔱"
    echo "=========================================="
    echo -e "${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed${NC}"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed${NC}"
        exit 1
    }
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed${NC}"
        exit 1
    }
    
    # Check required Python packages
    echo "Checking Python packages..."
    pip3 install -r requirements.txt
    
    echo -e "${GREEN}All prerequisites met${NC}"
}

# Function to run core service tests
run_core_tests() {
    echo -e "${YELLOW}Running core service tests...${NC}"
    
    # Matrix News Service tests
    python3 tests/core/test_matrix_news.py
    
    # Consciousness Service tests
    python3 tests/core/test_consciousness.py
    
    # Temporal Worker tests
    python3 tests/core/test_temporal_worker.py
}

# Function to run monitoring tests
run_monitoring_tests() {
    echo -e "${YELLOW}Running monitoring tests...${NC}"
    
    # Prometheus metrics tests
    python3 tests/monitoring/test_prometheus.py
    
    # Grafana dashboard tests
    python3 tests/monitoring/test_grafana.py
}

# Function to run security tests
run_security_tests() {
    echo -e "${YELLOW}Running security tests...${NC}"
    
    # WAF protection tests
    python3 tests/security/test_waf.py
    
    # Vault integration tests
    python3 tests/security/test_vault.py
}

# Function to run state management tests
run_state_tests() {
    echo -e "${YELLOW}Running state management tests...${NC}"
    
    # Redis integration tests
    python3 tests/state/test_redis.py
    
    # State snapshot tests
    python3 tests/state/test_snapshot.py
}

# Function to run divine feature tests
run_divine_tests() {
    echo -e "${YELLOW}Running divine feature tests...${NC}"
    
    # Fibonacci integration tests
    python3 tests/divine/test_fibonacci.py
    
    # Schumann resonance tests
    python3 tests/divine/test_schumann.py
}

# Function to run integration tests
run_integration_tests() {
    echo -e "${YELLOW}Running integration tests...${NC}"
    
    # Service communication tests
    python3 tests/integration/test_service_communication.py
    
    # Monitoring integration tests
    python3 tests/integration/test_monitoring_integration.py
}

# Function to run performance tests
run_performance_tests() {
    echo -e "${YELLOW}Running performance tests...${NC}"
    
    # Load testing
    python3 tests/performance/test_load.py
    
    # Resource monitoring
    python3 tests/performance/test_resources.py
}

# Function to run recovery tests
run_recovery_tests() {
    echo -e "${YELLOW}Running recovery tests...${NC}"
    
    # Service restart tests
    python3 tests/recovery/test_service_restart.py
    
    # Data persistence tests
    python3 tests/recovery/test_data_persistence.py
}

# Main execution
main() {
    display_banner
    check_prerequisites
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --category)
                CATEGORY="$2"
                shift 2
                ;;
            --all)
                RUN_ALL=true
                shift
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Run specified category or all tests
    if [ "$RUN_ALL" = true ]; then
        run_core_tests
        run_monitoring_tests
        run_security_tests
        run_state_tests
        run_divine_tests
        run_integration_tests
        run_performance_tests
        run_recovery_tests
    elif [ -n "$CATEGORY" ]; then
        case $CATEGORY in
            "core")
                run_core_tests
                ;;
            "monitoring")
                run_monitoring_tests
                ;;
            "security")
                run_security_tests
                ;;
            "state")
                run_state_tests
                ;;
            "divine")
                run_divine_tests
                ;;
            "integration")
                run_integration_tests
                ;;
            "performance")
                run_performance_tests
                ;;
            "recovery")
                run_recovery_tests
                ;;
            *)
                echo "Unknown category: $CATEGORY"
                exit 1
                ;;
        esac
    else
        echo "Please specify --category or --all"
        exit 1
    fi
    
    echo -e "${GREEN}All tests completed${NC}"
}

# Execute main function
main "$@" 