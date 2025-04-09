import pytest
import json
from pathlib import Path
from datetime import datetime
from omega_ai.garvey_portal.portal import (
    load_garvey_quotes,
    load_community_wisdom,
    save_community_wisdom
)

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def sample_wisdom():
    """Create sample community wisdom data"""
    return [
        {
            "reflection": "Test reflection 1",
            "quote": {
                "quote": "Test quote 1",
                "author": "Test Author",
                "date": "2024",
                "context": "Test Context"
            },
            "timestamp": datetime.now().isoformat(),
            "type": "daily_reflection"
        }
    ]

def test_load_garvey_quotes():
    """Test loading Garvey quotes"""
    quotes = load_garvey_quotes()
    assert isinstance(quotes, list)
    assert len(quotes) > 0
    for quote in quotes:
        assert "quote" in quote
        assert "author" in quote
        assert "date" in quote
        assert "context" in quote

def test_load_community_wisdom_empty(test_data_dir):
    """Test loading community wisdom when file doesn't exist"""
    # Temporarily modify the data directory path
    import omega_ai.garvey_portal.portal as portal
    portal.DATA_DIR = test_data_dir
    
    wisdom = load_community_wisdom()
    assert isinstance(wisdom, list)
    assert len(wisdom) == 0

def test_save_and_load_community_wisdom(test_data_dir, sample_wisdom):
    """Test saving and loading community wisdom"""
    # Temporarily modify the data directory path
    import omega_ai.garvey_portal.portal as portal
    portal.DATA_DIR = test_data_dir
    
    # Save wisdom
    save_community_wisdom(sample_wisdom)
    
    # Load wisdom
    loaded_wisdom = load_community_wisdom()
    
    # Verify loaded wisdom matches saved wisdom
    assert len(loaded_wisdom) == len(sample_wisdom)
    assert loaded_wisdom[0]["reflection"] == sample_wisdom[0]["reflection"]
    assert loaded_wisdom[0]["quote"]["quote"] == sample_wisdom[0]["quote"]["quote"]
    assert loaded_wisdom[0]["type"] == sample_wisdom[0]["type"]

def test_community_wisdom_file_format(test_data_dir, sample_wisdom):
    """Test that community wisdom is saved in valid JSON format"""
    # Temporarily modify the data directory path
    import omega_ai.garvey_portal.portal as portal
    portal.DATA_DIR = test_data_dir
    
    # Save wisdom
    save_community_wisdom(sample_wisdom)
    
    # Read the file directly
    wisdom_file = test_data_dir / "community_wisdom.json"
    assert wisdom_file.exists()
    
    with open(wisdom_file, "r") as f:
        loaded_data = json.load(f)
        assert isinstance(loaded_data, list)
        assert len(loaded_data) == 1
        assert loaded_data[0]["reflection"] == sample_wisdom[0]["reflection"] 