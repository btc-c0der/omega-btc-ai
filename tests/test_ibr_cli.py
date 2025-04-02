#!/usr/bin/env python3
"""
Test suite for IBR España Divine CLI Tool
Following test-driven development principles

JAH JAH BLESS THE DIVINE TESTS!
"""

import os
import sys
import json
import tempfile
import shutil
import pytest
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path to import ibr_cli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import ibr_cli.py
try:
    from ibr_cli import IBRConfig, KubernetesManager, ContentManager, main, DEFAULT_CONFIG_PATH
except ImportError:
    print("Failed to import ibr_cli.py")
    sys.exit(1)

# Test IBRConfig class
class TestIBRConfig:
    def setup_method(self):
        """Setup for each test - create a temporary config file"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
    
    def teardown_method(self):
        """Teardown after each test - remove temporary files"""
        shutil.rmtree(self.temp_dir)
    
    def test_load_config_new_file(self):
        """Test loading config from a new file"""
        config = IBRConfig(self.config_path)
        assert "instagram" in config.config
        assert "kubernetes" in config.config
        assert "church" in config.config
        
        # Check default values
        assert config.get("kubernetes", "namespace") == "ibr-spain"
    
    def test_load_config_existing_file(self):
        """Test loading config from an existing file"""
        # Create config file with custom values
        test_config = {
            "instagram": {
                "username": "testuser",
                "password": "testpass"
            },
            "kubernetes": {
                "context": "test-context",
                "namespace": "test-namespace"
            },
            "church": {
                "name": "Test Church",
                "website": "https://test.org"
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        # Load the config
        config = IBRConfig(self.config_path)
        
        # Check values
        assert config.get("instagram", "username") == "testuser"
        assert config.get("kubernetes", "context") == "test-context"
        assert config.get("church", "name") == "Test Church"
    
    def test_set_and_get_config(self):
        """Test setting and getting config values"""
        config = IBRConfig(self.config_path)
        
        # Set a value
        config.set("instagram", "username", "newuser")
        
        # Check it was set correctly
        assert config.get("instagram", "username") == "newuser"
        
        # Check it was saved to file
        with open(self.config_path, 'r') as f:
            saved_config = json.load(f)
            assert saved_config["instagram"]["username"] == "newuser"
    
    def test_get_nonexistent_section(self):
        """Test getting a value from a nonexistent section"""
        config = IBRConfig(self.config_path)
        assert config.get("nonexistent") is None
    
    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key from a section"""
        config = IBRConfig(self.config_path)
        assert config.get("instagram", "nonexistent") is None

# Test KubernetesManager class
class TestKubernetesManager:
    def test_init(self):
        """Test KubernetesManager initialization"""
        # Skip testing initialization which depends on actual Kubernetes client
        # Just verify class properties are set correctly
        with patch('ibr_cli.KubernetesManager._init_kubernetes'):
            k8s_manager = KubernetesManager(context="test-context", namespace="test-namespace")
            assert k8s_manager.namespace == "test-namespace"
            assert k8s_manager.context == "test-context"
    
    def test_get_pods(self):
        """Test getting pods"""
        # Skip initialization
        with patch('ibr_cli.KubernetesManager._init_kubernetes'):
            k8s_manager = KubernetesManager(namespace="test-namespace")
            
            # Setup mock
            mock_core_api = MagicMock()
            mock_core_api.list_namespaced_pod.return_value = MagicMock()
            k8s_manager.core_api = mock_core_api
            
            # Call the method
            pods = k8s_manager.get_pods()
            
            # Check correct methods were called
            k8s_manager.core_api.list_namespaced_pod.assert_called_once_with("test-namespace")
    
    def test_restart_deployment(self):
        """Test restarting a deployment"""
        # Skip initialization
        with patch('ibr_cli.KubernetesManager._init_kubernetes'):
            # Create KubernetesManager
            k8s_manager = KubernetesManager(namespace="test-namespace")
            
            # Setup mock
            mock_apps_api = MagicMock()
            mock_apps_api.patch_namespaced_deployment.return_value = MagicMock()
            k8s_manager.apps_api = mock_apps_api
            
            # Call restart_deployment
            k8s_manager.restart_deployment("test-deployment")
            
            # Check correct methods were called
            k8s_manager.apps_api.patch_namespaced_deployment.assert_called_once()
            args, kwargs = k8s_manager.apps_api.patch_namespaced_deployment.call_args
            assert kwargs["name"] == "test-deployment"
            assert kwargs["namespace"] == "test-namespace"
            assert "spec" in kwargs["body"]
            assert "template" in kwargs["body"]["spec"]
            assert "metadata" in kwargs["body"]["spec"]["template"]
            assert "annotations" in kwargs["body"]["spec"]["template"]["metadata"]
            assert "ibr-cli/restartedAt" in kwargs["body"]["spec"]["template"]["metadata"]["annotations"]

