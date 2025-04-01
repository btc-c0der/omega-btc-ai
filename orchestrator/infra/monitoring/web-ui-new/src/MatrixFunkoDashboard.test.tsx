import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MatrixFunkoDashboard } from './MatrixFunkoDashboard';
import { ThemeProvider } from '../context/ThemeContext';
import { MatrixProvider } from '../context/MatrixContext';

// Mock the WebSocket connection
jest.mock('../hooks/useMatrixWebSocket', () => ({
    useMatrixWebSocket: () => ({
        connected: true,
        data: {
            testRate: 100,
            testFailures: 0,
            redisCommands: 500,
            marketTrends: 75,
            serviceHealth: 95,
            testCoverage: 85
        }
    })
}));

describe('MatrixFunkoDashboard', () => {
    const renderDashboard = () => {
        return render(
            <ThemeProvider>
                <MatrixProvider>
                    <MatrixFunkoDashboard />
                </MatrixProvider>
            </ThemeProvider>
        );
    };

    test('renders dashboard with all panels', () => {
        renderDashboard();

        // Check for main panels
        expect(screen.getByText('🔱 Divine Test Rate')).toBeInTheDocument();
        expect(screen.getByText('💫 Divine Test Failures')).toBeInTheDocument();
        expect(screen.getByText('🌟 Divine Redis Commands')).toBeInTheDocument();
        expect(screen.getByText('✨ Divine Market Trends')).toBeInTheDocument();
        expect(screen.getByText('🌌 Divine Service Health')).toBeInTheDocument();
        expect(screen.getByText('🌠 Divine Test Coverage')).toBeInTheDocument();
    });

    test('displays real-time metrics', async () => {
        renderDashboard();

        // Wait for metrics to be displayed
        await waitFor(() => {
            expect(screen.getByText('100')).toBeInTheDocument();
            expect(screen.getByText('0')).toBeInTheDocument();
            expect(screen.getByText('500')).toBeInTheDocument();
            expect(screen.getByText('75')).toBeInTheDocument();
            expect(screen.getByText('95')).toBeInTheDocument();
            expect(screen.getByText('85')).toBeInTheDocument();
        });
    });

    test('toggles dark/light theme', () => {
        renderDashboard();

        const themeToggle = screen.getByRole('button', { name: /toggle theme/i });
        fireEvent.click(themeToggle);

        // Check if theme class is updated
        expect(document.body).toHaveClass('matrix-funko-theme-dark');
    });

    test('displays Funko character when metrics are optimal', async () => {
        renderDashboard();

        // Wait for metrics to be displayed
        await waitFor(() => {
            expect(screen.getByTestId('funko-character')).toBeInTheDocument();
        });
    });

    test('shows alert when service health is low', async () => {
        // Mock low service health
        jest.spyOn(global, 'fetch').mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({ serviceHealth: 30 })
            })
        );

        renderDashboard();

        await waitFor(() => {
            expect(screen.getByText(/⚠️ Service Health Alert/i)).toBeInTheDocument();
        });
    });

    test('updates metrics in real-time', async () => {
        renderDashboard();

        // Initial values
        expect(screen.getByText('100')).toBeInTheDocument();

        // Simulate new data
        const newData = {
            testRate: 150,
            testFailures: 2,
            redisCommands: 600,
            marketTrends: 80,
            serviceHealth: 90,
            testCoverage: 88
        };

        // Trigger WebSocket update
        fireEvent(window, new MessageEvent('message', { data: JSON.stringify(newData) }));

        await waitFor(() => {
            expect(screen.getByText('150')).toBeInTheDocument();
            expect(screen.getByText('2')).toBeInTheDocument();
            expect(screen.getByText('600')).toBeInTheDocument();
            expect(screen.getByText('80')).toBeInTheDocument();
            expect(screen.getByText('90')).toBeInTheDocument();
            expect(screen.getByText('88')).toBeInTheDocument();
        });
    });
}); 