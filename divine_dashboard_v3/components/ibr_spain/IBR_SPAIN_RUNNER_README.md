# IBR España Component Runner

This README provides instructions on how to run the IBR España component of the Divine Dashboard v3 using the provided runner scripts.

## Overview

The IBR España component includes:

- Instagram Manager (main feature)
- Sermon library
- Prayer requests
- Church events
- Devotionals
- Instagram integration

## Running the Component

There are two ways to run the IBR España component:

### 1. Using the Shell Script (Recommended for macOS/Linux)

The shell script automatically sets up the environment, installs required dependencies, and runs the dashboard.

```bash
# Navigate to the divine dashboard directory
cd divine_dashboard_v3

# Make the script executable (if not already)
chmod +x run_ibr_spain.sh

# Run the script
./run_ibr_spain.sh
```

### 2. Using the Python Script (Cross-platform)

The Python script provides more options and works across different platforms.

```bash
# Navigate to the divine dashboard directory
cd divine_dashboard_v3

# Make the script executable (if not already)
chmod +x run_ibr_spain.py

# Run the script with default options
./run_ibr_spain.py

# Or with custom options
./run_ibr_spain.py --port 8000 --share --debug
```

Command-line options:

- `--port`: Set the port number (default: 7860)
- `--share`: Create a public shareable link
- `--debug`: Run in debug mode with verbose logging

## Configuration

Both scripts will create a default configuration file at `divine_dashboard_v3/config/ibr_spain.json` if it doesn't exist. You can customize this file to change:

- Data storage location
- Instagram account name
- Logging level
- API integration settings (if applicable)

Example configuration:

```json
{
  "instagram_manager": {
    "data_dir": "/path/to/your/custom/data/directory",
    "account_name": "ibrespana",
    "logging_level": "INFO",
    "api": {
      "access_token": "YOUR_ACCESS_TOKEN",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

## Prerequisites

- Python 3.7 or higher
- Internet connection for API integration (optional)
- Required Python packages (installed automatically by the scripts):
  - gradio
  - requests
  - pydantic
  - tenacity
  - python-dotenv
  - python-json-logger

## Troubleshooting

If you encounter issues:

1. Check the log file at `divine_dashboard_v3/ibr_spain_dashboard.log`
2. Ensure all dependencies are installed
3. Verify Python version is 3.7 or higher
4. Check if the data directory has proper permissions

## Support

For additional support, contact the OMEGA BTC AI team.

---

© IBR España 2023 | Developed by OMEGA BTC AI
