#!/usr/bin/env python3
"""
QA Knowledge Model for CyBer1t4L QA Bot
---------------------------------------

This module provides a knowledge base of QA best practices, test patterns,
and debugging strategies for the CyBer1t4L QA Bot. It serves as both documentation
and a programmatic way to access QA knowledge.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CyBer1t4L.QAKnowledge")

class TestCategory(Enum):
    """Categories of tests in the QA knowledge model."""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    USABILITY = "usability"
    COMPATIBILITY = "compatibility"
    PENETRATION = "penetration"
    CONNECTIVITY = "connectivity"
    DISCORD = "discord"
    API = "api"
    DATABASE = "database"
    UI = "ui"
    BOT = "bot"

class TestPriority(Enum):
    """Test priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TestFrequency(Enum):
    """Test frequency recommendations."""
    CONTINUOUS = "continuous"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_RELEASE = "on_release"

@dataclass
class TestPattern:
    """A test pattern in the QA knowledge model."""
    name: str
    description: str
    categories: List[TestCategory]
    priority: TestPriority
    frequency: TestFrequency
    example_code: Optional[str] = None
    applicability: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "categories": [cat.value for cat in self.categories],
            "priority": self.priority.value,
            "frequency": self.frequency.value,
            "example_code": self.example_code,
            "applicability": self.applicability,
            "benefits": self.benefits,
            "limitations": self.limitations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestPattern':
        """Create a TestPattern from a dictionary."""
        return cls(
            name=data["name"],
            description=data["description"],
            categories=[TestCategory(cat) for cat in data["categories"]],
            priority=TestPriority(data["priority"]),
            frequency=TestFrequency(data["frequency"]),
            example_code=data.get("example_code"),
            applicability=data.get("applicability", []),
            benefits=data.get("benefits", []),
            limitations=data.get("limitations", [])
        )

@dataclass
class DebugStrategy:
    """A debugging strategy in the QA knowledge model."""
    name: str
    description: str
    steps: List[str]
    applicable_issues: List[str]
    tools: List[str] = field(default_factory=list)
    example: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "applicable_issues": self.applicable_issues,
            "tools": self.tools,
            "example": self.example
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebugStrategy':
        """Create a DebugStrategy from a dictionary."""
        return cls(
            name=data["name"],
            description=data["description"],
            steps=data["steps"],
            applicable_issues=data["applicable_issues"],
            tools=data.get("tools", []),
            example=data.get("example")
        )

@dataclass
class QAMetric:
    """A quality metric in the QA knowledge model."""
    name: str
    description: str
    measurement_method: str
    target_value: Optional[str] = None
    acceptable_range: Optional[str] = None
    categories: List[TestCategory] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "measurement_method": self.measurement_method,
            "target_value": self.target_value,
            "acceptable_range": self.acceptable_range,
            "categories": [cat.value for cat in self.categories]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QAMetric':
        """Create a QAMetric from a dictionary."""
        return cls(
            name=data["name"],
            description=data["description"],
            measurement_method=data["measurement_method"],
            target_value=data.get("target_value"),
            acceptable_range=data.get("acceptable_range"),
            categories=[TestCategory(cat) for cat in data.get("categories", [])]
        )

class QAKnowledgeModel:
    """QA knowledge model for CyBer1t4L QA Bot."""
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize the QA knowledge model."""
        self.test_patterns: Dict[str, TestPattern] = {}
        self.debug_strategies: Dict[str, DebugStrategy] = {}
        self.qa_metrics: Dict[str, QAMetric] = {}
        self.best_practices: Dict[str, List[str]] = {}
        
        # Load data if file is provided
        if data_file and os.path.exists(data_file):
            self.load_from_file(data_file)
        else:
            # Initialize with default knowledge
            self._initialize_default_knowledge()
    
    def _initialize_default_knowledge(self):
        """Initialize the model with default QA knowledge."""
        # Add test patterns
        self.add_test_pattern(TestPattern(
            name="Discord Command Response",
            description="Tests if a Discord bot command responds correctly with expected output.",
            categories=[TestCategory.DISCORD, TestCategory.BOT, TestCategory.INTEGRATION],
            priority=TestPriority.CRITICAL,
            frequency=TestFrequency.CONTINUOUS,
            example_code="""
async def test_ping_command():
    # Setup a mock interaction
    interaction = MockInteraction()
    
    # Call the ping command
    await ping_command(interaction)
    
    # Assert that the response was sent
    assert interaction.response.send_message.called
    
    # Assert the content contains expected text
    args, kwargs = interaction.response.send_message.call_args
    assert "pong" in kwargs.get("content", "").lower()
