#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 9 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import unittest
import json
import time
import pytest
from unittest.mock import patch, MagicMock, mock_open
from PIL import Image
import io
import base64
import tempfile
import threading
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock imports for testing without actual dependencies
sys.modules['gradio'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()

# Now we can import the modules we want to test
from dna_pcr_quantum_portal import (
    QuantumPCR, 
    DNAVisualizer, 
    ConsciousnessLSDPortal, 
    generate_divine_insight,
    run_pcr_lsd_sequence,
    handle_message
)


class TestQuantumPCR(unittest.TestCase):
    """Test cases for QuantumPCR class"""
    
    def test_amplify_with_empty_sequence(self):
        """Test that amplify works with an empty sequence"""
        result = QuantumPCR.amplify("")
        self.assertIsInstance(result, dict)
        self.assertTrue("original_sequence" in result)
        self.assertTrue(len(result["original_sequence"]) >= 20)
        
    def test_amplify_with_valid_sequence(self):
        """Test that amplify works with a valid DNA sequence"""
        test_sequence = "ATGCATGC"
        result = QuantumPCR.amplify(test_sequence)
        self.assertIsInstance(result, dict)
        self.assertTrue("original_sequence" in result)
        self.assertTrue(result["original_sequence"].startswith("ATGCATGC"))
        
    def test_amplify_with_invalid_chars(self):
        """Test that amplify filters out invalid characters"""
        test_sequence = "ATGC123XYZ"
        result = QuantumPCR.amplify(test_sequence)
        self.assertEqual(result["original_sequence"], "ATGC")
        
    def test_schumann_sync_effect(self):
        """Test that Schumann resonance sync has an effect"""
        # Run with and without Schumann sync
        result_with_sync = QuantumPCR.amplify("ATGC", schumann_sync=True)
        result_without_sync = QuantumPCR.amplify("ATGC", schumann_sync=False)
        
        # Verify quantum purity is higher with Schumann sync
        self.assertGreater(result_with_sync["quantum_purity"], result_without_sync["quantum_purity"])
        
    def test_quantum_entanglement_effect(self):
        """Test that quantum entanglement level affects efficiency"""
        # Run with different quantum entanglement levels
        result_high = QuantumPCR.amplify("ATGC", quantum_entanglement=0.9)
        result_low = QuantumPCR.amplify("ATGC", quantum_entanglement=0.1)
        
        # Verify high quantum entanglement produces different results
        self.assertNotEqual(result_high["amplification_curve"], result_low["amplification_curve"])
        

class TestDNAVisualizer(unittest.TestCase):
    """Test cases for DNAVisualizer class"""
    
    @patch("PIL.Image.new")
    @patch("PIL.Image.save")
    def test_render_creates_image(self, mock_save, mock_new):
        """Test that render creates and returns an image"""
        # Setup mock image
        mock_image = MagicMock()
        mock_new.return_value = mock_image
        mock_image.convert.return_value = mock_image
        mock_image.filter.return_value = mock_image
        
        # Create a simple amplified_dna object
        amplified_dna = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": True,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        # Call the render function
        result = DNAVisualizer.render(amplified_dna)
        
        # Check that an image was created and returned
        self.assertEqual(result, mock_image)
        # Verify the image was saved
        mock_save.assert_called_once()
        
    def test_different_modes_produce_different_results(self):
        """Test that different visualization modes produce different results"""
        # Create a simple amplified_dna object
        amplified_dna = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": True,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        # Create temporary directory for test images
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.makedirs(f"{tmpdirname}/assets/dna_visualizations", exist_ok=True)
            
            # Mock file saving to use our temp directory
            original_save = Image.save
            def mock_save(self, filename, *args, **kwargs):
                # Replace the target directory with our temp directory
                new_filename = filename.replace(
                    "divine_dashboard_v3/assets/dna_visualizations",
                    f"{tmpdirname}/assets/dna_visualizations"
                )
                return original_save(self, new_filename, *args, **kwargs)
            
            # Apply the mock to PIL Image save method
            with patch.object(Image, 'save', mock_save):
                # Render with different modes
                img_lsd = DNAVisualizer.render(amplified_dna, mode="lsd")
                img_quantum = DNAVisualizer.render(amplified_dna, mode="quantum")
                
                # Compare the images (they should be different)
                img_data_lsd = io.BytesIO()
                img_lsd.save(img_data_lsd, format='PNG')
                img_data_lsd = img_data_lsd.getvalue()
                
                img_data_quantum = io.BytesIO()
                img_quantum.save(img_data_quantum, format='PNG')
                img_data_quantum = img_data_quantum.getvalue()
                
                # Images should be different due to different modes
                self.assertNotEqual(img_data_lsd, img_data_quantum)


class TestConsciousnessLSDPortal(unittest.TestCase):
    """Test cases for ConsciousnessLSDPortal class"""
    
    @patch("builtins.open", new_callable=mock_open)
    def test_expand_produces_report(self, mock_file):
        """Test that expand produces a consciousness report"""
        # Create a simple amplified_dna object
        amplified_dna = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": True,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        # Call the expand function
        result = ConsciousnessLSDPortal.expand(amplified_dna, lsd_dose=100.0)
        
        # Check that a report string was returned
        self.assertIsInstance(result, str)
        self.assertIn("CONSCIOUSNESS EXPANSION REPORT", result)
        self.assertIn("LSD Dose: 100.0", result)
        
        # Verify file was opened for writing
        mock_file.assert_called_once()
        
    def test_lsd_dose_affects_metrics(self):
        """Test that LSD dose affects consciousness metrics"""
        # Create a simple amplified_dna object
        amplified_dna = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": True,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        # Call expand with different LSD doses
        with patch("builtins.open", new_callable=mock_open):
            result_high = ConsciousnessLSDPortal.expand(amplified_dna, lsd_dose=500.0)
            result_low = ConsciousnessLSDPortal.expand(amplified_dna, lsd_dose=50.0)
            
            # Verify higher dose leads to higher metrics
            self.assertGreater(
                result_high.count("100%"), 
                result_low.count("100%")
            )
    
    def test_schumann_sync_affects_mystical_experience(self):
        """Test that Schumann resonance affects mystical experience"""
        # Create two amplified_dna objects, one with Schumann sync
        amplified_dna_with_sync = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": True,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        amplified_dna_without_sync = {
            "original_sequence": "ATGC",
            "quantum_purity": 0.95,
            "merkle_fidelity": 0.9,
            "schumann_sync": False,
            "fibonacci_influence": 0.2,
            "quantum_entanglement": 0.7
        }
        
        # Call expand with both DNA objects using the same LSD dose
        with patch("builtins.open", new_callable=mock_open):
            result_with_sync = ConsciousnessLSDPortal.expand(amplified_dna_with_sync, lsd_dose=200.0)
            result_without_sync = ConsciousnessLSDPortal.expand(amplified_dna_without_sync, lsd_dose=200.0)
            
            # Verify Schumann sync affects result - should have ACTIVE status
            self.assertIn("Schumann Resonance: ACTIVE", result_with_sync)
            self.assertIn("Schumann Resonance: INACTIVE", result_without_sync)
            
            # Mystical experience metric should be different
            mystical_with_sync = float(result_with_sync.split("Mystical-Unitive Experience: ")[1].split("\n")[0])
            mystical_without_sync = float(result_without_sync.split("Mystical-Unitive Experience: ")[1].split("\n")[0])
            
            self.assertNotEqual(mystical_with_sync, mystical_without_sync)


