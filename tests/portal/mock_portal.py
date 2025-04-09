#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA MOCK PORTAL
Sacred implementation of the OMEGA CLI DIVINE PORTAL for testing purposes.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""

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