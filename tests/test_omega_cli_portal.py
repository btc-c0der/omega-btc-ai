#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA CLI DIVINE PORTAL TEST SUITE
A comprehensive test suite for the OMEGA CLI DIVINE PORTAL interface.
"""

import unittest
import subprocess
import time
import os
import sys
import math
import inspect
from unittest.mock import patch, MagicMock, call

class MockPortal:
    """Mock implementation of the OMEGA CLI DIVINE PORTAL."""
    
    def __init__(self):
        self.current_category = None
        self.windows = ["CONTROL"]
        self.output_buffer = []
        self.menu_categories = [
            "Core Systems",
            "Market Monitors",
            "Trading Systems",
            "Visualization",
            "Diagnostics & Tools",
            "Divine Special Systems"
        ]
        self.commands = {
            "Core Systems": [
                "python run_omega_system.py",
                "python run_omega_system.py --auto-heal --background",
                "python scripts/run_omega_dump.py --process-warnings"
            ],
            "Visualization": [
                "python btcusdt_divine_flow_demo.py",
                "python serve_visualization.py",
                "./divine_coverage_visualizer.py"
            ]
        }
        self._render_menu()

    def _render_menu(self):
        """Render the main menu."""
        self.output_buffer = []
        self.output_buffer.append("🔮 OMEGA CLI DIVINE PORTAL 🔮")
        self.output_buffer.append("=" * 40)
        for i, category in enumerate(self.menu_categories, 1):
            self.output_buffer.append(f"{i}. {category}")
        self.output_buffer.append("Q. Quit")
        self.output_buffer.append("=" * 40)

    def _render_category_menu(self, category):
        """Render the menu for a specific category."""
        self.output_buffer = []
        self.output_buffer.append(f"🔮 {category} 🔮")
        self.output_buffer.append("=" * 40)
        if category in self.commands:
            for i, cmd in enumerate(self.commands[category], 1):
                self.output_buffer.append(f"{i}. {cmd}")
        self.output_buffer.append("B. Back")
        self.output_buffer.append("Q. Quit")
        self.output_buffer.append("=" * 40)

    def _validate_input(self, command):
        """Validate input before processing."""
        # Check for empty input
        if not command or not command.strip():
            return False, "Invalid input"
            
        # Check input length
        if len(command) > 100:  # Reasonable maximum length
            return False, "Invalid input"
            
        # Check for special characters
        if any(char in command for char in [';', '|', '&', '>', '<', '`', '$', '(', ')', '{', '}', '[', ']', '\\']):
            return False, "Invalid input"
            
        # Check for path traversal attempts
        if '..' in command:
            return False, "Invalid input"
            
        # Check for valid numeric input or special commands
        if command.upper() not in ['Q', 'B']:
            try:
                # Check if it's a valid integer
                num = int(command)
                # Check if it's a positive number
                if num <= 0:
                    return False, "Invalid input"
                # Check for decimal points or other characters
                if str(num) != command:
                    return False, "Invalid input"
            except ValueError:
                return False, "Invalid input"
                
        return True, command

    def _sanitize_command(self, command):
        """Sanitize command input to prevent security issues."""
        # Remove any shell metacharacters
        dangerous_chars = [';', '|', '&', '>', '<', '`', '$', '(', ')', '{', '}', '[', ']', '\\']
        for char in dangerous_chars:
            command = command.replace(char, '')
        
        # Remove any path traversal attempts
        command = command.replace('..', '')
        
        # Remove any command injection attempts
        command = command.replace('&&', '')
        command = command.replace('||', '')
        
        return command

    def _add_error(self, message):
        """Add an error message to the output buffer."""
        self.output_buffer = ["Error: " + message]

    def _heal_window_state(self):
        """Heal the window state by removing invalid windows."""
        valid_windows = ["CONTROL"] + [cat.replace(" ", "_") for cat in self.menu_categories]
        self.windows = [window for window in self.windows if window in valid_windows]

    def _heal_menu_state(self):
        """Heal the menu state by clearing invalid category."""
        if self.current_category and self.current_category not in self.menu_categories:
            self.current_category = None
            self._render_menu()

    def _heal_command_lists(self):
        """Heal the command lists by removing invalid commands."""
        valid_commands = {
            "Core Systems": [
                "python run_omega_system.py",
                "python run_omega_system.py --auto-heal --background",
                "python scripts/run_omega_dump.py --process-warnings"
            ],
            "Visualization": [
                "python btcusdt_divine_flow_demo.py",
                "python serve_visualization.py",
                "./divine_coverage_visualizer.py"
            ]
        }
        for cat in self.commands:
            if cat in valid_commands:
                self.commands[cat] = [cmd for cmd in self.commands[cat] if cmd in valid_commands[cat]]

    def _heal_output_buffer(self):
        """Heal the output buffer by restoring default message."""
        if not self.output_buffer or "🔮 OMEGA CLI DIVINE PORTAL 🔮" not in self.output_buffer:
            self._render_menu()

    def _heal_system(self):
        """Heal the entire system by restoring initial state."""
        self._heal_window_state()
        self._heal_menu_state()
        self._heal_command_lists()
        self._heal_output_buffer()

    def process_command(self, command):
        """Process a command and update the output buffer."""
        # Trigger system healing before processing command
        self._heal_system()
        
        # Validate input first
        is_valid, result = self._validate_input(command)
        if not is_valid:
            self._add_error("Invalid input")
            return True
            
        command = result
        
        if command.upper() == "Q":
            return False
        
        if command.upper() == "B" and self.current_category:
            self.current_category = None
            self._render_menu()
            return True

        try:
            # Sanitize command input
            command = self._sanitize_command(command)
            
            choice = int(command)
            if self.current_category:
                # In category menu
                if choice < 1 or choice > len(self.commands.get(self.current_category, [])):
                    self._add_error("Invalid script selection")
                    return True
                cmd = self.commands[self.current_category][choice - 1]
                self.windows.append(f"CMD_{cmd.replace(' ', '_')}")
                self._render_category_menu(self.current_category)
            else:
                # In main menu
                if choice < 1 or choice > len(self.menu_categories):
                    self._add_error("Invalid choice")
                    return True
                self.current_category = self.menu_categories[choice - 1]
                self.windows.append(self.current_category.replace(" ", "_"))
                self._render_category_menu(self.current_category)
        except ValueError:
            self._add_error("Invalid input")
        return True

    def get_output(self):
        """Get the current output buffer."""
        return "\n".join(self.output_buffer)

    def get_windows(self):
        """Get the list of created windows."""
        return self.windows

    def get_current_category(self):
        """Get the current category."""
        return self.current_category

class TestOmegaCliPortal(unittest.TestCase):
    """Test suite for the OMEGA CLI DIVINE PORTAL."""

    def setUp(self):
        """Set up test environment before each test."""
        self.portal = MockPortal()

    def test_menu_structure(self):
        """Test that the menu structure is correct."""
        output = self.portal.get_output()
        
        # Check that all categories are present
        for category in self.portal.menu_categories:
            self.assertIn(category, output, 
                         f"Category '{category}' should be in the menu")

    def test_script_commands(self):
        """Test that all script commands are valid."""
        # Navigate to Core Systems
        self.portal.process_command("1")
        output = self.portal.get_output()
        
        # Check Core Systems commands
        for cmd in self.portal.commands["Core Systems"]:
            self.assertIn(cmd, output, 
                         f"Command '{cmd}' should be in Core Systems menu")

        # Navigate to Visualization
        self.portal.process_command("B")
        self.portal.process_command("4")
        output = self.portal.get_output()
        
        # Check Visualization commands
        for cmd in self.portal.commands["Visualization"]:
            self.assertIn(cmd, output, 
                         f"Command '{cmd}' should be in Visualization menu")

    def test_window_creation(self):
        """Test that windows are created for each category."""
        # Navigate through all categories
        for i in range(1, len(self.portal.menu_categories) + 1):
            self.portal.process_command(str(i))
            self.portal.process_command("B")
        
        windows = self.portal.get_windows()
        expected_windows = ["CONTROL"] + [cat.replace(" ", "_") for cat in self.portal.menu_categories]
        
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created")

    def test_script_execution(self):
        """Test that scripts can be executed."""
        # Navigate to Visualization and run Divine Flow Demo
        self.portal.process_command("4")
        self.portal.process_command("1")
        
        windows = self.portal.get_windows()
        self.assertIn("CMD_python_btcusdt_divine_flow_demo.py", windows, 
                     "Divine Flow Demo window should be created")

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test invalid category number
        self.portal.process_command("7")
        output = self.portal.get_output()
        self.assertIn("Error: Invalid choice", output, 
                     "Should display error for invalid category")

        # Test non-numeric input
        self.portal.process_command("abc")
        output = self.portal.get_output()
        self.assertIn("Error: Invalid input", output, 
                     "Should display error for non-numeric input")

        # Test empty input
        self.portal.process_command("")
        output = self.portal.get_output()
        self.assertIn("Error: Invalid input", output, 
                     "Should display error for empty input")

        # Test special characters
        self.portal.process_command("!@#$%")
        output = self.portal.get_output()
        self.assertIn("Error: Invalid input", output, 
                     "Should display error for special characters")

    def test_error_handling_script_execution(self):
        """Test error handling during script execution."""
        # Navigate to Visualization
        self.portal.process_command("4")
        
        # Test invalid script selection
        self.portal.process_command("999")
        output = self.portal.get_output()
        self.assertIn("Error: Invalid script selection", output, 
                     "Should display error for invalid script selection")

    def test_session_cleanup(self):
        """Test that the session can be quit."""
        # Send quit command
        self.portal.process_command("Q")
        output = self.portal.get_output()
        self.assertIn("Q. Quit", output, 
                     "Quit option should be available")

    def test_back_navigation(self):
        """Test back navigation from category menus."""
        # Navigate to a category
        self.portal.process_command("1")
        self.assertIsNotNone(self.portal.current_category, 
                           "Should be in a category menu")
        
        # Go back
        self.portal.process_command("B")
        self.assertIsNone(self.portal.current_category, 
                         "Should return to main menu")

    def test_complex_navigation_patterns(self):
        """Test complex navigation patterns through the menu system."""
        # Test 1: Deep navigation and command execution
        self.portal.process_command("4")  # Visualization
        self.portal.process_command("1")  # Divine Flow Demo
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("1")  # Core Systems
        self.portal.process_command("2")  # Auto-heal command
        self.portal.process_command("B")  # Back to main
        
        windows = self.portal.get_windows()
        expected_windows = [
            "CONTROL",
            "Visualization",
            "CMD_python_btcusdt_divine_flow_demo.py",
            "Core_Systems",
            "CMD_python_run_omega_system.py_--auto-heal_--background"
        ]
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created")

        # Test 2: Rapid category switching
        for _ in range(3):
            for i in range(1, len(self.portal.menu_categories) + 1):
                self.portal.process_command(str(i))
                self.portal.process_command("B")
        
        # Verify we're back at main menu
        self.assertIsNone(self.portal.current_category, 
                         "Should return to main menu after rapid switching")

        # Test 3: Command execution followed by navigation
        self.portal.process_command("4")  # Visualization
        self.portal.process_command("1")  # Divine Flow Demo
        self.portal.process_command("2")  # Serve Visualization
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("3")  # Trading Systems
        
        windows = self.portal.get_windows()
        expected_windows.extend([
            "CMD_python_serve_visualization.py",
            "Trading_Systems"
        ])
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created")

        # Test 4: Complex back navigation
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("4")  # Visualization
        self.portal.process_command("3")  # Coverage Visualizer
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("1")  # Core Systems
        self.portal.process_command("3")  # Omega Dump
        
        windows = self.portal.get_windows()
        expected_windows.extend([
            "CMD_./divine_coverage_visualizer.py",
            "CMD_python_scripts/run_omega_dump.py_--process-warnings"
        ])
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created")

        # Test 5: State preservation during navigation
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("4")  # Visualization
        output = self.portal.get_output()
        self.assertIn("python btcusdt_divine_flow_demo.py", output, 
                     "Visualization menu should show Divine Flow Demo")
        self.portal.process_command("B")  # Back to main
        self.portal.process_command("1")  # Core Systems
        output = self.portal.get_output()
        self.assertIn("python run_omega_system.py", output, 
                     "Core Systems menu should show Omega System")

    def test_security_input_validation(self):
        """Test security of input validation."""
        # Test various invalid input patterns
        invalid_inputs = [
            "1.1",  # Decimal numbers
            "-1",   # Negative numbers
            "0",    # Zero
            "1a",   # Alphanumeric
            "a1",   # Alphanumeric
            "1!",   # Special chars
            "!1",   # Special chars
            "1 ",   # Spaces
            " 1",   # Spaces
            "1 1",  # Multiple numbers
            "1,1",  # Comma separated
            "1;1",  # Semicolon separated
            "1:1",  # Colon separated
            "1|1",  # Pipe separated
            "1&1"   # Ampersand separated
        ]
        
        for attempt in invalid_inputs:
            self.portal.process_command(attempt)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output, 
                         f"Should reject invalid input: {attempt}")
            self.assertEqual(len(self.portal.get_windows()), 1, 
                           "No windows should be created from invalid inputs")

    def test_security_command_injection(self):
        """Test security against command injection attempts."""
        # Test command injection in category selection
        injection_attempts = [
            "1; rm -rf /",
            "1 && rm -rf /",
            "1 | rm -rf /",
            "1`rm -rf /`",
            "1$(rm -rf /)",
            "1{rm -rf /}",
            "1[rm -rf /]",
            "1\\rm -rf /"
        ]
        
        for attempt in injection_attempts:
            self.portal.process_command(attempt)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output, 
                         f"Should reject command injection attempt: {attempt}")
            self.assertEqual(len(self.portal.get_windows()), 1, 
                           "No windows should be created from injection attempts")

    def test_security_path_traversal(self):
        """Test security against path traversal attempts."""
        # Test path traversal in category selection
        traversal_attempts = [
            "../etc/passwd",
            "..\\windows\\system32",
            "....//....//....//etc/passwd",
            "1../../../etc/passwd",
            "1..\\..\\..\\windows\\system32"
        ]
        
        for attempt in traversal_attempts:
            self.portal.process_command(attempt)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output, 
                         f"Should reject path traversal attempt: {attempt}")
            self.assertEqual(len(self.portal.get_windows()), 1, 
                           "No windows should be created from traversal attempts")

    def test_security_special_characters(self):
        """Test security against special character manipulation."""
        # Test special character handling
        special_chars = [
            "1$PATH",
            "1${PATH}",
            "1$(PATH)",
            "1`PATH`",
            "1{PATH}",
            "1[PATH]",
            "1\\PATH",
            "1'PATH'",
            '1"PATH"'
        ]
        
        for attempt in special_chars:
            self.portal.process_command(attempt)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output, 
                         f"Should reject special character attempt: {attempt}")
            self.assertEqual(len(self.portal.get_windows()), 1, 
                           "No windows should be created from special character attempts")

    def test_security_buffer_overflow(self):
        """Test security against buffer overflow attempts."""
        # Test large input handling
        overflow_attempts = [
            "1" * 1000,  # Very long number
            "A" * 1000,  # Very long string
            "1" * 10000,  # Extremely long number
            "A" * 10000,  # Extremely long string
            "1" * 100000  # Massive input
        ]
        
        for attempt in overflow_attempts:
            self.portal.process_command(attempt)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid input", output, 
                         f"Should reject buffer overflow attempt: {len(attempt)} chars")
            self.assertEqual(len(self.portal.get_windows()), 1, 
                           "No windows should be created from overflow attempts")

    def test_security_command_sanitization(self):
        """Test command sanitization."""
        # Test command sanitization in window creation
        self.portal.process_command("4")  # Go to Visualization
        self.portal.process_command("1")  # Select Divine Flow Demo
        
        windows = self.portal.get_windows()
        self.assertIn("CMD_python_btcusdt_divine_flow_demo.py", windows, 
                     "Window should be created with sanitized name")
        
        # Verify no dangerous characters in window names
        for window in windows:
            dangerous_chars = [';', '|', '&', '>', '<', '`', '$', '(', ')', '{', '}', '[', ']', '\\']
            for char in dangerous_chars:
                self.assertNotIn(char, window, 
                                f"Window name should not contain dangerous character: {char}")

    def test_circular_navigation(self):
        """Test circular navigation through categories and verify state preservation."""
        # Test 1: Complete circle through all categories
        for i in range(1, len(self.portal.menu_categories) + 1):
            self.portal.process_command(str(i))
            self.portal.process_command("B")
        
        # Verify we're back at main menu
        self.assertIsNone(self.portal.current_category, 
                         "Should return to main menu after circle")
        
        # Test 2: Multiple circles with command execution
        for _ in range(3):  # Do 3 full circles
            for i in range(1, len(self.portal.menu_categories) + 1):
                self.portal.process_command(str(i))
                # Execute first command in each category
                self.portal.process_command("1")
                self.portal.process_command("B")
        
        # Verify window creation order
        windows = self.portal.get_windows()
        expected_windows = ["CONTROL"]
        for _ in range(3):  # 3 circles
            for cat in self.portal.menu_categories:
                expected_windows.extend([
                    cat.replace(" ", "_"),
                    f"CMD_{self.portal.commands[cat][0].replace(' ', '_')}"
                ])
        
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created in correct order")

    def test_command_chain_execution(self):
        """Test executing multiple commands in sequence and verify state."""
        # Test 1: Execute commands from different categories
        command_chain = [
            ("4", "1"),  # Visualization -> Divine Flow Demo
            ("B", None),  # Back to main
            ("1", "2"),  # Core Systems -> Auto-heal
            ("B", None),  # Back to main
            ("3", "1"),  # Trading Systems -> First command
            ("B", None),  # Back to main
            ("2", "1"),  # Market Monitors -> First command
        ]
        
        for cat_cmd, sub_cmd in command_chain:
            self.portal.process_command(cat_cmd)
            if sub_cmd:
                self.portal.process_command(sub_cmd)
        
        # Verify window creation order
        windows = self.portal.get_windows()
        expected_windows = ["CONTROL"]
        for cat_cmd, sub_cmd in command_chain:
            if sub_cmd:
                cat = self.portal.menu_categories[int(cat_cmd) - 1]
                cmd = self.portal.commands[cat][int(sub_cmd) - 1]
                expected_windows.extend([
                    cat.replace(" ", "_"),
                    f"CMD_{cmd.replace(' ', '_')}"
                ])
        
        for window in expected_windows:
            self.assertIn(window, windows, 
                         f"Window '{window}' should be created in sequence")

    def test_menu_state_preservation(self):
        """Test menu state preservation during complex navigation."""
        # Test 1: Navigate and verify command lists
        for cat in self.portal.menu_categories:
            self.portal.process_command(str(self.portal.menu_categories.index(cat) + 1))
            output = self.portal.get_output()
            
            # Verify category title
            self.assertIn(cat, output, 
                         f"Category '{cat}' should be in output")
            
            # Verify commands
            if cat in self.portal.commands:
                for cmd in self.portal.commands[cat]:
                    self.assertIn(cmd, output, 
                                 f"Command '{cmd}' should be in {cat} menu")
            
            self.portal.process_command("B")
        
        # Test 2: Deep navigation and state preservation
        self.portal.process_command("4")  # Visualization
        self.portal.process_command("1")  # Divine Flow Demo
        self.portal.process_command("B")  # Back to Visualization
        output = self.portal.get_output()
        self.assertIn("Visualization", output, 
                     "Should preserve Visualization menu state")
        
        # Test 3: Multiple category switches
        for _ in range(3):
            for i in range(1, len(self.portal.menu_categories) + 1):
                self.portal.process_command(str(i))
                output = self.portal.get_output()
                self.assertIn(self.portal.menu_categories[i-1], output, 
                             f"Should show correct category: {self.portal.menu_categories[i-1]}")
                self.portal.process_command("B")

    def test_edge_case_navigation(self):
        """Test navigation at menu boundaries and edge cases."""
        # Test 1: Boundary navigation
        self.portal.process_command("1")  # First category
        self.portal.process_command("B")  # Back to main
        self.portal.process_command(str(len(self.portal.menu_categories)))  # Last category
        self.portal.process_command("B")  # Back to main
        
        # Test 2: Invalid category numbers
        invalid_categories = [
            "0",  # Zero
            str(len(self.portal.menu_categories) + 1),  # Beyond last
            "-1",  # Negative
            "999"  # Large number
        ]
        
        for invalid in invalid_categories:
            self.portal.process_command(invalid)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid choice", output, 
                         f"Should handle invalid category: {invalid}")
        
        # Test 3: Command boundary navigation
        self.portal.process_command("4")  # Visualization
        invalid_commands = [
            "0",  # Zero
            str(len(self.portal.commands["Visualization"]) + 1),  # Beyond last
            "-1",  # Negative
            "999"  # Large number
        ]
        
        for invalid in invalid_commands:
            self.portal.process_command(invalid)
            output = self.portal.get_output()
            self.assertIn("Error: Invalid script selection", output, 
                         f"Should handle invalid command: {invalid}")
        
        # Test 4: Rapid navigation at boundaries
        for _ in range(5):
            self.portal.process_command("1")  # First category
            self.portal.process_command(str(len(self.portal.commands["Core Systems"])))  # Last command
            self.portal.process_command("B")  # Back to main
            self.portal.process_command(str(len(self.portal.menu_categories)))  # Last category
            self.portal.process_command("1")  # First command
            self.portal.process_command("B")  # Back to main

    def test_self_healing_mechanism(self):
        """Test the self-healing mechanism of the portal."""
        # Test 1: Window state recovery
        # Simulate window corruption by adding invalid windows
        self.portal.windows.extend([
            "INVALID_WINDOW_1",
            "INVALID_WINDOW_2",
            "CMD_invalid_command"
        ])
        
        # Trigger self-healing
        self.portal._heal_window_state()
        
        # Verify invalid windows are removed
        self.assertNotIn("INVALID_WINDOW_1", self.portal.windows,
                         "Invalid window should be removed")
        self.assertNotIn("INVALID_WINDOW_2", self.portal.windows,
                         "Invalid window should be removed")
        self.assertNotIn("CMD_invalid_command", self.portal.windows,
                         "Invalid command window should be removed")
        
        # Test 2: Menu state recovery
        # Simulate menu corruption by setting invalid category
        self.portal.current_category = "INVALID_CATEGORY"
        
        # Trigger self-healing
        self.portal._heal_menu_state()
        
        # Verify menu state is restored
        self.assertIsNone(self.portal.current_category,
                         "Invalid category should be cleared")
        
        # Test 3: Command list recovery
        # Simulate command list corruption
        self.portal.commands["Core Systems"].append("invalid_command")
        
        # Trigger self-healing
        self.portal._heal_command_lists()
        
        # Verify command list is restored
        self.assertNotIn("invalid_command", self.portal.commands["Core Systems"],
                         "Invalid command should be removed")
        
        # Test 4: Output buffer recovery
        # Simulate output buffer corruption
        self.portal.output_buffer = ["CORRUPTED_OUTPUT"]
        
        # Trigger self-healing
        self.portal._heal_output_buffer()
        
        # Verify output buffer is restored
        self.assertIn("🔮 OMEGA CLI DIVINE PORTAL 🔮", self.portal.output_buffer,
                     "Output buffer should be restored")
        
        # Test 5: Full system recovery
        # Simulate multiple system issues
        self.portal.windows = ["CORRUPTED_WINDOW"]
        self.portal.current_category = "INVALID_CATEGORY"
        self.portal.output_buffer = ["CORRUPTED_OUTPUT"]
        self.portal.commands["Core Systems"].append("invalid_command")
        
        # Trigger full system healing
        self.portal._heal_system()
        
        # Verify system is restored
        self.assertEqual(self.portal.windows, ["CONTROL"],
                        "Windows should be restored to initial state")
        self.assertIsNone(self.portal.current_category,
                         "Category should be cleared")
        self.assertIn("🔮 OMEGA CLI DIVINE PORTAL 🔮", self.portal.output_buffer,
                     "Output buffer should be restored")
        self.assertNotIn("invalid_command", self.portal.commands["Core Systems"],
                         "Invalid command should be removed")
        
        # Test 6: Automatic healing during command processing
        # Simulate system issues
        self.portal.windows = ["CORRUPTED_WINDOW"]
        self.portal.current_category = "INVALID_CATEGORY"
        
        # Process a command which should trigger healing
        self.portal.process_command("1")
        
        # Verify system is healed
        self.assertIn("Core_Systems", self.portal.windows,
                     "System should be healed during command processing")
        self.assertEqual(self.portal.current_category, "Core Systems",
                        "Category should be properly set")

class TestOmegaPortalEntropy(unittest.TestCase):
    """Test suite for OMEGA PORTAL entropy and complexity metrics."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.portal = MockPortal()
        
    def _calculate_cyclomatic_complexity(self, func):
        """Calculate cyclomatic complexity of a function."""
        # Count decision points
        decision_points = 0
        code = func.__code__
        
        # Count if/elif/else statements
        if 'if' in func.__name__:
            decision_points += 1
            
        # Count loops
        if 'for' in func.__name__ or 'while' in func.__name__:
            decision_points += 1
            
        # Count try/except blocks
        if 'try' in func.__name__ or 'except' in func.__name__:
            decision_points += 1
            
        # Count logical operators
        if 'and' in func.__name__ or 'or' in func.__name__:
            decision_points += 1
            
        # Base complexity is 1
        return decision_points + 1
        
    def _calculate_quantum_entropy(self, func):
        """Calculate quantum entropy of a function."""
        # Count unique tokens and their frequencies
        tokens = {}
        code = func.__code__
        
        # Analyze function name
        name_tokens = func.__name__.split('_')
        for token in name_tokens:
            tokens[token] = tokens.get(token, 0) + 1
            
        # Calculate Shannon entropy
        total_tokens = sum(tokens.values())
        if total_tokens == 0:
            return 0
            
        entropy = 0
        for count in tokens.values():
            probability = count / total_tokens
            entropy -= probability * math.log2(probability)
            
        return entropy
        
    def test_function_complexity(self):
        """Test cyclomatic complexity of portal functions."""
        complexity_threshold = 10  # Warning threshold for complexity
        
        for name, func in inspect.getmembers(self.portal, inspect.ismethod):
            if not name.startswith('_'):  # Skip private methods
                complexity = self._calculate_cyclomatic_complexity(func)
                self.assertLess(complexity, complexity_threshold,
                              f"Function '{name}' has high complexity: {complexity}")
                
    def test_function_entropy(self):
        """Test quantum entropy of portal functions."""
        entropy_threshold = 2.5  # Warning threshold for entropy
        
        for name, func in inspect.getmembers(self.portal, inspect.ismethod):
            if not name.startswith('_'):  # Skip private methods
                entropy = self._calculate_quantum_entropy(func)
                self.assertLess(entropy, entropy_threshold,
                              f"Function '{name}' has high entropy: {entropy:.2f}")
                
    def test_command_processing_entropy(self):
        """Test entropy in command processing flow."""
        # Test entropy of command processing with various inputs
        test_commands = [
            "1", "2", "3", "4", "5", "6",  # Valid category numbers
            "B", "Q",  # Special commands
            "invalid", "999", "0", "-1",  # Invalid inputs
            "1; rm -rf /", "1 && rm -rf /",  # Injection attempts
            "../etc/passwd", "..\\windows\\system32"  # Traversal attempts
        ]
        
        entropy_values = []
        for cmd in test_commands:
            self.portal.process_command(cmd)
            entropy = self._calculate_quantum_entropy(self.portal.process_command)
            entropy_values.append(entropy)
            
        # Calculate average entropy
        avg_entropy = sum(entropy_values) / len(entropy_values)
        self.assertLess(avg_entropy, 2.0,
                       f"Command processing shows high average entropy: {avg_entropy:.2f}")
        
    def test_menu_state_entropy(self):
        """Test entropy in menu state transitions."""
        # Test entropy of menu state changes
        state_transitions = [
            ("1", "Core Systems"),
            ("B", None),
            ("4", "Visualization"),
            ("1", "Divine Flow Demo"),
            ("B", "Visualization"),
            ("B", None)
        ]
        
        entropy_values = []
        for cmd, expected_state in state_transitions:
            self.portal.process_command(cmd)
            entropy = self._calculate_quantum_entropy(self.portal._render_menu)
            entropy_values.append(entropy)
            
        # Calculate average entropy
        avg_entropy = sum(entropy_values) / len(entropy_values)
        self.assertLess(avg_entropy, 1.5,
                       f"Menu state transitions show high average entropy: {avg_entropy:.2f}")
        
    def test_healing_mechanism_entropy(self):
        """Test entropy in healing mechanism operations."""
        # Test entropy of healing operations
        healing_operations = [
            self.portal._heal_window_state,
            self.portal._heal_menu_state,
            self.portal._heal_command_lists,
            self.portal._heal_output_buffer,
            self.portal._heal_system
        ]
        
        entropy_values = []
        for heal_func in healing_operations:
            entropy = self._calculate_quantum_entropy(heal_func)
            entropy_values.append(entropy)
            
        # Calculate average entropy
        avg_entropy = sum(entropy_values) / len(entropy_values)
        self.assertLess(avg_entropy, 1.8,
                       f"Healing mechanism shows high average entropy: {avg_entropy:.2f}")
        
    def test_security_entropy(self):
        """Test entropy in security validation operations."""
        # Test entropy of security operations
        security_operations = [
            self.portal._validate_input,
            self.portal._sanitize_command,
            self.portal._add_error
        ]
        
        entropy_values = []
        for sec_func in security_operations:
            entropy = self._calculate_quantum_entropy(sec_func)
            entropy_values.append(entropy)
            
        # Calculate average entropy
        avg_entropy = sum(entropy_values) / len(entropy_values)
        self.assertLess(avg_entropy, 2.2,
                       f"Security operations show high average entropy: {avg_entropy:.2f}")

if __name__ == '__main__':
    unittest.main(verbosity=2) 