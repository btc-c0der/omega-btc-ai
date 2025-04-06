#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Configuration
------------------------------------

This module provides configuration settings for the Quantum 5D QA Dashboard.
"""

# Quantum dimensions for 5D analysis
QUANTUM_DIMENSIONS = {
    "time": {
        "name": "Time",
        "description": "The temporal dimension tracking metric changes over time",
        "icon": "⏱️"
    },
    "quality": {
        "name": "Quality",
        "description": "Code quality and test success rate",
        "icon": "✓"
    },
    "coverage": {
        "name": "Coverage",
        "description": "Test coverage across codebase",
        "icon": "⬛"
    },
    "performance": {
        "name": "Performance",
        "description": "System performance metrics",
        "icon": "⚡"
    },
    "security": {
        "name": "Security",
        "description": "Security assessment of systems",
        "icon": "🔒"
    }
}

# Theme colors
quantum_theme = {
    "background": "#0a192f",
    "panel": "#172a45",
    "accent": "#64ffda",
    "success": "#36d399",
    "info": "#3abff8",
    "warning": "#fbbd23",
    "error": "#f87272",
    "text": "#e6f1ff",
    "text_secondary": "#8892b0"
}

# Animation configuration
ANIMATION_CONFIG = {
    "enabled": True,
    "speed": "normal",  # slow, normal, fast
    "duration": 0.5  # seconds
}

# Dashboard configuration settings
DASHBOARD_CONFIG = {
    # Metrics collection settings
    "metrics_collection_interval": 10,  # seconds
    "metrics_history_limit": 100,  # number of historical data points to keep
    
    # UI refresh settings
    "ui_refresh_interval": 2,  # seconds
    
    # Thresholds
    "threshold_warning": 70,  # below this is a warning
    "threshold_critical": 50,  # below this is critical
    
    # Animation settings
    "animation_enabled": ANIMATION_CONFIG["enabled"],
    "animation_speed": ANIMATION_CONFIG["speed"],
    "animation_duration": ANIMATION_CONFIG["duration"]
}

# Custom CSS for animations
CUSTOM_CSS = """
/* Blinking cursor animation */
@keyframes blink {
    50% {
        opacity: 0;
    }
}

.cursor {
    animation: blink 1s step-end infinite;
}
"""

# Custom HTML template for Dash index
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
        <style>
            """ + CUSTOM_CSS + """
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Terminal output styling
TERMINAL_STYLES = {
    "background": "#0d1117",
    "text": "#e6f1ff",
    "prompt": "#64ffda",
    "command": "#3abff8",
    "success": "#36d399",
    "warning": "#fbbd23",
    "error": "#f87272",
    "info": "#3abff8"
}

# ANSI color codes for terminal output
ANSI_COLORS = {
    "reset": "\033[0m",
    "info": "\033[94m",  # Blue
    "success": "\033[92m",  # Green
    "warning": "\033[93m",  # Yellow
    "error": "\033[91m",  # Red
    "bold": "\033[1m",
    "underline": "\033[4m",
    "dim": "\033[2m"
} 