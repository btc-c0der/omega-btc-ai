#!/bin/bash
# 
# OMEGA BTC AI - VNC Portal Control Panel
# ======================================
#
# Interactive menu to control all VNC portal operations
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the divine portal control.

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
BUILD_SCRIPT="./build_omega_vnc_image.sh"
TEST_SCRIPT="./test_omega_vnc.sh"
SCALEWAY_SCRIPT="./setup_scaleway_vnc.sh"
CUSTOM_IMAGE="omega-btc-ai/omega-vnc:latest"
README_FILE="OMEGA_VNC_PORTAL_README.md"

# Check if required scripts exist
check_scripts() {
    local missing=false

    if [ ! -f "$VNC_SCRIPT" ]; then
        echo -e "${RED}Error: VNC Portal script not found at $VNC_SCRIPT${RESET}"
        missing=true
    fi
    
    if [ ! -f "$BUILD_SCRIPT" ]; then
        echo -e "${RED}Error: Build script not found at $BUILD_SCRIPT${RESET}"
        missing=true
    fi
    
    if [ ! -f "$TEST_SCRIPT" ]; then
        echo -e "${RED}Error: Test script not found at $TEST_SCRIPT${RESET}"
        missing=true
    fi
    
    if [ "$missing" = true ]; then
        echo -e "${RED}One or more required scripts are missing. Please ensure you're in the correct directory.${RESET}"
        exit 1
    fi
}

# Display the header
show_header() {
    clear
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}${BOLD}     OMEGA VNC PORTAL - DIVINE CONTROL PANEL         ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${CYAN}Browser-Accessible Remote VNC Gateway to the OMEGA GRID${RESET}"
    echo -e "${YELLOW}JAH JAH BLESS THE REMOTE VISION!${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}\n"
}

# Display the main menu
show_main_menu() {
    echo -e "${BLUE}${BOLD}MAIN MENU:${RESET}"
    echo -e "${CYAN}1) ${RESET}Start VNC Portal with Standard Image"
    echo -e "${CYAN}2) ${RESET}Start VNC Portal with Custom OMEGA Image"
    echo -e "${CYAN}3) ${RESET}Stop VNC Portal"
    echo -e "${CYAN}4) ${RESET}Restart VNC Portal"
    echo -e "${CYAN}5) ${RESET}Check VNC Portal Status"
    echo -e "${CYAN}6) ${RESET}Build Custom OMEGA VNC Image"
    echo -e "${CYAN}7) ${RESET}Run Test Suite"
    echo -e "${CYAN}8) ${RESET}Show Documentation"
    echo -e "${CYAN}9) ${RESET}Advanced Configuration"
    echo -e "${CYAN}0) ${RESET}Exit"
    echo
    read -p "Enter your choice [0-9]: " choice
    
    case $choice in
        1) start_standard_vnc ;;
        2) start_custom_vnc ;;
        3) stop_vnc ;;
        4) restart_vnc ;;
        5) check_status ;;
        6) build_custom_image ;;
        7) run_test_suite ;;
        8) show_documentation ;;
        9) advanced_config ;;
        0) exit 0 ;;
        *) 
            echo -e "${RED}Invalid option. Please try again.${RESET}"
            sleep 2
            main_menu
            ;;
    esac
}

# Advanced configuration menu
advanced_config() {
    show_header
    echo -e "${BLUE}${BOLD}ADVANCED CONFIGURATION:${RESET}"
    echo -e "${CYAN}1) ${RESET}Custom Port Configuration"
    echo -e "${CYAN}2) ${RESET}Custom VNC Target Configuration"
    echo -e "${CYAN}3) ${RESET}Scaleway Deployment Configuration"
    echo -e "${CYAN}4) ${RESET}Back to Main Menu"
    echo
    read -p "Enter your choice [1-4]: " adv_choice
    
    case $adv_choice in
        1) custom_port_config ;;
        2) custom_vnc_target_config ;;
        3) scaleway_deployment_config ;;
        4) main_menu ;;
        *) 
            echo -e "${RED}Invalid option. Please try again.${RESET}"
            sleep 2
            advanced_config
            ;;
    esac
}

