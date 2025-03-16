import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { Box } from '@mui/material';
import { TrapData } from '../types/types';

// Mock data for development - will be replaced with real data
const mockData = {
    dates: Array.from({ length: 100 }, (_, i) => new Date(Date.now() - (100 - i) * 86400000).toISOString().split('T')[0]),
    prices: Array.from({ length: 100 }, () => {
        const base = 30000 + Math.random() * 5000;
        return [
            base - Math.random() * 200,  // Open
            base + Math.random() * 200,  // Close
            base - Math.random() * 400,  // Low
            base + Math.random() * 400,  // High
        ];
    }),
    traps: [
        { type: 'FAKE_PUMP', timestamp: new Date(Date.now() - 20 * 86400000).toISOString(), confidence: 0.85 },
        { type: 'LIQUIDITY_GRAB', timestamp: new Date(Date.now() - 40 * 86400000).toISOString(), confidence: 0.92 },
        { type: 'FAKE_DUMP', timestamp: new Date(Date.now() - 60 * 86400000).toISOString(), confidence: 0.78 },
    ],
};

const PriceChart: React.FC = () => {
    const [options, setOptions] = useState({});

    useEffect(() => {
        const trapMarkers = mockData.traps.map(trap => ({
            name: trap.type,
            coord: [
                mockData.dates.indexOf(trap.timestamp.split('T')[0]),
                mockData.prices[mockData.dates.indexOf(trap.timestamp.split('T')[0])][1]
            ],
            value: trap.confidence,
            symbol: trap.type === 'FAKE_PUMP' ? 'triangle' : trap.type === 'FAKE_DUMP' ? 'diamond' : 'circle',
            symbolSize: 20,
            itemStyle: {
                color: trap.type === 'FAKE_PUMP' ? '#ff4d4f' : trap.type === 'FAKE_DUMP' ? '#52c41a' : '#1890ff'
            }
        }));

        const chartOptions = {
            title: {
                text: 'BTC Price & MM Traps',
                left: 'center',
                top: 0,
                textStyle: {
                    color: '#fff'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                },
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 0,
                textStyle: {
                    color: '#fff'
                }
            },
            legend: {
                data: ['Price', 'MA5', 'MA10'],
                top: 30,
                textStyle: {
                    color: '#fff'
                }
            },
            grid: {
                left: '3%',
                right: '3%',
                bottom: '3%',
                top: 100,
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: mockData.dates,
                axisLine: { lineStyle: { color: '#8392A5' } }
            },
            yAxis: {
                type: 'value',
                scale: true,
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                axisLine: { lineStyle: { color: '#8392A5' } }
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    bottom: 10,
                    start: 50,
                    end: 100,
                    textStyle: {
                        color: '#fff'
                    }
                }
            ],
            series: [
                {
                    name: 'Price',
                    type: 'candlestick',
                    data: mockData.prices,
                    itemStyle: {
                        color: '#ff4d4f',
                        color0: '#52c41a',
                        borderColor: '#ff4d4f',
                        borderColor0: '#52c41a'
                    }
                },
                {
                    name: 'Traps',
                    type: 'scatter',
                    data: trapMarkers,
                    symbolSize: 20,
                    label: {
                        show: true,
                        formatter: (params: any) => `${params.name}\n${Math.round(params.value * 100)}%`,
                        position: 'top',
                        textStyle: {
                            color: '#fff'
                        }
                    }
                }
            ]
        };

        setOptions(chartOptions);
    }, []);

    return (
        <Box sx={{ width: '100%', height: '100%' }}>
            <ReactECharts
                option={options}
                style={{ height: '100%', width: '100%' }}
                opts={{ renderer: 'canvas' }}
            />
        </Box>
    );
};

export default PriceChart; 