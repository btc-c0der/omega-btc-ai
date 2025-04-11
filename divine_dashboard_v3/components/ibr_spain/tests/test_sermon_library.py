#!/usr/bin/env python3

"""
Test suite for the IBR España Sermon Library micro module
"""

import os
import json
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import the module to test
from ..micro_modules.sermon_library import SermonLibrary, render_sermon_card

# Test data
SAMPLE_SERMON = {
    "id": "test_sermon_001",
    "title": "Test Sermon Title",
    "preacher": "Test Preacher",
    "date": "2023-11-15",
    "duration": "35:42",
    "scripture": "Test 1:1-10",
    "language": "es",
    "audio_url": "https://example.com/test.mp3",
    "thumbnail": "https://example.com/test.jpg"
}

# Fixture for temporary directory
@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up after test
    shutil.rmtree(temp_dir)

class TestSermonLibrary:
    """Test cases for the SermonLibrary class"""
    
    def test_initialization(self, temp_data_dir):
        """Test library initialization"""
        library = SermonLibrary(temp_data_dir)
        
        # Check that the data directory was created
        assert Path(temp_data_dir).exists()
        
        # Check that sermons were loaded (should have sample data)
        assert len(library.sermons) > 0
        
        # Check that the sermons file path is correct
        expected_file = Path(temp_data_dir) / "sermons.json"
        assert library.sermons_file == expected_file
    
    def test_add_sermon(self, temp_data_dir):
        """Test adding a sermon"""
        library = SermonLibrary(temp_data_dir)
        initial_count = len(library.sermons)
        
        # Add a sermon
        result = library.add_sermon(SAMPLE_SERMON)
        
        # Check that the sermon was added
        assert result is True
        assert len(library.sermons) == initial_count + 1
        
        # Check that the sermon was saved to file
        assert Path(library.sermons_file).exists()
        
        # Verify sermon data in library
        found_sermon = None
        for sermon in library.sermons:
            if sermon.get("id") == SAMPLE_SERMON["id"]:
                found_sermon = sermon
                break
        
        assert found_sermon is not None
        assert found_sermon["title"] == SAMPLE_SERMON["title"]
        assert found_sermon["preacher"] == SAMPLE_SERMON["preacher"]
    
    def test_get_sermon(self, temp_data_dir):
        """Test retrieving a sermon by ID"""
        library = SermonLibrary(temp_data_dir)
        
        # Add a sermon
        library.add_sermon(SAMPLE_SERMON)
        
        # Get the sermon
        sermon = library.get_sermon(SAMPLE_SERMON["id"])
        
        # Check that the sermon was retrieved
        assert sermon is not None
        assert sermon["id"] == SAMPLE_SERMON["id"]
        assert sermon["title"] == SAMPLE_SERMON["title"]
        
        # Test non-existent sermon
        non_existent = library.get_sermon("non_existent_id")
        assert non_existent is None
    
    def test_update_sermon(self, temp_data_dir):
        """Test updating a sermon"""
        library = SermonLibrary(temp_data_dir)
        
        # Add a sermon
        library.add_sermon(SAMPLE_SERMON)
        
        # Update the sermon
        updated_data = {
            "title": "Updated Title",
            "duration": "40:00"
        }
        result = library.update_sermon(SAMPLE_SERMON["id"], updated_data)
        
        # Check that the update was successful
        assert result is True
        
        # Get the updated sermon
        updated_sermon = library.get_sermon(SAMPLE_SERMON["id"])
        
        # Check that the fields were updated
        assert updated_sermon["title"] == updated_data["title"]
        assert updated_sermon["duration"] == updated_data["duration"]
        
        # Check that other fields remain unchanged
        assert updated_sermon["preacher"] == SAMPLE_SERMON["preacher"]
        assert updated_sermon["scripture"] == SAMPLE_SERMON["scripture"]
        
        # Test updating non-existent sermon
        non_existent_result = library.update_sermon("non_existent_id", updated_data)
        assert non_existent_result is False
    
    def test_delete_sermon(self, temp_data_dir):
        """Test deleting a sermon"""
        library = SermonLibrary(temp_data_dir)
        
        # Add a sermon
        library.add_sermon(SAMPLE_SERMON)
        initial_count = len(library.sermons)
        
        # Delete the sermon
        result = library.delete_sermon(SAMPLE_SERMON["id"])
        
        # Check that the deletion was successful
        assert result is True
        assert len(library.sermons) == initial_count - 1
        
        # Check that the sermon was actually deleted
        deleted_sermon = library.get_sermon(SAMPLE_SERMON["id"])
        assert deleted_sermon is None
        
        # Test deleting non-existent sermon
        non_existent_result = library.delete_sermon("non_existent_id")
        assert non_existent_result is False
    
    def test_search_sermons(self, temp_data_dir):
        """Test searching sermons"""
        library = SermonLibrary(temp_data_dir)
        
        # Add multiple sermons with different languages and content
        sermon1 = {**SAMPLE_SERMON, "id": "sermon1", "title": "La Gracia de Dios", "language": "es"}
        sermon2 = {**SAMPLE_SERMON, "id": "sermon2", "title": "God's Grace", "language": "en"}
        sermon3 = {**SAMPLE_SERMON, "id": "sermon3", "title": "La Soberanía", "preacher": "Juan Pablo", "language": "es"}
        
        library.add_sermon(sermon1)
        library.add_sermon(sermon2)
        library.add_sermon(sermon3)
        
        # Test search by language
        es_results = library.search_sermons(language="es")
        assert len(es_results) == 2
        assert all(s["language"] == "es" for s in es_results)
        
        en_results = library.search_sermons(language="en")
        assert len(en_results) == 1
        assert en_results[0]["language"] == "en"
        
        # Test search by query
        grace_results = library.search_sermons(query="grace")
        assert len(grace_results) == 2  # Should match both "La Gracia" and "God's Grace"
        
        pablo_results = library.search_sermons(query="pablo")
        assert len(pablo_results) == 1
        assert pablo_results[0]["id"] == "sermon3"
        
        # Test combined search
        combined_results = library.search_sermons(query="grace", language="es")
        assert len(combined_results) == 1
        assert combined_results[0]["id"] == "sermon1"
        
        # Test search with no results
        no_results = library.search_sermons(query="nonexistent")
        assert len(no_results) == 0

class TestRenderSermonCard:
    """Test cases for the render_sermon_card function"""
    
    def test_render_sermon_card(self):
        """Test rendering a sermon card"""
        html = render_sermon_card(SAMPLE_SERMON)
        
        # Check that the HTML contains essential sermon information
        assert SAMPLE_SERMON["title"] in html
        assert SAMPLE_SERMON["preacher"] in html
        assert SAMPLE_SERMON["scripture"] in html
        assert SAMPLE_SERMON["audio_url"] in html
        
        # Check for date formatting
        formatted_date = "15 Nov 2023"  # Expected format for "2023-11-15"
        assert formatted_date in html
        
        # Check for language badge
        assert "Español" in html
    
    def test_render_sermon_card_handles_missing_data(self):
        """Test rendering a sermon card with missing data"""
        # Create a sermon with minimal data
        minimal_sermon = {
            "id": "minimal_sermon",
            "title": "Minimal Sermon"
        }
        
        html = render_sermon_card(minimal_sermon)
        
        # Check that the HTML contains the title
        assert minimal_sermon["title"] in html
        
        # Check that the HTML doesn't break due to missing data
        assert "<div class=\"sermon-card\">" in html
        assert "</div>" in html

# For direct test execution
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 