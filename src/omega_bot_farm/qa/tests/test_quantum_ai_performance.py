#!/usr/bin/env python3
"""
Performance Tests for the Quantum AI Knowledge Model
---------------------------------------------------

This module contains performance tests for the quantum AI knowledge model
to measure efficiency and resource usage.
"""
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


import os
import time
import pytest
import tempfile
import numpy as np
from datetime import datetime
import gc
import psutil
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple

# Import the module to test
from src.omega_bot_farm.qa.quantum_ai_knowledge_model import (
    QuantumAIKnowledgeModel,
    create_quantum_ai_knowledge_model
)

# Skip performance tests by default
pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_PERFORMANCE_TESTS") != "1",
    reason="Performance tests are skipped by default. Set RUN_PERFORMANCE_TESTS=1 to run."
)

@pytest.fixture
def ai_model():
    """Create an AI knowledge model for testing."""
    return create_quantum_ai_knowledge_model()

@pytest.fixture
def large_code_sample():
    """Generate a large code sample for testing."""
    # Generate a 1000-line Python file
    lines = []
    for i in range(1, 1001):
        if i % 10 == 0:
            # Add a class every 10 lines
            lines.append(f"class TestClass{i//10}:")
            lines.append(f"    def __init__(self):")
            lines.append(f"        self.value = {i}")
            lines.append(f"        self.name = 'Class{i//10}'")
            lines.append("")
        elif i % 5 == 0:
            # Add a function every 5 lines
            lines.append(f"def test_function_{i}(x, y):")
            lines.append(f"    '''Function that adds x and y and multiplies by {i}.'''")
            lines.append(f"    result = (x + y) * {i}")
            lines.append(f"    return result")
            lines.append("")
        else:
            # Add a simple line
            lines.append(f"variable_{i} = {i} * 2")
    
    return "\n".join(lines)

def measure_execution_time(func, *args, **kwargs) -> float:
    """Measure the execution time of a function in seconds."""
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time

def measure_memory_usage(func, *args, **kwargs) -> Tuple[float, float]:
    """Measure memory usage before and after function execution in MB."""
    # Force garbage collection
    gc.collect()
    
    # Get process
    process = psutil.Process(os.getpid())
    
    # Measure memory before
    mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    
    # Run function
    func(*args, **kwargs)
    
    # Force garbage collection again
    gc.collect()
    
    # Measure memory after
    mem_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    
    return mem_before, mem_after

def plot_performance_results(title: str, labels: List[str], values: List[float], 
                           ylabel: str, output_file: str):
    """Plot performance results and save to a file."""
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.1, f"{v:.2f}", ha='center')
    
    # Save plot
    plt.savefig(output_file)
    plt.close()

# Performance Tests

def test_model_initialization_time():
    """Test the time it takes to initialize the model."""
    # Measure initialization time
    init_time = measure_execution_time(create_quantum_ai_knowledge_model)
    
    # Log the result
    print(f"\nModel initialization time: {init_time:.4f} seconds")
    
    # Set a reasonable threshold (adjust based on your system)
    assert init_time < 5.0, f"Model initialization took too long: {init_time:.4f} seconds"

def test_test_generation_performance(ai_model, large_code_sample):
    """Test the performance of test generation."""
    # Measure execution time for different code sizes
    code_sizes = [10, 100, 500, 1000]
    times = []
    
    for size in code_sizes:
        # Get a slice of the code
        code_slice = "\n".join(large_code_sample.split("\n")[:size])
        
        # Measure time - run multiple times to get a measurable value
        total_time = 0
        iterations = 10
        for _ in range(iterations):
            time_taken = measure_execution_time(ai_model.generate_test, code_slice)
            total_time += time_taken
        
        avg_time = total_time / iterations
        times.append(avg_time)
        
        print(f"Test generation time for {size} lines: {avg_time:.4f} seconds")
    
    # Create a performance graph
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    plot_performance_results(
        "Test Generation Performance",
        [f"{size} lines" for size in code_sizes],
        times,
        "Time (seconds)",
        os.path.join(reports_dir, "test_generation_performance.png")
    )
    
    # Check scaling - should be sub-quadratic
    # Avoid division by zero
    if times[0] > 0:
        scaling_factor = times[-1] / times[0]
        size_increase_factor = code_sizes[-1] / code_sizes[0]
        
        assert scaling_factor < size_increase_factor ** 2, \
            f"Test generation doesn't scale well. Scaling factor: {scaling_factor:.2f}"
    else:
        # If times are too small to measure, just make sure they're all reasonable
        assert all(t < 0.1 for t in times), "Some operations took too long"

