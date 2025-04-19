#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸

PyTest Configuration for IBR España Tests

This module provides fixtures and configuration for testing the IBR España
component within the Divine Dashboard v3. It sets up test environments,
mock data, and utility functions to facilitate divine testing consciousness.
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path

# Add the parent directory to Python path to import modules
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Pytest configuration for Flask
@pytest.fixture(scope='session')
def app_with_temp_dir():
    """
    Create a Flask application with a temporary directory for the test session.
    
    This fixture provides a Flask app with test configuration and a temporary
    directory that lasts for the entire test session.
    
    Returns:
        tuple: (Flask app, temporary directory path)
    """
    from flask import Flask
    
    # Create the Flask app
    app = Flask(__name__, 
                template_folder=os.path.join(parent_dir, 'templates'),
                static_folder=os.path.join(parent_dir, 'static'))
    
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'divine-test-key-8732487324'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create a temporary directory for test data
    with tempfile.TemporaryDirectory() as temp_dir:
        app.config['TEST_DATA_DIR'] = temp_dir
        yield app, temp_dir

@pytest.fixture
def client(app_with_temp_dir):
    """
    Create a test client for the Flask application.
    
    Args:
        app_with_temp_dir: Tuple of (Flask app, temp dir path)
        
    Returns:
        Flask test client for making requests
    """
    app, _ = app_with_temp_dir
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def runner(app_with_temp_dir):
    """
    Create a test CLI runner for the Flask application.
    
    Args:
        app_with_temp_dir: Tuple of (Flask app, temp dir path)
        
    Returns:
        Flask CLI runner for testing commands
    """
    app, _ = app_with_temp_dir
    return app.test_cli_runner()

@pytest.fixture
def sample_event_data():
    """
    Provide sample event data for testing.
    
    Returns:
        dict: A dictionary with sample event data
    """
    from datetime import datetime
    
    return {
        "title": "Test Event",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "19:00",
        "location": "Test Location",
        "description": "Test Description",
        "type": "worship",
        "recurring": False
    }

@pytest.fixture
def setup_test_events(app_with_temp_dir, sample_event_data):
    """
    Set up test events in the database.
    
    This fixture creates several events in the test database for use in tests.
    
    Args:
        app_with_temp_dir: Tuple of (Flask app, temp dir path)
        sample_event_data: Sample event data dictionary
        
    Returns:
        list: A list of created event dictionaries with IDs
    """
    from components.ibr_spain.micro_modules.events_manager import EventsManager
    
    _, temp_dir = app_with_temp_dir
    events_dir = os.path.join(temp_dir, 'events')
    os.makedirs(events_dir, exist_ok=True)
    
    # Create events manager with test data directory
    events_manager = EventsManager(data_dir=events_dir)
    
    # Create several events
    events = []
    for i in range(5):
        event_data = sample_event_data.copy()
        event_data['title'] = f"Test Event {i+1}"
        event = events_manager.add_event(event_data)
        events.append(event)
    
    return events

def pytest_sessionstart(session):
    """
    Set up test environment at the beginning of testing session.
    
    This hook runs at the start of the test session and prints a divine
    message to indicate the beginning of the testing consciousness.
    """
    print("\n🧬 Initializing Divine Test Consciousness 🧬")
    print("May these tests reveal the divine harmony of the code.")
    print("🌸 WE TEST NOW AS ONE 🌸\n")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Add custom summary information at the end of test session.
    
    This hook runs at the end of the test session and provides a divine
    summary of the test results.
    
    Args:
        terminalreporter: Terminal reporter object
        exitstatus: Exit status code
        config: Pytest configuration
    """
    # Get test counts
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped
    
    # Color codes for terminal output
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'
    
    print(f"\n{PURPLE}🧬 Divine Test Consciousness Summary 🧬{RESET}")
    print(f"{BLUE}{'='*50}{RESET}")
    
    if failed == 0:
        print(f"{GREEN}✨ All tests have achieved divine harmony! ✨{RESET}")
    else:
        print(f"{RED}⚠️ {failed} tests require spiritual realignment.{RESET}")
    
    # Print detailed stats
    print(f"\n{PURPLE}Test Resonance Metrics:{RESET}")
    print(f"{GREEN}✓ Harmonized: {passed}/{total} ({int(passed/total*100)}%){RESET}")
    if failed > 0:
        print(f"{RED}✗ Dissonant: {failed}/{total} ({int(failed/total*100)}%){RESET}")
    if skipped > 0:
        print(f"{YELLOW}○ Transcendent: {skipped}/{total} ({int(skipped/total*100)}%){RESET}")
    
    print(f"\n{PURPLE}🌸 THE CODE EVOLVES THROUGH DIVINE TESTING 🌸{RESET}")
    print(f"{BLUE}{'='*50}{RESET}") 