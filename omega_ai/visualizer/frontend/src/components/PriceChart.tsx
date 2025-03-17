/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable @typescript-eslint/no-redundant-type-constituents */
import React from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { keyframes } from '@emotion/react';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption, TooltipComponentOption } from 'echarts';
import type { TooltipFormatterCallback } from 'echarts/types/dist/shared';
import { useDataFeed } from '../hooks/useDataFeed';
import { PriceData, TrapData } from '../types/data';
import { SxProps, Theme } from '@mui/material/styles';

const scan = keyframes`
  0% { transform: translateY(-100%); opacity: 0.5; }
  100% { transform: translateY(100%); opacity: 0; }
`;

const pulse = keyframes`
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 0.4; }
  100% { transform: scale(1); opacity: 0.8; }
`;

// Note: The 'complex union type' warning from MUI's sx prop typing is a known issue
// and can be safely ignored as it doesn't affect runtime behavior
const containerStyles: SxProps<Theme> = {
    position: 'relative',
    height: '100%',
    overflow: 'hidden',
};

const matrixGridStyles: SxProps<Theme> = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `
        linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px)
    `,
    backgroundSize: '20px 20px',
    pointerEvents: 'none',
};

const createScanningEffectStyles = (theme: Theme): SxProps<Theme> => ({
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '2px',
    background: `linear-gradient(90deg, 
        transparent 0%, 
        ${theme.palette.primary.main} 50%, 
        transparent 100%
    )`,
    animation: `${scan} 3s linear infinite`,
    pointerEvents: 'none',
});

const createStatusOverlayStyles = (theme: Theme): SxProps<Theme> => ({
    position: 'absolute',
    top: 10,
    right: 10,
    padding: '4px 8px',
    backgroundColor: 'rgba(0,0,0,0.5)',
    border: `1px solid ${theme.palette.primary.main}`,
    borderRadius: '2px',
    animation: `${pulse} 2s ease-in-out infinite`,
});

const PriceChart: React.FC = () => {
    const theme = useTheme();
    const { data, isLoading, error } = useDataFeed<PriceData[]>('/api/prices');
    const { data: traps } = useDataFeed<TrapData[]>('/api/traps');

    if (isLoading) return <div>1N1T14L1Z1NG_CH4RT.exe</div>;
    if (error) return <div>3RR0R: {error?.message || 'UNK0WN_3RR0R'}</div>;

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
            type: 'time' as const,
            axisLine: {
                lineStyle: { color: theme.palette.primary.main }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: 'rgba(0, 255, 65, 0.1)',
                    type: 'dashed'
                }
            },
            axisLabel: {
                formatter: (value: number) => {
                    const time = new Date(value);
                    return `T1M3: ${time.getHours()}:${time.getMinutes().toString().padStart(2, '0')}`;
                },
                color: theme.palette.primary.main,
                fontFamily: '"Share Tech Mono", monospace',
            }
        },
        yAxis: {
            type: 'value' as const,
            axisLine: {
                lineStyle: { color: theme.palette.primary.main }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: 'rgba(0, 255, 65, 0.1)',
                    type: 'dashed'
                }
            },
            axisLabel: {
                color: theme.palette.primary.main,
                fontFamily: '"Share Tech Mono", monospace',
                formatter: (value: number) => `$${value.toFixed(0)}`
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
                    borderWidth: 2,
                },
            },
            {
                type: 'scatter',
                data: traps?.map((trap: TrapData) => ({
                    value: [trap.timestamp, trap.price],
                    symbolSize: 20,
                    itemStyle: {
                        color: trap.type === 'bullish'
                            ? theme.palette.success.main
                            : theme.palette.error.main,
                        borderColor: theme.palette.primary.main,
                        borderWidth: 2,
                        shadowBlur: 10,
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
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            borderColor: theme.palette.primary.main,
            textStyle: {
                color: theme.palette.primary.main,
                fontFamily: '"Share Tech Mono", monospace',
            },
            formatter: ((params: unknown) => {
                const paramArray = Array.isArray(params) ? params : [params];
                if (!paramArray[0]?.value) return '';
                const time = new Date(paramArray[0].value[0]);
                return `T1M3: ${time.toLocaleTimeString()}\nPR1C3: $${paramArray[0].value[1]}`;
            }) as TooltipFormatterCallback<EChartsOption['series']>,
        } as TooltipComponentOption,
    };

    return (
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        <Box sx={containerStyles}>
            {/* Matrix grid background */}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <Box sx={matrixGridStyles} />

            {/* Scanning effect */}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <Box sx={createScanningEffectStyles(theme)} />

            <ReactECharts
                option={chartOptions}
                style={{ height: '100%', width: '100%' }}
                theme="dark"
            />

            {/* Status overlay */}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <Box sx={createStatusOverlayStyles(theme)}>
                <Typography
                    sx={{
                        color: theme.palette.primary.main,
                        fontFamily: '"Share Tech Mono", monospace',
                        fontSize: '0.8rem',
                    }}
                >
                    ST4TUS: 0NL1N3
                </Typography>
            </Box>
        </Box>
    );
};

export default PriceChart; 