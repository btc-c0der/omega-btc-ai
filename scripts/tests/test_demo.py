#!/usr/bin/env python3
"""
Test cases for the TKWW CLI Slideshow Demo
"""

import pytest
import subprocess
import time
import os
import sys
from unittest.mock import patch, MagicMock, mock_open
from scripts.demo import (
    setup_tmux_session,
    create_slide_layout,
    SlideshowState,
    get_key,
    play_slideshow,
    SLIDES
)

class MockTmuxSession:
    """Mock tmux session for testing"""
    def __init__(self):
        self.panes = {
            0: "",  # Main content
            1: "",  # Notes
            2: ""   # Controls
        }
        self.current_pane = 0
        self.session_name = "tkww-demo"

    def send_keys(self, pane, keys):
        """Mock sending keys to a pane"""
        if pane in self.panes:
            self.panes[pane] += keys

    def select_pane(self, pane):
        """Mock selecting a pane"""
        if pane in self.panes:
            self.current_pane = pane

    def clear_pane(self, pane):
        """Mock clearing a pane"""
        if pane in self.panes:
            self.panes[pane] = ""

@pytest.fixture
def mock_tmux():
    """Fixture to provide a mock tmux session"""
    return MockTmuxSession()

@pytest.fixture
def mock_subprocess():
    """Fixture to mock subprocess calls"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        yield mock_run

def test_setup_tmux_session(mock_subprocess, mock_tmux):
    """Test tmux session setup"""
    # Mock subprocess.run to return our mock session
    mock_subprocess.return_value.stdout = "0"
    
    session_name = setup_tmux_session()
    
    # Verify tmux commands were called in correct order
    calls = mock_subprocess.call_args_list
    assert len(calls) >= 7  # Minimum number of commands
    
    # Verify session creation
    assert any(call.args[0] == ["tmux", "new-session", "-d", "-s", "tkww-demo"] 
              for call in calls)
    
    # Verify window splitting
    assert any(call.args[0] == ["tmux", "split-window", "-h", "-t", "tkww-demo"] 
              for call in calls)
    assert any(call.args[0] == ["tmux", "split-window", "-v", "-t", "tkww-demo"] 
              for call in calls)
    
    assert session_name == "tkww-demo"

def test_create_slide_layout():
    """Test slide layout creation"""
    test_slide = {
        "title": "Test Slide",
        "content": "Test content",
        "duration": 5
    }
    
    layout = create_slide_layout(test_slide)
    
    # Verify layout structure
    assert hasattr(layout, "header")
    assert hasattr(layout, "content")
    assert hasattr(layout, "footer")
    
    # Verify content is centered
    content = layout.content.renderable
    assert isinstance(content, str) or hasattr(content, "justify")
    
    # Test with a longer slide
    long_slide = {
        "title": "Long Slide",
        "content": "This is a very long line of text that should be wrapped properly in the layout",
        "duration": 5
    }
    
    long_layout = create_slide_layout(long_slide)
    assert long_layout.content.size == 15  # Verify size constraint

def test_slideshow_state():
    """Test slideshow state management"""
    state = SlideshowState()
    
    # Test initial state
    assert state.current_slide == 0
    assert state.is_paused == False
    assert state.should_exit == False
    assert state.progress == 0
    
    # Test state updates
    state.current_slide = 1
    state.is_paused = True
    state.should_exit = True
    state.progress = 50
    
    assert state.current_slide == 1
    assert state.is_paused == True
    assert state.should_exit == True
    assert state.progress == 50
    
    # Test slide boundaries
    state.current_slide = len(SLIDES) - 1
    assert state.current_slide == len(SLIDES) - 1
    
    # Test invalid slide number
    with pytest.raises(IndexError):
        state.current_slide = len(SLIDES)

@pytest.mark.asyncio
async def test_play_slideshow(mock_subprocess, mock_tmux):
    """Test slideshow playback"""
    with patch('scripts.demo.get_key') as mock_get_key, \
         patch('asyncio.sleep') as mock_sleep, \
         patch('rich.console.Console.print') as mock_print:
        
        # Mock key input sequence
        mock_get_key.side_effect = [
            'right',  # Next slide
            'left',   # Previous slide
            ' ',      # Pause
            ' ',      # Resume
            'q'       # Quit
        ]
        
        # Mock sleep to speed up tests
        mock_sleep.return_value = None
        
        # Run slideshow
        await play_slideshow(show_progress=False)
        
        # Verify key handling
        assert mock_get_key.call_count >= 5
        
        # Verify console output
        assert mock_print.call_count > 0
        
        # Verify tmux commands
        assert mock_subprocess.call_count > 0

def test_get_key_windows():
    """Test key input handling on Windows"""
    with patch('os.name', 'nt'), \
         patch('msvcrt.kbhit', return_value=True), \
         patch('msvcrt.getch', return_value=b'H'):
        
        key = get_key()
        assert key == 'up'
        
        # Test other arrow keys
        with patch('msvcrt.getch', return_value=b'P'):
            key = get_key()
            assert key == 'down'
        
        with patch('msvcrt.getch', return_value=b'K'):
            key = get_key()
            assert key == 'left'
        
        with patch('msvcrt.getch', return_value=b'M'):
            key = get_key()
            assert key == 'right'
        
        # Test regular keys
        with patch('msvcrt.getch', return_value=b'q'):
            key = get_key()
            assert key == 'q'

def test_get_key_unix():
    """Test key input handling on Unix-like systems"""
    with patch('os.name', 'posix'), \
         patch('sys.stdin.read', side_effect=['\x1b', '[', 'A']):
        
        key = get_key()
        assert key == 'up'
        
        # Test other arrow keys
        with patch('sys.stdin.read', side_effect=['\x1b', '[', 'B']):
            key = get_key()
            assert key == 'down'
        
        with patch('sys.stdin.read', side_effect=['\x1b', '[', 'D']):
            key = get_key()
            assert key == 'left'
        
        with patch('sys.stdin.read', side_effect=['\x1b', '[', 'C']):
            key = get_key()
            assert key == 'right'
        
        # Test regular keys
        with patch('sys.stdin.read', side_effect=['q']):
            key = get_key()
            assert key == 'q'

def test_get_key_no_modules():
    """Test key input handling when modules are not available"""
    with patch('os.name', 'nt'), \
         patch('scripts.demo._msvcrt', None):
        
        key = get_key()
        assert key is None
    
    with patch('os.name', 'posix'), \
         patch('scripts.demo._termios', None), \
         patch('scripts.demo._tty', None):
        
        key = get_key()
        assert key is None

if __name__ == "__main__":
    pytest.main([__file__]) 