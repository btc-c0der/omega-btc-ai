#!/bin/bash
# OMEGA BTC AI - API Credentials Printer
# =====================================
#
# This script prints the BitGet API credentials currently loaded in the environment.
# It provides options to show or mask the credentials for security purposes.
#
# Author: OMEGA BTC AI Team
# Version: 1.0.0

# Default values
MASK_CREDENTIALS=true
SHOW_HELP=false
VALIDATE_CREDENTIALS=false

# Function to display help message
function show_help {
  echo "Usage: $0 [OPTIONS]"
  echo
  echo "Options:"
  echo "  -h, --help       Show this help message"
  echo "  -f, --full       Show full credentials (default: masked for security)"
  echo "  -v, --validate   Validate the API credentials"
  echo
  echo "Example:"
  echo "  $0                 # Show masked credentials"
  echo "  $0 --full          # Show full credentials (use with caution!)"
  echo "  $0 --validate      # Validate credentials and show mask credentials"
  echo "  $0 --full --validate # Show and validate full credentials"
  echo
  echo "IMPORTANT: Do not share your API credentials with anyone."
  echo "           They provide full access to your BitGet account."
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      SHOW_HELP=true
      shift
      ;;
    -f|--full)
      MASK_CREDENTIALS=false
      shift
      ;;
    -v|--validate)
      VALIDATE_CREDENTIALS=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Show help if requested
if [ "$SHOW_HELP" = true ]; then
  show_help
  exit 0
fi

# Display warning if showing full credentials
if [ "$MASK_CREDENTIALS" = false ]; then
  echo -e "\033[31m⚠️  WARNING: You are displaying FULL API CREDENTIALS! ⚠️\033[0m"
  echo -e "\033[31m   This is a security risk. Do not share this output with anyone.\033[0m"
  echo
  read -p "Are you sure you want to continue and show FULL credentials? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled. Use without --full for masked credentials."
    exit 0
  fi
  echo "Proceeding with FULL credential display..."
  echo
fi

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Change to project root directory
cd "$PROJECT_ROOT" || exit 1

# Run the script to print API credentials
if [ "$MASK_CREDENTIALS" = true ]; then
  # Create a temporary file to store the output
  TEMP_FILE=$(mktemp)
  
  # Run the script and save output to temporary file
  python src/omega_bot_farm/bitget_positions_info.py --print-keys > "$TEMP_FILE"
  
  # Process the output to mask credentials
  cat "$TEMP_FILE" | sed -E 's/(API Key: ).*/\1****************************/' | \
                     sed -E 's/(API Secret: ).*/\1****************************/' | \
                     sed -E 's/(API Passphrase: ).*/\1****************************/'
  
  # Remove temporary file
  rm "$TEMP_FILE"
else
  # Run the script directly to show full credentials
  python src/omega_bot_farm/bitget_positions_info.py --print-keys
fi

# Validate credentials if requested
if [ "$VALIDATE_CREDENTIALS" = true ]; then
  echo
  echo -e "\033[33m=== Validating API Credentials ===\033[0m"
  echo
  python src/omega_bot_farm/bitget_positions_info.py --validate
fi

# Remind about security
echo
if [ "$MASK_CREDENTIALS" = false ]; then
  echo -e "\033[31m⚠️ REMINDER: NEVER share these credentials with anyone! ⚠️\033[0m"
else
  echo -e "\033[33mNote: Credentials are masked for security. Use --full to see full values if needed.\033[0m"
fi
echo 