"""
Unit tests demonstrating how to mock Discord.py classes for testing.

This file provides examples of mocking various Discord.py objects, including:
- Discord Client
- Context
- Guild
- Channel
- Member
- Message
- Interaction
- Embeds
"""

import pytest
import discord
from discord.ext import commands
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio


class MockDiscordBot:
    """A helper class that provides common Discord mocks."""

    @staticmethod
    def mock_user(**kwargs):
        """Create a mock Discord User object."""
        user = MagicMock(spec=discord.User)
        user.id = kwargs.get("id", 12345)
        user.name = kwargs.get("name", "TestUser")
        user.display_name = kwargs.get("display_name", user.name)
        user.mention = kwargs.get("mention", f"<@{user.id}>")
        user.bot = kwargs.get("bot", False)
        user.avatar = kwargs.get("avatar", "https://example.com/avatar.png")
        user.dm_channel = kwargs.get("dm_channel", MagicMock(spec=discord.DMChannel))
        user.send = AsyncMock()
        return user

    @staticmethod
    def mock_member(**kwargs):
        """Create a mock Discord Member object."""
        guild = kwargs.get("guild", MagicMock(spec=discord.Guild))
        member = MagicMock(spec=discord.Member)
        member.id = kwargs.get("id", 12345)
        member.name = kwargs.get("name", "TestMember")
        member.display_name = kwargs.get("display_name", member.name)
        member.nick = kwargs.get("nick", None)
        member.mention = kwargs.get("mention", f"<@{member.id}>")
        member.bot = kwargs.get("bot", False)
        member.guild = guild
        member.avatar = kwargs.get("avatar", "https://example.com/avatar.png")
        member.roles = kwargs.get("roles", [MagicMock(spec=discord.Role, id=123, name="TestRole")])
        member.top_role = kwargs.get("top_role", member.roles[-1] if member.roles else None)
        member.guild_permissions = kwargs.get("guild_permissions", discord.Permissions())
        member.dm_channel = kwargs.get("dm_channel", MagicMock(spec=discord.DMChannel))
        member.send = AsyncMock()
        member.add_roles = AsyncMock()
        member.remove_roles = AsyncMock()
        return member

    @staticmethod
    def mock_guild(**kwargs):
        """Create a mock Discord Guild object."""
        guild = MagicMock(spec=discord.Guild)
        guild.id = kwargs.get("id", 67890)
        guild.name = kwargs.get("name", "TestGuild")
        guild.owner = kwargs.get("owner", MockDiscordBot.mock_member(id=54321, name="GuildOwner"))
        guild.owner_id = guild.owner.id
        guild.me = kwargs.get("me", MockDiscordBot.mock_member(id=9876, name="Bot", bot=True))
        guild.members = kwargs.get("members", [guild.owner, guild.me])
        
        # Create a member lookup function
        def get_member(member_id):
            for member in guild.members:
                if member.id == member_id:
                    return member
            return None
        
        guild.get_member = get_member
        
        # Set up mock channels
        text_channel = MagicMock(spec=discord.TextChannel, id=111, name="test-channel", guild=guild)
        text_channel.send = AsyncMock()
        voice_channel = MagicMock(spec=discord.VoiceChannel, id=222, name="VoiceTest", guild=guild)
        
        guild.channels = kwargs.get("channels", [text_channel, voice_channel])
        
        # Add functions to get and create channels
        def get_channel(channel_id):
            for channel in guild.channels:
                if channel.id == channel_id:
                    return channel
            return None
        
        guild.get_channel = get_channel
        guild.create_text_channel = AsyncMock()
        guild.create_voice_channel = AsyncMock()
        return guild

    @staticmethod
    def mock_text_channel(**kwargs):
        """Create a mock Discord TextChannel object."""
        guild = kwargs.get("guild", MockDiscordBot.mock_guild())
        channel = MagicMock(spec=discord.TextChannel)
        channel.id = kwargs.get("id", 111)
        channel.name = kwargs.get("name", "test-channel")
        channel.topic = kwargs.get("topic", "A test channel")
        channel.guild = guild
        channel.mention = kwargs.get("mention", f"<#{channel.id}>")
        channel.category = kwargs.get("category", None)
        channel.send = AsyncMock()
        channel.delete = AsyncMock()
        channel.purge = AsyncMock()
        channel.history = AsyncMock()
        
        # Create a default history response
        history_mock = AsyncMock()
        history_messages = kwargs.get("history_messages", [])
        history_mock.__aiter__.return_value = history_messages
        history_mock.__await__ = lambda: asyncio.sleep(0).__await__()
        
        channel.history.return_value = history_mock
        
        return channel

    @staticmethod
    def mock_dm_channel(**kwargs):
        """Create a mock Discord DMChannel object."""
        recipient = kwargs.get("recipient", MockDiscordBot.mock_user())
        channel = MagicMock(spec=discord.DMChannel)
        channel.id = kwargs.get("id", 333)
        channel.recipient = recipient
        channel.send = AsyncMock()
        return channel

    @staticmethod
    def mock_message(**kwargs):
        """Create a mock Discord Message object."""
        author = kwargs.get("author", MockDiscordBot.mock_user())
        guild = kwargs.get("guild", MockDiscordBot.mock_guild())
        channel = kwargs.get("channel", MockDiscordBot.mock_text_channel(guild=guild))
        
        message = MagicMock(spec=discord.Message)
        message.id = kwargs.get("id", 444)
        message.content = kwargs.get("content", "This is a test message")
        message.author = author
        message.channel = channel
        message.guild = guild
        message.mentions = kwargs.get("mentions", [])
        message.mention_everyone = kwargs.get("mention_everyone", False)
        message.role_mentions = kwargs.get("role_mentions", [])
        message.created_at = kwargs.get("created_at", discord.utils.utcnow())
        message.edited_at = kwargs.get("edited_at", None)
        message.attachments = kwargs.get("attachments", [])
        message.embeds = kwargs.get("embeds", [])
        message.reactions = kwargs.get("reactions", [])
        
        # Add async methods
        message.delete = AsyncMock()
        message.edit = AsyncMock()
        message.add_reaction = AsyncMock()
        message.remove_reaction = AsyncMock()
        message.reply = AsyncMock()
        
        return message

    @staticmethod
    def mock_context(**kwargs):
        """Create a mock Discord Context object for command invocation."""
        bot = kwargs.get("bot", MagicMock(spec=commands.Bot))
        guild = kwargs.get("guild", MockDiscordBot.mock_guild())
        channel = kwargs.get("channel", MockDiscordBot.mock_text_channel(guild=guild))
        author = kwargs.get("author", MockDiscordBot.mock_member(guild=guild))
        message = kwargs.get("message", MockDiscordBot.mock_message(
            author=author, 
            channel=channel, 
            guild=guild
        ))
        
        ctx = MagicMock(spec=commands.Context)
        ctx.bot = bot
        ctx.guild = guild
        ctx.channel = channel
        ctx.author = author
        ctx.message = message
        ctx.invoked_with = kwargs.get("invoked_with", "command_name")
        ctx.prefix = kwargs.get("prefix", "!")
        ctx.command = kwargs.get("command", None)
        ctx.args = kwargs.get("args", [ctx, "arg1", "arg2"])
        ctx.kwargs = kwargs.get("kwargs", {"kwarg1": "value1"})
        
        # Add async methods
        ctx.send = AsyncMock()
        ctx.reply = AsyncMock()
        ctx.typing = AsyncMock()
        ctx.trigger_typing = AsyncMock()
        
        return ctx

    @staticmethod
    def mock_interaction(**kwargs):
        """Create a mock Discord Interaction object for slash commands."""
        guild = kwargs.get("guild", MockDiscordBot.mock_guild())
        channel = kwargs.get("channel", MockDiscordBot.mock_text_channel(guild=guild))
        user = kwargs.get("user", MockDiscordBot.mock_user())
        member = kwargs.get("member", MockDiscordBot.mock_member(guild=guild))
        
        interaction = MagicMock(spec=discord.Interaction)
        interaction.id = kwargs.get("id", 555)
        interaction.application_id = kwargs.get("application_id", 777)
        interaction.type = kwargs.get("type", discord.InteractionType.application_command)
        interaction.guild = guild
        interaction.channel = channel
        interaction.user = user
        interaction.member = member
        interaction.response = MagicMock(spec=discord.InteractionResponse)
        
        # Add async methods
        interaction.response.send_message = AsyncMock()
        interaction.response.edit_message = AsyncMock()
        interaction.response.defer = AsyncMock()
        interaction.followup = MagicMock()
        interaction.followup.send = AsyncMock()
        
        # Add data for slash command parameters
        interaction.data = kwargs.get("data", {
            "name": "command_name",
            "options": [
                {"name": "option1", "value": "value1"},
                {"name": "option2", "value": 42}
            ]
        })
        
        # Function to get option values by name
        def get_option(name):
            if not interaction.data or "options" not in interaction.data:
                return None
            for option in interaction.data["options"]:
                if option["name"] == name:
                    return option.get("value")
            return None
            
        interaction.get_option = get_option
        
        return interaction

    @staticmethod
    def mock_embed(**kwargs):
        """Create a mock Discord Embed object."""
        embed = MagicMock(spec=discord.Embed)
        embed.title = kwargs.get("title", "Test Embed")
        embed.description = kwargs.get("description", "This is a test embed")
        embed.color = kwargs.get("color", discord.Color.blue())
        embed.fields = kwargs.get("fields", [])
        
        # Add methods to add fields
        def add_field(name, value, inline=False):
            embed.fields.append({"name": name, "value": value, "inline": inline})
            return embed
        
        embed.add_field = add_field
        embed.set_footer = MagicMock(return_value=embed)
        embed.set_author = MagicMock(return_value=embed)
        embed.set_thumbnail = MagicMock(return_value=embed)
        embed.set_image = MagicMock(return_value=embed)
        
        return embed


