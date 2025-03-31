module.exports = {
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    moduleNameMapper: {
        '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
    },
    transform: {
        '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
    },
    testMatch: ['<rootDir>/src/**/*.test.tsx'],
    moduleDirectories: ['node_modules', 'src'],
    roots: ['<rootDir>/src'],
}; 