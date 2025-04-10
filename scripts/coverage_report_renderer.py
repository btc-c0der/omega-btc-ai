#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Report Renderer
-------------------------------------------

This module handles the rendering of coverage report templates.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import chevron
from coverage_report_utils import (
    load_config,
    calculate_divine_metrics,
    format_coverage_value,
    get_trend_data,
    create_output_directory,
    copy_assets
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_report_renderer')

class CoverageReportRenderer:
    """Renderer for coverage reports."""
    
    def __init__(self):
        """Initialize the renderer."""
        self.config = load_config()
        if not self.config:
            raise ValueError('Failed to load configuration')
        
        self.template_path = self.config['report']['template']['html']
        self.output_dir = self.config['report']['template']['output_dir']
        self.output_file = self.config['report']['template']['output_file']
    
    def load_template(self) -> Optional[str]:
        """Load the report template."""
        try:
            with open(self.template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.error('Template file not found')
            return None
        except Exception as e:
            logger.error(f'Error loading template: {e}')
            return None
    
    def prepare_template_data(
        self,
        coverage_data: Dict[str, Any],
        history_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare data for template rendering."""
        totals = coverage_data.get('totals', {})
        coverage = totals.get('percent_covered', 0)
        
        # Calculate divine metrics
        divine_metrics = calculate_divine_metrics(coverage, history_data)
        
        # Get trend data
        trend_window = self.config['report']['features']['history']['trend_window']
        trend_data = get_trend_data(history_data, trend_window)
        
        return {
            'coverage': format_coverage_value(coverage),
            'lines_covered': totals.get('covered_lines', 0),
            'total_lines': totals.get('num_statements', 0),
            'branches_covered': totals.get('covered_branches', 0),
            'total_branches': totals.get('num_branches', 0),
            'functions_covered': totals.get('covered_functions', 0),
            'total_functions': totals.get('num_functions', 0),
            'divine_harmony': format_coverage_value(divine_metrics['harmony'] * 100),
            'sacred_balance': format_coverage_value(divine_metrics['balance'] * 100),
            'divine_resonance': format_coverage_value(divine_metrics['resonance'] * 100),
            'divine_alignment': format_coverage_value(divine_metrics['total'] * 100),
            'modules': self.prepare_modules_data(coverage_data),
            'trend_dates': json.dumps([d.isoformat() for d in trend_data['dates']]),
            'trend_coverage': json.dumps(trend_data['values']),
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def prepare_modules_data(
        self,
        coverage_data: Dict[str, Any]
    ) -> list:
        """Prepare modules data for template rendering."""
        modules = []
        for file_path, data in coverage_data.get('files', {}).items():
            if not file_path.startswith('test_'):
                summary = data.get('summary', {})
                modules.append({
                    'name': file_path,
                    'coverage': format_coverage_value(
                        summary.get('percent_covered', 0)
                    ),
                    'lines_covered': summary.get('covered_lines', 0),
                    'total_lines': summary.get('num_statements', 0),
                    'branches_covered': summary.get('covered_branches', 0),
                    'total_branches': summary.get('num_branches', 0),
                    'functions_covered': summary.get('covered_functions', 0),
                    'total_functions': summary.get('num_functions', 0)
                })
        return sorted(modules, key=lambda x: x['name'])
    
    def render_report(
        self,
        coverage_data: Dict[str, Any],
        history_data: Dict[str, Any]
    ) -> bool:
        """Render the coverage report."""
        try:
            # Load template
            template = self.load_template()
            if not template:
                return False
            
            # Prepare template data
            template_data = self.prepare_template_data(coverage_data, history_data)
            
            # Create output directory
            if not create_output_directory(self.output_dir):
                return False
            
            # Copy assets
            if not copy_assets(self.output_dir):
                return False
            
            # Render template
            output = chevron.render(template, template_data)
            
            # Save rendered report
            output_path = os.path.join(self.output_dir, self.output_file)
            with open(output_path, 'w') as f:
                f.write(output)
            
            logger.info(f'Coverage report rendered successfully: {output_path}')
            return True
        except Exception as e:
            logger.error(f'Error rendering report: {e}')
            return False

def main():
    """Main function to render the coverage report."""
    try:
        # Load coverage data
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
        
        # Load history data
        with open('coverage_history.json', 'r') as f:
            history_data = json.load(f)
        
        # Initialize renderer
        renderer = CoverageReportRenderer()
        
        # Render report
        if renderer.render_report(coverage_data, history_data):
            logger.info('Coverage report generation completed')
        else:
            logger.error('Failed to generate coverage report')
    except FileNotFoundError as e:
        logger.error(f'Required file not found: {e}')
    except json.JSONDecodeError as e:
        logger.error(f'Invalid JSON in data file: {e}')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')

if __name__ == '__main__':
    main() 