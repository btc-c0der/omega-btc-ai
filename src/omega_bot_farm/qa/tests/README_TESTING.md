# CyBer1t4L Discord Integration Tests

This directory contains tests for the Discord integration of the CyBer1t4L QA Bot. The tests are designed to simulate Discord interactions without requiring a live connection to Discord.

## Overview

The test suite includes several approaches to testing Discord bot functionality:

1. **Mock-based tests**: Using Python's unittest.mock to simulate Discord interactions
2. **discord.ext.test**: Using a specialized testing framework for discord.py
3. **HTTP mock tests**: Simulating Discord's webhook interactions (disabled by default)
4. **End-to-end tests**: For testing with a real Discord connection (new!)
5. **VCR.py tests**: Recording and replaying real Discord API interactions

## Prerequisites

### Required Packages

```bash
# Core testing packages
pip install pytest pytest-asyncio

# Discord testing extension
pip install -U discord.ext.test

# Optional: For HTTP-based tests
pip install httpx respx starlette

# For live testing
pip install python-dotenv
```

## Running the Tests

### Basic Test Run

```bash
# Run all tests
python -m pytest src/omega_bot_farm/qa/tests/test_discord_integration.py -v

# Run specific test class
python -m pytest src/omega_bot_farm/qa/tests/test_discord_integration.py::TestDiscordIntegration -v

# Run specific test
python -m pytest src/omega_bot_farm/qa/tests/test_discord_integration.py::TestDiscordIntegration::test_slash_ping_command -v
```

### Running with Coverage

```bash
# Run tests with coverage report
python -m pytest src/omega_bot_farm/qa/tests/test_discord_integration.py --cov=src.omega_bot_farm.qa.cyber1t4l_qa_bot --cov-report=term
```

### Using the Unified Test Runner

We now have a unified test runner script that can run all tests and generate reports:

```bash
# Install dependencies and run all tests with HTML report
python -m src.omega_bot_farm.qa.tests.run_discord_tests --install-deps --html

# Run specific test file
python -m src.omega_bot_farm.qa.tests.run_discord_tests --test-file src/omega_bot_farm/qa/tests/test_discord_buttons.py
```

### Live Testing with Running Bot

You can now run tests against a live running instance of the CyBer1t4L QA Bot:

```bash
# Easy way - use the script that handles everything
./src/omega_bot_farm/qa/tests/run_live_tests.sh

# Or run manually
python -m src.omega_bot_farm.qa.tests.run_discord_tests --live
```

For more information about live testing, see [LIVE_TESTING.md](LIVE_TESTING.md).

## Test Categories

### Unit Tests with Mocks

These tests use Python's `unittest.mock` to create mock Discord objects and verify that our bot code interacts with them correctly. These tests don't require any external connections and are fast to run.

Example:

```python
@pytest.mark.asyncio
async def test_slash_ping_command():
    interaction = MockInteraction(command_name="ping")
    await slash_ping(interaction)
    interaction.response.send_message.assert_called_once_with("🧪 PONG! CyBer1t4L QA Bot is alive")
```

### Integration Tests with discord.ext.test

These tests use the `discord.ext.test` library to simulate a more complete Discord environment. This allows testing the integration between our bot code and discord.py.

Example:

```python
@pytest.mark.asyncio
async def test_ping_command(bot_setup):
    await dpytest.message("!testcommand")
    assert dpytest.verify().message().content("Test command executed successfully!")
```

### HTTP-based Tests

These tests simulate the HTTP interactions between Discord and our bot, which is particularly useful for testing slash commands and interaction components.

Example (requires httpx and respx):

```python
def test_interaction_webhook():
    client = TestClient(app)
    interaction_payload = {...}  # Discord interaction payload
    response = client.post("/interactions", json=interaction_payload)
    assert response.status_code == 200
```

### End-to-end Tests

These tests verify that our bot can actually connect to Discord and has registered the expected commands. They work with a running bot instance and use the Discord API to verify functionality.

Example:

```python
@pytest.mark.asyncio
async def test_bot_command_registration(self, check_bot_process):
    # Check global application commands
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://discord.com/api/v10/applications/{app_id}/commands',
            headers=headers
        )
        
        # Verify commands are registered
        command_names = [cmd['name'] for cmd in response.json()]
        assert any(cmd in command_names for cmd in expected_commands)
```

## Troubleshooting

### Missing discord.ext.test

If you see tests being skipped with the message "discord.ext.test not installed", install it with:

```bash
pip install -U discord.ext.test
```

### Discord.py Version Compatibility

Make sure you're using a compatible version of discord.py:

```bash
pip install -U discord.py==2.3.0
```

### Rate Limiting

If running tests with a real Discord token, be aware of Discord's rate limits.

### Missing Dependencies

You can install all dependencies at once with:

```bash
./src/omega_bot_farm/qa/tests/install_test_deps.sh
```

## Extending the Tests

### Adding New Slash Command Tests

To add tests for a new slash command:

1. Add a mock test in `TestDiscordIntegration`
2. Add a simulated command in the `bot_setup` fixture for dpytest
3. Optionally add an HTTP mock test if the command has complex interactions

### Testing Interactive Components

For buttons, select menus, and modals:

1. Create appropriate mock objects with expected attributes
2. Simulate the interaction events
3. Verify the bot responds correctly

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [discord.ext.test Documentation](https://github.com/CheeseCake87/discord.ext.test)
- [Discord API Documentation](https://discord.com/developers/docs/intro)
- [pytest Documentation](https://docs.pytest.org/)
