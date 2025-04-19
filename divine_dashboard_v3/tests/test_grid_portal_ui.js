/**
 * "TEST COVERAGE" — "OMEGA GRID PORTAL UI"
 * ========================================
 * 
 * "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST SUITE
 * TESTS THE FRONTEND FUNCTIONALITY OF THE OMEGA GRID PORTAL
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

// Mock fetch for testing API calls
const originalFetch = global.fetch;

describe('"OMEGA GRID PORTAL"', () => {
    let omegaGridPortal;
    let mockElements = {};

    // Setup before each test
    beforeEach(() => {
        // Create mock DOM elements
        document.body.innerHTML = `
            <div id="omega-grid-portal">
                <div id="omega-command-grid"></div>
                <div id="omega-terminal" class="virgil-terminal">
                    <div id="omega-terminal-content"></div>
                </div>
                <div id="virgil-mode-toggle"></div>
                <div id="omega-bots-list"></div>
                <select id="bot-select"></select>
                <input id="custom-command-input" />
                <button id="custom-command-btn"></button>
            </div>
        `;

        // Mock document.addEventListener
        const originalAddEventListener = document.addEventListener;
        document.addEventListener = jest.fn((event, callback) => {
            if (event === 'DOMContentLoaded') {
                callback();
            }
            return originalAddEventListener(event, callback);
        });

        // Mock localStorage
        global.localStorage = {
            getItem: jest.fn(),
            setItem: jest.fn()
        };

        // Mock fetch API
        global.fetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve({
                    status: 'success',
                    commands: [
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
                        }
                    ],
                    bots: [
                        { "id": "test_bot", "name": "Test Bot", "status": "inactive" }
                    ],
                    output: "Command executed successfully"
                })
            })
        );

        // Import the OmegaGridPortal class
        jest.isolateModules(() => {
            const OmegaGridPortal = require('../static/js/omega-grid-virgil').OmegaGridPortal;
            omegaGridPortal = new OmegaGridPortal();
        });

        // Setup spy on console.error
        console.error = jest.fn();
    });

    // Clean up after each test
    afterEach(() => {
        global.fetch = originalFetch;
        jest.clearAllMocks();
    });

    // Test initialization
    test('"INITIALIZATION" — "VERIFY PROPER INITIALIZATION"', async () => {
        await omegaGridPortal.init();
        expect(global.fetch).toHaveBeenCalledTimes(2);
        expect(omegaGridPortal.commands.length).toBeGreaterThan(0);
        expect(omegaGridPortal.bots.length).toBeGreaterThan(0);
    });

    // Test Virgil mode toggle
    test('"VIRGIL MODE" — "VERIFY MODE TOGGLE FUNCTIONALITY"', () => {
        omegaGridPortal.elements = {
            virgilModeToggle: document.getElementById('virgil-mode-toggle'),
            commandGrid: document.getElementById('omega-command-grid'),
            terminal: document.getElementById('omega-terminal')
        };

        // Initially off
        omegaGridPortal.virgilModeEnabled = false;

        // Toggle on
        omegaGridPortal.toggleVirgilMode();
        expect(omegaGridPortal.virgilModeEnabled).toBe(true);
        expect(localStorage.setItem).toHaveBeenCalledWith('virgilMode', true);
        expect(document.body.classList.contains('virgil-mode')).toBe(true);

        // Toggle off
        omegaGridPortal.toggleVirgilMode();
        expect(omegaGridPortal.virgilModeEnabled).toBe(false);
        expect(localStorage.setItem).toHaveBeenCalledWith('virgilMode', false);
        expect(document.body.classList.contains('virgil-mode')).toBe(false);
    });

    // Test command grid rendering
    test('"COMMAND GRID" — "VERIFY GRID RENDERING"', () => {
        omegaGridPortal.elements = {
            commandGrid: document.getElementById('omega-command-grid')
        };
        omegaGridPortal.commands = [
            {
                "id": "test_command",
                "name": "TEST COMMAND",
                "description": "Test command description",
                "emoji": "🧪"
            }
        ];

        omegaGridPortal.renderCommandGrid();

        const cardElement = document.querySelector('.command-card');
        expect(cardElement).not.toBeNull();
        expect(cardElement.dataset.commandId).toBe('test_command');
        expect(document.querySelector('.command-card-header').innerHTML).toContain('TEST COMMAND');
        expect(document.querySelector('.command-description').textContent).toBe('Test command description');
    });

    // Test command execution
    test('"COMMAND EXECUTION" — "VERIFY COMMAND EXECUTION FLOW"', async () => {
        // Setup elements and mocks
        omegaGridPortal.elements = {
            terminalContent: document.getElementById('omega-terminal-content')
        };
        omegaGridPortal.commands = [
            {
                "id": "test_command",
                "name": "TEST COMMAND",
                "description": "Test command description",
                "emoji": "🧪"
            }
        ];

        // Mock showNotification
        omegaGridPortal.showNotification = jest.fn();

        // Mock addTerminalOutput
        omegaGridPortal.addTerminalOutput = jest.fn();

        // Execute command
        await omegaGridPortal.executeCommand('test_command');

        // Verify API call
        expect(global.fetch).toHaveBeenCalledWith('/api/grid/execute', expect.any(Object));

        // Verify notification
        expect(omegaGridPortal.showNotification).toHaveBeenCalledTimes(2);

        // Verify terminal output
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalled();
    });

    // Test terminal output
    test('"TERMINAL OUTPUT" — "VERIFY TERMINAL OUTPUT HANDLING"', () => {
        // Setup elements
        omegaGridPortal.elements = {
            terminalContent: document.getElementById('omega-terminal-content')
        };

        // Add various types of output
        omegaGridPortal.addTerminalOutput('Command message', 'command');
        omegaGridPortal.addTerminalOutput('Regular output', 'output');
        omegaGridPortal.addTerminalOutput('Error message', 'error');

        // Verify DOM updates
        const lines = document.querySelectorAll('.terminal-line');
        expect(lines.length).toBe(3);
        expect(lines[0].classList.contains('command')).toBe(true);
        expect(lines[1].classList.contains('output')).toBe(true);
        expect(lines[2].classList.contains('error')).toBe(true);

        // Verify timestamps on command lines
        const timestamp = document.querySelector('.terminal-timestamp');
        expect(timestamp).not.toBeNull();
    });

    // Test command output processing
    test('"OUTPUT PROCESSING" — "VERIFY COMMAND OUTPUT PARSING"', () => {
        // Setup
        omegaGridPortal.addTerminalOutput = jest.fn();

        // Test multiline output with different content types
        const testOutput = `
HEADER LINE
==========
Command info line
SOME ERROR OCCURRED
------------------
"THIS IS A QUOTE"
SUCCESS: Operation completed
`;

        omegaGridPortal.processCommandOutput(testOutput);

        // Verify different line types were correctly identified
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('HEADER LINE', 'header');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('==========', 'header');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('Command info line', 'output');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('SOME ERROR OCCURRED', 'error');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('------------------', 'divider');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('"THIS IS A QUOTE"', 'quote');
        expect(omegaGridPortal.addTerminalOutput).toHaveBeenCalledWith('SUCCESS: Operation completed', 'success');
    });

    // Test bot selection
    test('"BOT MANAGEMENT" — "VERIFY BOT SELECT POPULATION"', () => {
        // Setup
        omegaGridPortal.elements = {
            botSelect: document.getElementById('bot-select')
        };

        omegaGridPortal.bots = [
            { "id": "bot1", "name": "Bot One", "status": "inactive" },
            { "id": "bot2", "name": "Bot Two", "status": "active" }
        ];

        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.textContent = "SELECT BOT";
        omegaGridPortal.elements.botSelect.appendChild(defaultOption);

        // Populate select
        omegaGridPortal.populateBotSelect();

        // Verify options
        const options = document.querySelectorAll('#bot-select option');
        expect(options.length).toBe(3); // default + 2 bots
        expect(options[1].value).toBe('bot1');
        expect(options[1].textContent).toBe('Bot One');
    });

    // Test notification system
    test('"NOTIFICATIONS" — "VERIFY NOTIFICATION SYSTEM"', () => {
        // Setup mock for setTimeout
        jest.useFakeTimers();

        // Show notification
        omegaGridPortal.showNotification('"TEST NOTIFICATION"', 'info');

        // Verify DOM updates
        const notification = document.querySelector('.virgil-notification');
        expect(notification).not.toBeNull();
        expect(notification.textContent).toBe('"TEST NOTIFICATION"');
        expect(notification.classList.contains('info')).toBe(true);

        // First timeout shows the notification
        jest.advanceTimersByTime(10);
        expect(notification.classList.contains('show')).toBe(true);

        // Second timeout hides the notification
        jest.advanceTimersByTime(4000);
        expect(notification.classList.contains('show')).toBe(false);

        // Restore timers
        jest.useRealTimers();
    });

    // Test quote system
    test('"QUOTES" — "VERIFY RANDOM QUOTE FUNCTIONALITY"', () => {
        // Setup with predefined quotes
        omegaGridPortal.quotes = ["QUOTE1", "QUOTE2", "QUOTE3"];

        // Mock Math.random to return predictable values
        const originalRandom = Math.random;
        Math.random = jest.fn().mockReturnValue(0.1); // Will select QUOTE1

        // Get a quote
        const quote = omegaGridPortal.getRandomQuote();
        expect(quote).toBe("QUOTE1");

        // Restore Math.random
        Math.random = originalRandom;
    });
});

/**
 * Mocked OmegaGridPortal export for testing
 */
module.exports = {
    OmegaGridPortal: window.OmegaGridPortal
}; 