/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

/**
 * OMEGA Divine Book Browser v2.0
 * Jest Setup File
 * 
 * This file extends Jest with custom matchers and adds global mocks
 * for testing the OMEGA Divine Book Browser v2.0
 */

// Import testing-library utilities
require('@testing-library/jest-dom');

// Mock Chart.js to prevent rendering errors
global.Chart = class Chart {
    constructor() {
        this.data = null;
        this.options = null;
    }

    destroy() {
        // Mock destroy method
    }

    update() {
        // Mock update method
    }
};

// Mock localStorage
if (!global.localStorage) {
    global.localStorage = {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn(),
        clear: jest.fn()
    };
}

// Mock window.alert and window.confirm
if (!global.alert) {
    global.alert = jest.fn();
}

if (!global.confirm) {
    global.confirm = jest.fn(() => true);
}

// Create mock for marked.js (markdown parser)
global.marked = {
    setOptions: jest.fn(),
    parse: jest.fn(text => `<div>${text}</div>`)
};

// Create mock for highlight.js (code syntax highlighting)
global.hljs = {
    highlight: jest.fn((code, opts) => ({ value: code })),
    highlightAuto: jest.fn(code => ({ value: code })),
    getLanguage: jest.fn(() => true)
};

// Extend expect with custom matchers
expect.extend({
    toHaveBeenCalledWithCategory(received, category) {
        const calls = received.mock.calls;
        const pass = calls.some(call => call[0] === category);

        if (pass) {
            return {
                message: () => `expected ${received} not to have been called with category "${category}"`,
                pass: true
            };
        } else {
            return {
                message: () => `expected ${received} to have been called with category "${category}"`,
                pass: false
            };
        }
    },

    // Check if an element has style property with specified value
    toHaveStyleProperty(received, property, value) {
        const style = window.getComputedStyle(received);
        const pass = style[property] === value;

        if (pass) {
            return {
                message: () => `expected ${received} not to have style property "${property}: ${value}"`,
                pass: true
            };
        } else {
            return {
                message: () => `expected ${received} to have style property "${property}: ${value}", got "${style[property]}"`,
                pass: false
            };
        }
    }
});

// Console message customization
const originalError = console.error;
console.error = function (...args) {
    // Silence specific expected errors that occur during tests
    if (args[0]?.includes('Error: Not implemented: navigation')) {
        return;
    }
    originalError.apply(console, args);
};

// Add test performance measurement
beforeEach(() => {
    jest.spyOn(performance, 'now');
});

// Add support for fake timers
jest.useFakeTimers();

// Log the test setup
console.log('OMEGA Divine Book Browser Test Suite Initialized');
console.log('Target: 80% code coverage');
console.log('--------------------------------------------------'); 