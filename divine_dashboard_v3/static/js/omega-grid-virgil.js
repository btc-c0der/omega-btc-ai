/**
 * OMEGA GRID PORTAL - Virgil Abloh / OFF-WHITE™ Edition
 * ====================================================
 * JavaScript functionality for the OMEGA GRID PORTAL UI integration
 * with design inspiration from Virgil Abloh and OFF-WHITE.
 * 
 * "FUNCTIONALITY" AND "DESIGN" AS ONE
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

class OmegaGridPortal {
    constructor() {
        // State
        this.virgilModeEnabled = false;
        this.activeCommandId = null;
        this.terminalOutput = [];
        this.commands = [];
        this.bots = [];
        this.quotes = [
            "THE MARKET WILL TEST YOU",
            "TRADING IS SIMPLY INFORMATION EXCHANGE",
            "POSITIONS ARE JUST TEMPORARY STATES",
            "A LOSS IS ONLY A LESSON",
            "RISK IS THE TAX PAID FOR OPPORTUNITY",
            "PATIENCE IS THE ULTIMATE EDGE",
            "THE TREND IS YOUR \"FRIEND\"",
            "TECHNICAL ANALYSIS IS \"POETRY\"",
            "BUY THE \"DIP\"",
            "SELL THE \"NEWS\""
        ];

        // DOM Element references
        this.elements = {};

        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => this.init());
    }

    /**
     * Initialize the portal
     */
    async init() {
        console.log("🌐 Initializing OMEGA GRID PORTAL - Virgil Abloh Edition");

        // Set up DOM references
        this.cacheElements();

        // Setup event listeners
        this.setupEventListeners();

        // Fetch commands and bots
        await Promise.all([
            this.fetchCommands(),
            this.fetchBots()
        ]);

        // Render the command grid
        this.renderCommandGrid();

        // Apply Virgil mode based on localStorage setting
        this.applyVirgilMode(localStorage.getItem('virgilMode') === 'true');

        // Show initial quote in terminal
        this.addTerminalOutput(`"${this.getRandomQuote()}"   "OMEGA SYSTEM READY"`, 'quote');

        console.log("🌐 OMEGA GRID PORTAL initialized");
    }

    /**
     * Cache DOM elements for quick access
     */
    cacheElements() {
        this.elements.container = document.getElementById('omega-grid-portal');

        if (!this.elements.container) {
            console.error("OMEGA GRID PORTAL container not found");
            return;
        }

        this.elements.commandGrid = document.getElementById('omega-command-grid');
        this.elements.terminal = document.getElementById('omega-terminal');
        this.elements.terminalContent = document.getElementById('omega-terminal-content');
        this.elements.virgilModeToggle = document.getElementById('virgil-mode-toggle');
        this.elements.botsList = document.getElementById('omega-bots-list');
        this.elements.botSelect = document.getElementById('bot-select');
        this.elements.customCommandInput = document.getElementById('custom-command-input');
        this.elements.customCommandBtn = document.getElementById('custom-command-btn');
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        if (!this.elements.container) return;

        // Virgil mode toggle
        if (this.elements.virgilModeToggle) {
            this.elements.virgilModeToggle.addEventListener('click', () => {
                this.toggleVirgilMode();
            });
        }

        // Custom command execution
        if (this.elements.customCommandBtn && this.elements.customCommandInput) {
            this.elements.customCommandBtn.addEventListener('click', () => {
                const command = this.elements.customCommandInput.value.trim();
                if (command) {
                    this.executeCommand('run_custom', command);
                    this.elements.customCommandInput.value = '';
                }
            });

            this.elements.customCommandInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const command = this.elements.customCommandInput.value.trim();
                    if (command) {
                        this.executeCommand('run_custom', command);
                        this.elements.customCommandInput.value = '';
                    }
                }
            });
        }
    }

    /**
     * Toggle Virgil Abloh design mode
     */
    toggleVirgilMode() {
        this.applyVirgilMode(!this.virgilModeEnabled);
    }

    /**
     * Apply Virgil Abloh design mode
     * @param {boolean} enable - Whether to enable Virgil mode
     */
    applyVirgilMode(enable) {
        this.virgilModeEnabled = enable;

        // Store preference
        localStorage.setItem('virgilMode', this.virgilModeEnabled);

        // Apply to body class
        document.body.classList.toggle('virgil-mode', this.virgilModeEnabled);

        // Update toggle button text
        if (this.elements.virgilModeToggle) {
            this.elements.virgilModeToggle.textContent = this.virgilModeEnabled
                ? '"VIRGIL MODE" ON'
                : '"VIRGIL MODE" OFF';
        }

        // Command grid styling
        if (this.elements.commandGrid) {
            this.elements.commandGrid.classList.toggle('virgil-grid', this.virgilModeEnabled);
        }

        // Terminal styling
        if (this.elements.terminal) {
            this.elements.terminal.classList.toggle('virgil-terminal', this.virgilModeEnabled);
        }

        // Notify
        this.showNotification(
            this.virgilModeEnabled
                ? '"VIRGIL MODE" ACTIVATED   "OFF—WHITE™ FOR OMEGA"'
                : '"VIRGIL MODE" DEACTIVATED',
            'info'
        );

        // If enabling, show a quote
        if (this.virgilModeEnabled) {
            this.addTerminalOutput(`"${this.getRandomQuote()}"   "DESIGN AXIOM"`, 'quote');
        }
    }

    /**
     * Fetch available commands from the API
     */
    async fetchCommands() {
        try {
            // In a real implementation, this would be an API call
            // For now, we'll simulate with static data
            const response = await fetch('/api/grid/commands');
            const data = await response.json();

            if (data.status === 'success') {
                this.commands = data.commands;
            } else {
                console.error("Failed to fetch commands:", data);
                // Use fallback commands
                this.useFallbackCommands();
            }
        } catch (error) {
            console.error("Error fetching commands:", error);
            // Use fallback commands
            this.useFallbackCommands();
        }
    }

    /**
     * Use fallback command data when API is unavailable
     */
    useFallbackCommands() {
        // This is the same data structure we have on the backend
        this.commands = [
            {
                "id": "show_status",
                "name": "SHOW STATUS",
                "description": "Display the current status of all bots and services",
                "emoji": "👁️‍🗨️"
            },
            {
                "id": "launch_dashboard",
                "name": "LAUNCH 5D DASHBOARD",
                "description": "Launch the 5D comprehensive dashboard",
                "emoji": "🌌"
            },
            {
                "id": "launch_matrix",
                "name": "LAUNCH MATRIX VIEW",
                "description": "Launch the Matrix terminal dashboard",
                "emoji": "🧮"
            },
            {
                "id": "launch_web",
                "name": "LAUNCH WEB VIEW",
                "description": "Launch the web-based dashboard",
                "emoji": "🌐"
            },
            {
                "id": "start_all",
                "name": "START ALL BOTS",
                "description": "Activate all available bots in the system",
                "emoji": "🚀"
            },
            {
                "id": "draw_wisdom",
                "name": "DRAW WISDOM CARD",
                "description": "Draw a wisdom card from King Solomon's deck",
                "emoji": "🃏"
            },
            {
                "id": "solomon_portal",
                "name": "OPEN SOLOMON PORTAL",
                "description": "Open the spiritual portal to King Solomon's wisdom",
                "emoji": "👑"
            },
            {
                "id": "install_deps",
                "name": "INSTALL DEPENDENCIES",
                "description": "Install all required dependencies for OMEGA GRID",
                "emoji": "📦"
            },
            {
                "id": "export_status",
                "name": "EXPORT STATUS REPORT",
                "description": "Export the current system status to a file",
                "emoji": "📊"
            },
            {
                "id": "start_bot",
                "name": "START BOT",
                "description": "Start a specific bot by name",
                "param_required": true,
                "emoji": "🤖"
            },
            {
                "id": "stop_bot",
                "name": "STOP BOT",
                "description": "Stop a specific bot by name",
                "param_required": true,
                "emoji": "🛑"
            },
            {
                "id": "restart_bot",
                "name": "RESTART BOT",
                "description": "Restart a specific bot by name",
                "param_required": true,
                "emoji": "🔄"
            },
            {
                "id": "run_custom",
                "name": "RUN CUSTOM COMMAND",
                "description": "Run a custom OMEGA GRID command",
                "custom_input": true,
                "emoji": "⌨️"
            },
            {
                "id": "show_help",
                "name": "SHOW HELP",
                "description": "Display all available commands and options",
                "emoji": "❓"
            }
        ];
    }

    /**
     * Fetch available bots from the API
     */
    async fetchBots() {
        try {
            // In a real implementation, this would be an API call
            const response = await fetch('/api/grid/bots');
            const data = await response.json();

            if (data.status === 'success') {
                this.bots = data.bots;
            } else {
                console.error("Failed to fetch bots:", data);
                // Use fallback bots
                this.useFallbackBots();
            }
        } catch (error) {
            console.error("Error fetching bots:", error);
            // Use fallback bots
            this.useFallbackBots();
        }

        // Populate bot select if it exists
        this.populateBotSelect();
    }

    /**
     * Use fallback bot data when API is unavailable
     */
    useFallbackBots() {
        this.bots = [
            { "id": "bitget_position_analyzer", "name": "BitGet Position Analyzer", "status": "inactive" },
            { "id": "matrix_cli", "name": "Matrix CLI Interface", "status": "inactive" },
            { "id": "discord_bot", "name": "Discord Bot", "status": "inactive" },
            { "id": "strategic_trader", "name": "Strategic Trader", "status": "inactive" },
            { "id": "position_monitor", "name": "Position Monitor", "status": "inactive" },
            { "id": "cybernetic_quantum_bloom", "name": "Cybernetic Quantum Bloom", "status": "inactive" },
            { "id": "matrix_btc_cyberpunk", "name": "Matrix BTC Cyberpunk", "status": "inactive" }
        ];
    }

    /**
     * Populate the bot select dropdown
     */
    populateBotSelect() {
        if (!this.elements.botSelect) return;

        // Clear existing options except the default
        const defaultOption = this.elements.botSelect.querySelector('option[value=""]');
        this.elements.botSelect.innerHTML = '';
        if (defaultOption) {
            this.elements.botSelect.appendChild(defaultOption);
        }

        // Add bots to select
        this.bots.forEach(bot => {
            const option = document.createElement('option');
            option.value = bot.id;
            option.textContent = bot.name;
            this.elements.botSelect.appendChild(option);
        });
    }

    /**
     * Render the command grid based on available commands
     */
    renderCommandGrid() {
        if (!this.elements.commandGrid) return;

        // Clear existing grid
        this.elements.commandGrid.innerHTML = '';

        // Render each command as a card
        this.commands.forEach(command => {
            const needsParam = command.param_required || command.custom_input;
            const cardElement = this.createCommandCard(command, needsParam);
            this.elements.commandGrid.appendChild(cardElement);
        });
    }

    /**
     * Create a command card element
     * @param {Object} command - The command object
     * @param {boolean} needsParam - Whether the command requires a parameter
     * @returns {HTMLElement} The command card element
     */
    createCommandCard(command, needsParam = false) {
        const card = document.createElement('div');
        card.className = 'command-card';
        card.dataset.commandId = command.id;

        // Card header
        const header = document.createElement('div');
        header.className = 'command-card-header';
        header.innerHTML = `${command.emoji} "${command.name}"`;
        card.appendChild(header);

        // Card content
        const content = document.createElement('div');
        content.className = 'command-card-content';

        // Description
        const description = document.createElement('div');
        description.className = 'command-description';
        description.textContent = command.description;
        content.appendChild(description);

        // Parameter input if needed
        if (needsParam && command.id !== 'run_custom') {
            const paramContainer = document.createElement('div');
            paramContainer.className = 'command-param-container';

            const select = document.createElement('select');
            select.className = 'command-param-select';
            select.id = `${command.id}-param`;

            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select Bot';
            select.appendChild(defaultOption);

            // Add bots as options
            this.bots.forEach(bot => {
                const option = document.createElement('option');
                option.value = bot.id;
                option.textContent = bot.name;
                select.appendChild(option);
            });

            paramContainer.appendChild(select);
            content.appendChild(paramContainer);
        }

        // Execute button
        const button = document.createElement('button');
        button.className = 'command-card-button';
        button.textContent = 'EXECUTE';

        // Add click event listener to execute the command
        button.addEventListener('click', () => {
            if (needsParam && command.id !== 'run_custom') {
                const paramSelect = document.getElementById(`${command.id}-param`);
                if (paramSelect && paramSelect.value) {
                    this.executeCommand(command.id, paramSelect.value);
                } else {
                    this.showNotification('"BOT SELECTION REQUIRED"', 'error');
                }
            } else if (command.id !== 'run_custom') {
                this.executeCommand(command.id);
            }
        });

        content.appendChild(button);
        card.appendChild(content);

        // Add overlay text (Virgil style)
        const overlay = document.createElement('div');
        overlay.className = 'command-card-overlay';
        overlay.textContent = command.name.split(' ')[0];
        card.appendChild(overlay);

        return card;
    }

    /**
     * Execute a command
     * @param {string} commandId - The ID of the command to execute
     * @param {string} param - Optional parameter for the command
     */
    async executeCommand(commandId, param = null) {
        console.log(`Executing command: ${commandId}${param ? ` with param: ${param}` : ''}`);

        // Find the command
        const command = this.commands.find(cmd => cmd.id === commandId);
        if (!command) {
            console.error(`Command not found: ${commandId}`);
            this.showNotification('"COMMAND NOT FOUND"', 'error');
            return;
        }

        // Set active command
        this.activeCommandId = commandId;

        // Show executing notification
        this.showNotification(`"EXECUTING: ${command.name}"`, 'info');

        // Add command to terminal
        this.addTerminalOutput(`"EXECUTING COMMAND"   "${command.name}"${param ? `   "PARAM: ${param}"` : ''}`, 'command');

        try {
            // In a real implementation, this would be an API call
            const response = await fetch('/api/grid/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    commandId,
                    param
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Add output to terminal
                this.processCommandOutput(data.output);

                // Show success notification
                this.showNotification(`"${command.name} COMPLETED"`, 'success');
            } else {
                // Add error to terminal
                this.addTerminalOutput(`"ERROR"   "${data.output}"`, 'error');

                // Show error notification
                this.showNotification(`"${command.name} FAILED"`, 'error');
            }
        } catch (error) {
            console.error(`Error executing command ${commandId}:`, error);

            // Simulate output for development
            this.simulateCommandOutput(commandId, param);

            // Add error to terminal
            this.addTerminalOutput(`"ERROR"   "${error.message}"`, 'error');

            // Show error notification
            this.showNotification(`"${command.name} FAILED"   "CONNECTION ERROR"`, 'error');
        }

        // Clear active command
        this.activeCommandId = null;
    }

    /**
     * Process command output and add to terminal
     * @param {string} output - The command output text
     */
    processCommandOutput(output) {
        // Split output into lines and add to terminal
        const lines = output.split('\n');
        for (const line of lines) {
            // Don't add empty lines
            if (line.trim()) {
                // Determine line type based on content
                let type = 'output';

                if (line.includes('ERROR') || line.includes('FAILED')) {
                    type = 'error';
                } else if (line.includes('SUCCESS') || line.includes('COMPLETED')) {
                    type = 'success';
                } else if (line.match(/={3,}/)) {
                    type = 'header';
                } else if (line.match(/-{3,}/)) {
                    type = 'divider';
                } else if (line.includes('"')) {
                    type = 'quote';
                }

                this.addTerminalOutput(line, type);
            }
        }
    }

    /**
     * Simulate command output for development
     * @param {string} commandId - The ID of the command
     * @param {string} param - Optional parameter
     */
    simulateCommandOutput(commandId, param) {
        // Find the command
        const command = this.commands.find(cmd => cmd.id === commandId);
        if (!command) return;

        let output = '';

        // Generate simulated outputs for different commands
        if (commandId === 'show_status') {
            output = `
OMEGA GRID STATUS
==========================================================
TIMESTAMP: ${new Date().toLocaleString()}
==========================================================
GRID     X: 23.7516     Y: 42.1893     Z: 19.3721
SIDE     QUANTUM ALIGNED     DENSITY: 87.3%
----------------------------------------------------------

ACTIVE BOTS   STATUS: RUNNING
  • 📊 BITGET_POSITION_ANALYZER — Analyzes BitGet positions with Fibonacci levels
  • 🧮 MATRIX_CLI — Matrix-style CLI interface for position monitoring

INACTIVE BOTS   STATUS: STANDBY
  • 🤖 DISCORD_BOT — Discord bot for positions management
  • 📈 STRATEGIC_TRADER — CCXT-based strategic trading bot
  • 👁️ POSITION_MONITOR — Monitors BitGet positions for changes
  • 🔮 CYBERNETIC_QUANTUM_BLOOM — Quantum-aligned market prediction system
  • 🌐 MATRIX_BTC_CYBERPUNK — Cyberpunk visualization for BTC

SERVICES   INFRASTRUCTURE
  • 💾 REDIS — ONLINE   MEMORY: AVAILABLE
  • 🌊 REGGAE DASHBOARD — ONLINE   UI: VIRGIL MODE

==========================================================
THE SYSTEM IS YOURS   c/o OMEGA GRID   FOR TRAINING PURPOSES
==========================================================
`;
        } else if (commandId === 'draw_wisdom') {
            output = `
============================================================
          👑 THE DIVINE RULER 👑
============================================================
ELEMENT: ✨ SPIRIT

WISDOM:
The greatest power is the power to rule oneself. Seek inner mastery before external control.

ACTION:
Meditate on your self-discipline today and strengthen your inner kingdom.
============================================================
`;
        } else if (commandId.includes('_bot') && param) {
            const action = commandId.split('_')[0].toUpperCase();
            output = `
${action} BOT: ${param}
----------------------------------------------------------
PROCESSING REQUEST...
COMMAND RECEIVED
BOT NAME: ${param}
TIMESTAMP: ${new Date().toLocaleString()}
QUANTUM ALIGNMENT: IN PROGRESS
----------------------------------------------------------
RESULT: SUCCESS
BOT ${param} ${action}ED SUCCESSFULLY
GRID UPDATED
----------------------------------------------------------
`;
        } else if (commandId === 'run_custom' && param) {
            output = `
Running custom command: ${param}
----------------------------------------------------------
COMMAND EXECUTED
CUSTOM INPUT: ${param}
TIMESTAMP: ${new Date().toLocaleString()}
----------------------------------------------------------
RESULT: SUCCESS
CUSTOM COMMAND EXECUTED
GRID UPDATED
----------------------------------------------------------
`;
        } else {
            output = `Command ${command.name} executed successfully.`;
        }

        // Process output
        this.processCommandOutput(output);
    }

    /**
     * Add output to the terminal
     * @param {string} text - The text to add
     * @param {string} type - The type of output (command, output, error, etc.)
     */
    addTerminalOutput(text, type = 'output') {
        if (!this.elements.terminalContent) return;

        // Create output element
        const output = document.createElement('div');
        output.className = `terminal-line ${type}`;
        output.textContent = text;

        // Add timestamp for certain types
        if (['command', 'error', 'success'].includes(type)) {
            const timestamp = document.createElement('span');
            timestamp.className = 'terminal-timestamp';
            timestamp.textContent = new Date().toLocaleTimeString();
            output.prepend(timestamp);
        }

        // Add to terminal
        this.elements.terminalContent.appendChild(output);

        // Auto-scroll to bottom
        this.elements.terminalContent.scrollTop = this.elements.terminalContent.scrollHeight;

        // Store in history (limited to 100 items)
        this.terminalOutput.push({ text, type });
        if (this.terminalOutput.length > 100) {
            this.terminalOutput.shift();
        }
    }

    /**
     * Show a notification
     * @param {string} message - The notification message
     * @param {string} type - The notification type (info, success, error)
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `virgil-notification ${type}`;
        notification.textContent = message;

        // Add to body
        document.body.appendChild(notification);

        // Trigger animation (show)
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        // Auto-hide after 4 seconds
        setTimeout(() => {
            notification.classList.remove('show');

            // Remove from DOM after animation completes
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 4000);
    }

    /**
     * Get a random quote
     * @returns {string} A random quote
     */
    getRandomQuote() {
        return this.quotes[Math.floor(Math.random() * this.quotes.length)];
    }
}

// Initialize the portal
const omegaGridPortal = new OmegaGridPortal(); 