
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Discord.py Testing Utilities

This directory contains utilities and examples for testing Discord.py bots and commands using pytest.

## Overview

Testing Discord bots can be challenging because they typically interact with the Discord API, which requires network calls and valid tokens. These utilities provide mock implementations of Discord objects to enable easier unit testing without making actual API calls.

## Files

- `test_discord_mocks.py` - Contains the `MockDiscordBot` helper class with methods to create mock Discord objects
- `test_discord_events.py` - Example tests for Discord event handlers (on_message, on_member_join, etc.)

## MockDiscordBot Utility

The `MockDiscordBot` class provides methods to create mock versions of common Discord objects:

- `mock_user()` - Creates a mock Discord User
- `mock_member()` - Creates a mock Discord Member (guild user)
- `mock_guild()` - Creates a mock Discord Guild (server)
- `mock_text_channel()` - Creates a mock Discord TextChannel
- `mock_dm_channel()` - Creates a mock Discord DMChannel
- `mock_message()` - Creates a mock Discord Message
- `mock_context()` - Creates a mock commands.Context for testing command invocations
- `mock_interaction()` - Creates a mock Interaction for testing slash commands
- `mock_embed()` - Creates a mock Embed for testing rich message content

## Usage Examples

### Testing a Simple Command

```python
@pytest.mark.asyncio
async def test_ping_command():
    # Create mock context
    ctx = MockDiscordBot.mock_context()
    
    # Call the command function
    await ping_command(ctx)
    
    # Assert the expected response
    ctx.send.assert_called_once_with("Pong!")
```

### Testing a Slash Command

```python
@pytest.mark.asyncio
async def test_slash_command():
    # Create a mock interaction with command options
    interaction = MockDiscordBot.mock_interaction(data={
        "name": "greet",
        "options": [{"name": "name", "value": "World"}]
    })
    
    # Get option value
    name = interaction.get_option("name")
    
    # Call the command
    await greet_command(interaction, name)
    
    # Assert the expected response
    interaction.response.send_message.assert_called_once_with("Hello, World!")
```

### Testing Event Handlers

```python
@pytest.mark.asyncio
async def test_on_message_handler(bot):
    # Create a mock message
    message = MockDiscordBot.mock_message(content="!hello")
    
    # Call the event handler
    await on_message(message)
    
    # Assert expected behavior
    message.channel.send.assert_called_once_with("Hello there!")
```

## Best Practices

1. **Isolate dependencies**: Mock all external Discord API calls to ensure tests run quickly and reliably.

2. **Use fixtures**: Create pytest fixtures for common objects like bot instances to avoid repetition.

3. **Test edge cases**: Include tests for error conditions, empty inputs, and unusual scenarios.

4. **Parameterize tests**: Use `@pytest.mark.parametrize` to test multiple variations of inputs.

5. **Check for specific behavior**: Assert that the correct methods were called with the expected arguments.

## Setup for Your Tests

Add the following to your `conftest.py` file to make these helpers available to all your tests:

```python
import sys
import pytest
from pathlib import Path

# Add the discord mocks directory to the path
test_dir = Path(__file__).parent
sys.path.append(str(test_dir / "unit" / "discord"))

# Import the mock helper
from test_discord_mocks import MockDiscordBot

@pytest.fixture
def discord_mock():
    """Provide the MockDiscordBot helper to tests."""
    return MockDiscordBot
```

## Known Limitations

- These mocks simulate Discord objects but don't fully replicate all Discord API behaviors.
- Some advanced Discord features may require additional customization of the mock objects.
- Interactions with external services (like databases or APIs) used by your bot still need to be mocked separately.

## Contributing

Feel free to enhance these mocks with additional Discord functionality as needed for your testing. Consider submitting improvements back to the project if they're broadly useful.
