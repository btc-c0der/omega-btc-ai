import React from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import ReactECharts from 'echarts-for-react';
import { MetricsData } from '../types/types';

// Mock data for development
const mockMetrics: MetricsData = {
    totalTraps: 157,
    trapsByType: {
        'FAKE_PUMP': 45,
        'FAKE_DUMP': 38,
        'LIQUIDITY_GRAB': 52,
        'HALF_LIQUIDITY_GRAB': 22
    },
    averageConfidence: 0.87,
    timeDistribution: {
        '00-04': 15,
        '04-08': 22,
        '08-12': 45,
        '12-16': 38,
        '16-20': 25,
        '20-24': 12
    },
    successRate: 0.92
};

const MetricCard: React.FC<{ title: string; value: string | number; color: string }> = ({ title, value, color }) => (
    <Paper
        sx={{
            p: 2,
            height: '100%',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center'
        }}
    >
        <Typography variant="h6" color="text.secondary" gutterBottom>
            {title}
        </Typography>
        <Typography variant="h4" color={color}>
            {value}
        </Typography>
    </Paper>
);

const TrapDistributionChart: React.FC<{ data: Record<string, number> }> = ({ data }) => {
    const options = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            textStyle: { color: '#fff' }
        },
        series: [
            {
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '20',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: Object.entries(data).map(([name, value]) => ({
                    name,
                    value,
                    itemStyle: {
                        color: name === 'FAKE_PUMP' ? '#ff4d4f' :
                            name === 'FAKE_DUMP' ? '#52c41a' :
                                name === 'LIQUIDITY_GRAB' ? '#1890ff' :
                                    '#722ed1'
                    }
                }))
            }
        ]
    };

    return (
        <ReactECharts
            option={options}
            style={{ height: '200px', width: '100%' }}
        />
    );
};

const TimeDistributionChart: React.FC<{ data: Record<string, number> }> = ({ data }) => {
    const options = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: Object.keys(data),
            axisLabel: { color: '#fff' }
        },
        yAxis: {
            type: 'value',
            axisLabel: { color: '#fff' }
        },
        series: [
            {
                data: Object.values(data),
                type: 'bar',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#1890ff' },
                        { offset: 1, color: '#722ed1' }
                    ])
                }
            }
        ]
    };

    return (
        <ReactECharts
            option={options}
            style={{ height: '200px', width: '100%' }}
        />
    );
};

const MetricsOverview: React.FC = () => {
    return (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Grid container spacing={2}>
                <Grid item xs={6}>
                    <MetricCard
                        title="Total Traps"
                        value={mockMetrics.totalTraps}
                        color="#1890ff"
                    />
                </Grid>
                <Grid item xs={6}>
                    <MetricCard
                        title="Success Rate"
                        value={`${(mockMetrics.successRate * 100).toFixed(1)}%`}
                        color="#52c41a"
                    />
                </Grid>
                <Grid item xs={12}>
                    <MetricCard
                        title="Average Confidence"
                        value={`${(mockMetrics.averageConfidence * 100).toFixed(1)}%`}
                        color="#722ed1"
                    />
                </Grid>
            </Grid>

            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Trap Distribution
            </Typography>
            <TrapDistributionChart data={mockMetrics.trapsByType} />

            <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Time Distribution (UTC)
            </Typography>
            <TimeDistributionChart data={mockMetrics.timeDistribution} />
        </Box>
    );
};

export default MetricsOverview; 