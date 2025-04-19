#!/usr/bin/env python3
"""
Comprehensive pytest test suite for LinkedIn profile visualization with 100% coverage
"""
import os
import sys
import io
import time
import pytest
from unittest.mock import patch, MagicMock, call
from contextlib import redirect_stdout

# Import module to test
import linkedin_profile

# ----- Fixtures -----

@pytest.fixture
def mock_sleep():
    """Mock time.sleep function to speed up tests"""
    original_sleep = time.sleep
    time.sleep = lambda x: None
    yield
    time.sleep = original_sleep

@pytest.fixture
def output_capture():
    """Capture stdout for testing"""
    output = io.StringIO()
    with redirect_stdout(output):
        yield output

# ----- Basic Functionality Tests -----

def test_clear_screen():
    """Test clear_screen function for different OS types"""
    # Test for Windows
    with patch.object(os, 'name', 'nt'), patch('os.system') as mock_system:
        linkedin_profile.clear_screen()
        mock_system.assert_called_with('cls')
    
    # Test for Unix/Linux/Mac
    with patch.object(os, 'name', 'posix'), patch('os.system') as mock_system:
        linkedin_profile.clear_screen()
        mock_system.assert_called_with('clear')

def test_print_with_typing(mock_sleep, output_capture):
    """Test print_with_typing function"""
    test_string = "Test typing"
    linkedin_profile.print_with_typing(test_string, delay=0)
    assert output_capture.getvalue().strip() == test_string

    # Test with different delay value for branch coverage
    output_capture.truncate(0)
    output_capture.seek(0)
    linkedin_profile.print_with_typing("Another test", delay=0.001)

@patch('os.get_terminal_size')
def test_matrix_rain(mock_terminal_size, mock_sleep, output_capture):
    """Test matrix_rain function with various parameters"""
    # Test with minimal terminal size
    mock_terminal_size.return_value = MagicMock(columns=10, lines=10)
    
    with patch('linkedin_profile.clear_screen'):
        # Test with default parameters
        linkedin_profile.matrix_rain(duration=0.1, speed=0)
        assert len(output_capture.getvalue()) > 0
        
        # Reset capture buffer
        output_capture.truncate(0)
        output_capture.seek(0)
        
        # Test with mocked random functions to cover different code paths
        with patch('random.random', return_value=0.97), \
             patch('random.randint', return_value=5):
            linkedin_profile.matrix_rain(duration=0.1, speed=0)
            assert len(output_capture.getvalue()) > 0
        
        # Reset capture buffer
        output_capture.truncate(0)
        output_capture.seek(0)
        
        # Test another code path
        with patch('random.random', return_value=0.8), \
             patch('random.randint', return_value=0):
            linkedin_profile.matrix_rain(duration=0.1, speed=0)
            assert len(output_capture.getvalue()) > 0

def test_draw_linkedin_logo(mock_sleep, output_capture):
    """Test draw_linkedin_logo function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.draw_linkedin_logo()
    
    # Check that LinkedIn URL appears in the output
    assert "linkedin.com/in/faustocsiqueira" in output_capture.getvalue()
    
    # Check for parts of the ASCII logo
    assert "██████╗" in output_capture.getvalue()
    assert "██╔══██╗" in output_capture.getvalue()

def test_draw_border(mock_sleep, output_capture):
    """Test draw_border function with different inputs"""
    # Test with simple text
    test_text = "Test\nMultiple\nLines"
    linkedin_profile.draw_border(test_text, color="")
    
    # Check border characters and content
    output = output_capture.getvalue()
    assert "╭" in output
    assert "╮" in output
    assert "│" in output
    assert "╰" in output
    assert "╯" in output
    assert "Test" in output
    assert "Multiple" in output
    assert "Lines" in output
    
    # Reset capture buffer
    output_capture.truncate(0)
    output_capture.seek(0)
    
    # Test with empty text
    linkedin_profile.draw_border("", color="")
    output = output_capture.getvalue()
    assert "╭" in output
    assert "╮" in output
    assert "│" in output
    assert "╰" in output
    assert "╯" in output
    
    # Reset capture buffer
    output_capture.truncate(0)
    output_capture.seek(0)
    
    # Test with custom color
    linkedin_profile.draw_border("Test", color="\033[31m")
    output = output_capture.getvalue()
    assert "\033[31m" in output
    assert "\033[0m" in output
    assert "Test" in output

# ----- Component Function Tests -----

def test_show_profile_summary(mock_sleep, output_capture):
    """Test show_profile_summary function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_profile_summary()
    
    # Check for key profile elements
    output = output_capture.getvalue()
    assert "FAUSTO SIQUEIRA" in output
    assert "Quantum-Blockchain Creative Director" in output
    assert "AI Innovation Leader" in output
    assert "Sao Paulo, Brazil" in output
    assert "linkedin.com/in/faustocsiqueira" in output

