"""
Shared constants for OMEGA AI testing suite.
"""

# Quantum Constants
SCHUMANN_BASE_FREQUENCY = 7.83  # Hz
COSMIC_ALIGNMENT_THRESHOLD = 0.85

# Quantum States
QUANTUM_STATES = ["prophetic", "analytical", "intuitive", "superposition"]

# Test Data
DIVINE_HARMONY_CODE = """
def add(a, b):
    return a + b
"""

ZEN_MASTER_CODE = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

BALANCED_CODE = """
def process_data(data, threshold=0.5):
    results = []
    for item in data:
        if item['value'] > threshold:
            if item['category'] == 'priority':
                results.append(item)
            elif item['category'] == 'standard' and len(results) < 10:
                results.append(item)
    return results
"""

BABYLON_SYSTEM_CODE = """
def process_complex_data(data, options):
    results = []
    for item in data:
        if item['value'] > options['threshold']:
            if item['category'] == 'priority':
                if item['status'] == 'active' or (item['status'] == 'pending' and options['include_pending']):
                    if item['score'] > options['min_score']:
                        if item['region'] in options['allowed_regions']:
                            for tag in item['tags']:
                                if tag in options['target_tags']:
                                    if options['apply_discount']:
                                        item['value'] *= 0.9
                                    if options['sort_by_value']:
                                        results.sort(key=lambda x: x['value'])
                                    results.append(item)
    return results
""" 