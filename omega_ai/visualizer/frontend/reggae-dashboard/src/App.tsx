import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import WebSocketComponent from './components/WebSocketComponent';
import PositionTracker from './components/PositionTracker';
import TrapProbabilityMeter from './components/TrapProbabilityMeter';
import CandlestickChart from './components/CandlestickChart';
import TrapAlertPanel from './components/TrapAlertPanel';
import RedisFeedMonitor from './components/RedisFeedMonitor';
import HaileSalassieQuote from './components/HaileSalassieQuote';
import { TrapProbabilityData, PositionData } from './types';

const App: React.FC = () => {
    const [trapData, setTrapData] = useState<TrapProbabilityData | null>(null);
    const [positionData, setPositionData] = useState<PositionData | null>(null);
    const [connected, setConnected] = useState(false);

    // Handle WebSocket data updates
    const handleWebSocketData = (data: any) => {
        if (data.trap_probability) {
            setTrapData(data.trap_probability);
        }
        if (data.position) {
            setPositionData(data.position);
        }
    };

    return (
        <div className="min-h-screen bg-reggae-black text-reggae-text font-body">
            {/* Header */}
            <header className="bg-reggae-black-light p-4 border-b border-reggae-gold/30">
                <div className="container mx-auto flex justify-between items-center">
                    <motion.h1
                        className="text-3xl font-display text-reggae-gold animate-glow"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 1.5 }}
                    >
                        OMEGA BTC AI 🔱 REGGAE DASHBOARD
                    </motion.h1>
                    <div className="flex items-center space-x-4">
                        <div className={`h-3 w-3 rounded-full ${connected ? 'bg-reggae-green' : 'bg-reggae-red'}`}></div>
                        <span className="text-sm">{connected ? 'Connected' : 'Disconnected'}</span>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto p-4 grid grid-cols-12 gap-4">
                {/* Left Column - Position and Trap Probability */}
                <div className="col-span-12 lg:col-span-4 space-y-4">
                    <PositionTracker positionData={positionData} />
                    <TrapProbabilityMeter trapData={trapData} />
                    <TrapAlertPanel trapData={trapData} />
                </div>

                {/* Center Column - Charts */}
                <div className="col-span-12 lg:col-span-5 space-y-4">
                    <CandlestickChart positionData={positionData} />
                </div>

                {/* Right Column - Redis Monitor */}
                <div className="col-span-12 lg:col-span-3 space-y-4">
                    <RedisFeedMonitor />
                </div>
            </main>

            {/* Footer Quote */}
            <footer className="mt-8 p-4 bg-reggae-black-light border-t border-reggae-gold/30">
                <div className="container mx-auto">
                    <HaileSalassieQuote />
                </div>
            </footer>

            {/* WebSocket Connection (hidden) */}
            <WebSocketComponent
                onData={handleWebSocketData}
                onConnectionChange={setConnected}
            />
        </div>
    );
}

export default App; 