# Example test cases to demonstrate usage of the mocks

@pytest.mark.asyncio
async def test_send_message_with_mock():
    """Test sending a message using the mock channel."""
    # Setup
    channel = MockDiscordBot.mock_text_channel()
    
    # Test sending a message
    await channel.send("Hello World!")
    
    # Assertions
    channel.send.assert_called_once_with("Hello World!")

@pytest.mark.asyncio
async def test_bot_command_with_context():
    """Test a bot command using mock context."""
    # Define a simple command function to test
    async def ping_command(ctx):
        await ctx.send("Pong!")
    
    # Setup mock context
    ctx = MockDiscordBot.mock_context()
    
    # Run the command
    await ping_command(ctx)
    
    # Assertions
    ctx.send.assert_called_once_with("Pong!")

@pytest.mark.asyncio
async def test_slash_command_with_interaction():
    """Test a slash command using mock interaction."""
    # Define a simple slash command function to test
    async def greet_command(interaction, name: str):
        await interaction.response.send_message(f"Hello, {name}!")
    
    # Setup mock interaction with custom data
    interaction = MockDiscordBot.mock_interaction(data={
        "name": "greet",
        "options": [{"name": "name", "value": "World"}]
    })
    
    # Get the option value
    name = interaction.get_option("name")
    
    # Run the command
    await greet_command(interaction, name)
    
    # Assertions
    interaction.response.send_message.assert_called_once_with("Hello, World!")

