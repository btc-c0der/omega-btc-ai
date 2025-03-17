import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import MetricsOverview from '../MetricsOverview';
import { TrapData } from '../../types';

interface MetricsProps {
    data: TrapData[];
}

const mockData: TrapData[] = [
    {
        id: '1',
        type: 'bullish',
        timestamp: '2024-03-16T01:30:00Z',
        confidence: 0.85,
        price: 100
    },
    {
        id: '2',
        type: 'bearish',
        timestamp: '2024-03-16T02:30:00Z',
        confidence: 0.92,
        price: 110
    },
    {
        id: '3',
        type: 'bullish',
        timestamp: '2024-03-16T03:30:00Z',
        confidence: 0.78,
        price: 105
    }
];

describe('MetricsOverview', () => {
    it('renders without crashing', () => {
        render(<MetricsOverview data={mockData} />);
        expect(screen.getByText('Trap Detection Metrics')).toBeInTheDocument();
    });

    it('displays total trap count', () => {
        render(<MetricsOverview data={mockData} />);
        expect(screen.getByText('Total Traps')).toBeInTheDocument();
        expect(screen.getByText('3')).toBeInTheDocument();
    });

    it('shows trap type distribution', () => {
        render(<MetricsOverview data={mockData} />);
        expect(screen.getByText('Trap Distribution')).toBeInTheDocument();
        const chart = screen.getByTestId('echarts-mock');
        const chartConfig = JSON.parse(chart.textContent || '{}');

        expect(chartConfig.series[0].data).toEqual([
            { value: 2, name: 'bullish' },
            { value: 1, name: 'bearish' }
        ]);
    });

    it('displays average confidence', () => {
        render(<MetricsOverview data={mockData} />);
        expect(screen.getByText('Average Confidence')).toBeInTheDocument();
        expect(screen.getByText('85%')).toBeInTheDocument(); // (0.85 + 0.92 + 0.78) / 3 ≈ 0.85
    });

    it('shows time distribution chart', () => {
        render(<MetricsOverview data={mockData} />);
        expect(screen.getByText('Time Distribution')).toBeInTheDocument();
        const chart = screen.getByTestId('echarts-mock');
        const chartConfig = JSON.parse(chart.textContent || '{}');

        expect(chartConfig.xAxis.type).toBe('time');
        expect(chartConfig.series[0].data).toHaveLength(3);
    });

    it('handles empty data gracefully', () => {
        render(<MetricsOverview data={[]} />);
        expect(screen.getByText('Total Traps')).toBeInTheDocument();
        expect(screen.getByText('0')).toBeInTheDocument();
        expect(screen.getByText('Average Confidence')).toBeInTheDocument();
        expect(screen.getByText('N/A')).toBeInTheDocument();
    });
}); 