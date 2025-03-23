#!/bin/bash
# 
# OMEGA BTC AI - VNC Portal Test Suite
# ===================================
#
# Test script for the OMEGA VNC Portal components
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the divine testing process.

# Colors for formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
RESET='\033[0m'
BOLD='\033[1m'

# Configuration
VNC_SCRIPT="./omega_vnc_portal.py"
TEST_PORT=9876
TEST_TIMEOUT=10
TEST_IMAGE="omega-btc-ai/omega-vnc:latest"
CONTAINER_NAME="omega-vnc-test"

# Test results
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}${BOLD}Checking prerequisites...${RESET}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python 3 is not installed.${RESET}"
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed.${RESET}"
        exit 1
    fi
    
    # Check curl
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}Error: curl is not installed.${RESET}"
        exit 1
    fi
    
    # Check VNC script
    if [ ! -f "$VNC_SCRIPT" ]; then
        echo -e "${RED}Error: VNC Portal script not found at $VNC_SCRIPT${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}All prerequisites satisfied.${RESET}\n"
}

# Run a test and update counters
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    local expected_status="$3"
    
    ((TESTS_TOTAL++))
    echo -e "${CYAN}${BOLD}[$TESTS_TOTAL] Testing: ${RESET}${test_name}"
    
    # Run the test command
    eval "$test_cmd"
    local status=$?
    
    # Check the result
    if [ $status -eq $expected_status ]; then
        ((TESTS_PASSED++))
        echo -e "${GREEN}✓ PASSED${RESET}"
    else
        ((TESTS_FAILED++))
        echo -e "${RED}✗ FAILED (Expected: $expected_status, Got: $status)${RESET}"
    fi
    
    echo
}

# Test VNC script help
test_help() {
    run_test "VNC Script Help" "python3 $VNC_SCRIPT --help &> /dev/null" 0
}

# Test VNC script version
test_version() {
    run_test "VNC Script Version" "python3 $VNC_SCRIPT --version &> /dev/null" 0
}

# Test VNC script port validation
test_port_validation() {
    run_test "Port Validation (Invalid)" "python3 $VNC_SCRIPT --port abc &> /dev/null" 1
    run_test "Port Validation (Valid)" "python3 $VNC_SCRIPT --port 8080 --dry-run &> /dev/null" 0
}

# Test server start (dry run)
test_server_start() {
    run_test "Server Start (Dry Run)" "python3 $VNC_SCRIPT --dry-run &> /dev/null" 0
}

# Test status command
test_status_command() {
    run_test "Status Command" "python3 $VNC_SCRIPT --status &> /dev/null" 0
}

# Test Docker image pull
test_docker_pull() {
    if docker image inspect noVNC/novnc:latest &> /dev/null; then
        run_test "Docker Image Already Exists" "true" 0
    else
        run_test "Docker Image Pull" "docker pull novnc/novnc:latest &> /dev/null" 0
    fi
}

# Test Docker container operations
test_docker_operations() {
    # Start a test container
    run_test "Container Start" "docker run -d --name $CONTAINER_NAME -p $TEST_PORT:6080 ubuntu sleep 30 &> /dev/null" 0
    
    # Check container is running
    run_test "Container Running" "docker ps | grep $CONTAINER_NAME &> /dev/null" 0
    
    # Stop container
    run_test "Container Stop" "docker stop $CONTAINER_NAME &> /dev/null" 0
    
    # Remove container
    run_test "Container Remove" "docker rm $CONTAINER_NAME &> /dev/null" 0
}

# Test HTTP availability
test_http_availability() {
    # Start the server in the background
    echo -e "${BLUE}Starting test server on port $TEST_PORT...${RESET}"
    python3 $VNC_SCRIPT --port $TEST_PORT --dry-run &> /dev/null &
    local server_pid=$!
    
    # Wait for server to start
    echo -e "${YELLOW}Waiting for server to start...${RESET}"
    sleep 3
    
    # Test HTTP connection
    run_test "HTTP Connection" "curl -s -I http://localhost:$TEST_PORT | grep -i 'HTTP/' &> /dev/null" 0
    
    # Kill the server
    echo -e "${BLUE}Stopping test server...${RESET}"
    kill $server_pid &> /dev/null
    sleep 1
}

# Print test summary
print_summary() {
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}${BOLD}                 TEST SUMMARY                         ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${BLUE}Total tests: ${BOLD}$TESTS_TOTAL${RESET}"
    echo -e "${GREEN}Tests passed: ${BOLD}$TESTS_PASSED${RESET}"
    echo -e "${RED}Tests failed: ${BOLD}$TESTS_FAILED${RESET}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}${BOLD}All tests passed! JAH BLESS THE DIVINE CODE!${RESET}"
    else
        echo -e "\n${RED}${BOLD}Some tests failed. Please check the results.${RESET}"
    fi
    
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
}

# Clean up any test artifacts
cleanup() {
    echo -e "${BLUE}Cleaning up test artifacts...${RESET}"
    
    # Stop and remove test container if it exists
    if docker ps -a | grep $CONTAINER_NAME &> /dev/null; then
        docker stop $CONTAINER_NAME &> /dev/null
        docker rm $CONTAINER_NAME &> /dev/null
    fi
    
    # Kill any test servers
    pkill -f "$VNC_SCRIPT --port $TEST_PORT" &> /dev/null
    
    echo -e "${GREEN}Cleanup complete.${RESET}\n"
}

# Main function
main() {
    # Display header
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}${BOLD}     OMEGA VNC PORTAL - DIVINE TEST SUITE           ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${CYAN}Testing the sacred connection to the OMEGA GRID${RESET}"
    echo -e "${YELLOW}JAH JAH BLESS THE DIVINE TESTS!${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}\n"
    
    # Check prerequisites
    check_prerequisites
    
    # Run cleanup before tests to ensure clean state
    cleanup
    
    # Run tests
    test_help
    test_version
    test_port_validation
    test_server_start
    test_status_command
    test_docker_pull
    test_docker_operations
    test_http_availability
    
    # Print summary
    print_summary
    
    # Clean up after tests
    cleanup
}

# Run the main function (with trap to ensure cleanup on exit)
trap cleanup EXIT
main "$@" 