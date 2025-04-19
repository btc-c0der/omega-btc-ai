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
 * Jest configuration for Divine Dashboard v3 tests
 */

module.exports = {
    // Test environment for DOM testing
    testEnvironment: 'jsdom',

    // File extensions for test files
    moduleFileExtensions: ['js', 'jsx', 'json', 'html'],

    // Coverage reporting configuration
    collectCoverage: true,
    coverageDirectory: 'coverage',
    coverageReporters: ['text', 'lcov', 'json-summary'],

    // Coverage thresholds to ensure we meet our target
    coverageThreshold: {
        global: {
            branches: 90,
            functions: 90,
            lines: 90,
            statements: 90
        }
    },

    // Transform files with babel-jest
    transform: {
        '^.+\\.jsx?$': 'babel-jest'
    },

    // Test patterns to look for
    testMatch: [
        '**/tests/**/*.test.js',
        '**/__tests__/**/*.js'
    ],

    // Setup files to run before tests
    setupFilesAfterEnv: ['./tests/setup.js'],

    // Module name mapper for non-JS assets
    moduleNameMapper: {
        '\\.(css|less|scss)$': '<rootDir>/tests/mocks/styleMock.js',
        '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/tests/mocks/fileMock.js',
        '\\.html$': '<rootDir>/tests/mocks/htmlMock.js'
    },

    // Automatically clear mock calls between every test
    clearMocks: true,

    // Display test results with more details
    verbose: true
}; 