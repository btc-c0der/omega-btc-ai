#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌌 AIXBT Divine Monitor Coverage Report Generator
---------------------------------------------

This script generates a coverage report using the coverage data and templates.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import chevron

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('coverage_report_generator')

def load_coverage_data():
    """Load coverage data from coverage.json file."""
    try:
        with open('coverage.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error('Coverage data file not found')
        return None
    except json.JSONDecodeError:
        logger.error('Invalid JSON in coverage data file')
        return None

def load_coverage_history():
    """Load coverage history from coverage_history.json file."""
    try:
        with open('coverage_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error('Coverage history file not found')
        return None
    except json.JSONDecodeError:
        logger.error('Invalid JSON in coverage history file')
        return None

def prepare_template_data(coverage_data, history_data):
    """Prepare data for the report template."""
    if not coverage_data or not history_data:
        return None

    totals = coverage_data.get('totals', {})
    history = history_data.get('history', {})
    entries = history.get('entries', [])
    latest_entry = entries[0] if entries else {}
    divine_metrics = latest_entry.get('divine_metrics', {})

    return {
        'coverage': round(totals.get('percent_covered', 0), 2),
        'lines_covered': totals.get('covered_lines', 0),
        'total_lines': totals.get('num_statements', 0),
        'branches_covered': totals.get('covered_branches', 0),
        'total_branches': totals.get('num_branches', 0),
        'functions_covered': totals.get('covered_functions', 0),
        'total_functions': totals.get('num_functions', 0),
        'divine_harmony': round(divine_metrics.get('harmony', 0) * 100, 2),
        'sacred_balance': round(divine_metrics.get('balance', 0) * 100, 2),
        'divine_resonance': round(divine_metrics.get('resonance', 0) * 100, 2),
        'divine_alignment': round(history.get('summary', {}).get('divine_alignment', 0) * 100, 2),
        'modules': prepare_modules_data(coverage_data),
        'trend_dates': [entry['timestamp'] for entry in entries],
        'trend_coverage': [entry['coverage'] for entry in entries],
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def prepare_modules_data(coverage_data):
    """Prepare modules data for the report template."""
    modules = []
    for file_path, data in coverage_data.get('files', {}).items():
        if not file_path.startswith('test_'):
            modules.append({
                'name': file_path,
                'coverage': round(data.get('summary', {}).get('percent_covered', 0), 2),
                'lines_covered': data.get('summary', {}).get('covered_lines', 0),
                'total_lines': data.get('summary', {}).get('num_statements', 0),
                'branches_covered': data.get('summary', {}).get('covered_branches', 0),
                'total_branches': data.get('summary', {}).get('num_branches', 0),
                'functions_covered': data.get('summary', {}).get('covered_functions', 0),
                'total_functions': data.get('summary', {}).get('num_functions', 0)
            })
    return sorted(modules, key=lambda x: x['name'])

def generate_report(template_data, output_dir='coverage_reports'):
    """Generate the coverage report using the template."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Read template
        with open('coverage_report_template.html', 'r') as f:
            template = f.read()

        # Generate report
        report = chevron.render(template, template_data)

        # Save report
        output_path = os.path.join(output_dir, 'coverage_report.html')
        with open(output_path, 'w') as f:
            f.write(report)

        logger.info(f'Coverage report generated successfully: {output_path}')
        return True
    except Exception as e:
        logger.error(f'Error generating report: {e}')
        return False

def main():
    """Main function to generate the coverage report."""
    logger.info('Starting coverage report generation')

    # Load data
    coverage_data = load_coverage_data()
    history_data = load_coverage_history()

    if not coverage_data or not history_data:
        return

    # Prepare template data
    template_data = prepare_template_data(coverage_data, history_data)
    if not template_data:
        logger.error('Failed to prepare template data')
        return

    # Generate report
    if generate_report(template_data):
        logger.info('Coverage report generation completed')
    else:
        logger.error('Failed to generate coverage report')

if __name__ == '__main__':
    main() 