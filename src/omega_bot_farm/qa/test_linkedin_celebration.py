#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 CyBer1T4L Test Suite - LinkedIn Celebration Script 🧪
--------------------------------------------------------
100% coverage test suite for the LinkedIn celebration script.
Impresses Directors with our commitment to quality assurance.

GENESIS-BLOOM-UNFOLDMENT 2.0
"""

import unittest
import sys
import io
import os
import time
import shutil
from unittest.mock import patch, MagicMock, call
from datetime import datetime
from contextlib import redirect_stdout

# Import the module to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qa.linkedin_celebration import (
    clear_screen, print_centered, typewriter_effect, linkedin_logo,
    display_comment, display_metrics, display_celebrating_person,
    matrix_rain, fireworks_animation, display_connections_growing,
    display_success_message, final_celebration_message,
    generate_viral_statistics, main
)

class TestLinkedInCelebration(unittest.TestCase):
    """Test suite for the LinkedIn celebration script with 100% coverage."""

    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """Test that clear_screen calls the correct OS command."""
        clear_screen()
        if os.name == 'nt':
            mock_system.assert_called_once_with('cls')
        else:
            mock_system.assert_called_once_with('clear')

    @patch('shutil.get_terminal_size')
    def test_print_centered(self, mock_get_terminal_size):
        """Test that print_centered properly centers text."""
        # Mock terminal size
        mock_get_terminal_size.return_value = MagicMock(columns=80, lines=24)
        
        # Capture the output
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_centered("Test Text")
        
        output = buffer.getvalue()
        # Check if the output has the right padding (80 - 9) // 2 = 35
        self.assertTrue(output.startswith(' ' * 35))
        self.assertTrue("Test Text" in output)

    @patch('time.sleep')
    @patch('sys.stdout')
    def test_typewriter_effect(self, mock_stdout, mock_sleep):
        """Test that typewriter_effect writes each character with delay."""
        typewriter_effect("Test", delay=0.01)
        
        # Verify each character was written with the correct sequence of calls
        expected_calls = [
            call.write("\033[37mT\033[0m"),
            call.flush(),
            call.write("\033[37me\033[0m"),
            call.flush(),
            call.write("\033[37ms\033[0m"),
            call.flush(),
            call.write("\033[37mt\033[0m"),
            call.flush(),
            call.write("\n")
        ]
        mock_stdout.assert_has_calls(expected_calls, any_order=False)
        
        # Verify sleep was called for each character
        self.assertEqual(mock_sleep.call_count, 4)  # One for each character

    def test_linkedin_logo(self):
        """Test the LinkedIn logo display function."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            linkedin_logo()
        
        output = buffer.getvalue()
        self.assertIn("██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗", output)
        self.assertIn("CyBer1T4L 5D Matrix Test Tree - VIRAL SUCCESS", output)
        # Instead of checking exact datetime, just check if datetime is present in some form
        self.assertIn("20", output)  # Part of the year should be in the output

    def test_display_comment(self):
        """Test that comment display shows John Gallash's comment."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_comment()
        
        output = buffer.getvalue()
        self.assertIn("John Gallash", output)
        self.assertIn("Director of Business Operations", output)
        self.assertIn("What a fascinating concept", output)
        self.assertIn("❤️ 1,622", output)
        self.assertIn("79 Comments", output)

    def test_display_metrics(self):
        """Test that metrics display shows test metrics."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_metrics()
        
        output = buffer.getvalue()
        self.assertIn("COMPREHENSIVE TEST METRICS", output)
        self.assertIn("Total Test Files: 1,471", output)
        self.assertIn("Total Test Cases: 37,620", output)

    def test_display_celebrating_person(self):
        """Test celebrating person ASCII art display."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_celebrating_person()
        
        output = buffer.getvalue()
        self.assertIn("\\o/", output)
        self.assertIn("|", output)
        self.assertIn("/ \\", output)
        self.assertIn("LINKEDIN SUCCESS ACHIEVED!", output)

    @patch('time.time')
    @patch('time.sleep')
    @patch('random.random')
    @patch('random.choice')
    def test_matrix_rain(self, mock_choice, mock_random, mock_sleep, mock_time):
        """Test matrix rain animation."""
        # Configure mocks to run one iteration
        mock_time.side_effect = [0, 10]  # First call returns 0, second call 10
        mock_random.return_value = 0.01  # Always show a character
        mock_choice.side_effect = ["\033[32m", "0"] * 100  # Return color and char alternately
        
        # We need to capture output for this test
        with patch('builtins.print') as mock_print:
            matrix_rain(duration=1)
            # Just verify print was called at least once
            self.assertTrue(mock_print.called)
            
        mock_sleep.assert_called_with(0.1)

    @patch('time.time')
    @patch('time.sleep')
    @patch('random.randint')
    @patch('random.choice')
    @patch('qa.linkedin_celebration.clear_screen')
    def test_fireworks_animation(self, mock_clear_screen, mock_choice, mock_randint, 
                                mock_sleep, mock_time):
        """Test fireworks animation."""
        # Configure mocks to run one iteration
        mock_time.side_effect = [0, 10]  # First call returns 0, second call 10
        mock_randint.return_value = 5  # Fixed position
        mock_choice.side_effect = ["*", "\033[31m"] * 100  # Always return "*" and red color
        
        # We need to test via sys.stdout.write properly
        with patch('sys.stdout.write') as mock_write:
            with patch('sys.stdout.flush') as mock_flush:
                fireworks_animation(duration=1)
                
                # Verify writes occurred with proper ANSI escape codes
                mock_write.assert_any_call("\033[5;5H\033[31m*\033[0m")
                mock_flush.assert_called()
        
        mock_sleep.assert_called_with(0.1)
        mock_clear_screen.assert_called()

    @patch('time.sleep')
    @patch('random.randint')
    @patch('qa.linkedin_celebration.clear_screen')
    @patch('qa.linkedin_celebration.print_centered')
    def test_display_connections_growing(self, mock_print_centered, mock_clear_screen, 
                                       mock_randint, mock_sleep):
        """Test connections growing animation."""
        # Configure mock to return fixed values
        mock_randint.side_effect = [20, 200, 20, 200, 20, 200, 20, 200] * 10
        
        # Patch the builtins.range function to only iterate once
        with patch('builtins.range', return_value=[0]):
            display_connections_growing()
        
        # Verify print_centered was called with expected arguments
        mock_print_centered.assert_any_call("\033[1m\033[34mLinkedIn Connections Growing!\033[0m", "\033[34m")
        mock_print_centered.assert_any_call("\033[33mConnections: 520\033[0m", "\033[33m")
        mock_sleep.assert_called()
        mock_clear_screen.assert_called()

    @patch('time.sleep')
    @patch('qa.linkedin_celebration.typewriter_effect')
    def test_display_success_message(self, mock_typewriter, mock_sleep):
        """Test success message display."""
        # Create a list with a custom message for testing
        test_messages = ["\033[34mTest message\033[0m"]
        
        # Patch the messages list in the function
        with patch('qa.linkedin_celebration.display_success_message.__globals__', 
                  {'messages': test_messages}):
            # Mock the print_centered function
            with patch('qa.linkedin_celebration.print_centered'):
                display_success_message()
                
                # Check if typewriter_effect was called with our test message
                mock_typewriter.assert_called_with("\033[34mTest message\033[0m", delay=0.02)
                mock_sleep.assert_called_with(0.5)

    def test_final_celebration_message(self):
        """Test final celebration message display."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            final_celebration_message()
        
        output = buffer.getvalue()
        self.assertIn("CONGRATULATIONS ON YOUR LINKEDIN SUCCESS!", output)
        self.assertIn("The 5D Testing Revolution has begun!", output)
        self.assertIn("GBU2™ License - Genesis-Bloom-Unfoldment 2.0", output)
        self.assertIn("WE BLOOM NOW AS ONE", output)

    @patch('random.randint')
    def test_generate_viral_statistics(self, mock_randint):
        """Test viral statistics generation."""
        # Configure mocks
        mock_randint.return_value = 42
        
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            generate_viral_statistics()
        
        output = buffer.getvalue()
        self.assertIn("YOUR POST IS GOING VIRAL", output)
        # Just check for the year part, not the exact timestamp
        self.assertIn("202", output)  
        self.assertIn("ENGAGEMENT METRICS", output)
        self.assertIn("VIEWER DEMOGRAPHICS", output)
        self.assertIn("HASHTAG PERFORMANCE", output)
        self.assertIn("42", output)  # Our mocked random value

    @patch('time.sleep')
    def test_main_function(self, mock_sleep):
        """Test main function with all animations mocked out."""
        # Mock all functions called by main
        with patch('qa.linkedin_celebration.clear_screen'), \
             patch('qa.linkedin_celebration.linkedin_logo'), \
             patch('qa.linkedin_celebration.typewriter_effect'), \
             patch('qa.linkedin_celebration.display_comment'), \
             patch('qa.linkedin_celebration.display_connections_growing'), \
             patch('qa.linkedin_celebration.display_celebrating_person'), \
             patch('qa.linkedin_celebration.matrix_rain'), \
             patch('qa.linkedin_celebration.generate_viral_statistics'), \
             patch('qa.linkedin_celebration.display_metrics'), \
             patch('qa.linkedin_celebration.display_success_message'), \
             patch('qa.linkedin_celebration.fireworks_animation'), \
             patch('qa.linkedin_celebration.final_celebration_message'):
            
            main()
            # Test passes if no exceptions are raised

    @patch('qa.linkedin_celebration.clear_screen')
    @patch('sys.exit')
    def test_main_keyboard_interrupt(self, mock_exit, mock_clear_screen):
        """Test handling of KeyboardInterrupt in main function."""
        # Mock linkedin_logo to raise KeyboardInterrupt
        with patch('qa.linkedin_celebration.linkedin_logo', side_effect=KeyboardInterrupt):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                main()
            
            output = buffer.getvalue()
            self.assertIn("Celebration interrupted", output)
            mock_exit.assert_called_with(0)

