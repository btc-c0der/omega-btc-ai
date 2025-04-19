/**
 * "JEST CONFIGURATION" — "OMEGA GRID PORTAL"
 * =========================================
 * 
 * "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST CONFIGURATION
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

module.exports = {
    // Basic Jest Configuration
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],

    // Collection of test files
    testMatch: [
        '<rootDir>/tests/test_*.js',
        '<rootDir>/tests/**/*test*.js'
    ],

    // Coverage options
    collectCoverage: true,
    collectCoverageFrom: [
        '<rootDir>/static/js/omega-grid-virgil.js',
        '!<rootDir>/node_modules/**'
    ],
    coverageDirectory: '<rootDir>/coverage',
    coverageReporters: ['json', 'lcov', 'text', 'clover'],

    // Transformation
    transform: {
        '^.+\\.jsx?$': 'babel-jest'
    },

    // Module resolution
    moduleNameMapper: {
        '\\.(css|less|scss|sass)$': '<rootDir>/tests/mocks/styleMock.js',
        '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4)$': '<rootDir>/tests/mocks/fileMock.js'
    },

    // Test timeout
    testTimeout: 10000,

    // Verbose output
    verbose: true,

    // Custom reporters
    reporters: ['default'],

    // Cache location (for CI/CD)
    cacheDirectory: './.jest-cache',

    // Display for test results
    bail: 1,
    displayName: {
        name: 'OMEGA_GRID',
        color: 'yellow'
    },

    // OFF-WHITE™ styled reporter options
    testResultsProcessor: '<rootDir>/tests/virgil-reporter.js',

    // Inject global variables
    globals: {
        'VIRGIL_MODE': true,
        'GRID_VERSION': 'Φ1.618'
    }
}; 