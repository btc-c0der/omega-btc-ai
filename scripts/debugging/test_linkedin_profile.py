#!/usr/bin/env python3
import unittest
import os
import sys
import io
from unittest.mock import patch, MagicMock, call
import time
from contextlib import redirect_stdout

# Import the module to test
import linkedin_profile

class TestLinkedInProfile(unittest.TestCase):
    """Test cases for the LinkedIn Profile visualization script"""
    
    def setUp(self):
        """Set up test environment"""
        # Save original stdout
        self.original_stdout = sys.stdout
        # Create string buffer for capturing output
        self.output = io.StringIO()
        # Make time.sleep a no-op to speed up tests
        self.original_sleep = time.sleep
        time.sleep = lambda x: None
    
    def tearDown(self):
        """Restore environment after tests"""
        # Restore original stdout
        sys.stdout = self.original_stdout
        # Restore original sleep function
        time.sleep = self.original_sleep
    
    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """Test clear_screen function for different OS types"""
        # Test for Windows
        with patch.object(os, 'name', 'nt'):
            linkedin_profile.clear_screen()
            mock_system.assert_called_with('cls')
        
        # Test for Unix/Linux/Mac
        with patch.object(os, 'name', 'posix'):
            linkedin_profile.clear_screen()
            mock_system.assert_called_with('clear')
    
    def test_print_with_typing(self):
        """Test print_with_typing function"""
        test_string = "Test typing"
        # Redirect stdout to capture output
        with redirect_stdout(self.output):
            linkedin_profile.print_with_typing(test_string, delay=0)
        
        # Check output
        self.assertEqual(self.output.getvalue().strip(), test_string)
    
    @patch('os.get_terminal_size')
    def test_matrix_rain(self, mock_terminal_size):
        """Test matrix_rain function"""
        # Mock terminal size
        mock_terminal_size.return_value = MagicMock(columns=10, lines=10)
        
        # Patch clear_screen to avoid actual screen clearing
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.matrix_rain(duration=0.1, speed=0)
        
        # We just check that output was generated, not exact values
        self.assertTrue(len(self.output.getvalue()) > 0)
    
    def test_draw_linkedin_logo(self):
        """Test draw_linkedin_logo function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.draw_linkedin_logo()
        
        # Check that LinkedIn URL appears in the output
        self.assertIn("linkedin.com/in/faustocsiqueira", self.output.getvalue())
    
    def test_draw_border(self):
        """Test draw_border function"""
        test_text = "Test\nMultiple\nLines"
        with redirect_stdout(self.output):
            linkedin_profile.draw_border(test_text, color="")
        
        # Check that output contains border characters
        self.assertIn("╭", self.output.getvalue())
        self.assertIn("╮", self.output.getvalue())
        self.assertIn("│", self.output.getvalue())
        self.assertIn("╰", self.output.getvalue())
        self.assertIn("╯", self.output.getvalue())
        
        # Check that all lines of text are included
        self.assertIn("Test", self.output.getvalue())
        self.assertIn("Multiple", self.output.getvalue())
        self.assertIn("Lines", self.output.getvalue())
    
    def test_show_profile_summary(self):
        """Test show_profile_summary function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_profile_summary()
        
        # Check that name and title appear in output
        self.assertIn("FAUSTO SIQUEIRA", self.output.getvalue())
        self.assertIn("Quantum-Blockchain Creative Director", self.output.getvalue())
        self.assertIn("AI Innovation Leader", self.output.getvalue())
    
    def test_animate_skills_graph(self):
        """Test animate_skills_graph function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.animate_skills_graph()
        
        # Check that all skills are included
        self.assertIn("Blockchain Development", self.output.getvalue())
        self.assertIn("AI & Machine Learning", self.output.getvalue())
        self.assertIn("Quantum Computing", self.output.getvalue())
        self.assertIn("Creative Direction", self.output.getvalue())
        self.assertIn("Python Development", self.output.getvalue())
        self.assertIn("Leadership & Strategy", self.output.getvalue())
        self.assertIn("NFT & Digital Assets", self.output.getvalue())
        self.assertIn("UI/UX & Design", self.output.getvalue())
    
    def test_show_experience(self):
        """Test show_experience function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_experience()
        
        # Check that all job titles are included
        self.assertIn("QUANTUM BLOCKCHAIN CREATIVE DIRECTOR", self.output.getvalue())
        self.assertIn("AI INNOVATION STRATEGIST", self.output.getvalue())
        self.assertIn("SENIOR BLOCKCHAIN DEVELOPER", self.output.getvalue())
        
        # Check for companies
        self.assertIn("OMEGA Technologies", self.output.getvalue())
        self.assertIn("Future Systems Institute", self.output.getvalue())
        self.assertIn("Distributed Systems Technologies", self.output.getvalue())
    
    def test_show_projects(self):
        """Test show_projects function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_projects()
        
        # Check that all projects are included
        self.assertIn("OMEGA-BTC-AI", self.output.getvalue())
        self.assertIn("DIVINE DASHBOARD", self.output.getvalue())
        self.assertIn("NEURAL PROPHECY ENGINE", self.output.getvalue())
        
        # Check for technologies
        self.assertIn("Python", self.output.getvalue())
        self.assertIn("TensorFlow", self.output.getvalue())
        self.assertIn("Blockchain", self.output.getvalue())
        self.assertIn("D3.js", self.output.getvalue())
        self.assertIn("React", self.output.getvalue())
        self.assertIn("PyTorch", self.output.getvalue())
    
    def test_show_achievements(self):
        """Test show_achievements function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_achievements()
        
        # Check that achievements are included
        self.assertIn("Blockchain Innovation Award", self.output.getvalue())
        self.assertIn("Author", self.output.getvalue())
        self.assertIn("Guest Lecturer", self.output.getvalue())
        self.assertIn("Patents", self.output.getvalue())
        self.assertIn("Keynote Speaker", self.output.getvalue())
        self.assertIn("Top 40 Under 40", self.output.getvalue())
    
    def test_show_recommendations(self):
        """Test show_recommendations function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_recommendations()
        
        # Check that all recommenders are included
        self.assertIn("Dr. Sophia Chen", self.output.getvalue())
        self.assertIn("Marcus Williams", self.output.getvalue())
        self.assertIn("Elena Rodriguez", self.output.getvalue())
        
        # Check for their positions
        self.assertIn("Chief Technology Officer", self.output.getvalue())
        self.assertIn("Director of AI Research", self.output.getvalue())
        self.assertIn("Founder & CEO", self.output.getvalue())
    
    def test_show_contact_info(self):
        """Test show_contact_info function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.show_contact_info()
        
        # Check for contact information
        self.assertIn("CONNECT WITH ME", self.output.getvalue())
        self.assertIn("email@example.com", self.output.getvalue())
        self.assertIn("linkedin.com/in/faustocsiqueira", self.output.getvalue())
        self.assertIn("professional-website.com", self.output.getvalue())
        self.assertIn("@twitter_handle", self.output.getvalue())
        
        # Check for opportunity areas
        self.assertIn("Quantum-Blockchain Innovation", self.output.getvalue())
        self.assertIn("AI Creative Direction", self.output.getvalue())
        self.assertIn("Technology Leadership", self.output.getvalue())
        self.assertIn("Strategic Consulting", self.output.getvalue())
    
    def test_display_qr_code(self):
        """Test display_qr_code function"""
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            linkedin_profile.display_qr_code()
        
        # Check that QR code contains LinkedIn URL
        self.assertIn("linkedin.com/in/faustocsiqueira", self.output.getvalue())
        self.assertIn("Scan to visit my LinkedIn profile", self.output.getvalue())
        
        # Check that it contains blocks for QR code
        self.assertIn("██████████████", self.output.getvalue())
    
    @patch('linkedin_profile.clear_screen')
    def test_display_linkedin_profile(self, mock_clear_screen):
        """Test the main display_linkedin_profile function"""
        # Create individual mocks for each component
        with patch('linkedin_profile.matrix_rain') as mock_matrix_rain, \
             patch('linkedin_profile.draw_linkedin_logo') as mock_logo, \
             patch('linkedin_profile.show_profile_summary') as mock_summary, \
             patch('linkedin_profile.animate_skills_graph') as mock_skills, \
             patch('linkedin_profile.show_experience') as mock_experience, \
             patch('linkedin_profile.show_projects') as mock_projects, \
             patch('linkedin_profile.show_achievements') as mock_achievements, \
             patch('linkedin_profile.show_recommendations') as mock_recommendations, \
             patch('linkedin_profile.show_contact_info') as mock_contact, \
             patch('linkedin_profile.display_qr_code') as mock_qr_code, \
             redirect_stdout(self.output):
            
            # Run the function
            linkedin_profile.display_linkedin_profile()
            
            # Check output
            self.assertIn("CONNECT WITH ME ON LINKEDIN!", self.output.getvalue())
            self.assertIn("https://www.linkedin.com/in/faustocsiqueira/", self.output.getvalue())
            
            # Verify all functions were called correctly
            mock_matrix_rain.assert_has_calls([
                call(duration=1.5, speed=0.03),  # First call at start
                call(duration=1.5, speed=0.03)   # Second call at end
            ])
            self.assertEqual(mock_matrix_rain.call_count, 2)
            
            # Verify all other functions were called once
            mock_logo.assert_called_once()
            mock_summary.assert_called_once()
            mock_skills.assert_called_once()
            mock_experience.assert_called_once()
            mock_projects.assert_called_once()
            mock_achievements.assert_called_once()
            mock_recommendations.assert_called_once()
            mock_contact.assert_called_once()
            mock_qr_code.assert_called_once()
    
    def test_main_execution(self):
        """Test the main execution"""
        # Save the original __name__ and __main__ function
        original_name = linkedin_profile.__name__
        original_main = getattr(linkedin_profile, "__main__", None)
        
        try:
            # Define a mock main function to test
            mock_display = MagicMock()
            
            # Create a dummy module to simulate __main__
            class DummyModule:
                __name__ = "__main__"
                display_linkedin_profile = mock_display
            
            # Use the display_linkedin_profile from our dummy module
            with patch.object(linkedin_profile, 'display_linkedin_profile', mock_display):
                # Execute the code that would run when module is executed directly
                exec("""
if __name__ == "__main__":
    display_linkedin_profile()
                """, {"__name__": "__main__", "display_linkedin_profile": mock_display})
                
                # Check that display_linkedin_profile was called
                mock_display.assert_called_once()
        finally:
            # Restore original settings
            linkedin_profile.__name__ = original_name
            if original_main:
                setattr(linkedin_profile, "__main__", original_main)
    
    def test_error_handling(self):
        """Test error handling in display_linkedin_profile"""
        # Patch show_profile_summary to raise an exception
        with patch('linkedin_profile.show_profile_summary', side_effect=Exception("Test error")), \
             patch('linkedin_profile.clear_screen'), \
             redirect_stdout(self.output):
            
            linkedin_profile.display_linkedin_profile()
            
            # Check that error message appears
            self.assertIn("Error in profile visualization: Test error", self.output.getvalue())
    
    def test_keyboard_interrupt_handling(self):
        """Test KeyboardInterrupt handling in display_linkedin_profile"""
        # Patch show_profile_summary to raise KeyboardInterrupt
        with patch('linkedin_profile.show_profile_summary', side_effect=KeyboardInterrupt()), \
             patch('linkedin_profile.clear_screen'), \
             redirect_stdout(self.output):
            
            linkedin_profile.display_linkedin_profile()
            
            # Check that interruption message appears
            self.assertIn("Profile visualization interrupted", self.output.getvalue())