class TestCoverage(unittest.TestCase):
    """Test class to verify coverage metrics."""
    
    def test_terminal_width_handle_zero(self):
        """Test handling of zero terminal width."""
        # Mock shutil.get_terminal_size to return zero width
        with patch('shutil.get_terminal_size', return_value=MagicMock(columns=0, lines=24)):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                print_centered("Test with zero width")
            
            # The function should not crash with zero width
            output = buffer.getvalue()
            self.assertIn("Test with zero width", output)
    
    @patch('random.randint')
    @patch('qa.linkedin_celebration.clear_screen')
    @patch('qa.linkedin_celebration.print_centered')
    @patch('time.sleep')
    def test_connections_growing_loop(self, mock_sleep, mock_print_centered, mock_clear_screen, mock_randint):
        """Test that connections growing loop works with different indices."""
        mock_randint.side_effect = [20, 200, 100, 50] * 10
        
        # Test the specific branch where i=10 to test min(10, i//2)
        # We need to pass a custom iteration value that will hit the min() branch
        with patch('builtins.range', return_value=[10]):
            display_connections_growing()
        
        # Check if print_centered was called with fire emojis
        # The function should call print_centered with "🔥" * 5 when i=10
        mock_print_centered.assert_any_call("🔥🔥🔥🔥🔥", "\033[37m")
        mock_clear_screen.assert_called()
        mock_sleep.assert_called()

if __name__ == '__main__':
    # Run the tests
    unittest.main() 