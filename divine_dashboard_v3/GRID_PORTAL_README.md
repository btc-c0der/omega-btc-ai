# OMEGA GRID PORTAL - Virgil Abloh / OFF-WHITE™ Edition

A unified dashboard for the OMEGA GRID PORTAL CLI commands, featuring a Virgil Abloh / OFF-WHITE™ inspired design.

## Overview

The OMEGA GRID PORTAL integrates all 14 CLI entry points from the original CLI tool into a clean, minimalist web dashboard. The design follows Virgil Abloh's industrial aesthetic with OFF-WHITE visual tone, bold typography, and ample white space.

## Features

- **Unified Command Center**: All CLI commands accessible through a grid of command cards
- **Terminal-Style Output**: Real-time simulation of CLI command execution
- **Bot Management**: Start, stop, and restart bots from the dashboard
- **Custom Commands**: Execute custom commands directly from the interface
- **Virgil Mode**: Toggle the Virgil Abloh-inspired design aesthetic
- **NFT & Web3 Ready**: Reserved space for future NFT and Web3 functionality

## File Structure

```
divine_dashboard_v3/
├── components/
│   └── omega_grid_portal.py     # Backend Python component
├── static/
│   ├── css/
│   │   └── omega-grid-virgil.css # Virgil Abloh-inspired styling
│   └── js/
│       └── omega-grid-virgil.js  # Frontend JavaScript functionality
├── fastapi_app.py               # FastAPI application for the REST API
├── index.html                   # Main HTML file with OMEGA GRID PORTAL section
└── run_grid_portal.sh           # Shell script to run the portal
```

## Setup and Usage

1. Make the run script executable:

   ```
   chmod +x run_grid_portal.sh
   ```

2. Run the portal:

   ```
   ./run_grid_portal.sh
   ```

3. Access the dashboard at <http://localhost:8000>

## Design Philosophy

The design is inspired by Virgil Abloh's work with OFF-WHITE, featuring:

- Minimalist layout with large white space
- Bold Helvetica Neue and monospace fonts
- Black and yellow accent colors
- Industrial-style labeling with quotation marks
- Typography as a key design element
- Overlay elements with large, rotated text

## CLI Integration

The OMEGA GRID PORTAL integrates with the CLI tool located at:
`/src/omega_bot_farm/management/omega_grid_portal.py`

All original CLI commands are preserved and work identically to the command-line version.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, FastAPI
- **Styling**: Virgil Abloh / OFF-WHITE™ inspired design system

## Credits

Designed with inspiration from Virgil Abloh's design philosophy.

"DESIGN" — "COMMAND LINE" — "INDUSTRIAL AESTHETIC"

Copyright (c) 2024 OMEGA BTC AI
