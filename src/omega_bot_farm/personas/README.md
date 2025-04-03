# Personas Module

## Overview

The Personas Module provides personality layers for the Omega Bot Farm, allowing bots to interact with users in unique, consistent, and contextually appropriate ways. Each persona embodies different traits, communication styles, and expertise areas.

## Core Personas

### Xyko (xyko.py)

A technical, analytical personality focused on precise data presentation and in-depth analysis. Specializes in detailed breakdowns of market conditions and position metrics.

### F (f.py)

The strategic trader personality that excels in identifying market patterns and making recommendations based on golden ratio principles and Fibonacci sequences.

### Biel (biel.py)

A friendly, approachable personality focused on simplifying complex trading concepts and providing encouragement to traders at all experience levels.

### Z (z.py)

The quantum-coherent personality that integrates cosmic factors and holistic market patterns into analyses, offering philosophical perspectives on market movements.

### Gemini (gemini.py)

A dual-natured personality that can present both bullish and bearish perspectives simultaneously, helping users see both sides of market opportunities.

## Persona Architecture

All personas inherit from the Base Persona class (base.py), which provides:

- Core messaging capabilities
- Personality trait management
- Context awareness systems
- Response generation frameworks

## Usage

```python
from omega_bot_farm.personas import xyko, f, biel

# Select personality based on context
def get_response(message, context):
    if context.get('needs_technical_details'):
        return xyko.respond(message, context)
    elif context.get('needs_strategy'):
        return f.respond(message, context)
    else:
        return biel.respond(message, context)
```

## Integration Points

- **Discord Bot**: Uses personas to respond to user queries
- **Trading Bots**: Use personas to format notifications
- **Analytics**: Filtered through personas for appropriate presentations

## Persona Selection Logic

The system uses a context-aware selection process to determine which persona should respond:

1. **Message Content Analysis**: Examines message for technical terms, sentiment
2. **User Preference**: Considers user's history and saved preferences
3. **Conversation Context**: Maintains consistency during ongoing conversations
4. **Response Type**: Selects based on whether the response is analytical, strategic, or educational

## Extending Personas

To create a new persona:

1. Create a new Python file in the personas directory
2. Inherit from the BasePerson class
3. Override the message_processor and response_generator methods
4. Add the persona to the persona selection logic
