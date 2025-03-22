"""
Dashboard Integration for OMEGA BTC AI Bot Personification

This module provides functions to integrate bot personas into the
Divine Alignment Dashboard (DAD).
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from omega_ai.personification.persona_manager import PersonaManager


class DashboardIntegration:
    """
    Integrates bot personas into the Divine Alignment Dashboard.
    
    This class provides methods to generate persona-specific content
    for the dashboard and process user interactions with personas.
    """
    
    def __init__(self, persona_manager: Optional[PersonaManager] = None):
        """
        Initialize the dashboard integration.
        
        Args:
            persona_manager: Optional PersonaManager instance to use
        """
        self.persona_manager = persona_manager or PersonaManager()
        
    def get_personas_dropdown_html(self) -> str:
        """
        Generate HTML for a dropdown to select available personas.
        
        Returns:
            HTML string for persona selection dropdown
        """
        personas = self.persona_manager.get_persona_details()
        active_persona = self.persona_manager.get_active_persona()
        active_persona_name = active_persona.name if active_persona else ""
        
        html = '<div class="persona-selector">\n'
        html += '  <label for="persona-dropdown">Choose Oracle:</label>\n'
        html += '  <select id="persona-dropdown" onchange="switchPersona(this.value)">\n'
        
        for persona in personas:
            selected = "selected" if persona["name"] == active_persona_name else ""
            html += f'    <option value="{persona["name"]}" {selected}>{persona["name"]}</option>\n'
            
        html += '  </select>\n'
        html += '</div>\n'
        
        return self._sanitize_html_output(html)
    
    def get_persona_card_html(self, persona_name: Optional[str] = None) -> str:
        """
        Generate HTML for a card displaying the persona's information.
        
        Args:
            persona_name: Optional name of the persona to use
            
        Returns:
            HTML string for persona card
        """
        persona = self.persona_manager._get_target_persona(persona_name)
        if not persona:
            return '<div class="persona-card error">No active persona available.</div>'
        
        # Create a cleaner persona ID
        persona_id = persona.name.lower().replace(" ", "-")
        
        # Generate the HTML with better structure
        html = f'<div class="persona-card" id="persona-card-{persona_id}">\n'
        html += '  <div class="persona-card-inner">\n'
        html += f'    <div class="persona-avatar" style="background-image: url({persona.style.avatar_url});"></div>\n'
        html += '    <div class="persona-info">\n'
        html += f'      <h3 class="persona-name">{persona.name}</h3>\n'
        html += f'      <div class="persona-description">{self._format_text_for_html(persona.description)}</div>\n'
        html += '      <div class="persona-greeting-container">\n'
        html += f'        <div class="persona-greeting">{self._format_text_for_html(persona.get_greeting())}</div>\n'
        html += '      </div>\n'
        html += '    </div>\n'
        html += '  </div>\n'
        html += '</div>\n'
        
        return self._sanitize_html_output(html)
    
    def get_bitget_traders_panel_html(self) -> str:
        """
        Generate HTML for a panel displaying Bitget trader profiles with modern UI style.
        
        Returns:
            HTML string for Bitget traders panel
        """
        html = '<div class="bitget-traders-panel">\n'
        html += '  <div class="panel-header">\n'
        html += '    <h2>' + self._format_text_for_html("Bitget Trader Profiles") + '</h2>\n'
        html += '    <span class="panel-subtitle">Select a trading strategy profile</span>\n'
        html += '  </div>\n'
        html += '  <div class="trader-profiles">\n'
        
        # Strategic Trader
        html += '    <div class="trader-profile strategic">\n'
        html += '      <div class="trader-header">\n'
        html += '        <div class="trader-icon">📊</div>\n'
        html += '        <h3>' + self._format_text_for_html("Strategic Trader") + '</h3>\n'
        html += '      </div>\n'
        html += '      <div class="trader-content">\n'
        html += '        <div class="trader-description">' + self._format_text_for_html("Patient, methodical trader using Fibonacci levels and market structure for long-term gains.") + '</div>\n'
        html += '        <div class="trader-stats">\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Risk:") + '</span> <span class="value strategic-value">' + self._format_text_for_html("2%") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Patience:") + '</span> <span class="value strategic-value">' + self._format_text_for_html("High") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Win Rate:") + '</span> <span class="value strategic-value">' + self._format_text_for_html("65%") + '</span></div>\n'
        html += '        </div>\n'
        html += '        <button class="trader-select strategic-select" onclick="selectTraderPersona(\'Strategic Trader\')">' + self._format_text_for_html("Select") + '</button>\n'
        html += '      </div>\n'
        html += '    </div>\n'
        
        # Scalper Trader
        html += '    <div class="trader-profile scalper">\n'
        html += '      <div class="trader-header">\n'
        html += '        <div class="trader-icon">⚡</div>\n'
        html += '        <h3>' + self._format_text_for_html("Scalper Trader") + '</h3>\n'
        html += '      </div>\n'
        html += '      <div class="trader-content">\n'
        html += '        <div class="trader-description">' + self._format_text_for_html("Fast-paced trader targeting quick profits with high-frequency trades and tight risk management.") + '</div>\n'
        html += '        <div class="trader-stats">\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Risk:") + '</span> <span class="value scalper-value">' + self._format_text_for_html("0.5%") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Patience:") + '</span> <span class="value scalper-value">' + self._format_text_for_html("Low") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Win Rate:") + '</span> <span class="value scalper-value">' + self._format_text_for_html("55%") + '</span></div>\n'
        html += '        </div>\n'
        html += '        <button class="trader-select scalper-select" onclick="selectTraderPersona(\'Scalper Trader\')">' + self._format_text_for_html("Select") + '</button>\n'
        html += '      </div>\n'
        html += '    </div>\n'
        
        # Elite Exit Specialist
        html += '    <div class="trader-profile elite-exit">\n'
        html += '      <div class="trader-header">\n'
        html += '        <div class="trader-icon">🚪</div>\n'
        html += '        <h3>' + self._format_text_for_html("Elite Exit Specialist") + '</h3>\n'
        html += '      </div>\n'
        html += '      <div class="trader-content">\n'
        html += '        <div class="trader-description">' + self._format_text_for_html("Sophisticated exit strategist focused on trap awareness, optimal exit timing, and multi-factor analysis.") + '</div>\n'
        html += '        <div class="trader-stats">\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Trap Detection:") + '</span> <span class="value elite-value">' + self._format_text_for_html("85%") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Exit Efficiency:") + '</span> <span class="value elite-value">' + self._format_text_for_html("78%") + '</span></div>\n'
        html += '          <div class="stat"><span class="label">' + self._format_text_for_html("Profit Factor:") + '</span> <span class="value elite-value">' + self._format_text_for_html("2.3") + '</span></div>\n'
        html += '        </div>\n'
        html += '        <button class="trader-select elite-select" onclick="selectTraderPersona(\'Elite Exit Specialist\')">' + self._format_text_for_html("Select") + '</button>\n'
        html += '      </div>\n'
        html += '    </div>\n'
        
        html += '  </div>\n'
        html += '</div>\n'
        
        return self._sanitize_html_output(html)
    
    def get_profile_comparison_html(self) -> str:
        """
        Generate HTML for a comparison of different trading profiles.
        
        Returns:
            HTML string for profile comparison
        """
        html = '<div class="profile-comparison">\n'
        html += '  <h2>' + self._format_text_for_html("Trading Profile Comparison") + '</h2>\n'
        html += '  <table class="comparison-table">\n'
        html += '    <thead>\n'
        html += '      <tr>\n'
        html += '        <th>' + self._format_text_for_html("Feature") + '</th>\n'
        html += '        <th>' + self._format_text_for_html("Strategic") + '</th>\n'
        html += '        <th>' + self._format_text_for_html("Scalper") + '</th>\n'
        html += '        <th>' + self._format_text_for_html("Elite Exit") + '</th>\n'
        html += '      </tr>\n'
        html += '    </thead>\n'
        html += '    <tbody>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Timeframe Focus") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("4H-1D") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("1M-15M") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Multiple") + '</td>\n'
        html += '      </tr>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Trade Frequency") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Low") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Very High") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Medium") + '</td>\n'
        html += '      </tr>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Risk Per Trade") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("2%") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("0.5%") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("1%") + '</td>\n'
        html += '      </tr>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Stop Loss Strategy") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Structure-based") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Tight Fixed") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Trap-aware Dynamic") + '</td>\n'
        html += '      </tr>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Take Profit Strategy") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Multiple Levels") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Quick Fixed Target") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Adaptive Multi-level") + '</td>\n'
        html += '      </tr>\n'
        html += '      <tr>\n'
        html += '        <td>' + self._format_text_for_html("Key Advantage") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Higher R:R Ratio") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Frequent Small Wins") + '</td>\n'
        html += '        <td>' + self._format_text_for_html("Trap Avoidance") + '</td>\n'
        html += '      </tr>\n'
        html += '    </tbody>\n'
        html += '  </table>\n'
        html += '</div>\n'
        
        return self._sanitize_html_output(html)
    
    def get_persona_analysis_html(self, data: Dict[str, Any], analysis_type: str = "market", 
                                persona_name: Optional[str] = None) -> str:
        """
        Generate HTML for a persona's analysis of market or position data.
        
        Args:
            data: Dictionary containing data to be analyzed
            analysis_type: Type of analysis ("market", "position", "recommendation", or "performance")
            persona_name: Optional name of the persona to use
            
        Returns:
            HTML string for persona analysis
        """
        persona = self.persona_manager._get_target_persona(persona_name)
        if not persona:
            return '<div class="persona-analysis error">No active persona available.</div>'
        
        # Get the appropriate analysis based on type
        analysis_text = ""
        if analysis_type == "market":
            analysis_text = persona.analyze_market(data)
        elif analysis_type == "position":
            analysis_text = persona.analyze_position(data)
        elif analysis_type == "recommendation":
            analysis_text = persona.generate_recommendation(data)
        elif analysis_type == "performance":
            analysis_text = persona.summarize_performance(data)
        else:
            analysis_text = "Unknown analysis type requested."
        
        # Format and convert the analysis text to HTML
        analysis_html = self._format_text_for_html(analysis_text)
        # Convert paragraph breaks (double newlines) to proper paragraph tags
        analysis_html = analysis_html.replace('<br><br>', '</p><p>')
        
        # Generate HTML
        html = f'<div class="persona-analysis {analysis_type}-analysis">\n'
        html += f'  <div class="analysis-header">{persona.name}\'s {analysis_type.capitalize()} Analysis</div>\n'
        html += f'  <div class="analysis-content"><p>{analysis_html}</p></div>\n'
        html += f'  <div class="analysis-timestamp">Generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>\n'
        html += '</div>\n'
        
        return self._sanitize_html_output(html)
    
    def get_persona_css(self, persona_name: Optional[str] = None) -> str:
        """
        Generate CSS for styling based on the active or specified persona.
        
        Args:
            persona_name: Optional name of the persona to use
            
        Returns:
            CSS string for persona styling
        """
        persona = self.persona_manager._get_target_persona(persona_name)
        if not persona:
            return "/* No active persona available */\n"
        
        # Base CSS for persona integration
        css = """
        /* Persona Integration Styles */
        .persona-selector {
            margin: 20px 0;
            text-align: center;
        }
        
        .persona-selector label {
            margin-right: 10px;
            font-weight: bold;
        }
        
        .persona-selector select {
            padding: 8px 15px;
            border-radius: 5px;
            background-color: rgba(30, 30, 30, 0.7);
            color: var(--light-text);
            border: 1px solid var(--border-color);
        }
        
        /* Improved Persona Card Styles */
        .persona-card {
            background-color: rgba(30, 30, 30, 0.7);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border-left: 4px solid var(--persona-accent-color);
        }
        
        .persona-card-inner {
            display: flex;
            align-items: flex-start;
        }
        
        .persona-avatar {
            width: 80px;
            height: 80px;
            min-width: 80px;
            border-radius: 50%;
            background-size: cover;
            background-position: center;
            margin-right: 20px;
            border: 2px solid var(--persona-accent-color);
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
        }
        
        .persona-info {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .persona-name {
            color: var(--persona-primary-color);
            margin: 0;
            padding: 0;
            font-size: 1.4rem;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        
        .persona-description {
            color: var(--persona-secondary-color);
            margin: 0;
            padding: 0;
            line-height: 1.5;
            font-size: 1rem;
        }
        
        .persona-greeting-container {
            margin-top: 5px;
        }
        
        .persona-greeting {
            color: var(--light-text);
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            padding: 12px;
            font-style: italic;
            line-height: 1.5;
            position: relative;
            border-left: 3px solid var(--persona-accent-color);
        }
        
        .persona-greeting::before {
            content: '"';
            position: absolute;
            left: 5px;
            top: 0;
            font-size: 1.5rem;
            color: var(--persona-accent-color);
            opacity: 0.6;
        }
        
        .persona-greeting::after {
            content: '"';
            position: absolute;
            right: 5px;
            bottom: 0;
            font-size: 1.5rem;
            color: var(--persona-accent-color);
            opacity: 0.6;
        }
        
        .persona-analysis {
            background-color: rgba(30, 30, 30, 0.7);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            font-family: var(--persona-font-family);
        }
        
        .analysis-header {
            color: var(--persona-primary-color);
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .analysis-content {
            color: var(--light-text);
            line-height: 1.5;
        }
        
        .analysis-content p {
            margin: 10px 0;
        }
        
        .analysis-timestamp {
            color: var(--persona-secondary-color);
            font-size: 0.8em;
            text-align: right;
            margin-top: 15px;
            font-style: italic;
        }
        
        .error {
            color: var(--red-trapped);
            border: 1px solid var(--red-trapped);
        }
        
        /* Analysis type-specific styles */
        .market-analysis {
            border-left: 4px solid #3498db;
        }
        
        .position-analysis {
            border-left: 4px solid #2ecc71;
        }
        
        .recommendation-analysis {
            border-left: 4px solid #f39c12;
        }
        
        .performance-analysis {
            border-left: 4px solid #9b59b6;
        }
        """
        
        # Add persona-specific CSS variables
        css += "\n/* Persona-specific variables */\n"
        css += ":root {\n"
        css += persona.style.to_css()
        css += "}\n"
        
        return self._sanitize_html_output(css)
    
    def get_persona_js(self) -> str:
        """
        Generate JavaScript for persona functionality in the dashboard.
        
        Returns:
            JavaScript string for persona functionality
        """
        js = """
        // Persona Integration JavaScript
        
        // Function to switch the active persona
        function switchPersona(personaName) {
            // Send request to server to change active persona
            fetch('/api/change_persona', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    persona: personaName
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload the page to apply new persona
                    window.location.reload();
                } else {
                    console.error('Failed to change persona:', data.error);
                    alert('Failed to change persona: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error changing persona:', error);
                alert('Error changing persona. Please try again.');
            });
        }
        
        // Function to request persona analysis
        function requestPersonaAnalysis(analysisType, dataId = null) {
            // Get any additional data needed for the analysis
            const additionalData = {};
            
            // If data ID is provided, include it
            if (dataId) {
                additionalData.dataId = dataId;
            }
            
            // Send request to server to get analysis
            fetch(`/api/persona_analysis/${analysisType}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(additionalData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Insert analysis HTML into appropriate container
                    const container = document.getElementById(`${analysisType}-analysis-container`);
                    if (container) {
                        container.innerHTML = data.analysisHtml;
                    } else {
                        console.error(`Container for ${analysisType} analysis not found`);
                    }
                } else {
                    console.error('Failed to get analysis:', data.error);
                }
            })
            .catch(error => {
                console.error('Error getting analysis:', error);
            });
        }
        
        // Initialize persona functionality when page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Auto-load market analysis if container exists
            const marketContainer = document.getElementById('market-analysis-container');
            if (marketContainer) {
                requestPersonaAnalysis('market');
            }
            
            // Set up periodic refresh for market analysis
            if (marketContainer) {
                setInterval(() => {
                    requestPersonaAnalysis('market');
                }, 300000); // Refresh every 5 minutes
            }
        });
        """
        
        return self._sanitize_html_output(js)
    
    def generate_api_routes(self) -> Dict[str, Any]:
        """
        Generate FastAPI route handler functions for persona integration.
        
        Returns:
            Dictionary mapping route paths to handler functions
        """
        routes = {}
        
        # Change active persona route
        async def change_persona(request):
            try:
                data = await request.json()
                persona_name = data.get("persona")
                
                if not persona_name:
                    return {"success": False, "error": "Persona name required"}
                
                success = self.persona_manager.set_active_persona(persona_name)
                
                if success:
                    return {"success": True, "persona": persona_name}
                else:
                    return {"success": False, "error": f"Persona '{persona_name}' not found"}
            
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        routes["/api/change_persona"] = change_persona
        
        # Persona analysis routes
        async def get_persona_analysis(request, analysis_type):
            try:
                # Get appropriate data based on analysis type
                if analysis_type == "market":
                    # Mock market data for demonstration
                    data = {
                        "price": 50000.0,
                        "price_change_24h": 2.5,
                        "volume_24h": 25000000000,
                        "trend": "bullish",
                        "signal_strength": 0.7
                    }
                elif analysis_type == "position":
                    # Get position ID from request
                    req_data = await request.json()
                    position_id = req_data.get("dataId")
                    
                    # Get position data (mock for demonstration)
                    data = {
                        "id": position_id,
                        "symbol": "BTCUSDT",
                        "side": "long",
                        "entry_price": 48000.0,
                        "current_price": 50000.0,
                        "pnl": 2000.0,
                        "pnl_percentage": 4.17
                    }
                elif analysis_type == "recommendation":
                    # Mock recommendation data
                    data = {
                        "price": 50000.0,
                        "trend": "bullish",
                        "signal_strength": 0.7,
                        "fib_level": "0.618",
                        "fib_price": 48310.0,
                        "trap_probability": 0.2
                    }
                elif analysis_type == "performance":
                    # Mock performance data
                    data = {
                        "total_pnl": 12500.0,
                        "win_rate": 0.65,
                        "trade_count": 25,
                        "avg_win": 1200.0,
                        "avg_loss": -400.0
                    }
                else:
                    return {"success": False, "error": f"Unknown analysis type: {analysis_type}"}
                
                # Generate analysis HTML
                analysis_html = self.get_persona_analysis_html(data, analysis_type)
                
                return {
                    "success": True,
                    "analysisHtml": analysis_html,
                    "analysisType": analysis_type
                }
            
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        routes["/api/persona_analysis/{analysis_type}"] = get_persona_analysis
        
        return routes
    
    def _format_text_for_html(self, text: str) -> str:
        """
        Format text for HTML display by replacing newlines with <br> tags.
        
        Args:
            text: Raw text that may contain newline characters
            
        Returns:
            HTML-safe text with proper line breaks
        """
        if not text:
            return ""
        
        # Replace literal \n with <br> tags
        return text.replace('\\n', '<br>').replace('\n', '<br>')
    
    def _sanitize_html_output(self, html: str) -> str:
        """
        Sanitize HTML output to ensure no literal newline characters appear in the rendered output.
        
        Args:
            html: HTML string that may contain unwanted newline characters
            
        Returns:
            Sanitized HTML string
        """
        if not html:
            return ""
        
        # Replace literal "\n" strings with actual <br> tags
        sanitized = html.replace('\\n', '<br>')
        sanitized = sanitized.replace('\\n', '<br>')  # Double replacement to catch any missed
        sanitized = sanitized.replace('\n', '<br>')   # Replace actual newlines
        
        # Fix double <br> tags from previous replacements
        sanitized = sanitized.replace('<br><br><br>', '<br><br>')
        
        # Replace any remaining literal escaped backslashes
        sanitized = sanitized.replace('\\\\', '\\')
        
        return sanitized 