@pytest.mark.asyncio
async def test_message_with_embeds():
    """Test sending a message with an embed."""
    # Setup
    channel = MockDiscordBot.mock_text_channel()
    embed = MockDiscordBot.mock_embed(title="Embed Test", description="Testing embeds")
    embed.add_field("Field 1", "Value 1", inline=True)
    
    # Send message with embed
    await channel.send("Here's an embed", embed=embed)
    
    # Assertions
    channel.send.assert_called_once()
    args, kwargs = channel.send.call_args
    assert args[0] == "Here's an embed"
    assert kwargs["embed"] == embed
    assert len(embed.fields) == 1
    assert embed.fields[0]["name"] == "Field 1"
    assert embed.fields[0]["value"] == "Value 1"

@pytest.mark.asyncio
async def test_member_role_manipulation():
    """Test adding and removing roles from a member."""
    # Setup
    guild = MockDiscordBot.mock_guild()
    role = MagicMock(spec=discord.Role, id=999, name="TestRole")
    member = MockDiscordBot.mock_member(guild=guild)
    
    # Add role to member
    await member.add_roles(role, reason="Testing role addition")
    
    # Assertions
    member.add_roles.assert_called_once_with(role, reason="Testing role addition")
    
    # Remove role from member
    await member.remove_roles(role, reason="Testing role removal")
    
    # Assertions
    member.remove_roles.assert_called_once_with(role, reason="Testing role removal")

@pytest.mark.asyncio
async def test_message_reply():
    """Test replying to messages."""
    # Setup
    message = MockDiscordBot.mock_message(content="Original message")
    
    # Reply to the message
    await message.reply("This is a reply!")
    
    # Assertions
    message.reply.assert_called_once_with("This is a reply!")

@pytest.mark.asyncio
async def test_reaction_handling():
    """Test adding and removing reactions."""
    # Setup
    message = MockDiscordBot.mock_message()
    
    # Add reaction
    await message.add_reaction("👍")
    
    # Assertions
    message.add_reaction.assert_called_once_with("👍")
    
    # Remove reaction
    await message.remove_reaction("👍", message.author)
    
    # Assertions
    message.remove_reaction.assert_called_once_with("👍", message.author)

@pytest.mark.asyncio
async def test_full_bot_workflow():
    """Test a more complex workflow with the bot."""
    # Setup
    guild = MockDiscordBot.mock_guild()
    channel = MockDiscordBot.mock_text_channel(guild=guild)
    member = MockDiscordBot.mock_member(guild=guild, name="CommandUser")
    message = MockDiscordBot.mock_message(
        content="!analyze BTC",
        author=member,
        channel=channel,
        guild=guild
    )
    ctx = MockDiscordBot.mock_context(
        message=message,
        author=member,
        channel=channel,
        guild=guild,
        args=[None, "BTC"],
        invoked_with="analyze"
    )
    
    # Define a command function to test
    async def analyze_command(ctx, symbol):
        embed = discord.Embed(
            title=f"{symbol} Analysis", 
            description=f"Analysis for {symbol}", 
            color=discord.Color.green()
        )
        embed.add_field(name="Price", value="$50,000", inline=True)
        embed.add_field(name="Trend", value="Bullish", inline=True)
        await ctx.send(f"Analysis for {symbol}", embed=embed)
        await ctx.message.add_reaction("✅")
    
    # Run the command
    await analyze_command(ctx, "BTC")
    
    # Assertions
    ctx.send.assert_called_once()
    args, kwargs = ctx.send.call_args
    assert args[0] == "Analysis for BTC"
    assert "embed" in kwargs
    message.add_reaction.assert_called_once_with("✅")

if __name__ == "__main__":
    pytest.main() 