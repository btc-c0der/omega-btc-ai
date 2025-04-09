import '@testing-library/jest-dom';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    })),
});

// Mock WebSocket
global.WebSocket = class WebSocket {
    constructor() {
        this.readyState = 1;
        this.onmessage = null;
        this.onopen = null;
        this.onclose = null;
        this.onerror = null;
    }
    send() { }
    close() { }
};

// Mock localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    clear: jest.fn(),
};
global.localStorage = localStorageMock; 