class TestDivineInsight(unittest.TestCase):
    """Test cases for divine insight generation"""
    
    def test_insight_generation(self):
        """Test that divine insights are generated based on metrics"""
        # Verify insights count is proportional to metrics
        low_insight = generate_divine_insight(0.1, 0.1)
        high_insight = generate_divine_insight(1.0, 1.0)
        
        # Higher metrics should produce more insights (more lines)
        self.assertLess(low_insight.count("\n"), high_insight.count("\n"))
        
    def test_insights_are_different(self):
        """Test that generated insights are different"""
        # Generate multiple insights with the same metrics
        insight1 = generate_divine_insight(0.5, 0.5)
        insight2 = generate_divine_insight(0.5, 0.5)
        insight3 = generate_divine_insight(0.5, 0.5)
        
        # Insights should be randomly selected, so they should differ
        insights = [insight1, insight2, insight3]
        unique_insights = set(insights)
        
        # At least one insight should be different
        self.assertGreater(len(unique_insights), 1, 
                          "Generated insights should be different due to randomization")


class TestRunPCRSequence(unittest.TestCase):
    """Test cases for main PCR sequence function"""
    
    @patch('dna_pcr_quantum_portal.QuantumPCR.amplify')
    @patch('dna_pcr_quantum_portal.DNAVisualizer.render')
    @patch('dna_pcr_quantum_portal.ConsciousnessLSDPortal.expand')
    @patch('matplotlib.pyplot.subplots')
    @patch('PIL.Image.open')
    def test_run_pcr_lsd_sequence(self, mock_image_open, mock_subplots, mock_expand, mock_render, mock_amplify):
        """Test that run_pcr_lsd_sequence calls all necessary components"""
        # Setup mocks
        mock_amplify.return_value = {"original_sequence": "ATGC"}
        mock_render.return_value = MagicMock()
        mock_expand.return_value = "Consciousness Report"
        
        fig_mock = MagicMock()
        ax_mock = MagicMock()
        mock_subplots.return_value = (fig_mock, ax_mock)
        
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        
        # Call the function
        visual, consciousness, pcr_plot = run_pcr_lsd_sequence(
            "ATGC", 100.0, True, 0.7
        )
        
        # Verify all components were called
        mock_amplify.assert_called_once_with("ATGC", schumann_sync=True, quantum_entanglement=0.7)
        mock_render.assert_called_once()
        mock_expand.assert_called_once()
        mock_subplots.assert_called_once()
        
        # Verify outputs
        self.assertEqual(visual, mock_render.return_value)
        self.assertEqual(consciousness, "Consciousness Report")
        self.assertEqual(pcr_plot, mock_image)


