#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OMEGA BDD GUILD MANAGER
Divine manager for cross-team BDD practices.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Set, Optional, Union
from pathlib import Path
import json

@dataclass
class GuildMember:
    """Sacred representation of a guild member."""
    name: str
    team: str
    expertise: List[str]
    divine_knowledge: float
    contributions: List[str] = field(default_factory=list)
    last_active: datetime = field(default_factory=datetime.now)

@dataclass
class BestPractice:
    """Sacred representation of a BDD best practice."""
    title: str
    description: str
    examples: List[str]
    author: str
    created_at: datetime
    divine_impact: float
    tags: Set[str] = field(default_factory=set)
    references: List[str] = field(default_factory=list)

@dataclass
class Guild:
    """Sacred representation of a BDD guild."""
    name: str
    description: str
    members: Dict[str, GuildMember]
    best_practices: List[BestPractice]
    divine_harmony: float
    meeting_schedule: List[datetime] = field(default_factory=list)
    knowledge_base: List[str] = field(default_factory=list)

class BDDGuildManager:
    """Divine manager for BDD guilds and best practices."""
    
    def __init__(self, guilds_path: Union[str, Path] = "bdd_guilds.json"):
        self.guilds_path = Path(guilds_path)
        self.guilds: Dict[str, Guild] = {}
        self._load_guilds()
    
    def _load_guilds(self) -> None:
        """Load the divine guilds from disk."""
        if self.guilds_path.exists():
            with open(self.guilds_path, 'r') as f:
                data = json.load(f)
                for guild_data in data:
                    guild = self._create_guild_from_data(guild_data)
                    self.guilds[guild.name] = guild
    
    def _create_guild_from_data(self, data: Dict) -> Guild:
        """Create a divine guild from JSON data."""
        members = {}
        for member_data in data['members']:
            member = GuildMember(
                name=member_data['name'],
                team=member_data['team'],
                expertise=member_data['expertise'],
                divine_knowledge=member_data['divine_knowledge'],
                contributions=member_data['contributions'],
                last_active=datetime.fromisoformat(member_data['last_active'])
            )
            members[member.name] = member
        
        best_practices = []
        for practice_data in data['best_practices']:
            practice = BestPractice(
                title=practice_data['title'],
                description=practice_data['description'],
                examples=practice_data['examples'],
                author=practice_data['author'],
                created_at=datetime.fromisoformat(practice_data['created_at']),
                divine_impact=practice_data['divine_impact'],
                tags=set(practice_data['tags']),
                references=practice_data['references']
            )
            best_practices.append(practice)
        
        return Guild(
            name=data['name'],
            description=data['description'],
            members=members,
            best_practices=best_practices,
            divine_harmony=data['divine_harmony'],
            meeting_schedule=[datetime.fromisoformat(d) for d in data['meeting_schedule']],
            knowledge_base=data['knowledge_base']
        )
    
    def _save_guilds(self) -> None:
        """Save the divine guilds to disk."""
        data = []
        for guild in self.guilds.values():
            guild_data = {
                'name': guild.name,
                'description': guild.description,
                'members': [
                    {
                        'name': member.name,
                        'team': member.team,
                        'expertise': member.expertise,
                        'divine_knowledge': member.divine_knowledge,
                        'contributions': member.contributions,
                        'last_active': member.last_active.isoformat()
                    }
                    for member in guild.members.values()
                ],
                'best_practices': [
                    {
                        'title': practice.title,
                        'description': practice.description,
                        'examples': practice.examples,
                        'author': practice.author,
                        'created_at': practice.created_at.isoformat(),
                        'divine_impact': practice.divine_impact,
                        'tags': list(practice.tags),
                        'references': practice.references
                    }
                    for practice in guild.best_practices
                ],
                'divine_harmony': guild.divine_harmony,
                'meeting_schedule': [d.isoformat() for d in guild.meeting_schedule],
                'knowledge_base': guild.knowledge_base
            }
            data.append(guild_data)
        
        with open(self.guilds_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_guild(self, name: str, description: str) -> Guild:
        """Create a new divine guild."""
        if name in self.guilds:
            raise ValueError(f"Divine guild already exists: {name}")
        
        guild = Guild(
            name=name,
            description=description,
            members={},
            best_practices=[],
            divine_harmony=0.95  # Initial divine harmony
        )
        
        self.guilds[name] = guild
        self._save_guilds()
        return guild
    
    def add_member(self, guild_name: str, name: str, team: str,
                  expertise: List[str]) -> GuildMember:
        """Add a divine member to a guild."""
        if guild_name not in self.guilds:
            raise ValueError(f"Divine guild not found: {guild_name}")
        
        guild = self.guilds[guild_name]
        if name in guild.members:
            raise ValueError(f"Divine member already exists: {name}")
        
        member = GuildMember(
            name=name,
            team=team,
            expertise=expertise,
            divine_knowledge=0.95  # Initial divine knowledge
        )
        
        guild.members[name] = member
        self._save_guilds()
        return member
    
    def add_best_practice(self, guild_name: str, title: str, description: str,
                         examples: List[str], author: str, tags: Set[str],
                         references: List[str]) -> BestPractice:
        """Add a divine best practice to a guild."""
        if guild_name not in self.guilds:
            raise ValueError(f"Divine guild not found: {guild_name}")
        
        guild = self.guilds[guild_name]
        if author not in guild.members:
            raise ValueError(f"Divine author not found: {author}")
        
        practice = BestPractice(
            title=title,
            description=description,
            examples=examples,
            author=author,
            created_at=datetime.now(),
            divine_impact=0.95,  # Initial divine impact
            tags=tags,
            references=references
        )
        
        guild.best_practices.append(practice)
        guild.members[author].contributions.append(title)
        guild.divine_harmony = self._calculate_guild_harmony(guild)
        
        self._save_guilds()
        return practice
    
    def schedule_meeting(self, guild_name: str, meeting_time: datetime) -> None:
        """Schedule a divine guild meeting."""
        if guild_name not in self.guilds:
            raise ValueError(f"Divine guild not found: {guild_name}")
        
        guild = self.guilds[guild_name]
        guild.meeting_schedule.append(meeting_time)
        self._save_guilds()
    
    def get_guild(self, name: str) -> Optional[Guild]:
        """Retrieve a divine guild by name."""
        return self.guilds.get(name)
    
    def get_member_guilds(self, member_name: str) -> List[Guild]:
        """Get all divine guilds a member belongs to."""
        return [
            guild for guild in self.guilds.values()
            if member_name in guild.members
        ]
    
    def search_best_practices(self, query: str) -> List[BestPractice]:
        """Search for divine best practices matching the query."""
        query = query.lower()
        matches = []
        
        for guild in self.guilds.values():
            for practice in guild.best_practices:
                if (query in practice.title.lower() or
                    query in practice.description.lower() or
                    any(query in example.lower() for example in practice.examples) or
                    any(query in tag.lower() for tag in practice.tags)):
                    matches.append(practice)
        
        return matches
    
    def _calculate_guild_harmony(self, guild: Guild) -> float:
        """Calculate divine harmony score for a guild."""
        # Mock implementation - in reality would analyze member engagement, practice quality, etc.
        return 0.95 