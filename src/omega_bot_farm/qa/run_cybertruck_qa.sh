#!/bin/bash
# ===============================================================================
# CYBERTRUCK QA TEST RUNNER
# ===============================================================================
#
# Industrial-grade test coverage system for Tesla Cybertruck components.
# Follows a strict test-first methodology with micro-modules.
#
# Usage:
#   ./run_cybertruck_qa.sh [OPTIONS]
#
# Options:
#   --component COMPONENT   Run tests for a specific component
#                          (exoskeleton, powertrain, suspension, autopilot)
#   --all                   Run tests for all components
#   --report                Generate comprehensive test reports
#   --coverage              Calculate and display test coverage
#   --verbose               Display verbose output
#   --help                  Display this help message
#
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This script is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0)
# by the Omega Bot Farm team.

# Set script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Default values
COMPONENT=""
RUN_ALL=false
GENERATE_REPORT=false
CALCULATE_COVERAGE=false
VERBOSE=false

# Text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Function to print section header
print_header() {
    echo -e "\n${BOLD}${CYAN}=======================================================${RESET}"
    echo -e "${BOLD}${CYAN}$1${RESET}"
    echo -e "${BOLD}${CYAN}=======================================================${RESET}\n"
}

# Function to print step
print_step() {
    echo -e "\n${BOLD}${YELLOW}[STEP] $1${RESET}"
    echo -e "${YELLOW}$(printf '=%.0s' $(seq 1 $((${#1} + 7))))${RESET}\n"
}

# Display help
show_help() {
    cat << EOF
${BOLD}${CYAN}CYBERTRUCK QA TEST RUNNER${RESET}

Industrial-grade test coverage system for Tesla Cybertruck components.
Follows a strict test-first methodology with micro-modules.

${BOLD}Usage:${RESET}
  ./run_cybertruck_qa.sh [OPTIONS]

${BOLD}Options:${RESET}
  --component COMPONENT   Run tests for a specific component
                         (exoskeleton, powertrain, suspension, autopilot)
  --all                   Run tests for all components
  --report                Generate comprehensive test reports
  --coverage              Calculate and display test coverage
  --verbose               Display verbose output
  --help                  Display this help message

${BOLD}Examples:${RESET}
  ./run_cybertruck_qa.sh --component exoskeleton
  ./run_cybertruck_qa.sh --all --report
  ./run_cybertruck_qa.sh --component powertrain --coverage --verbose
EOF
}

# Check for Python and required packages
check_dependencies() {
    print_step "Checking dependencies"
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3 is required but not found.${RESET}"
        exit 1
    fi
    
    # Check for required packages
    python3 -c "import pytest" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Installing pytest...${RESET}"
        pip install pytest pytest-cov pytest-html
    fi
    
    echo -e "${GREEN}All dependencies satisfied.${RESET}"
}

# Create reports directory if it doesn't exist
create_reports_dir() {
    if [ ! -d "$SCRIPT_DIR/reports" ]; then
        mkdir -p "$SCRIPT_DIR/reports"
        echo -e "${GREEN}Created reports directory.${RESET}"
    fi
}

# Run tests for a specific component
run_component_tests() {
    local component=$1
    print_step "Running tests for component: $component"
    
    # Check if the component test file exists
    local test_file="cybertruck_components/${component}_test.py"
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}Error: Test file not found: $test_file${RESET}"
        return 1
    fi
    
    # Run the tests
    if [ "$VERBOSE" = true ]; then
        python3 -m pytest "$test_file" -v
    else
        python3 -m pytest "$test_file"
    fi
    
    local status=$?
    if [ $status -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}✅ All tests passed for $component!${RESET}"
    else
        echo -e "\n${RED}${BOLD}❌ Some tests failed for $component!${RESET}"
    fi
    
    return $status
}

# Generate reports for a component
generate_component_report() {
    local component=$1
    print_step "Generating report for component: $component"
    
    # Check if the component test file exists
    local test_file="cybertruck_components/${component}_test.py"
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}Error: Test file not found: $test_file${RESET}"
        return 1
    fi
    
    # Generate HTML report
    local report_file="reports/${component}_report.html"
    python3 -m pytest "$test_file" --html="$report_file" --self-contained-html
    
    echo -e "${GREEN}Report generated: $report_file${RESET}"
}

# Calculate coverage for a component
calculate_component_coverage() {
    local component=$1
    print_step "Calculating coverage for component: $component"
    
    # Check if the component test file exists
    local test_file="cybertruck_components/${component}_test.py"
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}Error: Test file not found: $test_file${RESET}"
        return 1
    fi
    
    # Check if the implementation file exists
    local impl_file="cybertruck_components/${component}.py"
    if [ ! -f "$impl_file" ]; then
        echo -e "${RED}Error: Implementation file not found: $impl_file${RESET}"
        return 1
    fi
    
    # Calculate coverage
    local coverage_file="reports/${component}_coverage.xml"
    python3 -m pytest "$test_file" --cov="cybertruck_components" --cov-report="xml:$coverage_file"
    
    # Display coverage info
    python3 -m coverage report
    
    echo -e "${GREEN}Coverage report generated: $coverage_file${RESET}"
}

