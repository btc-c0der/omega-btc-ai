#!/usr/bin/env python3
"""
Test suite for Quantum RGB Controller
===================================

Tests both simulation and real hardware modes.
Real hardware tests require iCUE SDK to be installed.
"""

import os
import pytest
import asyncio
import logging
from unittest.mock import Mock, patch, MagicMock
from typing import Generator, AsyncGenerator

# Import the module under test
from omega_ai.peripherals.quantum_rgb_controller import (
    RGBState,
    QuantumUSBController,
    QuantumAIController,
    QuantumRGBManager,
    HAS_ICUE
)

# Test Constants
TEST_BTC_PRICES = [45000, 45500, 44800, 46000, 45000]
TEST_TYPING_METRICS = [(60, 0.95), (75, 0.98), (50, 0.85)]
TEST_QUANTUM_STATES = [(0.8, 0.9), (0.95, 0.85), (0.7, 0.7)]

# Mock SDK for testing
class MockCUESDK:
    def __init__(self, *args):
        self.connected = False
        self.colors = {}
    
    def connect(self):
        self.connected = True
    
    def set_led_colors(self, colors):
        self.colors.update(colors)

# Fixtures
@pytest.fixture
def rgb_state() -> RGBState:
    """Create a test RGB state."""
    return RGBState(r=100, g=150, b=200, brightness=255)

@pytest.fixture
def mock_sdk() -> Generator[MockCUESDK, None, None]:
    """Create a mock SDK."""
    with patch('omega_ai.peripherals.quantum_rgb_controller.cue_sdk.CUESDK', MockCUESDK):
        yield MockCUESDK()

@pytest.fixture
def mock_usb_controller(mock_sdk) -> Generator[QuantumUSBController, None, None]:
    """Create a mock USB controller."""
    controller = QuantumUSBController(use_simulation=True)
    yield controller

@pytest.fixture
def real_usb_controller() -> Generator[QuantumUSBController, None, None]:
    """Create a real USB controller if iCUE is available."""
    if not HAS_ICUE:
        pytest.skip("iCUE SDK not installed")
    controller = QuantumUSBController(use_simulation=False)
    yield controller
    # Cleanup: Reset keyboard to default state
    controller.send_rgb_command(0, 0, 0)

@pytest.fixture
def ai_controller() -> QuantumAIController:
    """Create an AI controller for testing."""
    return QuantumAIController()

@pytest.fixture
async def rgb_manager(mock_usb_controller) -> AsyncGenerator[QuantumRGBManager, None]:
    """Create a test RGB manager with mock USB controller."""
    manager = QuantumRGBManager(use_simulation=True)
    await manager.start()
    yield manager

# Test RGBState
def test_rgb_state_creation():
    """Test RGBState creation and validation."""
    state = RGBState(r=100, g=150, b=200)
    assert state.r == 100
    assert state.g == 150
    assert state.b == 200
    assert state.brightness == 255  # Default
    assert not state.wave_active
    assert not state.pulse_active

def test_rgb_state_validation():
    """Test RGB value validation."""
    with pytest.raises(ValueError):
        RGBState(r=300, g=0, b=0)  # Invalid red value
    with pytest.raises(ValueError):
        RGBState(r=0, g=0, b=0, brightness=300)  # Invalid brightness

# Test QuantumUSBController - Simulation Mode
async def test_usb_controller_simulation(mock_usb_controller):
    """Test USB controller in simulation mode."""
    mock_usb_controller.connect()
    assert mock_usb_controller.connected
    
    # Test RGB command
    mock_usb_controller.send_rgb_command(255, 0, 0)
    assert mock_usb_controller.current_state.r == 255
    assert mock_usb_controller.current_state.g == 0
    assert mock_usb_controller.current_state.b == 0

# Test QuantumUSBController - Real Hardware
@pytest.mark.skipif(not HAS_ICUE, reason="iCUE SDK not installed")
async def test_usb_controller_real_hardware(real_usb_controller):
    """Test USB controller with real hardware."""
    real_usb_controller.connect()
    assert real_usb_controller.connected
    
    # Test basic colors
    real_usb_controller.send_rgb_command(255, 0, 0)  # Red
    await asyncio.sleep(1)
    real_usb_controller.send_rgb_command(0, 255, 0)  # Green
    await asyncio.sleep(1)
    real_usb_controller.send_rgb_command(0, 0, 255)  # Blue
    await asyncio.sleep(1)

