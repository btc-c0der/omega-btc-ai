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


# Script to archive the Code folder after migrating to GitHub repository
# Created by OMEGA-BTC-AI team

set -e  # Exit on error

# Define paths
CODE_FOLDER="/Users/fsiqueira/Desktop/Code/omega_btc_ai"
GITHUB_FOLDER="/Users/fsiqueira/Desktop/GitHub/omega-btc-ai"
ARCHIVE_FOLDER="/Users/fsiqueira/Desktop/Code_Archive_$(date +%Y%m%d)"

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}=========================================${RESET}"
echo -e "${BLUE}OMEGA BTC AI - Code Folder Archive Script${RESET}"
echo -e "${BLUE}=========================================${RESET}"

# Check if paths exist
if [ ! -d "$CODE_FOLDER" ]; then
  echo -e "${RED}Error: Code folder does not exist at $CODE_FOLDER${RESET}"
  exit 1
fi

if [ ! -d "$GITHUB_FOLDER" ]; then
  echo -e "${RED}Error: GitHub folder does not exist at $GITHUB_FOLDER${RESET}"
  exit 1
fi

# Verify user wants to proceed
echo -e "${YELLOW}This script will:${RESET}"
echo -e "1. Create a comprehensive backup of your Code folder"
echo -e "2. Run tests to verify GitHub repo has all necessary files"
echo -e "3. Archive the Code folder to $ARCHIVE_FOLDER"
echo 
echo -e "${RED}WARNING:${RESET} Make sure you have manually verified all important files have been migrated!"
echo 
read -p "Do you want to proceed? (y/n): " proceed

if [ "$proceed" != "y" ] && [ "$proceed" != "Y" ]; then
  echo -e "${YELLOW}Aborted by user.${RESET}"
  exit 0
fi

# Create backup
echo -e "\n${BLUE}Creating backup of Code folder...${RESET}"
mkdir -p "$ARCHIVE_FOLDER"
rsync -av --exclude='.git' --exclude='__pycache__' "$CODE_FOLDER/" "$ARCHIVE_FOLDER/"
echo -e "${GREEN}Backup created at $ARCHIVE_FOLDER${RESET}"

# Run tests on GitHub repo
echo -e "\n${BLUE}Running tests on GitHub repository...${RESET}"
cd "$GITHUB_FOLDER"
echo -e "${YELLOW}Running unit tests...${RESET}"
python -m pytest tests/unit || {
  echo -e "${RED}Tests failed! Please fix issues before archiving.${RESET}"
  exit 1
}
echo -e "${GREEN}Tests passed.${RESET}"

# Final verification
echo 
echo -e "${YELLOW}Final verification checklist:${RESET}"
echo -e "1. Have you committed all changes to GitHub repository? (y/n)"
read -p "> " committed

if [ "$committed" != "y" ] && [ "$committed" != "Y" ]; then
  echo -e "${RED}Please commit your changes first.${RESET}"
  exit 1
fi

echo -e "2. Have you manually verified important files are migrated? (y/n)"
read -p "> " verified

if [ "$verified" != "y" ] && [ "$verified" != "Y" ]; then
  echo -e "${RED}Please verify files before proceeding.${RESET}"
  exit 1
fi

echo -e "3. Do you have another backup of the Code folder? (y/n)"
read -p "> " another_backup

if [ "$another_backup" != "y" ] && [ "$another_backup" != "Y" ]; then
  echo -e "${YELLOW}Creating additional backup zip file...${RESET}"
  zip -r "${ARCHIVE_FOLDER}.zip" "$CODE_FOLDER"
  echo -e "${GREEN}Additional backup created at ${ARCHIVE_FOLDER}.zip${RESET}"
fi

# Final confirmation
echo 
echo -e "${RED}FINAL WARNING:${RESET} You are about to rename the original Code folder to $ARCHIVE_FOLDER"
echo -e "This is the last step. The Code folder will still exist but with a new name."
read -p "Proceed with archiving? (y/n): " final_confirm

if [ "$final_confirm" != "y" ] && [ "$final_confirm" != "Y" ]; then
  echo -e "${YELLOW}Archiving aborted. Your backups are still at $ARCHIVE_FOLDER${RESET}"
  exit 0
fi

# Rename Code folder 
mv "$CODE_FOLDER" "${CODE_FOLDER}_ARCHIVED_$(date +%Y%m%d)"
echo -e "${GREEN}SUCCESS: Code folder has been archived!${RESET}"
echo -e "${GREEN}Original folder renamed to ${CODE_FOLDER}_ARCHIVED_$(date +%Y%m%d)${RESET}"
echo -e "${GREEN}Backup available at $ARCHIVE_FOLDER${RESET}"
echo -e "${BLUE}Thank you for using OMEGA BTC AI - JAH BLESS THE DIVINE CODE!${RESET}" 