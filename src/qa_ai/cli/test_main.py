import pytest
import typer
import json
import tempfile
from unittest.mock import patch, mock_open
from pathlib import Path
from typer.testing import CliRunner
from datetime import datetime

from qa_ai.cli.main import app, version_callback

runner = CliRunner()

# Fixturesß
@pytest.fixture
def valid_config_file():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        json.dump({"test_framework": "pytest", "environment": "development"}, f)
        return Path(f.name)

@pytest.fixture
def invalid_config_file():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        f.write("this is not valid json")
        return Path(f.name)

# Test version callback
def test_version_callback():
    with pytest.raises(typer.Exit):
        version_callback(True)

# Test main CLI with version flag
def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "QA AI CLI version: 0.1.0" in result.output

# Test init command
@patch("builtins.open", new_callable=mock_open, read_data='{"test": "config"}')
def test_init_command_success(mock_file):
    result = runner.invoke(app, ["init", "--config", "config/qa_config.json"])
    assert result.exit_code == 0
    assert "Initializing QA AI Environment" in result.output
    assert "Environment initialized successfully" in result.output

def test_init_command_real_file(valid_config_file):
    result = runner.invoke(app, ["init", "--config", str(valid_config_file)])
    assert result.exit_code == 0
    assert "Initializing QA AI Environment" in result.output
    assert "Environment initialized successfully" in result.output

def test_init_command_invalid_file(invalid_config_file):
    result = runner.invoke(app, ["init", "--config", str(invalid_config_file)])
    assert result.exit_code == 1
    assert "Error initializing environment" in result.output

# Test generate_tests command
def test_generate_tests_default_type():
    result = runner.invoke(app, ["generate-tests", "--target", "http://example.com"])
    assert result.exit_code == 0
    assert "Generating e2e Tests" in result.output
    assert "Target: http://example.com" in result.output
    assert "Output directory: tests/generated" in result.output

def test_generate_tests_custom_type():
    result = runner.invoke(app, [
        "generate-tests", 
        "--type", "unit", 
        "--target", "http://example.com",
        "--output", "custom/output"
    ])
    assert result.exit_code == 0
    assert "Generating unit Tests" in result.output
    assert "Target: http://example.com" in result.output
    assert "Output directory: custom/output" in result.output

def test_generate_tests_missing_required_target():
    result = runner.invoke(app, ["generate-tests"])
    assert result.exit_code != 0
    assert "Missing option" in result.output

# Test run_tests command
def test_run_tests_sequential():
    result = runner.invoke(app, ["run-tests"])
    assert result.exit_code == 0
    assert "Running QA Tests" in result.output
    assert "Running tests sequentially" in result.output
    assert "Tests completed successfully" in result.output

def test_run_tests_parallel():
    result = runner.invoke(app, ["run-tests", "--parallel"])
    assert result.exit_code == 0
    assert "Running QA Tests" in result.output
    assert "Running tests in parallel" in result.output
    assert "Tests completed successfully" in result.output

# Test metrics command
@patch("datetime.datetime")
def test_metrics_without_dashboard(mock_datetime):
    mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"
    result = runner.invoke(app, ["metrics"])
    assert result.exit_code == 0
    assert "QA Metrics Dashboard" in result.output
    assert "Test Coverage" in result.output
    assert "85%" in result.output
    assert "2023-01-01 12:00:00" in result.output
    assert "Opening metrics dashboard" not in result.output

@patch("datetime.datetime")
def test_metrics_with_dashboard(mock_datetime):
    mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"
    result = runner.invoke(app, ["metrics", "--dashboard"])
    assert result.exit_code == 0
    assert "QA Metrics Dashboard" in result.output
    assert "Test Coverage" in result.output
    assert "85%" in result.output
    assert "Opening metrics dashboard" in result.output
    assert "Metrics displayed successfully" in result.output

# Test persona command
def test_persona_default():
    result = runner.invoke(app, ["persona", "architect"])
    assert result.exit_code == 0
    assert "Activating architect Persona" in result.output
    assert "architect persona activated successfully" in result.output
    assert "Task:" not in result.output

def test_persona_with_task():
    result = runner.invoke(app, ["persona", "explorer", "--task", "security-scan"])
    assert result.exit_code == 0
    assert "Activating explorer Persona" in result.output
    assert "Task: security-scan" in result.output
    assert "explorer persona activated successfully" in result.output

def test_persona_missing_required_type():
    result = runner.invoke(app, ["persona"])
    assert result.exit_code != 0
    assert "Missing argument" in result.output

# Test for "configure" command - new command from prompt
@pytest.mark.parametrize("test_framework", ["pytest", "robot", "playwright"])
def test_configure_test_framework(test_framework):
    result = runner.invoke(app, ["configure", "--test-framework", test_framework])
    assert result.exit_code == 0
    assert f"Test framework configured: {test_framework}" in result.output

# Advanced test for configuration with multiple options
def test_configure_complex_settings():
    result = runner.invoke(app, [
        "configure", 
        "--test-framework", "pytest", 
        "--browser", "chrome",
        "--headless",
        "--parallel-threads", "4",
        "--environment", "staging"
    ])
    assert result.exit_code == 0
    assert "Test framework configured: pytest" in result.output
    assert "Browser: chrome" in result.output
    assert "Headless mode: enabled" in result.output
    assert "Parallel threads: 4" in result.output
    assert "Environment: staging" in result.output