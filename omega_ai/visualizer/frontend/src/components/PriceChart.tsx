/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable @typescript-eslint/no-redundant-type-constituents */
import React, { useMemo } from 'react';
import { Box, Typography, useTheme, CircularProgress } from '@mui/material';
import { keyframes } from '@emotion/react';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import { useRealtimePriceData } from '../hooks/useRealtimePriceData';
import { TrapData } from '../types';
import { useDataFeed } from '../hooks/useDataFeed';
import { SxProps, Theme } from '@mui/material/styles';

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const containerStyles: SxProps<Theme> = {
    position: 'relative',
    height: '100%',
    borderRadius: 2,
    overflow: 'hidden',
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
};

const loadingContainerStyles: SxProps<Theme> = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: 2,
    animation: `${fadeIn} 0.3s ease-in-out`,
};

const PriceChart: React.FC = () => {
    const theme = useTheme();
    const { data, error, isConnected } = useRealtimePriceData();
    const { data: traps } = useDataFeed<TrapData[]>('/api/traps');

    const latestPrice = useMemo(() => {
        if (!data || data.length === 0) return null;
        return data[data.length - 1];
    }, [data]);

    const priceChange = useMemo(() => {
        if (!data || data.length < 2) return null;
        const current = data[data.length - 1].close;
        const previous = data[data.length - 2].close;
        const change = ((current - previous) / previous) * 100;
        return {
            value: change,
            isPositive: change >= 0
        };
    }, [data]);

    if (!data || data.length === 0) {
        return (
            <Box sx={containerStyles}>
                <Box sx={loadingContainerStyles}>
                    <CircularProgress size={32} sx={{ color: theme.palette.primary.main }} />
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                        Connecting to market data...
                    </Typography>
                </Box>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={containerStyles}>
                <Box sx={loadingContainerStyles}>
                    <Typography color="error.main">Failed to connect to market data</Typography>
                </Box>
            </Box>
        );
    }

    const chartOptions: EChartsOption = {
        backgroundColor: 'transparent',
        grid: [
            {
                left: '10%',
                right: '10%',
                top: '8%',
                height: '60%'
            },
            {
                left: '10%',
                right: '10%',
                top: '75%',
                height: '15%'
            }
        ],
        axisPointer: {
            link: [{ xAxisIndex: [0, 1] }]
        },
        xAxis: [
            {
                type: 'category',
                data: data?.map(item => item.time) || [],
                axisLine: { lineStyle: { color: '#303030' } },
                axisLabel: { color: '#808080' },
                axisTick: { show: false }
            },
            {
                type: 'category',
                gridIndex: 1,
                data: data?.map(item => item.time) || [],
                axisLine: { lineStyle: { color: '#303030' } },
                axisLabel: { show: false },
                axisTick: { show: false }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                axisLine: { lineStyle: { color: '#303030' } },
                axisLabel: {
                    color: '#808080',
                    formatter: (value: number) => `$${value.toLocaleString()}`
                },
                splitLine: { lineStyle: { color: '#202020' } }
            },
            {
                type: 'value',
                gridIndex: 1,
                axisLine: { show: false },
                axisLabel: { show: false },
                splitLine: { show: false }
            }
        ],
        series: [
            {
                type: 'candlestick',
                data: data?.map(item => [item.open, item.close, item.low, item.high]) || [],
                itemStyle: {
                    color: '#02C076',
                    color0: '#FF3B69',
                    borderColor: '#02C076',
                    borderColor0: '#FF3B69'
                }
            },
            {
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data?.map(item => ({
                    value: Math.abs(item.close - item.open) * 100,
                    itemStyle: {
                        color: item.close >= item.open ? '#02C07644' : '#FF3B6944'
                    }
                })) || [],
            },
            {
                type: 'scatter',
                data: traps?.map((trap: TrapData) => ({
                    value: [trap.timestamp, trap.price],
                    symbolSize: 16,
                    itemStyle: {
                        color: trap.type === 'bullish' ? '#02C076' : '#FF3B69',
                        borderColor: theme.palette.background.paper,
                        borderWidth: 2,
                        shadowBlur: 8,
                        shadowColor: trap.type === 'bullish' ? '#02C07666' : '#FF3B6966',
                    }
                })) || [],
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#404040'
                }
            },
            backgroundColor: 'rgba(28, 34, 48, 0.95)',
            borderColor: '#303030',
            textStyle: { color: '#fff' },
            formatter: (params: any) => {
                const item = params[0];
                if (!item) return '';

                const values = item.data;
                const color = values[1] >= values[0] ? '#02C076' : '#FF3B69';
                const change = ((values[1] - values[0]) / values[0] * 100).toFixed(2);

                return `
                    <div style="padding: 8px;">
                        <div style="margin-bottom: 8px; font-size: 12px; opacity: 0.7;">${item.name}</div>
                        <div style="margin-bottom: 4px;">
                            <span style="color: ${color}">
                                ${change}%
                            </span>
                        </div>
                        <div>O: $${values[0].toLocaleString()}</div>
                        <div>H: $${values[2].toLocaleString()}</div>
                        <div>L: $${values[3].toLocaleString()}</div>
                        <div>C: $${values[1].toLocaleString()}</div>
                    </div>
                `;
            }
        },
        animation: true,
        animationDuration: 300
    };

    return (
        <Box sx={containerStyles}>
            {latestPrice && (
                <Box
                    position="absolute"
                    top={16}
                    left={16}
                    zIndex={1}
                    p={2}
                    bgcolor="rgba(0,0,0,0.4)"
                    borderRadius={1}
                >
                    <Typography variant="h6" color="text.primary">
                        ${latestPrice.close.toLocaleString()}
                    </Typography>
                    {priceChange && (
                        <Typography
                            variant="body2"
                            color={priceChange.isPositive ? 'success.main' : 'error.main'}
                        >
                            {priceChange.isPositive ? '▲' : '▼'} {Math.abs(priceChange.value).toFixed(2)}%
                        </Typography>
                    )}
                </Box>
            )}
            {isConnected === false && (
                <Box
                    position="absolute"
                    top={16}
                    right={16}
                    bgcolor="error.main"
                    color="error.contrastText"
                    px={2}
                    py={0.5}
                    borderRadius={1}
                    zIndex={1}
                >
                    <Typography variant="caption">Reconnecting...</Typography>
                </Box>
            )}
            <ReactECharts
                option={chartOptions}
                style={{ height: '100%', minHeight: 400 }}
                notMerge={true}
            />
        </Box>
    );
};

export default PriceChart; 