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

import { renderHook, act } from '@testing-library/react';
import { fetchTraps, fetchPriceData, fetchMetrics } from '../../services/api';
import { TrapData, PriceData, MetricsData } from '../../types';
import useDataFeed from '../useDataFeed';

// Mock the API functions
jest.mock('../../services/api');
const mockFetchTraps = fetchTraps as jest.MockedFunction<typeof fetchTraps>;
const mockFetchPriceData = fetchPriceData as jest.MockedFunction<typeof fetchPriceData>;
const mockFetchMetrics = fetchMetrics as jest.MockedFunction<typeof fetchMetrics>;

describe('useDataFeed', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    it('initializes with loading state', () => {
        const { result } = renderHook(() => useDataFeed());
        expect(result.current.loading).toBe(true);
        expect(result.current.error).toBeNull();
    });

    it('fetches data successfully', async () => {
        const mockTraps: TrapData[] = [
            {
                id: '1',
                type: 'bullish' as const,
                timestamp: '2024-03-01T10:00:00Z',
                confidence: 0.85,
                price: 50000,
                volume: 1000,
                metadata: {}
            }
        ];

        const mockPrices: PriceData[] = [
            {
                time: '2024-03-01T10:00:00Z',
                open: 50000,
                close: 51000,
                high: 51500,
                low: 49800
            }
        ];

        const mockMetricsData: MetricsData = {
            totalTraps: 1,
            trapsByType: { bullish: 1 },
            averageConfidence: 0.85,
            successRate: 1,
            timeDistribution: { '2024-03-01': 1 }
        };

        mockFetchTraps.mockResolvedValue(mockTraps);
        mockFetchPriceData.mockResolvedValue(mockPrices);
        mockFetchMetrics.mockResolvedValue(mockMetricsData);

        const { result } = renderHook(() => useDataFeed());

        await act(async () => {
            await Promise.resolve();
        });

        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBeNull();
        expect(result.current.traps).toEqual(mockTraps);
        expect(result.current.prices).toEqual(mockPrices);
        expect(result.current.metrics).toEqual(mockMetricsData);
    });

    it('handles fetch errors', async () => {
        const errorMessage = 'Failed to fetch data';
        mockFetchTraps.mockRejectedValue(new Error(errorMessage));

        const { result } = renderHook(() => useDataFeed());

        await act(async () => {
            await Promise.resolve();
        });

        expect(result.current.loading).toBe(false);
        expect(result.current.error).toBe(errorMessage);
    });

    it('polls for new data at the specified interval', async () => {
        mockFetchTraps.mockResolvedValue([]);
        mockFetchPriceData.mockResolvedValue([]);
        mockFetchMetrics.mockResolvedValue({
            totalTraps: 0,
            trapsByType: {},
            averageConfidence: 0,
            successRate: 0,
            timeDistribution: {}
        });

        renderHook(() => useDataFeed());

        expect(mockFetchTraps).toHaveBeenCalledTimes(1);
        expect(mockFetchPriceData).toHaveBeenCalledTimes(1);
        expect(mockFetchMetrics).toHaveBeenCalledTimes(1);

        await act(async () => {
            jest.advanceTimersByTime(30000); // Advance by polling interval
        });

        expect(mockFetchTraps).toHaveBeenCalledTimes(2);
        expect(mockFetchPriceData).toHaveBeenCalledTimes(2);
        expect(mockFetchMetrics).toHaveBeenCalledTimes(2);
    });

    it('cleans up interval on unmount', () => {
        const { unmount } = renderHook(() => useDataFeed());
        const clearIntervalSpy = jest.spyOn(window, 'clearInterval');

        unmount();

        expect(clearIntervalSpy).toHaveBeenCalled();
    });
}); 