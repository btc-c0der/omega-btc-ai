# OMEGA BTC AI - Bot Personification

## Overview

The Bot Personification module brings unique personalities to the OMEGA BTC AI trading system. It allows different bot personas to represent and communicate about trading operations in unique styles, tones, and perspectives.

This feature enhances user engagement by providing multiple ways to interact with and understand trading data, strategies, and market analysis.

## Key Features

- **Multiple Personas**: Different personas with unique personalities and communication styles
- **Customizable Appearance**: Each persona has its own visual styling
- **Personalized Analysis**: Market analysis and recommendations in the persona's unique voice
- **Easy Switching**: Change personas on the fly through the dashboard
- **Styling Integration**: Seamless integration with the Divine Alignment Dashboard

## Available Personas

### Rasta Oracle

A spiritual guide who interprets market movements through divine rhythms and natural harmony. Speaks with Jamaican dialect influences and focuses on long-term balance.

### Technical Analyst

A data-driven market analyst focused on technical indicators, chart patterns, and quantitative metrics. Speaks with precision and confidence about market structures and probability-based trading.

## Usage

The Bot Personification feature is accessible through the Divine Alignment Dashboard. To use it:

1. Navigate to the dashboard
2. Select your preferred persona from the dropdown
3. View market analysis, position analysis, and recommendations in the selected persona's style

## API Endpoints

The following API endpoints are available for interacting with the Bot Personification feature:

- `GET /api/personas` - Get all available personas
- `GET /api/personas/active` - Get the currently active persona
- `POST /api/change_persona` - Change the active persona
- `POST /api/persona_analysis/{analysis_type}` - Get persona analysis for the specified type
- `GET /api/persona_css` - Get CSS for the specified or active persona
- `GET /api/persona_js` - Get JavaScript for persona functionality
- `GET /api/persona_card_html` - Get HTML for the persona card

## Adding New Personas

To create a new persona:

1. Create a new Python file in the `omega_ai/personification/personas` directory
2. Define a class that inherits from `BasePersona`
3. Implement the required abstract methods
4. Customize the persona's style, vocabulary, and analysis logic

Example:

```python
from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood

class ZenMonkPersona(BasePersona):
    def __init__(self):
        style = PersonaStyle(
            primary_color="#663399",  # Deep purple
            secondary_color="#E6E6FA",  # Light purple
            accent_color="#FFA500",    # Orange
            font_family="'Georgia', serif",
            avatar_url="/assets/images/personas/zen_monk_avatar.png"
        )
        
        super().__init__(
            name="Zen Monk",
            description="A tranquil, mindful observer of market movements who speaks in calm, measured tones with Eastern philosophical influences.",
            style=style
        )
        
    # Implement the required methods:
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        # Your implementation here
        pass
        
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        # Your implementation here
        pass
        
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        # Your implementation here
        pass
        
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        # Your implementation here
        pass
```

## Integration with Divine Alignment Dashboard

The Bot Personification feature seamlessly integrates with the Divine Alignment Dashboard, providing:

- Persona selection dropdown
- Persona information card
- Stylized analysis panels
- Consistent visual theming

## Future Enhancements

- Voice integration for spoken analysis
- User-defined custom personas
- Ability to save favorite analyses
- Automated persona switching based on market conditions
- More varied personas with unique perspectives

## License

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