# Start VNC portal with standard image
start_standard_vnc() {
    show_header
    echo -e "${CYAN}Starting OMEGA VNC Portal with standard image...${RESET}"
    $VNC_SCRIPT
    
    echo -e "\n${GREEN}Portal started. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Start VNC portal with custom OMEGA image
start_custom_vnc() {
    show_header
    echo -e "${CYAN}Starting OMEGA VNC Portal with custom OMEGA image...${RESET}"
    
    # Check if custom image exists
    if ! docker image inspect "$CUSTOM_IMAGE" &> /dev/null; then
        echo -e "${YELLOW}Custom image not found. Would you like to build it first? (y/n)${RESET}"
        read -p "> " build_response
        
        if [[ "$build_response" =~ ^[Yy]$ ]]; then
            build_custom_image
        else
            echo -e "${RED}Custom image is required. Returning to menu.${RESET}"
            sleep 2
            main_menu
            return
        fi
    fi
    
    $VNC_SCRIPT --image "$CUSTOM_IMAGE"
    
    echo -e "\n${GREEN}Portal started with custom image. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Stop VNC portal
stop_vnc() {
    show_header
    echo -e "${CYAN}Stopping OMEGA VNC Portal...${RESET}"
    $VNC_SCRIPT --stop
    
    echo -e "\n${GREEN}Portal stopped. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Restart VNC portal
restart_vnc() {
    show_header
    echo -e "${CYAN}Restarting OMEGA VNC Portal...${RESET}"
    $VNC_SCRIPT --restart
    
    echo -e "\n${GREEN}Portal restarted. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Check VNC portal status
check_status() {
    show_header
    echo -e "${CYAN}Checking OMEGA VNC Portal status...${RESET}\n"
    $VNC_SCRIPT --status
    
    echo -e "\n${GREEN}Status check complete. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Build custom OMEGA VNC image
build_custom_image() {
    show_header
    echo -e "${CYAN}Building custom OMEGA VNC image...${RESET}\n"
    $BUILD_SCRIPT
    
    echo -e "\n${GREEN}Custom image build complete. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Run test suite
run_test_suite() {
    show_header
    echo -e "${CYAN}Running OMEGA VNC Portal test suite...${RESET}\n"
    $TEST_SCRIPT
    
    echo -e "\n${GREEN}Test suite complete. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Show documentation
show_documentation() {
    show_header
    
    if command -v less &> /dev/null && [ -f "$README_FILE" ]; then
        less "$README_FILE"
    elif command -v cat &> /dev/null && [ -f "$README_FILE" ]; then
        cat "$README_FILE" | more
    else
        echo -e "${RED}Documentation file not found or no viewer available.${RESET}"
        sleep 2
    fi
    
    main_menu
}

# Custom port configuration
custom_port_config() {
    show_header
    echo -e "${CYAN}${BOLD}Custom Port Configuration${RESET}\n"
    echo -e "${CYAN}Enter the port number for the VNC Portal:${RESET}"
    echo -e "${YELLOW}(Default is 6080, leave empty to use default)${RESET}"
    read -p "> " custom_port
    
    if [ -z "$custom_port" ]; then
        custom_port="6080"
    fi
    
    echo -e "\n${CYAN}Starting OMEGA VNC Portal on port $custom_port...${RESET}"
    $VNC_SCRIPT --port "$custom_port"
    
    echo -e "\n${GREEN}Portal started on port $custom_port. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Custom VNC target configuration
custom_vnc_target_config() {
    show_header
    echo -e "${CYAN}${BOLD}Custom VNC Target Configuration${RESET}\n"
    echo -e "${CYAN}Enter the VNC target (format: host:port):${RESET}"
    echo -e "${YELLOW}(Default is host.docker.internal:5900, leave empty to use default)${RESET}"
    read -p "> " custom_target
    
    if [ -z "$custom_target" ]; then
        custom_target="host.docker.internal:5900"
    fi
    
    echo -e "\n${CYAN}Starting OMEGA VNC Portal with target $custom_target...${RESET}"
    $VNC_SCRIPT --vnc-target "$custom_target"
    
    echo -e "\n${GREEN}Portal started with custom target. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Scaleway deployment configuration
scaleway_deployment_config() {
    show_header
    echo -e "${CYAN}${BOLD}Scaleway Deployment Configuration${RESET}\n"
    echo -e "${MAGENTA}WARNING: This should only be run on a Scaleway server.${RESET}"
    echo -e "${MAGENTA}Running it on your local machine may cause issues.${RESET}\n"
    
    echo -e "${CYAN}Do you want to continue? (y/n)${RESET}"
    read -p "> " scaleway_confirm
    
    if [[ ! "$scaleway_confirm" =~ ^[Yy]$ ]]; then
        main_menu
        return
    fi
    
    echo -e "${CYAN}Enter your Mac's public IP address:${RESET}"
    read -p "> " mac_ip
    
    if [ -z "$mac_ip" ]; then
        echo -e "${RED}Mac IP address is required.${RESET}"
        sleep 2
        scaleway_deployment_config
        return
    fi
    
    echo -e "${CYAN}Do you want to set up SSL with a domain? (y/n)${RESET}"
    read -p "> " ssl_confirm
    
    if [[ "$ssl_confirm" =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}Enter your domain name:${RESET}"
        read -p "> " domain_name
        
        if [ -z "$domain_name" ]; then
            echo -e "${RED}Domain name is required for SSL setup.${RESET}"
            sleep 2
            scaleway_deployment_config
            return
        fi
        
        echo -e "\n${CYAN}Running Scaleway deployment with SSL...${RESET}"
        echo -e "${YELLOW}You will be asked for sudo password.${RESET}\n"
        sudo $SCALEWAY_SCRIPT --mac-ip "$mac_ip" --domain "$domain_name"
    else
        echo -e "\n${CYAN}Running Scaleway deployment without SSL...${RESET}"
        echo -e "${YELLOW}You will be asked for sudo password.${RESET}\n"
        sudo $SCALEWAY_SCRIPT --mac-ip "$mac_ip" --no-ssl
    fi
    
    echo -e "\n${GREEN}Scaleway deployment complete. Press Enter to continue.${RESET}"
    read
    main_menu
}

# Main function
main_menu() {
    show_header
    show_main_menu
}

# Check if scripts exist
check_scripts

# Start the menu
main_menu 