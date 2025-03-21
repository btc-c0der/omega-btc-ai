import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrapProbabilityData } from '../types';

interface TrapAlertPanelProps {
    trapData: TrapProbabilityData | null;
}

interface AlertMessage {
    id: string;
    type: string;
    message: string;
    confidence: number;
    timestamp: string;
}

const TrapAlertPanel: React.FC<TrapAlertPanelProps> = ({ trapData }) => {
    const [alerts, setAlerts] = useState<AlertMessage[]>([]);
    const [showingAlert, setShowingAlert] = useState(false);

    // Watch for high-probability traps and create alerts
    useEffect(() => {
        if (trapData && trapData.probability > 0.7 && trapData.trap_type) {
            // Create a new alert
            const newAlert: AlertMessage = {
                id: Date.now().toString(),
                type: trapData.trap_type,
                message: trapData.jah_message || `${trapData.trap_type.toUpperCase()} detected!`,
                confidence: trapData.confidence || 0,
                timestamp: new Date().toISOString()
            };

            // Check if we already have a similar recent alert
            const existingSimilarAlert = alerts.find(
                alert => alert.type === newAlert.type &&
                    new Date(alert.timestamp).getTime() > Date.now() - 60000
            );

            // Only add if no similar alert exists
            if (!existingSimilarAlert) {
                setAlerts(prev => [newAlert, ...prev].slice(0, 10)); // Keep last 10 alerts
                setShowingAlert(true);

                // Auto-hide the flashing alert after 5 seconds
                setTimeout(() => {
                    setShowingAlert(false);
                }, 5000);
            }
        }
    }, [trapData]);

    if (alerts.length === 0) {
        return (
            <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
                <h2 className="text-xl font-display text-reggae-gold mb-2">TRAP ALERTS</h2>
                <div className="text-center p-4 text-reggae-text/50">
                    <p>No trap alerts detected yet</p>
                    <p className="text-xs mt-2">Jah watching over your positions 🙏🏾</p>
                </div>
            </div>
        );
    }

    // Helper for formatting trap types
    const formatTrapType = (type: string) => {
        return type.replace(/_/g, ' ').toUpperCase();
    };

    // Helper for trap type emoji
    const getTrapEmoji = (type: string) => {
        switch (type.toLowerCase()) {
            case 'bull_trap': return '🐂';
            case 'bear_trap': return '🐻';
            case 'liquidity_grab': return '💰';
            case 'stop_hunt': return '🎯';
            case 'fake_pump': return '🚀';
            case 'fake_dump': return '📉';
            default: return '⚠️';
        }
    };

    // Helper for formatting time
    const formatTime = (timestamp: string) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
    };

    return (
        <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
            <h2 className="text-xl font-display text-reggae-gold mb-3">TRAP ALERTS</h2>

            {/* Flashing alert for newest trap */}
            <AnimatePresence>
                {showingAlert && alerts.length > 0 && (
                    <motion.div
                        className="mb-4 p-3 bg-reggae-red/20 rounded-lg border border-reggae-red"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{
                            opacity: [1, 0.7, 1],
                            scale: 1,
                            transition: {
                                opacity: { repeat: Infinity, duration: 1.5 },
                                scale: { duration: 0.3 }
                            }
                        }}
                        exit={{ opacity: 0, scale: 0.9 }}
                    >
                        <div className="flex items-center text-reggae-red mb-1">
                            <span className="text-xl mr-2">{getTrapEmoji(alerts[0].type)}</span>
                            <span className="font-bold">{formatTrapType(alerts[0].type)}</span>
                            <span className="ml-auto text-sm font-mono">
                                {(alerts[0].confidence * 100).toFixed(1)}%
                            </span>
                        </div>
                        <p className="text-reggae-gold font-display">{alerts[0].message}</p>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* List of past alerts */}
            <div className="space-y-2 max-h-60 overflow-y-auto custom-scrollbar">
                {alerts.map((alert) => (
                    <div
                        key={alert.id}
                        className="p-2 bg-reggae-black rounded border border-reggae-gold/10 text-sm"
                    >
                        <div className="flex justify-between items-center">
                            <span className="text-reggae-yellow">
                                {getTrapEmoji(alert.type)} {formatTrapType(alert.type)}
                            </span>
                            <span className="text-xs text-reggae-text/50">{formatTime(alert.timestamp)}</span>
                        </div>
                        <p className="mt-1 text-reggae-text/80 text-xs">{alert.message}</p>
                    </div>
                ))}
            </div>

            {/* Custom scrollbar style */}
            <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1E1E1E;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #FFD700;
          border-radius: 10px;
        }
      `}</style>
        </div>
    );
};

export default TrapAlertPanel; 