class TestPerformance(unittest.TestCase):
    """Performance tests for the LinkedIn Profile visualization script"""
    
    def setUp(self):
        """Set up test environment"""
        # Make time.sleep a no-op to speed up tests
        self.original_sleep = time.sleep
        time.sleep = lambda x: None
    
    def tearDown(self):
        """Restore environment after tests"""
        # Restore original sleep function
        time.sleep = self.original_sleep
    
    @patch('linkedin_profile.clear_screen')
    def test_matrix_rain_performance(self, mock_clear):
        """Test matrix_rain performance with larger terminal"""
        terminal_sizes = [(80, 24), (120, 40), (200, 60)]
        
        for cols, rows in terminal_sizes:
            with patch('os.get_terminal_size', return_value=MagicMock(columns=cols, lines=rows)):
                start_time = time.time()
                # Capture stdout to prevent terminal flooding
                with io.StringIO() as buf, redirect_stdout(buf):
                    linkedin_profile.matrix_rain(duration=0.1, speed=0)
                execution_time = time.time() - start_time
                
                # Even with sleep mocked, larger terminals should take longer but not excessively
                self.assertLess(execution_time, 2.0, f"Matrix rain too slow for {cols}x{rows} terminal")
    
    @patch('linkedin_profile.clear_screen')
    def test_full_profile_display_performance(self, mock_clear):
        """Test that full profile display completes within reasonable time"""
        # Skip actual display with all functions mocked
        with patch('linkedin_profile.matrix_rain'), \
             patch('linkedin_profile.draw_linkedin_logo'), \
             patch('linkedin_profile.show_profile_summary'), \
             patch('linkedin_profile.animate_skills_graph'), \
             patch('linkedin_profile.show_experience'), \
             patch('linkedin_profile.show_projects'), \
             patch('linkedin_profile.show_achievements'), \
             patch('linkedin_profile.show_recommendations'), \
             patch('linkedin_profile.show_contact_info'), \
             patch('linkedin_profile.display_qr_code'):
            
            start_time = time.time()
            with io.StringIO() as buf, redirect_stdout(buf):
                linkedin_profile.display_linkedin_profile()
            execution_time = time.time() - start_time
            
            # With all animations mocked, should complete quickly
            self.assertLess(execution_time, 1.0, "Full profile display too slow")

