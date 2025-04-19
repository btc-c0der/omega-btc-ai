
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

import pytest
from typer.testing import CliRunner
from pathlib import Path
import json
from src.qa_ai.cli.main import app

runner = CliRunner()

def test_cli_init():
    """Test the init command"""
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing QA AI Environment" in result.output
    assert "Environment initialized successfully" in result.output

def test_cli_init_with_config():
    """Test the init command with a custom config path"""
    config_path = "config/qa_config.json"
    result = runner.invoke(app, ["init", "--config", config_path])
    assert result.exit_code == 0
    assert f"Using config file: {config_path}" in result.output

def test_cli_generate_tests():
    """Test the generate-tests command"""
    result = runner.invoke(app, ["generate-tests", "--type", "e2e", "--target", "theknotww.com"])
    assert result.exit_code == 0
    assert "Generating e2e Tests" in result.output
    assert "Tests generated successfully" in result.output

def test_cli_generate_tests_with_output():
    """Test the generate-tests command with custom output directory"""
    output_dir = "tests/generated"
    result = runner.invoke(app, [
        "generate-tests",
        "--type", "e2e",
        "--target", "theknotww.com",
        "--output", output_dir
    ])
    assert result.exit_code == 0
    assert f"Output directory: {output_dir}" in result.output

def test_cli_run_tests():
    """Test the run-tests command"""
    result = runner.invoke(app, ["run-tests"])
    assert result.exit_code == 0
    assert "Running QA Tests" in result.output
    assert "Tests completed successfully" in result.output

def test_cli_run_tests_parallel():
    """Test the run-tests command with parallel execution"""
    result = runner.invoke(app, ["run-tests", "--parallel"])
    assert result.exit_code == 0
    assert "Running tests in parallel" in result.output

def test_cli_metrics():
    """Test the metrics command"""
    result = runner.invoke(app, ["metrics"])
    assert result.exit_code == 0
    assert "QA Metrics Dashboard" in result.output
    assert "Metrics displayed successfully" in result.output

def test_cli_metrics_dashboard():
    """Test the metrics command with dashboard option"""
    result = runner.invoke(app, ["metrics", "--dashboard"])
    assert result.exit_code == 0
    assert "Opening metrics dashboard" in result.output

def test_cli_persona():
    """Test the persona command"""
    result = runner.invoke(app, ["persona", "architect"])
    assert result.exit_code == 0
    assert "Activating architect Persona" in result.output
    assert "architect persona activated successfully" in result.output

def test_cli_persona_with_task():
    """Test the persona command with a specific task"""
    result = runner.invoke(app, ["persona", "architect", "--task", "analyze_requirements"])
    assert result.exit_code == 0
    assert "Task: analyze_requirements" in result.output

def test_cli_help():
    """Test the help command"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "QA AI Command Line Interface" in result.output
    assert "init" in result.output
    assert "generate-tests" in result.output
    assert "run-tests" in result.output
    assert "metrics" in result.output
    assert "persona" in result.output

def test_cli_version():
    """Test the version command"""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "QA AI CLI version" in result.output 