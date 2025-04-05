"""
Unit tests for Discord.py event handlers.

This file demonstrates how to test Discord event handlers such as:
- on_message
- on_member_join
- on_reaction_add
- on_guild_join
- on_command_error
"""

import pytest
import discord
import asyncio
from discord.ext import commands
from unittest.mock import AsyncMock, MagicMock, patch

# Import the mock helper from our other test file
from .test_discord_mocks import MockDiscordBot


class TestDiscordEventHandlers:
    """Test suite for Discord event handlers."""

    @pytest.fixture
    def bot(self):
        """Create a mock Discord bot instance for testing."""
        bot = MagicMock(spec=commands.Bot)
        # Setup async methods
        bot.send_message = AsyncMock()
        bot.add_reaction = AsyncMock()
        bot.process_commands = AsyncMock()
        
        # Set up bot attributes
        bot.user = MockDiscordBot.mock_user(id=9999, name="TestBot", bot=True)
        
        return bot
    
    @pytest.mark.asyncio
    async def test_on_message_event(self, bot):
        """Test the on_message event handler."""
        # Define a sample on_message handler
        async def on_message(message):
            # Don't respond to our own messages
            if message.author == bot.user:
                return
                
            # Echo the message content in uppercase if it starts with "!"
            if message.content.startswith("!echo "):
                echo_text = message.content[6:].upper()
                await message.channel.send(echo_text)
                
            # Process commands would normally be called here
            await bot.process_commands(message)
        
        # Create mock message from a regular user (not the bot)
        user_message = MockDiscordBot.mock_message(
            content="!echo hello world",
            author=MockDiscordBot.mock_user(id=12345)  # Different from bot.user
        )
        
        # Create mock message from the bot itself
        bot_message = MockDiscordBot.mock_message(
            content="!echo test",
            author=bot.user  # Same as bot.user
        )
        
        # Test handling a user message
        await on_message(user_message)
        
        # Verify channel.send was called with uppercase text
        user_message.channel.send.assert_called_once_with("HELLO WORLD")
        # Verify process_commands was called
        bot.process_commands.assert_called_once_with(user_message)
        
        # Reset mocks
        bot.process_commands.reset_mock()
        
        # Test handling a bot message (should be ignored)
        await on_message(bot_message)
        
        # Verify channel.send was NOT called
        bot_message.channel.send.assert_not_called()
        # Verify process_commands was NOT called
        bot.process_commands.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_on_member_join_event(self, bot):
        """Test the on_member_join event handler."""
        # Define a sample on_member_join handler
        async def on_member_join(member):
            # Send welcome message to a welcome channel
            welcome_channel_id = 111  # Example channel ID
            welcome_channel = member.guild.get_channel(welcome_channel_id)
            
            if welcome_channel:
                await welcome_channel.send(f"Welcome {member.mention} to the server!")
                
            # Add a default role
            default_role = discord.utils.get(member.guild.roles, name="Member")
            if default_role:
                await member.add_roles(default_role)
        
        # Mock guild setup
        guild = MockDiscordBot.mock_guild()
        welcome_channel = MockDiscordBot.mock_text_channel(id=111)
        
        # Add welcome_channel to guild channels
        guild.channels = [welcome_channel]
        
        # Create mock member and roles
        default_role = MagicMock(spec=discord.Role, id=222, name="Member")
        member = MockDiscordBot.mock_member(
            id=12345, 
            name="NewMember",
            guild=guild
        )
        
        # Configure guild to return the role when searched
        def get_role_by_name(roles, name):
            for role in roles:
                if role.name == name:
                    return role
            return None
            
        # Patch discord.utils.get to return our mock role
        with patch('discord.utils.get', side_effect=lambda roles, name: 
                   get_role_by_name([default_role], name) if name == "Member" else None):
            # Test the event handler
            await on_member_join(member)
            
        # Verify welcome message was sent
        welcome_channel.send.assert_called_once_with(f"Welcome {member.mention} to the server!")
        
        # Verify role was added
        member.add_roles.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_on_reaction_add_event(self, bot):
        """Test the on_reaction_add event handler."""
        # Define a sample on_reaction_add handler for a reaction role system
        async def on_reaction_add(reaction, user):
            # Don't respond to bot reactions
            if user.bot:
                return
                
            # Check if this is a role assignment message
            if reaction.message.id == 999888:  # Example role message ID
                # Map of emojis to role names
                role_emojis = {
                    "🔴": "Red Team",
                    "🔵": "Blue Team",
                    "🟢": "Green Team"
                }
                
                # Check if the emoji is one of our role emojis
                if reaction.emoji in role_emojis:
                    role_name = role_emojis[reaction.emoji]
                    role = discord.utils.get(reaction.message.guild.roles, name=role_name)
                    
                    if role:
                        # Get the member object for the user
                        member = reaction.message.guild.get_member(user.id)
                        if member:
                            await member.add_roles(role)
        
        # Mock guild setup
        guild = MockDiscordBot.mock_guild()
        
        # Create mock roles
        red_role = MagicMock(spec=discord.Role, id=111, name="Red Team")
        blue_role = MagicMock(spec=discord.Role, id=222, name="Blue Team")
        green_role = MagicMock(spec=discord.Role, id=333, name="Green Team")
        
        # Create mock user and member
        user = MockDiscordBot.mock_user(id=12345, name="ReactingUser")
        member = MockDiscordBot.mock_member(id=user.id, name=user.name, guild=guild)
        
        # Add member to guild
        guild.members.append(member)
        
        # Create a mock message
        message = MockDiscordBot.mock_message(id=999888, guild=guild)
        
        # Create a mock reaction
        reaction = MagicMock()
        reaction.emoji = "🔴"  # Red team emoji
        reaction.message = message
        
        # Configure guild to find the member and role
        guild.get_member.return_value = member
        
        # Patch discord.utils.get to return our mock roles
        def get_mock_role(roles, name):
            role_map = {
                "Red Team": red_role,
                "Blue Team": blue_role,
                "Green Team": green_role
            }
            return role_map.get(name)
            
        with patch('discord.utils.get', side_effect=lambda roles, name: get_mock_role(roles, name)):
            # Test the event handler
            await on_reaction_add(reaction, user)
            
        # Verify role was added
        member.add_roles.assert_called_once_with(red_role)
    
    @pytest.mark.asyncio
    async def test_on_guild_join_event(self, bot):
        """Test the on_guild_join event handler."""
        # Define a sample on_guild_join handler
        async def on_guild_join(guild):
            # Try to find a general channel to post an introduction
            general_channel = None
            
            # Check for a channel called general first
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == "general":
                    general_channel = channel
                    break
            
            # If no general channel, use the first text channel
            if not general_channel:
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        general_channel = channel
                        break
            
            # Send introduction message to the channel
            if general_channel:
                intro_message = (
                    f"Hello {guild.name}! Thanks for adding me to your server.\n"
                    f"Use `!help` to see my commands."
                )
                await general_channel.send(intro_message)
        
        # Create mock guild with channels
        general_channel = MockDiscordBot.mock_text_channel(id=111, name="general")
        random_channel = MockDiscordBot.mock_text_channel(id=222, name="random")
        
        guild = MockDiscordBot.mock_guild(
            id=55555,
            name="New Server",
            channels=[general_channel, random_channel]
        )
        
        # Test the event handler
        await on_guild_join(guild)
        
        # Verify the introduction message was sent to the general channel
        general_channel.send.assert_called_once()
        
        # Check the content of the message
        args, _ = general_channel.send.call_args
        assert f"Hello {guild.name}" in args[0]
        assert "!help" in args[0]
        
        # Now test with a guild that doesn't have a general channel
        other_channel = MockDiscordBot.mock_text_channel(id=333, name="other")
        guild_no_general = MockDiscordBot.mock_guild(
            id=66666,
            name="Another Server",
            channels=[other_channel]
        )
        
        # Reset mocks
        other_channel.send.reset_mock()
        
        # Test the event handler
        await on_guild_join(guild_no_general)
        
        # Verify the introduction message was sent to the first available text channel
        other_channel.send.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_on_command_error_event(self, bot):
        """Test the on_command_error event handler."""
        # Define a sample on_command_error handler
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f"Command not found. Use `{ctx.prefix}help` to see available commands.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Missing required argument: {error.param.name}")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("Invalid argument provided.")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send("You don't have permission to use this command.")
            else:
                await ctx.send(f"An error occurred: {str(error)}")
        
        # Create a mock context
        ctx = MockDiscordBot.mock_context(prefix="!")
        
        # Test CommandNotFound error
        command_not_found = commands.CommandNotFound()
        await on_command_error(ctx, command_not_found)
        
        # Verify correct response
        ctx.send.assert_called_once()
        args, _ = ctx.send.call_args
        assert "Command not found" in args[0]
        
        # Reset mock
        ctx.send.reset_mock()
        
        # Test MissingRequiredArgument error
        # We need to mock a Parameter object for MissingRequiredArgument
        param = MagicMock()
        param.name = "amount"
        missing_arg = commands.MissingRequiredArgument(param)
        
        await on_command_error(ctx, missing_arg)
        
        # Verify correct response
        ctx.send.assert_called_once()
        args, _ = ctx.send.call_args
        assert "Missing required argument: amount" in args[0]
        
        # Reset mock
        ctx.send.reset_mock()
        
        # Test BadArgument error
        bad_arg = commands.BadArgument()
        await on_command_error(ctx, bad_arg)
        
        # Verify correct response
        ctx.send.assert_called_once()
        args, _ = ctx.send.call_args
        assert "Invalid argument" in args[0]
    
    @pytest.mark.asyncio
    async def test_on_voice_state_update_event(self, bot):
        """Test the on_voice_state_update event handler."""
        # Define a sample on_voice_state_update handler for tracking join/leave
        async def on_voice_state_update(member, before, after):
            # Check if the member joined a voice channel
            if before.channel is None and after.channel is not None:
                # Member joined a voice channel
                log_channel = member.guild.get_channel(123)  # Log channel ID
                if log_channel:
                    await log_channel.send(f"{member.display_name} joined {after.channel.name}")
            
            # Check if the member left a voice channel
            elif before.channel is not None and after.channel is None:
                # Member left a voice channel
                log_channel = member.guild.get_channel(123)  # Log channel ID
                if log_channel:
                    await log_channel.send(f"{member.display_name} left {before.channel.name}")
        
        # Create mock guild and channels
        log_channel = MockDiscordBot.mock_text_channel(id=123, name="logs")
        voice_channel = MagicMock(spec=discord.VoiceChannel, id=456, name="Voice Chat")
        
        guild = MockDiscordBot.mock_guild(
            channels=[log_channel, voice_channel]
        )
        
        # Create mock member
        member = MockDiscordBot.mock_member(
            id=12345,
            name="VoiceUser",
            display_name="Voice User",
            guild=guild
        )
        
        # Create voice states for before/after
        before_state = MagicMock(channel=None)  # Not in a voice channel
        after_state = MagicMock(channel=voice_channel)  # In a voice channel
        
        # Test joining a voice channel
        await on_voice_state_update(member, before_state, after_state)
        
        # Verify log message
        log_channel.send.assert_called_once()
        args, _ = log_channel.send.call_args
        assert f"{member.display_name} joined {voice_channel.name}" in args[0]
        
        # Reset mock
        log_channel.send.reset_mock()
        
        # Test leaving a voice channel
        await on_voice_state_update(member, after_state, before_state)
        
        # Verify log message
        log_channel.send.assert_called_once()
        args, _ = log_channel.send.call_args
        assert f"{member.display_name} left {voice_channel.name}" in args[0]
    
    @pytest.mark.asyncio
    async def test_on_ready_event(self, bot):
        """Test the on_ready event handler."""
        # Create a tracking variable to verify the handler was called
        called = False
        
        # Define a sample on_ready handler
        async def on_ready():
            nonlocal called
            called = True
            
            # Set bot presence
            activity = discord.Game(name="Testing")
            await bot.change_presence(activity=activity)
            
            # Log that the bot is ready
            print(f"{bot.user.name} has connected to Discord!")
        
        # Set up the change_presence mock
        bot.change_presence = AsyncMock()
        
        # Test the on_ready event
        await on_ready()
        
        # Verify the handler was called and side effects occurred
        assert called is True
        bot.change_presence.assert_called_once()
        
        # Check that the activity was set correctly
        args, kwargs = bot.change_presence.call_args
        assert isinstance(kwargs['activity'], discord.Game)
        assert kwargs['activity'].name == "Testing"


if __name__ == "__main__":
    pytest.main() 