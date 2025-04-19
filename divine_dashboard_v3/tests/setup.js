/**
 * "TEST SETUP" — "OMEGA GRID PORTAL"
 * =================================
 * 
 * "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST SETUP
 * BOOTSTRAP CONFIGURATION FOR JEST TESTS
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

/**
 * Test setup file for Divine Dashboard v3
 * This file will run before any test files
 */

// Import test libraries
require('@testing-library/jest-dom');

// Configure console messages with Virgil-style quotations
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;

// Override console.log
console.log = function (...args) {
    // Add Virgil-style quotation marks to string arguments
    const virgilArgs = args.map(arg => {
        if (typeof arg === 'string' && !arg.includes('"')) {
            return `"${arg}"`;
        }
        return arg;
    });
    originalLog(...virgilArgs);
};

// Override console.error for Virgil styling
console.error = function (...args) {
    const virgilArgs = args.map(arg => {
        if (typeof arg === 'string' && !arg.includes('"')) {
            return `"ERROR" — "${arg}"`;
        }
        return arg;
    });
    originalError(...virgilArgs);
};

// Override console.warn for Virgil styling
console.warn = function (...args) {
    const virgilArgs = args.map(arg => {
        if (typeof arg === 'string' && !arg.includes('"')) {
            return `"WARNING" — "${arg}"`;
        }
        return arg;
    });
    originalWarn(...virgilArgs);
};

// Add global mock for window.OmegaGridPortal
window.OmegaGridPortal = class OmegaGridPortal {
    constructor() {
        this.virgilModeEnabled = false;
        this.commands = [];
        this.bots = [];
        this.quotes = [];
        this.elements = {};
    }

    async init() { }

    cacheElements() { }

    setupEventListeners() { }

    toggleVirgilMode() { }

    applyVirgilMode() { }

    async fetchCommands() { }

    useFallbackCommands() { }

    async fetchBots() { }

    useFallbackBots() { }

    populateBotSelect() { }

    renderCommandGrid() { }

    createCommandCard() {
        return document.createElement('div');
    }

    async executeCommand() { }

    processCommandOutput() { }

    simulateCommandOutput() { }

    addTerminalOutput() { }

    showNotification() { }

    getRandomQuote() {
        return this.quotes[0] || "DEFAULT QUOTE";
    }
};

// Mock OmegaGridPortal instance
global.omegaGridPortal = new window.OmegaGridPortal();

// Create custom error messages in Virgil style
const originalExpect = global.expect;
global.expect = (actual) => {
    const expectInstance = originalExpect(actual);
    const originalToEqual = expectInstance.toEqual;

    // Wrap toEqual with custom error message
    expectInstance.toEqual = (expected) => {
        try {
            return originalToEqual.call(expectInstance, expected);
        } catch (error) {
            error.message = `"ASSERTION FAILED" — "EXPECTED VALUE TO EQUAL" — "${JSON.stringify(expected)}" — "BUT GOT" — "${JSON.stringify(actual)}"`;
            throw error;
        }
    };

    return expectInstance;
};

// Mock browser APIs not implemented in jsdom
global.matchMedia = global.matchMedia || function (query) {
    return {
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    };
};

// Mock requestFullscreen method since it's not implemented in jsdom
Element.prototype.requestFullscreen = jest.fn();

// Mock fullscreen API
document.fullscreenElement = null;
document.exitFullscreen = jest.fn();

// Create storage mock for localStorage and sessionStorage
const storageMock = () => {
    let storage = {};
    return {
        getItem: key => key in storage ? storage[key] : null,
        setItem: (key, value) => { storage[key] = value.toString(); },
        removeItem: key => { delete storage[key]; },
        clear: () => { storage = {}; },
        key: index => Object.keys(storage)[index] || null,
        get length() { return Object.keys(storage).length; }
    };
};

// Apply storage mocks
Object.defineProperty(window, 'localStorage', { value: storageMock() });
Object.defineProperty(window, 'sessionStorage', { value: storageMock() }); 