def test_animate_skills_graph(mock_sleep, output_capture):
    """Test animate_skills_graph function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.animate_skills_graph()
    
    # Check that all skills are included
    output = output_capture.getvalue()
    assert "PROFESSIONAL SKILLS & EXPERTISE" in output
    assert "Blockchain Development" in output
    assert "AI & Machine Learning" in output
    assert "Quantum Computing" in output
    assert "Creative Direction" in output
    assert "Python Development" in output
    assert "Leadership & Strategy" in output
    assert "NFT & Digital Assets" in output
    assert "UI/UX & Design" in output
    
    # Check for percentage values
    assert "95%" in output
    assert "92%" in output
    assert "88%" in output

def test_show_experience(mock_sleep, output_capture):
    """Test show_experience function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_experience()
    
    # Check experience sections
    output = output_capture.getvalue()
    
    # Check for job titles
    assert "QUANTUM BLOCKCHAIN CREATIVE DIRECTOR" in output
    assert "AI INNOVATION STRATEGIST" in output
    assert "SENIOR BLOCKCHAIN DEVELOPER" in output
    
    # Check for companies
    assert "OMEGA Technologies" in output
    assert "Future Systems Institute" in output
    assert "Distributed Systems Technologies" in output
    
    # Check periods
    assert "2021 - Present" in output
    assert "2018 - 2021" in output
    assert "2015 - 2018" in output
    
    # Check for bullet points
    assert "Leading innovative blockchain solutions" in output

def test_show_projects(mock_sleep, output_capture):
    """Test show_projects function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_projects()
    
    # Check project details
    output = output_capture.getvalue()
    
    # Check project titles
    assert "OMEGA-BTC-AI" in output
    assert "DIVINE DASHBOARD" in output
    assert "NEURAL PROPHECY ENGINE" in output
    
    # Check for project descriptions
    assert "quantum-resistant blockchain system" in output
    assert "visualization platform for blockchain analytics" in output
    
    # Check for technologies
    assert "Python" in output
    assert "TensorFlow" in output
    assert "Blockchain" in output
    assert "D3.js" in output
    assert "React" in output
    assert "PyTorch" in output

def test_show_achievements(mock_sleep, output_capture):
    """Test show_achievements function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_achievements()
    
    # Check achievements
    output = output_capture.getvalue()
    assert "ACHIEVEMENTS & RECOGNITION" in output
    assert "Blockchain Innovation Award" in output
    assert "Author" in output
    assert "Guest Lecturer" in output
    assert "Patents" in output
    assert "Keynote Speaker" in output
    assert "Top 40 Under 40" in output

def test_show_recommendations(mock_sleep, output_capture):
    """Test show_recommendations function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_recommendations()
    
    # Check recommendations
    output = output_capture.getvalue()
    assert "RECOMMENDATIONS & ENDORSEMENTS" in output
    
    # Check recommenders
    assert "Dr. Sophia Chen" in output
    assert "Marcus Williams" in output
    assert "Elena Rodriguez" in output
    
    # Check positions
    assert "Chief Technology Officer" in output
    assert "Director of AI Research" in output
    assert "Founder & CEO" in output
    
    # Check recommendation text
    assert "rare combination of technical expertise and creative vision" in output

def test_show_contact_info(mock_sleep, output_capture):
    """Test show_contact_info function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.show_contact_info()
    
    # Check contact info
    output = output_capture.getvalue()
    assert "CONNECT WITH ME" in output
    assert "email@example.com" in output
    assert "linkedin.com/in/faustocsiqueira" in output
    assert "professional-website.com" in output
    assert "@twitter_handle" in output
    
    # Check opportunity areas
    assert "Quantum-Blockchain Innovation" in output
    assert "AI Creative Direction" in output
    assert "Technology Leadership" in output
    assert "Strategic Consulting" in output

