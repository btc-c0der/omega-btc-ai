#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA BDD GUILD MANAGER TESTS
Divine tests for the BDD guild manager.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
import json
import tempfile
import shutil

from .bdd_guild_manager import BDDGuildManager, Guild, GuildMember, BestPractice

@pytest.fixture
def temp_guilds_dir():
    """Create a temporary directory for guild data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def guild_manager(temp_guilds_dir):
    """Create a BDD guild manager with temporary storage."""
    return BDDGuildManager(Path(temp_guilds_dir) / "bdd_guilds.json")

def test_create_guild(guild_manager):
    """Test creating a new divine guild."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    assert guild.name == "Divine BDD Guild"
    assert guild.description == "A sacred guild for BDD practices"
    assert len(guild.members) == 0
    assert len(guild.best_practices) == 0
    assert guild.divine_harmony == 0.95

def test_add_member(guild_manager):
    """Test adding a divine member to a guild."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    member = guild_manager.add_member(
        guild_name="Divine BDD Guild",
        name="Divine Tester",
        team="Omega Team",
        expertise=["BDD", "Python", "Testing"]
    )
    
    assert member.name == "Divine Tester"
    assert member.team == "Omega Team"
    assert member.expertise == ["BDD", "Python", "Testing"]
    assert member.divine_knowledge == 0.95
    assert len(member.contributions) == 0

def test_add_best_practice(guild_manager):
    """Test adding a divine best practice to a guild."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    guild_manager.add_member(
        guild_name="Divine BDD Guild",
        name="Divine Tester",
        team="Omega Team",
        expertise=["BDD", "Python", "Testing"]
    )
    
    practice = guild_manager.add_best_practice(
        guild_name="Divine BDD Guild",
        title="Divine Scenario Writing",
        description="Write scenarios that transcend mortal understanding",
        examples=["Given the divine flow is active", "When the market aligns"],
        author="Divine Tester",
        tags={"scenarios", "writing", "divine"},
        references=["Divine Flow Documentation"]
    )
    
    assert practice.title == "Divine Scenario Writing"
    assert practice.author == "Divine Tester"
    assert practice.divine_impact == 0.95
    assert "scenarios" in practice.tags
    assert len(practice.examples) == 2

def test_schedule_meeting(guild_manager):
    """Test scheduling a divine guild meeting."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    meeting_time = datetime.now() + timedelta(days=7)
    guild_manager.schedule_meeting(
        guild_name="Divine BDD Guild",
        meeting_time=meeting_time
    )
    
    guild = guild_manager.get_guild("Divine BDD Guild")
    assert len(guild.meeting_schedule) == 1
    assert guild.meeting_schedule[0] == meeting_time

def test_search_best_practices(guild_manager):
    """Test searching for divine best practices."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    guild_manager.add_member(
        guild_name="Divine BDD Guild",
        name="Divine Tester",
        team="Omega Team",
        expertise=["BDD", "Python", "Testing"]
    )
    
    guild_manager.add_best_practice(
        guild_name="Divine BDD Guild",
        title="Divine Scenario Writing",
        description="Write scenarios that transcend mortal understanding",
        examples=["Given the divine flow is active", "When the market aligns"],
        author="Divine Tester",
        tags={"scenarios", "writing", "divine"},
        references=["Divine Flow Documentation"]
    )
    
    practices = guild_manager.search_best_practices("divine")
    assert len(practices) == 1
    assert practices[0].title == "Divine Scenario Writing"

def test_persistence(guild_manager, temp_guilds_dir):
    """Test that divine guilds persist between manager instances."""
    guild = guild_manager.create_guild(
        name="Divine BDD Guild",
        description="A sacred guild for BDD practices"
    )
    
    guild_manager.add_member(
        guild_name="Divine BDD Guild",
        name="Divine Tester",
        team="Omega Team",
        expertise=["BDD", "Python", "Testing"]
    )
    
    # Create a new manager instance
    new_manager = BDDGuildManager(Path(temp_guilds_dir) / "bdd_guilds.json")
    
    # Verify the guild exists in the new instance
    guild = new_manager.get_guild("Divine BDD Guild")
    assert guild is not None
    assert len(guild.members) == 1
    assert "Divine Tester" in guild.members 