# Run the comprehensive test workflow using our runner script
run_test_workflow() {
    local component=$1
    print_step "Running comprehensive test workflow for component: $component"
    
    # Run the test workflow
    python3 run_cybertruck_tests.py --component "$component"
}

# Process command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --component)
            COMPONENT="$2"
            shift
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        --report)
            GENERATE_REPORT=true
            shift
            ;;
        --coverage)
            CALCULATE_COVERAGE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${RESET}"
            show_help
            exit 1
            ;;
    esac
done

# Display banner
cat << EOF
${BOLD}${CYAN}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ████████╗██████╗ ██╗   ██╗ ██████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██║   ██║██╔════╝██║ ██╔╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝   ██║   ██████╔╝██║   ██║██║     █████╔╝ 
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗   ██║   ██╔══██╗██║   ██║██║     ██╔═██╗ 
╚██████╗   ██║   ██████╔╝███████╗██║  ██║   ██║   ██║  ██║╚██████╔╝╚██████╗██║  ██╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
                                                                                    
 ██████╗  █████╗     ████████╗███████╗███████╗████████╗██╗███╗   ██╗ ██████╗       
██╔═══██╗██╔══██╗    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██║████╗  ██║██╔════╝       
██║   ██║███████║       ██║   █████╗  ███████╗   ██║   ██║██╔██╗ ██║██║  ███╗      
██║▄▄ ██║██╔══██║       ██║   ██╔══╝  ╚════██║   ██║   ██║██║╚██╗██║██║   ██║      
╚██████╔╝██║  ██║       ██║   ███████╗███████║   ██║   ██║██║ ╚████║╚██████╔╝      
 ╚══▀▀═╝ ╚═╝  ╚═╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝
${RESET}
${BOLD}INDUSTRIAL-GRADE TEST COVERAGE SYSTEM${RESET}
${CYAN}──────────────────────────────────────────────────────────────────────${RESET}
${YELLOW}Follow test-first methodology with micro-modules (max 420 LoC)${RESET}
${CYAN}──────────────────────────────────────────────────────────────────────${RESET}
EOF

# Check dependencies
check_dependencies

# Create reports directory
create_reports_dir

# Define valid components
valid_components=("exoskeleton" "powertrain" "suspension" "autopilot")

# Run tests based on options
if [ "$RUN_ALL" = true ]; then
    print_header "RUNNING TESTS FOR ALL COMPONENTS"
    all_success=true
    
    for component in "${valid_components[@]}"; do
        if [ -f "cybertruck_components/${component}_test.py" ]; then
            if ! run_component_tests "$component"; then
                all_success=false
            fi
            
            if [ "$GENERATE_REPORT" = true ]; then
                generate_component_report "$component"
            fi
            
            if [ "$CALCULATE_COVERAGE" = true ]; then
                calculate_component_coverage "$component"
            fi
        else
            echo -e "${YELLOW}Skipping component $component: Test file not found${RESET}"
        fi
    done
    
    if [ "$all_success" = true ]; then
        echo -e "\n${GREEN}${BOLD}✅ All component tests passed!${RESET}"
    else
        echo -e "\n${RED}${BOLD}❌ Some component tests failed!${RESET}"
        exit 1
    fi
elif [ -n "$COMPONENT" ]; then
    # Check if component is valid
    if [[ ! " ${valid_components[*]} " =~ " ${COMPONENT} " ]]; then
        echo -e "${RED}Error: Invalid component: $COMPONENT${RESET}"
        echo -e "${YELLOW}Valid components are: ${valid_components[*]}${RESET}"
        exit 1
    fi
    
    print_header "RUNNING COMPREHENSIVE TEST WORKFLOW FOR $COMPONENT"
    run_test_workflow "$COMPONENT"
    
    # Additional testing based on options
    if [ "$GENERATE_REPORT" = true ]; then
        generate_component_report "$COMPONENT"
    fi
    
    if [ "$CALCULATE_COVERAGE" = true ]; then
        calculate_component_coverage "$COMPONENT"
    fi
else
    # No component or --all specified, show help
    echo -e "${YELLOW}No component specified. Please use --component or --all option.${RESET}"
    show_help
    exit 1
fi

print_header "CYBERTRUCK QA TESTING COMPLETE"
echo -e "${GREEN}${BOLD}All operations completed successfully!${RESET}"
exit 0 