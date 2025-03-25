#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA MOCK PORTAL TEST
Sacred test cases for the OMEGA CLI DIVINE PORTAL mock implementation.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""

import unittest
from tests.portal.mock_portal import MockPortal

class TestMockPortal(unittest.TestCase):
    """Test cases for the MockPortal class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.portal = MockPortal()
    
    def test_initial_state(self):
        """Test the initial state of the portal."""
        self.assertIsNone(self.portal.get_current_category())
        self.assertEqual(self.portal.get_windows(), ["CONTROL"])
        output = self.portal.get_output()
        self.assertIn("🔮 OMEGA CLI DIVINE PORTAL 🔮", output)
        self.assertIn("Core Systems", output)
        self.assertIn("Visualization", output)
    
    def test_valid_menu_selection(self):
        """Test selecting a valid menu option."""
        self.assertTrue(self.portal.process_command("1"))
        self.assertEqual(self.portal.get_current_category(), "Core Systems")
        output = self.portal.get_output()
        self.assertIn("🔮 Core Systems 🔮", output)
        self.assertIn("python run_omega_system.py", output)
    
    def test_invalid_menu_selection(self):
        """Test selecting an invalid menu option."""
        self.assertTrue(self.portal.process_command("999"))
        output = self.portal.get_output()
        self.assertIn("Error: Invalid choice", output)
    
    def test_back_command(self):
        """Test the back command functionality."""
        # First enter a category
        self.portal.process_command("1")
        self.assertEqual(self.portal.get_current_category(), "Core Systems")
        # Then go back
        self.portal.process_command("B")
        self.assertIsNone(self.portal.get_current_category())
        output = self.portal.get_output()
        self.assertIn("🔮 OMEGA CLI DIVINE PORTAL 🔮", output)
    
    def test_quit_command(self):
        """Test the quit command functionality."""
        self.assertFalse(self.portal.process_command("Q"))
    
    def test_invalid_input(self):
        """Test handling of invalid input."""
        invalid_inputs = ["", "abc", "1.5", ";;", "&&", "..", "|", ">", "<", "`", "$"]
        for cmd in invalid_inputs:
            self.assertTrue(self.portal.process_command(cmd))
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output)
    
    def test_command_selection(self):
        """Test selecting a command from a category."""
        # Enter Core Systems category
        self.portal.process_command("1")
        # Select first command
        self.assertTrue(self.portal.process_command("1"))
        output = self.portal.get_output()
        self.assertIn("python run_omega_system.py", output)
        self.assertIn("CMD_python_run_omega_system.py", self.portal.get_windows())
    
    def test_system_healing(self):
        """Test the system healing functionality."""
        # Corrupt the portal state
        self.portal.current_category = "Invalid Category"
        self.portal.windows.append("Invalid Window")
        self.portal.output_buffer = ["Invalid Output"]
        
        # Process any command to trigger healing
        self.portal.process_command("1")
        
        # Verify the system was healed
        self.assertEqual(self.portal.get_current_category(), "Core Systems")
        self.assertNotIn("Invalid Window", self.portal.get_windows())
        output = self.portal.get_output()
        self.assertIn("🔮 Core Systems 🔮", output)

if __name__ == '__main__':
    unittest.main() 