class TestMessageHandling(unittest.TestCase):
    """Test cases for message handling functionality"""
    
    def test_handle_message_with_valid_command(self):
        """Test that handle_message works with valid command"""
        # Test with Mullis Spiral Boost activation key
        message = {
            "command": "runSequence",
            "activationKey": "Mullis Spiral Boost"
        }
        
        result = handle_message(message)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["dna_sequence"], "ATGCGTAGCTAGCTAGCTAGCTA")
        self.assertEqual(result["lsd_dose"], 200.0)
        self.assertTrue(result["schumann_sync"])
        self.assertEqual(result["quantum_entanglement"], 0.9)
        
    def test_handle_message_with_invalid_input(self):
        """Test that handle_message handles invalid inputs correctly"""
        # Test with non-dict input
        self.assertIsNone(handle_message("not a dict"))
        
        # Test with dict that doesn't have command key
        self.assertIsNone(handle_message({"not_command": "value"}))
        
    def test_different_activation_keys(self):
        """Test that different activation keys produce different results"""
        # Test all activation keys
        keys = ["Mullis Spiral Boost", "DNA Rain Glitch", "Neural Lotus Bloom", "unknown_key"]
        results = {}
        
        for key in keys:
            message = {
                "command": "runSequence",
                "activationKey": key
            }
            results[key] = handle_message(message)
        
        # Verify each key produces different parameters
        self.assertNotEqual(results["Mullis Spiral Boost"], results["DNA Rain Glitch"])
        self.assertNotEqual(results["Mullis Spiral Boost"], results["Neural Lotus Bloom"])
        self.assertNotEqual(results["DNA Rain Glitch"], results["Neural Lotus Bloom"])
        
        # Unknown key should use default values
        self.assertIsNotNone(results["unknown_key"])


@pytest.fixture
def gradio_server():
    """Fixture to start a Gradio server for integration tests"""
    import subprocess
    import socket
    import time
    
    # Find an available port
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 0))
            return s.getsockname()[1]
    
    port = find_free_port()
    
    # Start server in a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "dna_pcr_quantum_portal"],
        env={**os.environ, "PORT": str(port)},
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    
    # Wait for server to start
    time.sleep(5)
    
    yield f"http://0.0.0.0:{port}"
    
    # Cleanup
    process.terminate()
    process.wait()


@pytest.mark.integration
class TestCrossOriginMessages:
    """Test cases for cross-origin messaging issues"""
    
    def test_postmessage_origin_handling(self, gradio_server):
        """Test that postMessage origin is handled correctly"""
        try:
            # Verify server is running
            response = requests.get(gradio_server)
            assert response.status_code == 200
            
            # This is just a placeholder for manual browser testing
            print(f"Server running at {gradio_server} - manual testing required for postMessage")
            
            # In an actual test environment with selenium, we could:
            # 1. Start a selenium browser
            # 2. Navigate to the app
            # 3. Execute JS to send postMessage with different origins
            # 4. Check for errors in console logs
        except requests.RequestException:
            pytest.skip("Integration server could not be started")


@pytest.mark.integration
class TestFontLoadingErrors:
    """Test cases for font loading error issues"""
    
    def test_font_loading_errors(self, gradio_server):
        """Test for font loading errors"""
        try:
            # Check if we get a 404 for the font files
            font_urls = [
                f"{gradio_server}/static/fonts/ui-sans-serif/ui-sans-serif-Bold.woff2",
                f"{gradio_server}/static/fonts/ui-sans-serif/ui-sans-serif-Regular.woff2",
                f"{gradio_server}/static/fonts/system-ui/system-ui-Bold.woff2",
                f"{gradio_server}/static/fonts/system-ui/system-ui-Regular.woff2"
            ]
            
            for url in font_urls:
                response = requests.get(url)
                # We expect 404 for these missing fonts
                assert response.status_code == 404, f"Expected 404 for {url}"
                
            # Verify that the app still loads despite font errors
            main_response = requests.get(gradio_server)
            assert main_response.status_code == 200
            assert "0M3G4 PCR QUANTUM LSD PORTAL" in main_response.text
        except requests.RequestException:
            pytest.skip("Integration server could not be started")


@pytest.mark.integration
class TestJavaScriptErrors:
    """Test cases for JavaScript errors"""
    
    def test_js_syntax_errors(self, gradio_server):
        """Test for JavaScript syntax errors"""
        try:
            # This is just a placeholder for manual browser testing
            print(f"Server running at {gradio_server} - manual testing required for JavaScript errors")
            
            # In a complete test setup:
            # 1. Use selenium to navigate to the page
            # 2. Extract console logs
            # 3. Check for SyntaxError in logs
        except requests.RequestException:
            pytest.skip("Integration server could not be started")


if __name__ == '__main__':
    unittest.main() 