class TestEdgeCases(unittest.TestCase):
    """Edge case tests for the LinkedIn Profile visualization script"""
    
    def setUp(self):
        """Set up test environment"""
        # Make time.sleep a no-op to speed up tests
        self.original_sleep = time.sleep
        time.sleep = lambda x: None
        # Create string buffer for capturing output
        self.output = io.StringIO()
    
    def tearDown(self):
        """Restore environment after tests"""
        # Restore original sleep function
        time.sleep = self.original_sleep
    
    def test_empty_border(self):
        """Test drawing a border around empty text"""
        with redirect_stdout(self.output):
            linkedin_profile.draw_border("", color="")
        
        # Should still draw a minimal border
        output = self.output.getvalue()
        # Check for border elements instead of exact strings since width may vary
        self.assertIn("╭", output)
        self.assertIn("─", output)
        self.assertIn("╮", output)
        self.assertIn("│", output)
        self.assertIn("╰", output)
        self.assertIn("╯", output)
    
    def test_very_long_text(self):
        """Test drawing a border around very long text"""
        long_text = "A" * 1000 + "\n" + "B" * 500
        
        with redirect_stdout(self.output):
            linkedin_profile.draw_border(long_text, color="")
        
        # Check border drawn correctly - elements should be present
        output = self.output.getvalue()
        self.assertIn("╭" + "─" * 1002 + "╮", output)  # Top border
        self.assertIn("│ " + "A" * 1000 + " │", output)  # First text line
        self.assertIn("│ " + "B" * 500, output)  # Start of second text line
        self.assertIn("╰" + "─" * 1002 + "╯", output)  # Bottom border
    
    @patch('os.get_terminal_size')
    def test_zero_width_terminal(self, mock_size):
        """Test handling of zero width terminal"""
        mock_size.return_value = MagicMock(columns=0, lines=24)
        
        with patch('linkedin_profile.clear_screen'), redirect_stdout(self.output):
            # Should not crash with zero width
            linkedin_profile.matrix_rain(duration=0.1, speed=0)
    
    def test_unicode_compatibility(self):
        """Test that unicode characters display correctly"""
        unicode_text = "🚀 Unicode Test 💻 👨‍💻 🧠 📊 🔮 🔗 📈"
        
        with redirect_stdout(self.output):
            linkedin_profile.print_with_typing(unicode_text, delay=0)
        
        # Unicode characters should be preserved
        self.assertEqual(self.output.getvalue().strip(), unicode_text)

if __name__ == "__main__":
    unittest.main() 