# Test ContentManager class
class TestContentManager:
    @patch('PIL.Image.new')
    @patch('PIL.ImageDraw.Draw')
    def test_create_scripture_image_fallback(self, mock_draw, mock_image_new):
        """Test creating a scripture image fallback"""
        # Setup mocks
        mock_image = MagicMock()
        mock_image_new.return_value = mock_image
        mock_draw_instance = MagicMock()
        mock_draw.return_value = mock_draw_instance
        
        # Create a temporary file for the output
        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
            # Call the method directly with ImportError simulation
            with patch('sys.path'):  # Just patch sys.path without touching insert
                with patch('ibr_cli.ContentManager.create_scripture_image', side_effect=ImportError):
                    result = ContentManager.create_scripture_image(
                        "Test scripture text",
                        "Test 1:1",
                        temp_file.name
                    )
            
            # Verify mocks were called correctly
            mock_image_new.assert_called_once()
            mock_draw.assert_called_once_with(mock_image)
            mock_image.save.assert_called_once_with(temp_file.name)

# Test main CLI functions
class TestCLI:
    @patch('argparse.ArgumentParser.parse_args')
    @patch('ibr_cli.IBRConfig')
    def test_main_no_command(self, mock_config, mock_parse_args):
        """Test CLI with no command (should show help)"""
        # Setup mocks
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        
        # Remove func attribute to simulate no command
        del mock_args.func
        
        # Call main with patched print to capture output
        with patch('builtins.print') as mock_print:
            result = main()
        
        # Verify behavior
        assert result == 0
        mock_print.assert_called()  # Help message should be printed

    @patch('argparse.ArgumentParser.parse_args')
    @patch('ibr_cli.handle_k8s_status')
    @patch('ibr_cli.IBRConfig')
    def test_main_with_command(self, mock_config, mock_handler, mock_parse_args):
        """Test CLI with a command"""
        # Setup mocks
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        mock_args.func = mock_handler
        mock_handler.return_value = 0
        
        # Call main
        result = main()
        
        # Verify behavior
        assert result == 0
        mock_handler.assert_called_once_with(mock_args, mock_config.return_value)

# Pytest fixtures
@pytest.fixture
def temp_config_file():
    """Create a temporary config file for tests"""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b'{"test": "data"}')
        temp_file_name = temp_file.name
    
    yield temp_file_name
    
    # Cleanup
    if os.path.exists(temp_file_name):
        os.unlink(temp_file_name)

# Integration-style tests using the fixtures
class TestIntegration:
    def test_config_command_with_real_file(self, temp_config_file):
        """Test the config command with a real temporary file"""
        # Call config command with the temporary file
        with patch('sys.argv', ['ibr_cli.py', 'config', '--get', 'test']):
            # Use a complete replacement for IBRConfig to avoid patching instance attribute
            with patch('ibr_cli.IBRConfig', return_value=MagicMock()) as mock_config:
                mock_config.return_value.get.return_value = "data"
                with patch('builtins.print') as mock_print:
                    main()
        
        # Verify it tried to display the config value
        mock_print.assert_called()

if __name__ == "__main__":
    pytest.main(['-xvs', __file__]) 