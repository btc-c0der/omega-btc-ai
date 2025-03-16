import React from 'react';
import { render, screen } from '@testing-library/react';
import PriceChart from '../PriceChart';

describe('PriceChart', () => {
    const mockData = {
        prices: [
            { time: '2024-03-16T01:00:00Z', open: 100, high: 110, low: 90, close: 105 },
            { time: '2024-03-16T02:00:00Z', open: 105, high: 115, low: 95, close: 110 }
        ],
        traps: [
            {
                id: '1',
                type: 'bullish',
                timestamp: '2024-03-16T01:30:00Z',
                confidence: 0.85,
                price: 100
            }
        ]
    };

    it('renders without crashing', () => {
        render(<PriceChart data={mockData} />);
        expect(screen.getByTestId('echarts-mock')).toBeInTheDocument();
    });

    it('displays correct chart configuration', () => {
        render(<PriceChart data={mockData} />);
        const chartElement = screen.getByTestId('echarts-mock');
        const chartConfig = JSON.parse(chartElement.textContent || '{}');

        expect(chartConfig.title.text).toBe('Price Chart with Trap Indicators');
        expect(chartConfig.series).toHaveLength(2); // Candlestick and scatter series
        expect(chartConfig.series[0].type).toBe('candlestick');
        expect(chartConfig.series[1].type).toBe('scatter');
    });

    it('formats data correctly for chart display', () => {
        render(<PriceChart data={mockData} />);
        const chartElement = screen.getByTestId('echarts-mock');
        const chartConfig = JSON.parse(chartElement.textContent || '{}');

        // Check candlestick data
        expect(chartConfig.series[0].data).toHaveLength(2);
        expect(chartConfig.series[0].data[0]).toEqual([
            '2024-03-16T01:00:00Z',
            100,
            110,
            90,
            105
        ]);

        // Check trap markers
        expect(chartConfig.series[1].data).toHaveLength(1);
        expect(chartConfig.series[1].data[0]).toMatchObject({
            value: [mockData.traps[0].timestamp, mockData.traps[0].price],
            itemStyle: expect.any(Object)
        });
    });

    it('handles empty data gracefully', () => {
        render(<PriceChart data={{ prices: [], traps: [] }} />);
        const chartElement = screen.getByTestId('echarts-mock');
        const chartConfig = JSON.parse(chartElement.textContent || '{}');

        expect(chartConfig.series[0].data).toHaveLength(0);
        expect(chartConfig.series[1].data).toHaveLength(0);
    });
}); 