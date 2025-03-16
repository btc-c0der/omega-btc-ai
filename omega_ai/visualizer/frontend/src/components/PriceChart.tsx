import React from 'react';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import { Box, CircularProgress } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import useDataFeed from '../hooks/useDataFeed';

const loadingStyles: SxProps<Theme> = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%'
};

const errorStyles: SxProps<Theme> = {
    ...loadingStyles,
    color: 'error.main'
};

const PriceChart: React.FC = () => {
    const { prices, traps, loading, error } = useDataFeed();

    if (loading) {
        return (
            <Box sx={loadingStyles}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={errorStyles}>
                {error}
            </Box>
        );
    }

    const option: EChartsOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['Price', 'Traps'],
            textStyle: {
                color: '#fff'
            }
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'time',
            splitLine: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                bottom: 60,
                start: 0,
                end: 100
            }
        ],
        series: [
            {
                name: 'Price',
                type: 'candlestick',
                data: prices.map(p => [
                    p.time,
                    p.open,
                    p.close,
                    p.low,
                    p.high
                ])
            },
            {
                name: 'Traps',
                type: 'scatter',
                data: traps.map(trap => ({
                    value: [trap.timestamp, trap.price],
                    itemStyle: {
                        color: trap.type === 'bullish' ? '#52c41a' : '#ff4d4f'
                    },
                    symbolSize: trap.confidence * 20,
                    tooltip: {
                        formatter: () =>
                            `${trap.type.toUpperCase()}<br/>` +
                            `Price: $${trap.price.toLocaleString()}<br/>` +
                            `Confidence: ${(trap.confidence * 100).toFixed(1)}%`
                    }
                }))
            }
        ]
    };

    return (
        <ReactECharts
            option={option}
            style={{ height: '100%', minHeight: '300px' }}
            theme="dark"
        />
    );
};

export default PriceChart; 