# Discord Interaction Testing Suite for CyBer1t4L Bot

This document covers the Discord interaction testing suite for CyBer1t4L QA Bot, which allows comprehensive testing of Discord.py's interaction endpoints used by the bot.

## Overview

The testing suite provides a way to verify that all Discord interaction methods used by the CyBer1t4L bot work correctly. It tests the following interaction endpoints:

1. `interaction.response.send_message()` - Direct message responses
2. `interaction.response.defer()` - Deferred responses with followup
3. `interaction.edit_original_response()` - Editing initial responses
4. `interaction.response.is_done()` - Checking if a response is complete
5. `interaction.original_response()` - Retrieving the original response
6. Error handling during interactions

## Installation Requirements

Ensure you have the required dependencies:

```bash
pip install discord.py python-dotenv
```

## Configuration

The test suite uses the same environment variables as the main bot:

- `DISCORD_BOT_TOKEN` - Your Discord bot token
- `CYBER1T4L_APP_ID` - Your bot's application ID

These can be set in your `.env` file or passed directly as command-line arguments.

## Running the Tests

To run the interaction tests:

```bash
python src/omega_bot_farm/qa/test_discord_interactions.py
```

Or with explicit token:

```bash
python src/omega_bot_farm/qa/test_discord_interactions.py --token YOUR_TOKEN --app-id YOUR_APP_ID
```

## Test Commands

Once the bot is running, the following slash commands will be available in your Discord server:

- `/test_interactions response_send_message` - Tests direct message responses
- `/test_interactions response_defer` - Tests deferred responses
- `/test_interactions response_edit` - Tests editing original responses
- `/test_interactions response_is_done` - Tests checking response completion status
- `/test_interactions error_handling` - Tests error handling during interactions
- `/test_interactions original_response` - Tests retrieving original responses
- `/test_interactions_report` - Generates a report of all test results

## Test Reports

After running the tests, use the `/test_interactions_report` command to get a summary of test results. This will show which tests passed and which failed, including error details for failures.

## Troubleshooting

If you encounter issues:

1. **Command sync issues**: Ensure your bot has the correct permissions, including the `applications.commands` scope.
2. **Response failures**: Check that your bot has proper permissions in the channel.
3. **Interaction timeouts**: Discord interactions must be acknowledged within 3 seconds. If you're seeing timeouts, check that your code is responding promptly.
4. **Privileged intent issues**: Verify that the "Message Content Intent" is enabled in the Discord Developer Portal.

## Mapping to Discord.py Interaction API

Here's how our tests map to the official Discord.py Interaction API:

| Test Command | API Method | Description |
|--------------|------------|-------------|
| `response_send_message` | `interaction.response.send_message()` | Sends an immediate response to an interaction |
| `response_defer` | `interaction.response.defer()` | Defers the response, allowing for longer processing time |
| `response_edit` | `interaction.edit_original_response()` | Edits the original interaction response |
| `response_is_done` | `interaction.response.is_done()` | Checks if the interaction has been responded to |
| `original_response` | `interaction.original_response()` | Fetches the original interaction response |

## Example Test Output

```
# Discord Interactions Test Report

✅ response_send_message: success
✅ response_defer: success
✅ response_edit: success
✅ response_is_done: success
✅ error_handling: success
✅ original_response: success
```

## Additional Resources

- [Discord.py Interactions API Documentation](https://discordpy.readthedocs.io/en/stable/interactions/api.html)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [CyBer1t4L Bot Documentation](README_CYBER1T4L.md)
