#!/bin/bash
#
# Clean Quantum Dashboard Logs
# ----------------------------
#
# This script cleans all Quantum Dashboard JSON logs and report files
# to reduce repository size and prevent them from being tracked by git.

set -e

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the absolute path to the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"
QA_DIR="$PROJECT_ROOT/src/omega_bot_farm/qa"
REPORTS_DIR="$PROJECT_ROOT/qa/reports"

echo -e "${BLUE}===== QUANTUM DASHBOARD LOG CLEANER =====${NC}"
echo -e "${BLUE}Project root:${NC} $PROJECT_ROOT"
echo -e "${BLUE}QA directory:${NC} $QA_DIR"
echo -e "${BLUE}Reports directory:${NC} $REPORTS_DIR"

# Function to count and print the number of files that will be deleted
count_files() {
    local dir=$1
    local pattern=$2
    local count=$(find "$dir" -type f -name "$pattern" 2>/dev/null | wc -l)
    echo -e "${YELLOW}Found ${count} files matching ${pattern} in $dir${NC}"
}

# Count files before deletion
echo -e "\n${BLUE}Counting files to be cleaned...${NC}"
count_files "$REPORTS_DIR" "*.json" 
count_files "$REPORTS_DIR" "test_run_*.json"
count_files "$REPORTS_DIR" "quantum_test_report_*.json"
count_files "$REPORTS_DIR" "*_report.html"
count_files "$REPORTS_DIR" "*_report.xml"
count_files "$QA_DIR" "*.json"

# Ask for confirmation
echo -e "\n${YELLOW}This will remove all quantum dashboard logs and reports.${NC}"
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Operation cancelled.${NC}"
    exit 1
fi

# Remove JSON report files from reports dir
echo -e "\n${BLUE}Removing JSON report files...${NC}"
find "$REPORTS_DIR" -type f -name "*.json" -exec rm -f {} \;
find "$REPORTS_DIR" -type f -name "test_run_*.json" -exec rm -f {} \;

# Remove HTML/XML report files from reports dir
echo -e "${BLUE}Removing HTML/XML report files...${NC}"
find "$REPORTS_DIR" -type f -name "*_report.html" -exec rm -f {} \;
find "$REPORTS_DIR" -type f -name "*_report.xml" -exec rm -f {} \;

# Remove data files from QA dir
echo -e "${BLUE}Removing data files...${NC}"
find "$QA_DIR/data" -type f -name "quantum_*.json" -exec rm -f {} \;

# Remove temporary JSON files
echo -e "${BLUE}Removing temporary files...${NC}"
find "$QA_DIR/tmp" -type f -name "quantum_*.json" -exec rm -f {} \;

# Remove JSON files from quantum dashboard assets
echo -e "${BLUE}Removing dashboard asset files...${NC}"
find "$QA_DIR/quantum_dashboard/assets" -type f -name "*.json" -exec rm -f {} \;

# Remove report directories (dated)
echo -e "${BLUE}Removing dated report directories...${NC}"
find "$REPORTS_DIR" -type d -name "20*" -exec rm -rf {} \; 2>/dev/null || true

echo -e "\n${GREEN}✅ Successfully cleaned quantum dashboard logs and reports!${NC}"
echo -e "${YELLOW}Note: These files are now also in .gitignore to prevent them from being tracked.${NC}"
echo -e "${YELLOW}To avoid committing these files, make sure to run this script before pushing changes.${NC}"

# Show remaining files (for verification)
remaining_json=$(find "$REPORTS_DIR" -name "*.json" 2>/dev/null | wc -l)
remaining_html=$(find "$REPORTS_DIR" -name "*.html" 2>/dev/null | wc -l)
remaining_xml=$(find "$REPORTS_DIR" -name "*.xml" 2>/dev/null | wc -l)
echo -e "\n${BLUE}Remaining JSON files:${NC} $remaining_json"
echo -e "${BLUE}Remaining HTML files:${NC} $remaining_html"
echo -e "${BLUE}Remaining XML files:${NC} $remaining_xml"

exit 0 