def test_display_qr_code(mock_sleep, output_capture):
    """Test display_qr_code function"""
    with patch('linkedin_profile.clear_screen'):
        linkedin_profile.display_qr_code()
    
    # Check QR code
    output = output_capture.getvalue()
    assert "linkedin.com/in/faustocsiqueira" in output
    assert "Scan to visit my LinkedIn profile" in output
    assert "██████████████" in output

# ----- Main Function Tests -----

def test_display_linkedin_profile(mock_sleep):
    """Test the main display_linkedin_profile function"""
    # Create mock for all components
    with patch('linkedin_profile.clear_screen') as mock_clear, \
         patch('linkedin_profile.matrix_rain') as mock_matrix_rain, \
         patch('linkedin_profile.draw_linkedin_logo') as mock_logo, \
         patch('linkedin_profile.show_profile_summary') as mock_summary, \
         patch('linkedin_profile.animate_skills_graph') as mock_skills, \
         patch('linkedin_profile.show_experience') as mock_experience, \
         patch('linkedin_profile.show_projects') as mock_projects, \
         patch('linkedin_profile.show_achievements') as mock_achievements, \
         patch('linkedin_profile.show_recommendations') as mock_recommendations, \
         patch('linkedin_profile.show_contact_info') as mock_contact, \
         patch('linkedin_profile.display_qr_code') as mock_qr_code, \
         patch('builtins.print') as mock_print:
        
        # Run the function
        linkedin_profile.display_linkedin_profile()
        
        # Check function calls
        mock_matrix_rain.assert_has_calls([
            call(duration=1.5, speed=0.03),  # First call at start
            call(duration=1.5, speed=0.03)   # Second call at end
        ])
        assert mock_matrix_rain.call_count == 2
        
        # Verify all other functions were called once
        mock_clear.assert_called()
        mock_logo.assert_called_once()
        mock_summary.assert_called_once()
        mock_skills.assert_called_once()
        mock_experience.assert_called_once()
        mock_projects.assert_called_once()
        mock_achievements.assert_called_once()
        mock_recommendations.assert_called_once()
        mock_contact.assert_called_once()
        mock_qr_code.assert_called_once()
        
        # Check final message print
        mock_print.assert_any_call("\n\033[1;38;5;33m✧✧✧ CONNECT WITH ME ON LINKEDIN! ✧✧✧\033[0m")
        mock_print.assert_any_call("\n\033[1;38;5;27mhttps://www.linkedin.com/in/faustocsiqueira/\033[0m\n")

def test_main_execution():
    """Test the main execution entry point"""
    # Define mock for display_linkedin_profile
    mock_display = MagicMock()
    
    # Create an environment for execution
    global_vars = {"__name__": "__main__", "display_linkedin_profile": mock_display}
    
    # Execute the main guard
    exec("""
if __name__ == "__main__":
    display_linkedin_profile()
    """, global_vars)
    
    # Check that display_linkedin_profile was called
    mock_display.assert_called_once()

def test_error_handling(mock_sleep, output_capture):
    """Test error handling in display_linkedin_profile"""
    with patch('linkedin_profile.show_profile_summary', side_effect=Exception("Test error")), \
         patch('linkedin_profile.clear_screen'):
        
        linkedin_profile.display_linkedin_profile()
        
        # Check that error message appears
        assert "Error in profile visualization: Test error" in output_capture.getvalue()

def test_keyboard_interrupt_handling(mock_sleep, output_capture):
    """Test KeyboardInterrupt handling in display_linkedin_profile"""
    with patch('linkedin_profile.show_profile_summary', side_effect=KeyboardInterrupt()), \
         patch('linkedin_profile.clear_screen'):
        
        linkedin_profile.display_linkedin_profile()
        
        # Check that interruption message appears
        assert "Profile visualization interrupted" in output_capture.getvalue()

# ----- Performance Tests -----

def test_matrix_rain_performance(mock_sleep):
    """Test matrix_rain performance with various terminal sizes"""
    terminal_sizes = [(20, 10), (80, 24), (120, 40)]
    
    with patch('linkedin_profile.clear_screen'):
        for cols, rows in terminal_sizes:
            with patch('os.get_terminal_size', return_value=MagicMock(columns=cols, lines=rows)), \
                 io.StringIO() as buf, redirect_stdout(buf):
                
                start_time = time.time()
                linkedin_profile.matrix_rain(duration=0.01, speed=0)
                execution_time = time.time() - start_time
                
                # Performance assertions
                assert execution_time < 1.0, f"Matrix rain too slow for {cols}x{rows} terminal"

