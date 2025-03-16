import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import PriceChart from '../PriceChart';
import useDataFeed from '../../hooks/useDataFeed';

// Mock the useDataFeed hook
jest.mock('../../hooks/useDataFeed');
const mockUseDataFeed = useDataFeed as jest.MockedFunction<typeof useDataFeed>;

// Mock ReactECharts since we don't need to test the actual chart rendering
jest.mock('echarts-for-react', () => ({
    __esModule: true,
    default: () => <div data-testid="echarts" />
}));

describe('PriceChart', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('shows loading state', () => {
        mockUseDataFeed.mockReturnValue({
            prices: [],
            traps: [],
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

        render(<PriceChart />);
        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('shows error state', () => {
        const errorMessage = 'Failed to fetch data';
        mockUseDataFeed.mockReturnValue({
            prices: [],
            traps: [],
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

        render(<PriceChart />);
        expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    it('renders chart when data is loaded', () => {
        mockUseDataFeed.mockReturnValue({
            prices: [
                {
                    time: '2024-03-01T10:00:00Z',
                    open: 50000,
                    close: 51000,
                    high: 51500,
                    low: 49800
                }
            ],
            traps: [
                {
                    id: '1',
                    type: 'bullish',
                    timestamp: '2024-03-01T10:00:00Z',
                    confidence: 0.85,
                    price: 50000,
                    volume: 1000,
                    metadata: {}
                }
            ],
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

        render(<PriceChart />);
        expect(screen.getByTestId('echarts')).toBeInTheDocument();
    });
}); 