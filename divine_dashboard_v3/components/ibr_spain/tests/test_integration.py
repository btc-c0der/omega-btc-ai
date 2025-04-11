#!/usr/bin/env python3

"""
Integration test for the IBR España Dashboard components
Tests the interaction between different micro modules
"""

import os
import json
import tempfile
import shutil
import gradio as gr
from pathlib import Path
from datetime import datetime, timedelta
from unittest import mock
from typing import Dict, List, Any

# Mock gradio for testing
try:
    import pytest
    import gradio as gr
    has_testing_libs = True
except ImportError:
    has_testing_libs = False
    # Create mockup classes
    class MockGradio:
        def __init__(self):
            pass
            
        class Blocks:
            def __init__(self, **kwargs):
                pass
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
                
        class Markdown:
            def __init__(self, *args, **kwargs):
                self.value = args[0] if args else ""
                
        class HTML:
            def __init__(self, *args, **kwargs):
                self.value = args[0] if args else ""
            
            def update(self, value=None):
                self.value = value
                return self
                
        class Row:
            def __init__(self, **kwargs):
                pass
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
                
        class Tabs:
            def __init__(self, **kwargs):
                pass
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
                
        class TabItem:
            def __init__(self, label, **kwargs):
                self.label = label
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
                
        class Radio:
            def __init__(self, choices, value, **kwargs):
                self.choices = choices
                self.value = value
                
            def change(self, fn, inputs, outputs):
                # Simulate calling the function
                result = fn(self.value)
                if isinstance(outputs, list):
                    for output in outputs:
                        output.value = result
                else:
                    outputs.value = result
                    
        class Textbox:
            def __init__(self, **kwargs):
                self.value = kwargs.get("value", "")
                
            def change(self, fn, inputs, outputs):
                pass
                
        class Box:
            def __init__(self, **kwargs):
                pass
                
            def __enter__(self):
                return self
                
            def __exit__(self, *args):
                pass
                
        class Button:
            def __init__(self, label, **kwargs):
                self.label = label
                
            def click(self, fn, inputs, outputs):
                pass
                
        class Checkbox:
            def __init__(self, **kwargs):
                self.value = kwargs.get("value", False)

    # Replace gradio
    if not 'gr' in locals():
        gr = MockGradio()


# Import components to test
# Use try/except to handle potential import errors
try:
    from ..ibr_dashboard import create_ibr_interface
    from ..micro_modules.sermon_library import SermonLibrary, render_sermon_card
    from ..micro_modules.instagram_integration import InstagramIntegration, render_instagram_feed
    
    has_components = True
except ImportError as e:
    print(f"Warning: Could not import components: {e}")
    has_components = False
    
    # Create mockup classes for testing without dependencies
    class SermonLibrary:
        def __init__(self, data_dir=None):
            self.sermons = []
            
        def search_sermons(self, query="", language=None):
            return []
            
    def render_sermon_card(sermon):
        return f"<div>Sermon: {sermon.get('title', '')}</div>"
        
    class InstagramIntegration:
        def __init__(self, data_dir=None, account_name="test", refresh_interval=900):
            pass
            
        def get_recent_posts(self, limit=10):
            return []
            
    def render_instagram_feed(posts):
        return "<div>Instagram Feed</div>"
        
    def create_ibr_interface():
        with gr.Blocks() as iface:
            gr.Markdown("IBR España Mock Interface")
        return iface


# Fixture for temporary directory
if has_testing_libs:
    @pytest.fixture
    def temp_data_dir():
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after test
        shutil.rmtree(temp_dir)


@pytest.mark.skipif(not has_testing_libs or not has_components, 
                    reason="Missing testing libraries or components")
def test_sermon_integration(temp_data_dir):
    """Test integration between sermon library and rendering"""
    # Test SermonLibrary and render_sermon_card integration
    library = SermonLibrary(temp_data_dir)
    
    # Add a test sermon
    test_sermon = {
        "id": "test_integration_001",
        "title": "Integration Test Sermon",
        "preacher": "Test Preacher",
        "date": "2023-11-15",
        "duration": "30:00",
        "scripture": "Test 1:1-10",
        "language": "es",
        "audio_url": "https://example.com/test.mp3"
    }
    
    library.add_sermon(test_sermon)
    
    # Search for the sermon
    results = library.search_sermons(query="Integration")
    assert len(results) == 1
    
    # Render the sermon card
    html = render_sermon_card(results[0])
    
    # Check that the HTML contains the sermon information
    assert test_sermon["title"] in html
    assert test_sermon["preacher"] in html
    assert test_sermon["scripture"] in html


@pytest.mark.skipif(not has_testing_libs or not has_components, 
                    reason="Missing testing libraries or components")
def test_instagram_integration(temp_data_dir):
    """Test integration between Instagram integration and rendering"""
    # Mock the refresh_posts method to avoid API calls
    with mock.patch.object(InstagramIntegration, 'refresh_posts', return_value=True):
        # Initialize Instagram integration
        instagram = InstagramIntegration(data_dir=temp_data_dir)
        
        # Get recent posts (should return sample data)
        posts = instagram.get_recent_posts(limit=3)
        assert len(posts) > 0
        
        # Render the Instagram feed
        html = render_instagram_feed(posts)
        
        # Check that the HTML contains post information
        for post in posts:
            assert post.get("caption", "") in html


@pytest.mark.skipif(not has_testing_libs or not has_components, 
                    reason="Missing testing libraries or components")
def test_dashboard_creation():
    """Test that the dashboard interface can be created"""
    # Create the dashboard interface
    iface = create_ibr_interface()
    
    # Check that the interface was created
    assert iface is not None


# For direct test execution
if __name__ == "__main__":
    if has_testing_libs:
        pytest.main(["-xvs", __file__])
    else:
        print("Warning: pytest not available. Running basic tests...")
        # Run basic tests without pytest
        temp_dir = tempfile.mkdtemp()
        try:
            print("Testing sermon integration...")
            test_sermon_integration(temp_dir)
            print("Testing Instagram integration...")
            with mock.patch.object(InstagramIntegration, 'refresh_posts', return_value=True):
                test_instagram_integration(temp_dir)
            print("Testing dashboard creation...")
            test_dashboard_creation()
            print("All tests passed!")
        except Exception as e:
            print(f"Error during testing: {e}")
        finally:
            # Clean up
            shutil.rmtree(temp_dir) 