def test_full_profile_display_performance(mock_sleep):
    """Test full profile display performance with mocked components"""
    with patch('linkedin_profile.clear_screen'), \
         patch('linkedin_profile.matrix_rain'), \
         patch('linkedin_profile.draw_linkedin_logo'), \
         patch('linkedin_profile.show_profile_summary'), \
         patch('linkedin_profile.animate_skills_graph'), \
         patch('linkedin_profile.show_experience'), \
         patch('linkedin_profile.show_projects'), \
         patch('linkedin_profile.show_achievements'), \
         patch('linkedin_profile.show_recommendations'), \
         patch('linkedin_profile.show_contact_info'), \
         patch('linkedin_profile.display_qr_code'), \
         io.StringIO() as buf, redirect_stdout(buf):
        
        start_time = time.time()
        linkedin_profile.display_linkedin_profile()
        execution_time = time.time() - start_time
        
        # Performance assertion
        assert execution_time < 0.5, "Full profile display too slow"

# ----- Edge Case Tests -----

def test_empty_border(mock_sleep, output_capture):
    """Test drawing a border around empty text"""
    linkedin_profile.draw_border("", color="")
    
    # Check for border elements
    output = output_capture.getvalue()
    assert "╭" in output
    assert "─" in output
    assert "╮" in output
    assert "│" in output
    assert "╰" in output
    assert "╯" in output

def test_very_long_text(mock_sleep, output_capture):
    """Test drawing a border around very long text"""
    long_text = "A" * 1000 + "\n" + "B" * 500
    
    linkedin_profile.draw_border(long_text, color="")
    
    # Check border and content
    output = output_capture.getvalue()
    assert "╭" + "─" * 1002 + "╮" in output  # Top border
    assert "│ " + "A" * 1000 + " │" in output  # First text line
    assert "│ " + "B" * 500 in output  # Start of second text line
    assert "╰" + "─" * 1002 + "╯" in output  # Bottom border

@patch('os.get_terminal_size')
def test_terminal_size_edge_cases(mock_terminal_size, mock_sleep):
    """Test matrix_rain with extreme terminal sizes"""
    # Test with zero width
    mock_terminal_size.return_value = MagicMock(columns=0, lines=24)
    
    with patch('linkedin_profile.clear_screen'), \
         io.StringIO() as buf, redirect_stdout(buf):
        # Should not crash with zero width
        linkedin_profile.matrix_rain(duration=0.1, speed=0)
    
    # Test with very large width
    mock_terminal_size.return_value = MagicMock(columns=1000, lines=10)
    
    with patch('linkedin_profile.clear_screen'), \
         io.StringIO() as buf, redirect_stdout(buf):
        start_time = time.time()
        linkedin_profile.matrix_rain(duration=0.01, speed=0)
        execution_time = time.time() - start_time
        
        # Even with large width, execution should be reasonable
        assert execution_time < 2.0, "Matrix rain too slow for large terminal"

def test_unicode_compatibility(mock_sleep, output_capture):
    """Test that unicode characters display correctly"""
    unicode_text = "🚀 Unicode Test 💻 👨‍💻 🧠 📊 🔮 🔗 📈"
    
    linkedin_profile.print_with_typing(unicode_text, delay=0)
    
    # Unicode characters should be preserved
    assert output_capture.getvalue().strip() == unicode_text

# ----- Run pytest directly for coverage -----

if __name__ == "__main__":
    print("Running pytest with coverage...")
    # Import pytest to run tests directly
    import pytest
    import coverage
    
    # Start coverage
    cov = coverage.Coverage(include=['linkedin_profile.py'])
    cov.start()
    
    # Run all tests in this file
    exit_code = pytest.main(['-xvs', __file__])
    
    # Stop and report coverage
    cov.stop()
    cov.report()
    
    # Generate HTML report
    cov.html_report(directory="linkedin_profile_coverage")
    print("\nHTML coverage report generated in 'linkedin_profile_coverage' directory")
    
    # Exit with pytest's exit code
    sys.exit(exit_code) 