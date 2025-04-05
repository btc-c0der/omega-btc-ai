# 🔴 Live Discord Integration Testing 🔴

This document explains how to run integration tests against a live running instance of the CyBer1t4L Discord bot.

## Overview

While most of the Discord tests use mocking to simulate the Discord API, the live testing functionality connects to a real running instance of the bot to verify its functionality. This allows us to test:

1. The actual connection to Discord
2. Command registration
3. Real-time bot responses

## Prerequisites

To run live Discord tests, you need:

1. A running instance of the CyBer1t4L QA Bot
2. The `.env` file with valid Discord credentials:
   - `DISCORD_BOT_TOKEN`
   - `CYBER1T4L_APP_ID`
   - `CYBER1T4L_PUBLIC_KEY`
3. The required Python packages (see installation section)

## Starting the Bot

If the bot is not already running, you can start it with:

```bash
./src/omega_bot_farm/qa/daemon_runner.sh
```

This will start the bot in the background using a screen session. You can verify it's running with:

```bash
screen -ls
```

Which should show a session named `cyber1t4l_bot`.

## Running Live Tests

### Option 1: Using the Automated Script

The easiest way to run live tests is using the provided script:

```bash
./src/omega_bot_farm/qa/tests/run_live_tests.sh
```

This script will:

1. Check if the bot is running (and start it if not)
2. Install required dependencies
3. Run the live tests
4. Generate an HTML report

### Option 2: Manual Execution

You can also run the tests manually with:

```bash
# Install dependencies
./src/omega_bot_farm/qa/tests/install_test_deps.sh

# Run live tests
python -m src.omega_bot_farm.qa.tests.run_discord_tests --live

# Or run with report generation
python -m src.omega_bot_farm.qa.tests.run_discord_tests --live --html
```

## Understanding Test Results

The live tests will verify:

1. **Bot Process:** Confirms that the bot process is running
2. **Discord Connection:** Verifies that the bot is connected to Discord by querying the Discord API
3. **Command Registration:** Checks that our slash commands are properly registered with Discord

If all tests pass, you should see output like:

```
PASSED src/omega_bot_farm/qa/tests/test_discord_integration.py::TestRunningBotE2E::test_bot_process_running
PASSED src/omega_bot_farm/qa/tests/test_discord_integration.py::TestRunningBotE2E::test_bot_connection_status
PASSED src/omega_bot_farm/qa/tests/test_discord_integration.py::TestRunningBotE2E::test_bot_command_registration
```

## Troubleshooting

### Bot Not Running

If the tests can't find a running bot instance, try:

```bash
# Start the bot manually
./src/omega_bot_farm/qa/daemon_runner.sh

# Verify it's running
ps aux | grep cyber1t4l
```

### Discord API Connection Issues

If tests fail with Discord API errors:

1. Verify your `.env` file has valid credentials
2. Check the bot logs in `src/omega_bot_farm/qa/local_run/logs/`
3. Ensure the bot is properly connected to Discord

### Missing Dependencies

If you encounter import errors:

```bash
# Install all dependencies
./src/omega_bot_farm/qa/tests/install_test_deps.sh
```

## Extension and Customization

### Running Specific Tests

To run a specific live test:

```bash
python -m pytest src/omega_bot_farm/qa/tests/test_discord_integration.py::TestRunningBotE2E::test_bot_connection_status -v
```

### Adding New Live Tests

To add new live tests:

1. Add test methods to the `TestRunningBotE2E` class in `test_discord_integration.py`
2. Use the `check_bot_process` fixture to ensure a bot is running
3. Add appropriate assertions

Example:

```python
@pytest.mark.asyncio
async def test_new_functionality(self, check_bot_process):
    # Your test code here
    assert some_condition
```

## Continuous Integration

For CI environments, you will need to:

1. Set up the bot to run in the CI environment
2. Provide Discord credentials as CI secrets
3. Run the tests with the `--live` flag

Configuring the CI to run the live tests is recommended only for scheduled builds or release validations, not for every commit.

---

🔴 **Note:** Live tests depend on external services and may occasionally fail due to Discord API rate limits or connectivity issues.

🟡 **Reminder:** Always keep your Discord credentials secure and never commit them to the repository.

🟢 **Best Practice:** Use mock-based tests for most development work and reserve live testing for verifying crucial integration points.
