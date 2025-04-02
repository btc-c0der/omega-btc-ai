#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Badge Updater
--------------------------------------------

This script updates the coverage badge with the latest coverage percentage.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_badge_updater')

def load_coverage_data():
    """Load coverage data from coverage.json file."""
    try:
        with open('coverage.json', 'r') as f:
            data = json.load(f)
            return data.get('totals', {}).get('percent_covered', 0)
    except FileNotFoundError:
        logger.error('Coverage data file not found')
        return None
    except json.JSONDecodeError:
        logger.error('Invalid JSON in coverage data file')
        return None

def update_badge_template(coverage):
    """Update the badge template with the coverage percentage."""
    try:
        with open('coverage_badge_template.svg', 'r') as f:
            template = f.read()
        
        updated = template.replace('{{coverage}}', str(round(coverage, 2)))
        
        with open('coverage.svg', 'w') as f:
            f.write(updated)
            
        return True
    except FileNotFoundError:
        logger.error('Badge template file not found')
        return False
    except Exception as e:
        logger.error(f'Error updating badge: {e}')
        return False

def update_readme_badge():
    """Update the coverage badge in README.md."""
    try:
        with open('README.md', 'r') as f:
            content = f.read()
            
        badge_url = '![Coverage](coverage.svg)'
        if '![Coverage]' in content:
            content = content.replace(
                content[content.find('![Coverage]'):content.find(')')+1],
                badge_url
            )
        else:
            content = content.replace(
                '# 🌌 AIXBT Divine Monitor',
                f'# 🌌 AIXBT Divine Monitor\n\n{badge_url}'
            )
            
        with open('README.md', 'w') as f:
            f.write(content)
            
        return True
    except FileNotFoundError:
        logger.error('README.md file not found')
        return False
    except Exception as e:
        logger.error(f'Error updating README: {e}')
        return False

def main():
    """Main function to update the coverage badge."""
    logger.info('Starting coverage badge update')
    
    # Load coverage data
    coverage = load_coverage_data()
    if coverage is None:
        sys.exit(1)
    
    logger.info(f'Coverage percentage: {coverage}%')
    
    # Update badge template
    if not update_badge_template(coverage):
        sys.exit(1)
    logger.info('Badge template updated successfully')
    
    # Update README
    if not update_readme_badge():
        sys.exit(1)
    logger.info('README badge updated successfully')
    
    logger.info('Coverage badge update completed')

if __name__ == '__main__':
    main() 