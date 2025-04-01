import React, { useEffect, useState } from 'react';
import { useMatrixWebSocket } from '../hooks/useMatrixWebSocket';
import { useTheme } from '../context/ThemeContext';
import { MatrixPanel } from './MatrixPanel';
import { FunkoCharacter } from './FunkoCharacter';
import { MatrixRain } from './MatrixRain';
import { AlertBanner } from './AlertBanner';
import '../styles/MatrixFunkoDashboard.css';

interface MatrixMetrics {
    testRate: number;
    testFailures: number;
    redisCommands: number;
    marketTrends: number;
    serviceHealth: number;
    testCoverage: number;
}

export const MatrixFunkoDashboard: React.FC = () => {
    const { connected, data } = useMatrixWebSocket();
    const { theme, toggleTheme } = useTheme();
    const [metrics, setMetrics] = useState<MatrixMetrics>({
        testRate: 0,
        testFailures: 0,
        redisCommands: 0,
        marketTrends: 0,
        serviceHealth: 0,
        testCoverage: 0
    });

    useEffect(() => {
        if (connected && data) {
            setMetrics(data);
        }
    }, [connected, data]);

    const isOptimalHealth = metrics.serviceHealth > 90 && metrics.testCoverage > 85;

    return (
        <div className={`matrix-funko-dashboard ${theme}`}>
            <MatrixRain />

            <header className="dashboard-header">
                <h1>🔱 OMEGA BTC AI - DIVINE MATRIX FUNKO DASHBOARD 🔱</h1>
                <button onClick={toggleTheme} className="theme-toggle">
                    {theme === 'dark' ? '☀️' : '🌙'}
                </button>
            </header>

            {metrics.serviceHealth < 50 && (
                <AlertBanner
                    message="⚠️ Service Health Alert: System requires immediate attention"
                    severity="critical"
                />
            )}

            <div className="dashboard-grid">
                <MatrixPanel
                    title="🔱 Divine Test Rate"
                    value={metrics.testRate}
                    unit="tests/min"
                    trend={metrics.testRate > 100 ? 'up' : 'down'}
                />

                <MatrixPanel
                    title="💫 Divine Test Failures"
                    value={metrics.testFailures}
                    unit="failures"
                    trend={metrics.testFailures > 0 ? 'up' : 'down'}
                />

                <MatrixPanel
                    title="🌟 Divine Redis Commands"
                    value={metrics.redisCommands}
                    unit="cmds/sec"
                    trend="up"
                />

                <MatrixPanel
                    title="✨ Divine Market Trends"
                    value={metrics.marketTrends}
                    unit="%"
                    trend={metrics.marketTrends > 70 ? 'up' : 'down'}
                />

                <MatrixPanel
                    title="🌌 Divine Service Health"
                    value={metrics.serviceHealth}
                    unit="%"
                    trend={metrics.serviceHealth > 90 ? 'up' : 'down'}
                />

                <MatrixPanel
                    title="🌠 Divine Test Coverage"
                    value={metrics.testCoverage}
                    unit="%"
                    trend={metrics.testCoverage > 85 ? 'up' : 'down'}
                />
            </div>

            {isOptimalHealth && (
                <div className="funko-container" data-testid="funko-character">
                    <FunkoCharacter />
                </div>
            )}

            <footer className="dashboard-footer">
                <p>Connected: {connected ? '✅' : '❌'}</p>
                <p>Last Updated: {new Date().toLocaleTimeString()}</p>
            </footer>
        </div>
    );
}; 