""",
            applicability=["Discord bots", "Slash commands", "Message interactions"],
            benefits=["Ensures critical commands work", "Catches regressions quickly", "Ensures user experience"],
            limitations=["Mocking Discord interactions can be complex", "May not catch all edge cases"]
        ))
        
        self.add_test_pattern(TestPattern(
            name="API connectivity",
            description="Tests if the bot can connect to required APIs and services.",
            categories=[TestCategory.CONNECTIVITY, TestCategory.INTEGRATION],
            priority=TestPriority.CRITICAL,
            frequency=TestFrequency.DAILY,
            example_code="""
async def test_discord_api_connectivity():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com/api/v10/gateway") as response:
            assert response.status == 200
            data = await response.json()
            assert "url" in data
""",
            applicability=["Discord bots", "API integrations", "Service dependencies"],
            benefits=["Detects outages quickly", "Identifies network issues", "Validates API compatibility"],
            limitations=["May produce false positives with temporary outages", "Requires network access"]
        ))
        
        self.add_test_pattern(TestPattern(
            name="Discord Token Validation",
            description="Tests if the Discord bot token is valid and has correct permissions.",
            categories=[TestCategory.SECURITY, TestCategory.DISCORD, TestCategory.BOT],
            priority=TestPriority.CRITICAL,
            frequency=TestFrequency.DAILY,
            example_code="""
