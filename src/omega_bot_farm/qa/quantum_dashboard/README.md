# Quantum 5D QA Matrix Control Dashboard

```
 _______  _______  _        _        _______  _______    _______  ______  
(  ____ \(  ___  )( (    /|( (    /|(  ____ \(  ____ )  (  ____ \(  __  \ 
| (    \/| (   ) ||  \  ( ||  \  ( || (    \/| (    )|  | (    \/| (  \  )
| (_____ | |   | ||   \ | ||   \ | || (__    | (____)|  | (__    | |   ) |
(_____  )| |   | || (\ \) || (\ \) ||  __)   |     __)  |  __)   | |   | |
      ) || |   | || | \   || | \   || (      | (\ (     | (      | |   ) |
/\____) || (___) || )  \  || )  \  || (____/\| ) \ \__  | )      | (__/  )
\_______)(_______)|/    )_)|/    )_)(_______/|/   \__/  |/       (______/ 
                                                                        
 ______   _______  _______           ______   _______  _______           
(  ___ \ (  ___  )(  ___  )|\     /|(  ___ \ (  ___  )(  ____ \|\     /|
| (   ) )| (   ) || (   ) || )   ( || (   ) )| (   ) || (    \/| )   ( |
| (__/ / | |   | || (___) || |   | || (__/ / | |   | || (_____ | (___) |
|  __ (  | |   | ||  ___  || |   | ||  __ (  | |   | |(_____  )|  ___  |
| (  \ \ | |   | || (   ) || |   | || (  \ \ | |   | |      ) || (   ) |
| )___) )| (___) || )   ( || (___) || )___) )| (___) |/\____) || )   ( |
|/ \___/ (_______)|/     \|(_______)|/ \___/ (_______)\_______)|/     \|
```

## Introduction

The Quantum 5D QA Matrix Control Dashboard is a sophisticated monitoring and analysis tool designed for the OMEGA AI BTC system. It provides real-time visualization of quantum metrics, test execution, and system health in a cyberpunk-themed interface.

## Features

- **Real-time Metrics**: Monitor quantum entanglement, coherence, and stability
- **Interactive Visualizations**: Explore 5D quantum metrics with interactive charts
- **Test Runner**: Execute tests directly from the dashboard
- **Matrix Interface**: Cyberpunk-themed UI for enhanced user experience
- **Automatic Version Management**: Dashboard changes are tracked and versioned

## Installation

The dashboard is part of the OMEGA AI BTC project and can be run directly:

```bash
# Navigate to the dashboard directory
cd src/omega_bot_farm/qa

# Run the dashboard with the latest version
python quantum_qa_dashboard_v4.py

# Or use with specific options
python quantum_qa_dashboard_v4.py --port 8052 --browser
```

## Dashboard Versions

The dashboard comes in multiple versions:

| Version | Description | Key Features |
|---------|-------------|-------------|
| v4.x    | Latest release with auto-versioning | Version tracking, auto Git tagging, changelog generation |
| v3.x    | Matrix cyberpunk interface | Test runner integration, enhanced styling |
| v2.x    | Modular refactored version | Component architecture, improved error handling |
| v1.x    | Original dashboard | Basic quantum metrics visualization |

## Auto-Versioning System

The dashboard includes an automatic versioning system that:

1. **Tracks Changes**: Monitors changes to dashboard files
2. **Archives Versions**: Creates snapshots of dashboard releases
3. **Manages Git Tags**: Automatically tags releases in Git
4. **Generates Changelogs**: Creates detailed change documentation

### Version Tracking

The dashboard uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Using Version Management

You can use auto-versioning features with the v4+ dashboard:

```bash
# Run with auto-archiving of changes
python quantum_qa_dashboard_v4.py --auto-archive

# Specify version increment type
python quantum_qa_dashboard_v4.py --auto-archive --version-type minor

# Just check version status without running
python quantum_dashboard_check_version.py --status-only
```

### Version Check Script

A standalone version checker is available:

```bash
# Run the version checker
python -m quantum_dashboard.version_check

# Or use the dashboard check version script
python quantum_dashboard_check_version.py
```

## Connection Management

The dashboard includes smart connection management:

- **Auto Port Detection**: Finds available ports if requested port is in use
- **URL Generation**: Creates access URLs for different network interfaces
- **Browser Opening**: Can automatically open the dashboard in a browser

## Usage Examples

```bash
# Basic usage
python quantum_qa_dashboard_v4.py

# Run on a specific port
python quantum_qa_dashboard_v4.py --port 8055

# Run in debug mode
python quantum_qa_dashboard_v4.py --debug

# Open in browser automatically
python quantum_qa_dashboard_v4.py --browser

# Skip Matrix boot animation
python quantum_qa_dashboard_v4.py --no-matrix-boot

# Auto-archive changes with version bump
python quantum_qa_dashboard_v4.py --auto-archive --version-type minor
```

## Directory Structure

```
quantum_dashboard/
├── __init__.py                # Package initialization with version info
├── app.py                     # Main Dash application
├── callbacks.py               # Dashboard callbacks
├── config.py                  # Configuration settings
├── connection.py              # Connection management
├── layout.py                  # Dashboard layout components
├── metrics.py                 # Quantum metrics calculations
├── test_runner.py             # Test runner interface
├── version_check.py           # Version checking utilities
├── version_manager.py         # Version management system
├── visualization.py           # Data visualization functions
├── assets/                    # Dashboard assets (CSS, JS, images)
│   └── styles.css             # Dashboard styling
└── archives/                  # Archived dashboard versions
    └── v1.0.0/                # Example archived version
```

## Development

For dashboard development:

1. Make your changes to dashboard files
2. Run the dashboard with `--auto-archive` to track changes
3. Use `--version-type` to specify the version increment
4. Check the generated changelogs for documentation

## License

✨ GBU2™ License - Consciousness Level 8 🧬
This dashboard is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸
