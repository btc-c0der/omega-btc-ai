/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable @typescript-eslint/no-redundant-type-constituents */
import React from 'react';
import { Box, Typography, useTheme, CircularProgress } from '@mui/material';
import { keyframes } from '@emotion/react';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption, TooltipComponentOption } from 'echarts';
import type { TooltipFormatterCallback } from 'echarts/types/dist/shared';
import { useDataFeed } from '../hooks/useDataFeed';
import { PriceData, TrapData } from '../types/data';
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
    const { data, isLoading, error } = useDataFeed<PriceData[]>('/api/prices');
    const { data: traps } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) {
        return (
            <Box sx={containerStyles}>
                <Box sx={loadingContainerStyles}>
                    <CircularProgress
                        size={32}
                        thickness={3}
                        sx={{
                            color: theme.palette.primary.main,
                        }}
                    />
                    <Typography
                        variant="body2"
                        sx={{
                            color: 'text.secondary',
                            fontWeight: 500,
                        }}
                    >
                        Loading market data...
                    </Typography>
                </Box>
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={containerStyles}>
                <Box sx={loadingContainerStyles}>
                    <Typography
                        variant="body1"
                        sx={{
                            color: 'error.main',
                            textAlign: 'center',
                            fontWeight: 500,
                        }}
                    >
                        {error?.message || 'Failed to load market data'}
                    </Typography>
                </Box>
            </Box>
        );
    }

    const chartOptions: EChartsOption = {
        backgroundColor: 'transparent',
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            top: '3%',
            containLabel: true,
        },
        xAxis: {
            type: 'time',
            axisLine: {
                lineStyle: { color: theme.palette.divider }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: theme.palette.divider,
                    type: 'dashed'
                }
            },
            axisLabel: {
                formatter: (value: number) => {
                    const time = new Date(value);
                    return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                },
                color: theme.palette.text.secondary,
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                lineStyle: { color: theme.palette.divider }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: theme.palette.divider,
                    type: 'dashed'
                }
            },
            axisLabel: {
                color: theme.palette.text.secondary,
                formatter: (value: number) => `$${value.toLocaleString()}`
            }
        },
        series: [
            {
                type: 'candlestick',
                data: data?.map((item: PriceData) => [
                    item.time,
                    item.open,
                    item.close,
                    item.low,
                    item.high
                ]) || [],
                itemStyle: {
                    color: theme.palette.error.main,
                    color0: theme.palette.success.main,
                    borderColor: theme.palette.error.main,
                    borderColor0: theme.palette.success.main,
                    borderWidth: 1,
                },
            },
            {
                type: 'scatter',
                data: traps?.map((trap: TrapData) => ({
                    value: [trap.timestamp, trap.price],
                    symbolSize: 16,
                    itemStyle: {
                        color: trap.type === 'bullish'
                            ? theme.palette.success.main
                            : theme.palette.error.main,
                        borderColor: theme.palette.background.paper,
                        borderWidth: 2,
                        shadowBlur: 8,
                        shadowColor: trap.type === 'bullish'
                            ? theme.palette.success.main
                            : theme.palette.error.main,
                    }
                })) || [],
            }
        ],
        animation: true,
        tooltip: {
            trigger: 'axis',
            backgroundColor: theme.palette.background.paper,
            borderColor: theme.palette.divider,
            textStyle: {
                color: theme.palette.text.primary,
            },
            formatter: ((params: unknown) => {
                const paramArray = Array.isArray(params) ? params : [params];
                if (!paramArray[0]?.value) return '';
                const time = new Date(paramArray[0].value[0]);
                const price = paramArray[0].value[1];
                return `
                    <div style="padding: 4px 8px;">
                        <div style="margin-bottom: 4px;">${time.toLocaleString()}</div>
                        <div style="font-weight: 500;">$${price.toLocaleString()}</div>
                    </div>
                `;
            }) as TooltipFormatterCallback<EChartsOption['series']>,
        } as TooltipComponentOption,
    };

    return (
        <Box sx={containerStyles}>
            <ReactECharts
                option={chartOptions}
                style={{ height: '100%', width: '100%' }}
                theme="dark"
            />
        </Box>
    );
};

export default PriceChart; 