async def test_discord_token():
    # Load token from environment
    token = os.environ.get("DISCORD_BOT_TOKEN")
    
    # Call Discord API to validate
    headers = {"Authorization": f"Bot {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
            assert response.status == 200
            data = await response.json()
            assert "id" in data
            assert "username" in data
""",
            applicability=["Discord bots", "Security validation", "Authentication"],
            benefits=["Detects token rotation issues", "Validates bot identity", "Ensures API access"],
            limitations=["Exposes token in test code", "Requires network access"]
        ))
        
        self.add_test_pattern(TestPattern(
            name="Command Registration Verification",
            description="Verifies that all Discord commands are properly registered with the API.",
            categories=[TestCategory.DISCORD, TestCategory.BOT, TestCategory.INTEGRATION],
            priority=TestPriority.HIGH,
            frequency=TestFrequency.ON_RELEASE,
            example_code="""
async def test_commands_registered():
    # Get application commands from Discord API
    url = f"https://discord.com/api/v10/applications/{app_id}/commands"
    headers = {"Authorization": f"Bot {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            assert response.status == 200
            commands = await response.json()
            
            # Check if expected commands exist
            command_names = [cmd["name"] for cmd in commands]
            assert "ping" in command_names
            assert "test_interactions_report" in command_names
""",
            applicability=["Discord bots", "Application command verification"],
            benefits=["Detects command registration issues", "Validates command availability", "Ensures API sync"],
            limitations=["Requires application ID", "Commands may take time to propagate in Discord API"]
        ))
        
        # Add debug strategies
        self.add_debug_strategy(DebugStrategy(
            name="Discord Command Not Found",
            description="Debugging strategy for when Discord returns a 'CommandNotFound' error.",
            steps=[
                "Check if the command name matches exactly what was registered (case-sensitive)",
                "Verify the command was registered with the tree.sync() method",
                "Check if the command was registered globally or to a specific guild",
                "Investigate if multiple tree.sync() calls are overriding each other",
                "Verify the command is defined at the top-level scope, not inside a function",
                "Check Discord API logs to see if the command is properly registered",
                "Try re-registering the command with both guild-specific and global sync",
                "Review your command handler implementation for proper parameter definitions"
            ],
            applicable_issues=[
                "discord.app_commands.errors.CommandNotFound",
                "Application command not found",
                "Unknown application command",
                "Command not appearing in the Discord UI"
            ],
            tools=[
                "test_command_registration.py",
                "fix_test_interactions_report.py",
                "Discord API Explorer",
                "Discord Developer Portal"
            ],
            example="""
# Problem: Command defined inside another function might not be registered properly
@client.event
async def on_ready():
    # This command might not be registered correctly when defined here
    @client.tree.command(name="problematic_command")
    async def my_command(interaction):
        await interaction.response.send_message("Hello!")
    
    await client.tree.sync()

# Fix: Define command at the top level
@client.tree.command(name="fixed_command")
async def my_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    # Just sync here, don't define commands
    await client.tree.sync()
"""
        ))
        
        self.add_debug_strategy(DebugStrategy(
            name="Discord Bot Not Responding",
            description="Debugging strategy for when a Discord bot doesn't respond to commands.",
            steps=[
                "Check if the bot is online and connected to Discord",
                "Verify the bot has the correct permissions in the server",
                "Check if the message content intent is enabled (both in code and Developer Portal)",
                "Look for errors in the bot's logs",
                "Test network connectivity to Discord API",
                "Verify the command is properly registered",
                "Check if the bot is handling the command interaction correctly",
                "Verify no errors are occurring during command processing"
            ],
            applicable_issues=[
                "Bot doesn't respond to commands",
                "Commands are visible but don't work",
                "Bot appears online but doesn't interact",
                "Ping command not responding"
            ],
            tools=[
                "test_network_connectivity.py",
                "Discord Developer Portal",
                "Logging output",
                "test_command_registration.py"
            ],
            example="""
# Common issue: Missing message content intent
# Fix in code:
intents = discord.Intents.default()
intents.message_content = True  # This line is often missing
bot = commands.Bot(command_prefix='!', intents=intents)

# Also enable it in Discord Developer Portal under "Bot" -> "Privileged Gateway Intents"
"""
        ))
        
        self.add_debug_strategy(DebugStrategy(
            name="Network Connectivity Issues",
            description="Debugging strategy for network and API connectivity problems.",
            steps=[
                "Check basic internet connectivity with simple ping tests",
                "Verify DNS resolution for critical domains",
                "Test connectivity to specific API endpoints",
                "Check if firewalls or security software is blocking connections",
                "Verify API credentials and authentication",
                "Look for API rate limiting or throttling",
                "Check for SSL/TLS certificate issues",
                "Monitor network latency and packet loss"
            ],
            applicable_issues=[
                "API connection failures",
                "Timeouts on network requests",
                "Intermittent connectivity issues",
                "SSL certificate errors"
            ],
            tools=[
                "test_network_connectivity.py",
                "curl / wget",
                "ping / traceroute",
                "Wireshark",
                "netstat / lsof"
            ]
        ))
        
        # Add QA metrics
        self.add_qa_metric(QAMetric(
            name="Test Coverage",
            description="Percentage of code covered by tests (statements, branches, etc.)",
            measurement_method="pytest-cov or similar tools that track which lines of code are executed during tests",
            target_value="80% or higher",
            acceptable_range="70-100%",
            categories=[TestCategory.UNIT, TestCategory.INTEGRATION]
        ))
        
        self.add_qa_metric(QAMetric(
            name="Command Response Time",
            description="Time taken for the bot to respond to commands",
            measurement_method="Measure time between command invocation and response in milliseconds",
            target_value="<1000ms",
            acceptable_range="200-2000ms",
            categories=[TestCategory.PERFORMANCE, TestCategory.BOT, TestCategory.DISCORD]
        ))
        
        self.add_qa_metric(QAMetric(
            name="API Success Rate",
            description="Percentage of API calls that succeed without errors",
            measurement_method="Number of successful API calls / Total API calls × 100%",
            target_value="99.9%",
            acceptable_range="99-100%",
            categories=[TestCategory.API, TestCategory.RELIABILITY]
        ))
        
        self.add_qa_metric(QAMetric(
            name="Successful Test Rate",
            description="Percentage of automated tests that pass",
            measurement_method="Number of passing tests / Total number of tests × 100%",
            target_value="100%",
            acceptable_range="95-100%",
            categories=[TestCategory.UNIT, TestCategory.INTEGRATION, TestCategory.SYSTEM]
        ))
        
        # Add best practices
        self.best_practices["discord_bot"] = [
            "Always define commands at the top level of your code, not inside functions",
            "Enable the message content intent both in code and the Developer Portal",
            "Use separate development and production bot tokens",
            "Implement proper error handling to prevent crashes",
            "Log all errors and important events",
            "Use guild-specific commands during development for faster updates",
            "Sync your command tree after all commands are defined",
            "Defer responses for commands that may take more than 3 seconds to process",
            "Implement a health checking command like /ping",
            "Set up a status page or monitoring for the bot"
        ]
        
        self.best_practices["testing"] = [
            "Use a consistent directory structure for tests",
            "Write both unit and integration tests",
            "Mock external dependencies when testing",
            "Aim for at least 80% code coverage",
            "Run critical tests in CI/CD pipelines",
            "Use fixtures to reduce test code duplication",
            "Test both expected behaviors and error handling",
            "Implement parameterized tests for variations of input",
            "Include response time and performance tests",
            "Document test scenarios and expected results"
        ]
        
        self.best_practices["debugging"] = [
            "Check logs first for error messages",
            "Verify all dependencies and configurations",
            "Test components in isolation",
            "Use a systematic approach rather than random changes",
            "Monitor system resources during operation",
            "Test in an environment similar to production",
            "Keep proper version control of all changes",
            "Document the debugging process and findings",
            "Create reproducer test cases for bugs",
            "Look for patterns in issues across different components"
        ]
    
    def add_test_pattern(self, pattern: TestPattern) -> None:
        """Add a test pattern to the model."""
        self.test_patterns[pattern.name] = pattern
    
    def add_debug_strategy(self, strategy: DebugStrategy) -> None:
        """Add a debugging strategy to the model."""
        self.debug_strategies[strategy.name] = strategy
    
    def add_qa_metric(self, metric: QAMetric) -> None:
        """Add a QA metric to the model."""
        self.qa_metrics[metric.name] = metric
    
    def get_test_patterns(self, category: Optional[TestCategory] = None) -> List[TestPattern]:
        """Get test patterns, optionally filtered by category."""
        if category is None:
            return list(self.test_patterns.values())
        return [p for p in self.test_patterns.values() if category in p.categories]
    
    def get_debug_strategies(self, issue: Optional[str] = None) -> List[DebugStrategy]:
        """Get debug strategies, optionally filtered by applicable issue."""
        if issue is None:
            return list(self.debug_strategies.values())
        
        # Return strategies that have the issue mentioned in applicable_issues
        return [s for s in self.debug_strategies.values() 
                if any(issue.lower() in ai.lower() for ai in s.applicable_issues)]
    
    def get_qa_metrics(self, category: Optional[TestCategory] = None) -> List[QAMetric]:
        """Get QA metrics, optionally filtered by category."""
        if category is None:
            return list(self.qa_metrics.values())
        return [m for m in self.qa_metrics.values() if category in m.categories]
    
    def get_best_practices(self, area: Optional[str] = None) -> Dict[str, List[str]]:
        """Get best practices, optionally filtered by area."""
        if area is None:
            return self.best_practices
        
        return {area: self.best_practices[area]} if area in self.best_practices else {}
    
    def find_strategy_for_error(self, error_message: str) -> Optional[DebugStrategy]:
        """Find the most relevant debug strategy for an error message."""
        # Check exact matches first
        for strategy in self.debug_strategies.values():
            if any(error in error_message for error in strategy.applicable_issues):
                return strategy
        
        # Check partial matches
        for strategy in self.debug_strategies.values():
            for issue in strategy.applicable_issues:
                # Extract meaningful words from the issue and check if they are in the error
                keywords = [word.lower() for word in issue.split() if len(word) > 3]
                if any(keyword in error_message.lower() for keyword in keywords):
                    return strategy
        
        return None
    
    def save_to_file(self, filepath: str) -> None:
        """Save the QA knowledge model to a file."""
        try:
            data = {
                "test_patterns": {name: pattern.to_dict() for name, pattern in self.test_patterns.items()},
                "debug_strategies": {name: strategy.to_dict() for name, strategy in self.debug_strategies.items()},
                "qa_metrics": {name: metric.to_dict() for name, metric in self.qa_metrics.items()},
                "best_practices": self.best_practices
            }
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"QA knowledge model saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving QA knowledge model: {str(e)}")
    
    def load_from_file(self, filepath: str) -> None:
        """Load the QA knowledge model from a file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Load test patterns
            self.test_patterns = {}
            for name, pattern_data in data.get("test_patterns", {}).items():
                self.test_patterns[name] = TestPattern.from_dict(pattern_data)
            
            # Load debug strategies
            self.debug_strategies = {}
            for name, strategy_data in data.get("debug_strategies", {}).items():
                self.debug_strategies[name] = DebugStrategy.from_dict(strategy_data)
            
            # Load QA metrics
            self.qa_metrics = {}
            for name, metric_data in data.get("qa_metrics", {}).items():
                self.qa_metrics[name] = QAMetric.from_dict(metric_data)
            
            # Load best practices
            self.best_practices = data.get("best_practices", {})
            
            logger.info(f"QA knowledge model loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading QA knowledge model: {str(e)}")
            # Initialize with default knowledge if loading fails
            self._initialize_default_knowledge()
    
    def generate_documentation(self) -> str:
        """Generate markdown documentation from the QA knowledge model."""
        docs = []
        
        # Title
        docs.append("# CyBer1t4L QA Bot - Knowledge Model")
        docs.append("\nQuality Assurance knowledge base for testing and debugging the CyBer1t4L QA Bot.\n")
        
        # Test Patterns
        docs.append("## Test Patterns")
        docs.append("\nStandardized test patterns for different aspects of the system.\n")
        
        for pattern in sorted(self.test_patterns.values(), key=lambda p: p.priority.value):
            docs.append(f"### {pattern.name}")
            docs.append(f"*Priority: {pattern.priority.value}, Frequency: {pattern.frequency.value}*\n")
            docs.append(pattern.description)
            docs.append("\n**Categories:**")
            docs.append(", ".join(c.value for c in pattern.categories))
            
            if pattern.applicability:
                docs.append("\n**Applicability:**")
                docs.append("- " + "\n- ".join(pattern.applicability))
            
            if pattern.benefits:
                docs.append("\n**Benefits:**")
                docs.append("- " + "\n- ".join(pattern.benefits))
            
            if pattern.limitations:
                docs.append("\n**Limitations:**")
                docs.append("- " + "\n- ".join(pattern.limitations))
            
            if pattern.example_code:
                docs.append("\n**Example:**")
                docs.append("```python")
                docs.append(pattern.example_code.strip())
                docs.append("```")
            
            docs.append("\n---\n")
        
        # Debug Strategies
        docs.append("## Debug Strategies")
        docs.append("\nSystematic approaches to diagnosing and fixing common issues.\n")
        
        for strategy in self.debug_strategies.values():
            docs.append(f"### {strategy.name}")
            docs.append(f"\n{strategy.description}\n")
            
            docs.append("**Steps:**")
            for i, step in enumerate(strategy.steps, 1):
                docs.append(f"{i}. {step}")
            
            docs.append("\n**Applicable Issues:**")
            docs.append("- " + "\n- ".join(strategy.applicable_issues))
            
            if strategy.tools:
                docs.append("\n**Tools:**")
                docs.append("- " + "\n- ".join(strategy.tools))
            
            if strategy.example:
                docs.append("\n**Example:**")
                docs.append("```python")
                docs.append(strategy.example.strip())
                docs.append("```")
            
            docs.append("\n---\n")
        
        # QA Metrics
        docs.append("## QA Metrics")
        docs.append("\nMeasurements used to assess quality and performance.\n")
        
        docs.append("| Metric | Description | Target | Acceptable Range |")
        docs.append("|--------|-------------|--------|------------------|")
        
        for metric in self.qa_metrics.values():
            target = metric.target_value or "N/A"
            range_val = metric.acceptable_range or "N/A"
            docs.append(f"| **{metric.name}** | {metric.description} | {target} | {range_val} |")
        
        docs.append("\n")
        
        # Best Practices
        docs.append("## Best Practices")
        docs.append("\nRecommended approaches for development, testing, and operations.\n")
        
        for area, practices in self.best_practices.items():
            docs.append(f"### {area.replace('_', ' ').title()}")
            docs.append("")
            for practice in practices:
                docs.append(f"- {practice}")
            docs.append("")
        
        return "\n".join(docs)

def create_qa_knowledge_model() -> QAKnowledgeModel:
    """Create and initialize a QA knowledge model."""
    # Check if a saved model exists
    model_path = os.path.join(os.path.dirname(__file__), "../data/qa_knowledge_model.json")
    
    if os.path.exists(model_path):
        model = QAKnowledgeModel(model_path)
    else:
        model = QAKnowledgeModel()
        # Save the initialized model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save_to_file(model_path)
    
    return model

def generate_documentation():
    """Generate and save documentation from the QA knowledge model."""
    model = create_qa_knowledge_model()
    docs = model.generate_documentation()
    
    docs_path = os.path.join(os.path.dirname(__file__), "../docs/QA_KNOWLEDGE_MODEL.md")
    os.makedirs(os.path.dirname(docs_path), exist_ok=True)
    
    with open(docs_path, 'w') as f:
        f.write(docs)
    
    print(f"Documentation generated and saved to {docs_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="QA Knowledge Model for CyBer1t4L QA Bot")
    parser.add_argument("--docs", action="store_true", help="Generate documentation")
    parser.add_argument("--save", type=str, help="Save model to specified file")
    parser.add_argument("--load", type=str, help="Load model from specified file")
    
    args = parser.parse_args()
    
    if args.docs:
        generate_documentation()
    elif args.save:
        model = create_qa_knowledge_model()
        model.save_to_file(args.save)
    elif args.load:
        model = QAKnowledgeModel(args.load)
        # Save to default location
        default_path = os.path.join(os.path.dirname(__file__), "../data/qa_knowledge_model.json")
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        model.save_to_file(default_path)
    else:
        # Just create the model by default
        create_qa_knowledge_model() 