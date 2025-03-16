import React from 'react';
import { Box, Grid, Typography, CircularProgress } from '@mui/material';
import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import useDataFeed from '../hooks/useDataFeed';

const MetricsOverview: React.FC = () => {
    const { metrics, loading, error } = useDataFeed();

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: 'error.main' }}>
                {error}
            </Box>
        );
    }

    const pieChartOption: EChartsOption = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            right: 10,
            top: 'center',
            textStyle: {
                color: '#fff'
            }
        },
        series: [
            {
                name: 'Trap Types',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: metrics.trapsByType.bullish || 0, name: 'Bullish', itemStyle: { color: '#52c41a' } },
                    { value: metrics.trapsByType.bearish || 0, name: 'Bearish', itemStyle: { color: '#ff4d4f' } }
                ]
            }
        ]
    };

    const timelineOption: EChartsOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'category',
            data: Object.keys(metrics.timeDistribution),
            axisLabel: {
                rotate: 45,
                color: '#fff'
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: '#fff'
            }
        },
        series: [
            {
                name: 'Daily Traps',
                type: 'bar',
                data: Object.values(metrics.timeDistribution),
                itemStyle: {
                    color: '#1976d2'
                }
            }
        ]
    };

    return (
        <Box sx={{ p: 2 }}>
            <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                    <Box sx={{ mb: 2, textAlign: 'center' }}>
                        <Typography variant="subtitle2" color="text.secondary">
                            Total Traps
                        </Typography>
                        <Typography variant="h4">
                            {metrics.totalTraps}
                        </Typography>
                    </Box>
                    <Box sx={{ mb: 2, textAlign: 'center' }}>
                        <Typography variant="subtitle2" color="text.secondary">
                            Success Rate
                        </Typography>
                        <Typography variant="h4">
                            {(metrics.successRate * 100).toFixed(1)}%
                        </Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="subtitle2" color="text.secondary">
                            Average Confidence
                        </Typography>
                        <Typography variant="h4">
                            {(metrics.averageConfidence * 100).toFixed(1)}%
                        </Typography>
                    </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                    <ReactECharts option={pieChartOption} style={{ height: '200px' }} theme="dark" />
                </Grid>
                <Grid item xs={12}>
                    <ReactECharts option={timelineOption} style={{ height: '200px' }} theme="dark" />
                </Grid>
            </Grid>
        </Box>
    );
};

export default MetricsOverview; 