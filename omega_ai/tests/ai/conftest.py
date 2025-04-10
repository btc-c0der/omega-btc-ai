
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

"""
Shared fixtures for OMEGA AI testing suite.
"""

import pytest
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from datetime import datetime
from unittest.mock import patch, MagicMock
from freezegun import freeze_time

from omega_ai.tests.ai.constants import (
    SCHUMANN_BASE_FREQUENCY,
    DIVINE_HARMONY_CODE,
    ZEN_MASTER_CODE,
    BALANCED_CODE,
    BABYLON_SYSTEM_CODE
)

class SimpleTestModel(nn.Module):
    """Simple neural network for testing"""
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)
        
    def forward(self, x):
        return self.fc(x)

@pytest.fixture
def tester():
    """Create a QuantumAITester instance for testing"""
    from omega_ai.tests.ai.quantum_ai_testing import QuantumAITester
    return QuantumAITester()

@pytest.fixture
def model():
    """Create a simple test model"""
    return SimpleTestModel()

@pytest.fixture
def test_data():
    """Create sample test data"""
    return torch.randn(32, 10)  # batch_size=32, input_size=10

@pytest.fixture
def sample_schumann_data():
    """Create sample Schumann resonance data"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-02', freq='H')
    return pd.DataFrame({
        'timestamp': dates,
        'frequency': np.random.normal(SCHUMANN_BASE_FREQUENCY, 0.1, len(dates)),
        'amplitude': np.random.uniform(0.5, 1.5, len(dates))
    })

@pytest.fixture
def omega_analyzer():
    """Provide a divine OMEGA FORMULA ALGO analyzer."""
    with patch('datetime.datetime') as mock_datetime:
        # Set mock date to ensure consistent moon phase
        mock_date = MagicMock()
        mock_date.day = 15
        mock_date.month = 3
        mock_datetime.now.return_value = mock_date
        
        from omega_ai.quality.omega_formula_algo import OmegaFormulaAlgo
        return OmegaFormulaAlgo(schumann_frequency=SCHUMANN_BASE_FREQUENCY)

@pytest.fixture
def test_code_samples():
    """Provide test code samples"""
    return {
        'divine_harmony': DIVINE_HARMONY_CODE,
        'zen_master': ZEN_MASTER_CODE,
        'balanced': BALANCED_CODE,
        'babylon_system': BABYLON_SYSTEM_CODE
    } 