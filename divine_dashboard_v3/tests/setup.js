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
 * Test setup file for Divine Dashboard v3
 * This file will run before any test files
 */

// Add custom jest matchers from jest-dom
require('@testing-library/jest-dom');

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

// Mock console methods to reduce noise
console.error = jest.fn();
console.warn = jest.fn();

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