def test_anomaly_detection_performance(ai_model, large_code_sample):
    """Test the performance of anomaly detection."""
    # Measure execution time for different code sizes
    code_sizes = [10, 100, 500, 1000]
    times = []
    
    for size in code_sizes:
        # Get a slice of the code
        code_slice = "\n".join(large_code_sample.split("\n")[:size])
        
        # Measure time - run multiple times to get a measurable value
        total_time = 0
        iterations = 10
        for _ in range(iterations):
            time_taken = measure_execution_time(ai_model.detect_code_anomalies, code_slice)
            total_time += time_taken
        
        avg_time = total_time / iterations
        times.append(avg_time)
        
        print(f"Anomaly detection time for {size} lines: {avg_time:.4f} seconds")
    
    # Create a performance graph
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    plot_performance_results(
        "Anomaly Detection Performance",
        [f"{size} lines" for size in code_sizes],
        times,
        "Time (seconds)",
        os.path.join(reports_dir, "anomaly_detection_performance.png")
    )
    
    # Check scaling - should be sub-quadratic
    # Avoid division by zero
    if times[0] > 0:
        scaling_factor = times[-1] / times[0]
        size_increase_factor = code_sizes[-1] / code_sizes[0]
        
        assert scaling_factor < size_increase_factor ** 2, \
            f"Anomaly detection doesn't scale well. Scaling factor: {scaling_factor:.2f}"
    else:
        # If times are too small to measure, just make sure they're all reasonable
        assert all(t < 0.1 for t in times), "Some operations took too long"

def test_memory_usage(ai_model, large_code_sample):
    """Test memory usage during operations."""
    # Create a dict to store memory usage
    memory_usage = {}
    
    # Measure memory usage for test generation
    mem_before, mem_after = measure_memory_usage(
        ai_model.generate_test, large_code_sample[:1000]
    )
    memory_usage["Test Generation"] = mem_after - mem_before
    
    # Measure memory usage for anomaly detection
    mem_before, mem_after = measure_memory_usage(
        ai_model.detect_code_anomalies, large_code_sample[:1000]
    )
    memory_usage["Anomaly Detection"] = mem_after - mem_before
    
    # Measure memory usage for dimension measurement
    mem_before, mem_after = measure_memory_usage(
        ai_model.measure_quantum_dimensions, large_code_sample[:1000]
    )
    memory_usage["Dimension Measurement"] = mem_after - mem_before
    
    # Measure memory usage for quantum operations
    def quantum_operations():
        ai_model.quantum_entangle()
        ai_model.quantum_collapse()
    
    mem_before, mem_after = measure_memory_usage(quantum_operations)
    memory_usage["Quantum Operations"] = mem_after - mem_before
    
    # Print memory usage
    for operation, usage in memory_usage.items():
        print(f"Memory usage for {operation}: {usage:.2f} MB")
    
    # Create a performance graph
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    plot_performance_results(
        "Memory Usage by Operation",
        list(memory_usage.keys()),
        list(memory_usage.values()),
        "Memory Usage (MB)",
        os.path.join(reports_dir, "memory_usage.png")
    )
    
    # Check that memory usage is reasonable
    # This threshold may need adjustment based on your system
    max_acceptable_usage = 200  # MB
    for operation, usage in memory_usage.items():
        assert usage < max_acceptable_usage, \
            f"{operation} used too much memory: {usage:.2f} MB"

def test_model_save_load_performance(ai_model):
    """Test performance of model serialization and deserialization."""
    # Create a temporary file
    fd, filepath = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        # Measure save time
        save_time = measure_execution_time(ai_model.save_to_file, filepath)
        print(f"Model save time: {save_time:.4f} seconds")
        
        # Create a new model
        new_model = QuantumAIKnowledgeModel()
        
        # Measure load time
        load_time = measure_execution_time(new_model.load_from_file, filepath)
        print(f"Model load time: {load_time:.4f} seconds")
        
        # Measure file size
        file_size = os.path.getsize(filepath) / (1024 * 1024)  # Convert to MB
        print(f"Model file size: {file_size:.2f} MB")
        
        # Create a performance graph
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        plot_performance_results(
            "Model Serialization Performance",
            ["Save Time", "Load Time"],
            [save_time, load_time],
            "Time (seconds)",
            os.path.join(reports_dir, "model_serialization_performance.png")
        )
        
        # Check performance is reasonable
        assert save_time < 1.0, f"Model saving took too long: {save_time:.4f} seconds"
        assert load_time < 1.0, f"Model loading took too long: {load_time:.4f} seconds"
        assert file_size < 10.0, f"Model file size is too large: {file_size:.2f} MB"
    
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

def test_parallel_dimensional_analysis(ai_model, large_code_sample):
    """Test performance of parallel dimensional analysis."""
    # This test is a placeholder for future parallel implementation
    # In a real implementation, you would compare sequential vs parallel execution
    
    # For now, just measure regular performance
    time_taken = measure_execution_time(ai_model.measure_quantum_dimensions, large_code_sample)
    print(f"Sequential dimensional analysis time: {time_taken:.4f} seconds")
    
    # In a future implementation, you might add:
    # time_taken_parallel = measure_execution_time(ai_model.measure_quantum_dimensions_parallel, large_code_sample)
    # print(f"Parallel dimensional analysis time: {time_taken_parallel:.4f} seconds")
    # 
    # speedup = time_taken / time_taken_parallel
    # print(f"Speedup from parallelization: {speedup:.2f}x")
    
    # For now, just check that the operation completes in a reasonable time
    assert time_taken < 5.0, f"Dimensional analysis took too long: {time_taken:.4f} seconds"

if __name__ == "__main__":
    # Force running all performance tests when script is executed directly
    os.environ["RUN_PERFORMANCE_TESTS"] = "1"
    pytest.main(["-v", __file__]) 