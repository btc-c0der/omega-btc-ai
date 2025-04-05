# Fixing the CommandNotFound Error for test_interactions_report

## The Problem

You're experiencing this error when trying to use the `/test_interactions_report` command in Discord:

```
discord.app_commands.errors.CommandNotFound: Application command 'test_interactions_report' not found
```

This occurs because the command is not properly registered with Discord's API.

## Root Cause Analysis

After examining the code in `test_discord_interactions.py`, we found these issues:

1. **Command defined in wrong scope**: The `test_interactions_report` command is defined inside the `run_tests()` method, which means it might not be properly registered.

2. **Command synchronization issues**: The command is defined after other commands are synced, which means it might not be included in the sync operation.

3. **Multiple sync operations conflicting**: There are multiple calls to `self.client.tree.sync()` which might be overriding each other.

## How to Fix It

### Option 1: Use the Patch Script

The quickest fix is to use the provided patch script:

```bash
# Make the patch executable
chmod +x src/omega_bot_farm/qa/test_discord_interactions_patch.py

# Run the patched version
python src/omega_bot_farm/qa/test_discord_interactions_patch.py
```

The patch script properly registers the `test_interactions_report` command and ensures it's synced both globally and to your Discord server.

### Option 2: Fix the Original File

If you prefer to fix the original file, make these changes:

1. **Move the command definition outside of the `run_tests()` method:**
   - Cut the `test_interactions_report` command definition from `run_tests()`
   - Paste it into the `register_test_commands()` method, at the top level (before defining other commands)

2. **Sync commands in the correct order:**
   - After registering all commands, sync them using two separate operations:

     ```python
     # First sync globally
     await self.client.tree.sync()
     # Then sync to the specific guild
     if self.guild_id:
         guild = discord.Object(id=self.guild_id)
         await self.client.tree.sync(guild=guild)
     ```

3. **Remove redundant sync in `run_tests()`:**
   - Remove the sync operations from `run_tests()` since commands are already synced in `register_test_commands()`

### Option 3: Use the Command Registration Fixer

For a more thorough diagnostic approach, you can use the command registration fixer:

```bash
# Make the fixer executable
chmod +x src/omega_bot_farm/qa/fix_test_interactions_report.py

# Run the fixer (optionally specify a guild ID)
python src/omega_bot_farm/qa/fix_test_interactions_report.py --guild-id YOUR_GUILD_ID
```

This will:

1. Connect to Discord API
2. Register the `test_interactions_report` command
3. Sync it both globally and to your guild
4. Verify that the command is properly registered

## Verifying the Fix

After applying any of these fixes, you should:

1. See log messages confirming that the command was registered and synced
2. Be able to use `/test_interactions_report` in Discord without errors
3. See the command in the Discord slash command list when typing `/`

If the command still doesn't appear in Discord, it may take up to an hour for global commands to propagate. Guild-specific commands should appear almost immediately.

## Prevention

To prevent this issue in the future:

1. Always define commands at the top level, not inside other async functions
2. Sync commands immediately after registering them
3. Verify command registration by fetching the command list from Discord API
4. Use guild-specific commands during development for faster updates