# Test QuantumAIController
async def test_btc_price_analysis(ai_controller):
    """Test BTC price analysis and color mapping."""
    # Test initial price
    state = ai_controller.analyze_btc_price(45000)
    assert state.r == 0
    assert state.g == 255  # Green for first price
    
    # Test price increase
    state = ai_controller.analyze_btc_price(45500)
    assert state.g > 0  # Should be green for increase
    assert state.r == 0
    
    # Test price decrease
    state = ai_controller.analyze_btc_price(44800)
    assert state.r > 0  # Should be red for decrease
    assert state.g == 0

async def test_typing_pattern_analysis(ai_controller):
    """Test typing pattern analysis and color mapping."""
    state = ai_controller.analyze_typing_pattern(wpm=75, accuracy=0.98)
    assert state.g > 150  # High green for good WPM
    assert state.r < 50   # Low red for high accuracy
    assert state.b > 200  # High blue for high accuracy

async def test_quantum_state_analysis(ai_controller):
    """Test quantum state analysis and color mapping."""
    state = ai_controller.analyze_quantum_state(coherence=0.8, entanglement=0.9)
    assert state.r == int(0.8 * 255)  # Coherence maps to red
    assert state.g == int(0.9 * 255)  # Entanglement maps to green
    assert state.b == int(0.85 * 255)  # Average maps to blue

# Test QuantumRGBManager
async def test_manager_mode_switching(rgb_manager):
    """Test mode switching in RGB manager."""
    # Test valid modes
    for mode in ["btc", "typing", "quantum", "wave", "pulse"]:
        rgb_manager.set_mode(mode)
        assert rgb_manager.current_mode == mode
    
    # Test invalid mode
    rgb_manager.set_mode("invalid_mode")
    assert rgb_manager.current_mode != "invalid_mode"

async def test_manager_btc_updates(rgb_manager):
    """Test BTC price updates through manager."""
    rgb_manager.set_mode("btc")
    for price in TEST_BTC_PRICES:
        await rgb_manager.update_btc_price(price)
        # Verify RGB state was updated
        assert rgb_manager.usb.current_state is not None

async def test_manager_typing_updates(rgb_manager):
    """Test typing metrics updates through manager."""
    rgb_manager.set_mode("typing")
    for wpm, accuracy in TEST_TYPING_METRICS:
        await rgb_manager.update_typing_metrics(wpm, accuracy)
        # Verify RGB state was updated
        assert rgb_manager.usb.current_state is not None

async def test_manager_quantum_updates(rgb_manager):
    """Test quantum state updates through manager."""
    rgb_manager.set_mode("quantum")
    for coherence, entanglement in TEST_QUANTUM_STATES:
        await rgb_manager.update_quantum_state(coherence, entanglement)
        # Verify RGB state was updated
        assert rgb_manager.usb.current_state is not None

# Integration Tests
@pytest.mark.skipif(not HAS_ICUE, reason="iCUE SDK not installed")
async def test_full_integration_with_hardware():
    """Full integration test with real hardware."""
    manager = QuantumRGBManager(use_simulation=False)
    await manager.start()
    
    # Test BTC mode
    manager.set_mode("btc")
    for price in TEST_BTC_PRICES:
        await manager.update_btc_price(price)
        await asyncio.sleep(0.5)
    
    # Test typing mode
    manager.set_mode("typing")
    for wpm, accuracy in TEST_TYPING_METRICS:
        await manager.update_typing_metrics(wpm, accuracy)
        await asyncio.sleep(0.5)
    
    # Test effects
    manager.set_mode("wave")
    await asyncio.sleep(2)
    manager.set_mode("pulse")
    await asyncio.sleep(2)
    
    # Reset to default
    manager.usb.send_rgb_command(0, 0, 0)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 