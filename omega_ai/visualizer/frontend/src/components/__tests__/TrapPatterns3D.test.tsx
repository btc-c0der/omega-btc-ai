import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TrapPatterns3D from '../TrapPatterns3D';
import useDataFeed from '../../hooks/useDataFeed';

// Mock the useDataFeed hook
jest.mock('../../hooks/useDataFeed');
const mockUseDataFeed = useDataFeed as jest.MockedFunction<typeof useDataFeed>;

// Mock @react-three/fiber and @react-three/drei since we don't need to test the actual 3D rendering
jest.mock('@react-three/fiber', () => ({
    Canvas: ({ children }: { children: React.ReactNode }) => <div data-testid="canvas">{children}</div>
}));

jest.mock('@react-three/drei', () => ({
    OrbitControls: () => <div data-testid="orbit-controls" />,
    Text: ({ children }: { children: React.ReactNode }) => <div data-testid="text">{children}</div>
}));

describe('TrapPatterns3D', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('shows loading state', () => {
        mockUseDataFeed.mockReturnValue({
            traps: [],
            prices: [],
            metrics: {
                totalTraps: 0,
                trapsByType: {},
                averageConfidence: 0,
                successRate: 0,
                timeDistribution: {}
            },
            loading: true,
            error: null
        });

        render(<TrapPatterns3D />);
        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('shows error state', () => {
        const errorMessage = 'Failed to fetch data';
        mockUseDataFeed.mockReturnValue({
            traps: [],
            prices: [],
            metrics: {
                totalTraps: 0,
                trapsByType: {},
                averageConfidence: 0,
                successRate: 0,
                timeDistribution: {}
            },
            loading: false,
            error: errorMessage
        });

        render(<TrapPatterns3D />);
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    it('renders 3D visualization when data is loaded', () => {
        mockUseDataFeed.mockReturnValue({
            traps: [
                {
                    id: '1',
                    type: 'bullish' as const,
                    timestamp: '2024-03-01T10:00:00Z',
                    confidence: 0.85,
                    price: 50000,
                    volume: 1000,
                    metadata: {}
                }
            ],
            prices: [],
            metrics: {
                totalTraps: 1,
                trapsByType: { bullish: 1 },
                averageConfidence: 0.85,
                successRate: 1,
                timeDistribution: { '2024-03-01': 1 }
            },
            loading: false,
            error: null
        });

        render(<TrapPatterns3D />);
        expect(screen.getByTestId('canvas')).toBeInTheDocument();
        expect(screen.getByTestId('orbit-controls')).toBeInTheDocument();
        expect(screen.getAllByTestId('text')).toHaveLength(3); // Price, Volume, Time labels
    });
}); 