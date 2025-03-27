#!/usr/bin/env python3

"""
🔮 OMEGA BTC AI - TEST CONSOLIDATION SCRIPT

This sacred script consolidates all test cases into a single, organized structure.
ONE LOVE, ONE HEART, ONE TEST SUITE!
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_consolidation.log')
    ]
)
logger = logging.getLogger(__name__)

# Terminal colors for spiritual output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Test directory mappings
TEST_MAPPINGS = {
    # Unit Tests
    'unit/ai/ml': ['ml'],
    'unit/ai/cosmic': ['cosmic_tests'],
    'unit/core/fibonacci': ['fibonacci'],
    'unit/core/mm_trap_detector': ['mm_trap_detector'],
    'unit/core/trading': ['trading'],
    'unit/data/redis': ['redis'],
    'unit/data/websocket': ['websocket'],
    'unit/monitoring/alerts': ['alerts'],
    'unit/monitoring/visualization': ['visualization'],
    'unit/utils/tools': ['tools'],
    
    # Integration Tests
    'integration/api': ['api'],
    'integration/portal': ['garvey_portal'],
    'integration/security': ['security'],
    
    # E2E Tests
    'e2e/system_flows': ['integration_tests'],
    'e2e/trading_flows': ['quality_tests']
}

def create_directory_structure(base_path: str) -> None:
    """Create the new test directory structure."""
    logger.info("Creating new test directory structure...")
    
    # Create main categories
    categories = ['unit', 'integration', 'e2e', 'performance']
    for category in categories:
        os.makedirs(os.path.join(base_path, category), exist_ok=True)
    
    # Create unit test subcategories
    unit_subcategories = [
        'ai/ml', 'ai/cosmic',
        'core/fibonacci', 'core/mm_trap_detector', 'core/trading',
        'data/redis', 'data/websocket',
        'monitoring/alerts', 'monitoring/visualization',
        'utils/tools'
    ]
    
    for subcategory in unit_subcategories:
        os.makedirs(os.path.join(base_path, 'unit', subcategory), exist_ok=True)
    
    # Create integration test subcategories
    integration_subcategories = ['api', 'portal', 'security']
    for subcategory in integration_subcategories:
        os.makedirs(os.path.join(base_path, 'integration', subcategory), exist_ok=True)
    
    # Create e2e test subcategories
    e2e_subcategories = ['trading_flows', 'system_flows']
    for subcategory in e2e_subcategories:
        os.makedirs(os.path.join(base_path, 'e2e', subcategory), exist_ok=True)
    
    # Create performance test subcategories
    performance_subcategories = ['load_tests', 'stress_tests']
    for subcategory in performance_subcategories:
        os.makedirs(os.path.join(base_path, 'performance', subcategory), exist_ok=True)
    
    logger.info("Directory structure created successfully")

def move_test_files(base_path: str) -> None:
    """Move test files to their new locations."""
    logger.info("Moving test files to new structure...")
    
    for new_path, old_paths in TEST_MAPPINGS.items():
        for old_path in old_paths:
            source = os.path.join(base_path, old_path)
            destination = os.path.join(base_path, new_path)
            
            if os.path.exists(source):
                try:
                    # Move all files from source to destination
                    for item in os.listdir(source):
                        s = os.path.join(source, item)
                        d = os.path.join(destination, item)
                        if os.path.isfile(s) or os.path.isdir(s):
                            shutil.move(s, d)
                    logger.info(f"Moved {old_path} to {new_path}")
                except Exception as e:
                    logger.error(f"Error moving {old_path} to {new_path}: {str(e)}")
            else:
                logger.warning(f"Source directory {old_path} does not exist")

def update_import_paths(base_path: str) -> None:
    """Update import paths in all test files."""
    logger.info("Updating import paths in test files...")
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Update import paths based on new structure
                    updated_content = content.replace(
                        'from omega_ai.tests.',
                        'from omega_ai.tests.'
                    )
                    
                    with open(file_path, 'w') as f:
                        f.write(updated_content)
                    
                    logger.info(f"Updated import paths in {file}")
                except Exception as e:
                    logger.error(f"Error updating {file}: {str(e)}")

def cleanup_old_directories(base_path: str) -> None:
    """Remove old test directories."""
    logger.info("Cleaning up old test directories...")
    
    for _, old_paths in TEST_MAPPINGS.items():
        for old_path in old_paths:
            path = os.path.join(base_path, old_path)
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    logger.info(f"Removed old directory: {old_path}")
                except Exception as e:
                    logger.error(f"Error removing {old_path}: {str(e)}")

def main() -> None:
    """Main entry point for test consolidation."""
    try:
        # Get the base test directory path
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        print(f"{GREEN}🔥 Starting OMEGA BTC AI Test Consolidation 🔥{RESET}")
        
        # Create new directory structure
        create_directory_structure(base_path)
        
        # Move test files
        move_test_files(base_path)
        
        # Update import paths
        update_import_paths(base_path)
        
        # Clean up old directories
        cleanup_old_directories(base_path)
        
        print(f"\n{GREEN}✅ Test consolidation completed successfully! ✅{RESET}")
        print(f"{YELLOW}Please review the changes and run the test suite to verify everything works.{RESET}")
        
    except Exception as e:
        logger.error(f"Fatal error during test consolidation: {str(e)}", exc_info=True)
        print(f"\n{RED}Fatal error: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main() 