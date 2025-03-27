import React from 'react';
import { motion } from 'framer-motion';
import { PositionData } from '../types';

interface PositionTrackerProps {
    positionData: PositionData | null;
}

const PositionTracker: React.FC<PositionTrackerProps> = ({ positionData }) => {
    if (!positionData || !positionData.has_position) {
        return (
            <div className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20">
                <h2 className="text-xl font-display text-reggae-gold mb-2">POSITION TRACKER</h2>
                <div className="text-center p-6">
                    <div className="inline-block rounded-full p-3 bg-reggae-black-light border border-reggae-text/20 mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-reggae-text/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <h3 className="text-lg font-mono text-reggae-text/70">NO ACTIVE POSITION</h3>
                    <p className="text-sm text-reggae-text/50 mt-1">Waiting for entry signal...</p>
                </div>
            </div>
        );
    }

    // Determine if position is in profit or loss
    const isProfit = positionData.pnl_percent && positionData.pnl_percent > 0;
    const pnlColor = isProfit ? 'text-reggae-green' : 'text-reggae-red';
    const pnlIcon = isProfit ? '🔥' : '📉';
    const positionSide = positionData.position_side?.toUpperCase() || 'UNKNOWN';
    const sideColor = positionSide === 'LONG' ? 'text-reggae-green' : 'text-reggae-red';

    // Format currency values
    const formatPrice = (price: number | string | null | undefined) => {
        if (price === null || price === undefined) return '---';
        return parseFloat(price.toString()).toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    // Format percentages
    const formatPercent = (percent: number | string | null | undefined) => {
        if (percent === null || percent === undefined) return '---';
        return `${parseFloat(percent.toString()) > 0 ? '+' : ''}${parseFloat(percent.toString()).toFixed(2)}%`;
    };

    return (
        <motion.div
            className="bg-reggae-black-light p-4 rounded-lg border border-reggae-gold/20"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="flex justify-between items-center mb-3">
                <h2 className="text-xl font-display text-reggae-gold">POSITION TRACKER</h2>
                <div className={`px-3 py-1 rounded-full ${sideColor} bg-reggae-black text-sm font-mono`}>
                    {positionSide}
                </div>
            </div>

            {/* Symbol */}
            <div className="flex items-center justify-center mb-4">
                <span className="text-2xl font-display text-reggae-text">{positionData.symbol || 'BTC/USDT'}</span>
            </div>

            {/* PnL Box */}
            <div className="bg-reggae-black p-3 rounded-lg border border-reggae-gold/10 mb-4">
                <div className="grid grid-cols-2 gap-2">
                    <div className="text-center">
                        <div className="text-sm text-reggae-text/60">PNL %</div>
                        <div className={`font-mono text-2xl font-bold ${pnlColor}`}>
                            {formatPercent(positionData.pnl_percent)}
                        </div>
                    </div>
                    <div className="text-center">
                        <div className="text-sm text-reggae-text/60">PNL $</div>
                        <div className={`font-mono text-2xl font-bold ${pnlColor}`}>
                            ${formatPrice(positionData.pnl_usd)} {pnlIcon}
                        </div>
                    </div>
                </div>
            </div>

            {/* Position Details */}
            <div className="space-y-2">
                {/* Entry Price */}
                <div className="flex justify-between items-center border-b border-reggae-gold/10 pb-2">
                    <span className="text-reggae-text/70">Entry Price</span>
                    <span className="font-mono text-reggae-gold">${formatPrice(positionData.entry_price)}</span>
                </div>

                {/* Current Price */}
                <div className="flex justify-between items-center border-b border-reggae-gold/10 pb-2">
                    <span className="text-reggae-text/70">Current Price</span>
                    <motion.span
                        className="font-mono text-reggae-text"
                        animate={{ color: ['#E0E0E0', '#3D5AFE', '#E0E0E0'] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    >
                        ${formatPrice(positionData.current_price)}
                    </motion.span>
                </div>

                {/* Take Profit */}
                <div className="flex justify-between items-center border-b border-reggae-gold/10 pb-2">
                    <span className="text-reggae-text/70">Take Profit</span>
                    <span className="font-mono text-reggae-green">${formatPrice(positionData.take_profit)}</span>
                </div>

                {/* Stop Loss */}
                <div className="flex justify-between items-center border-b border-reggae-gold/10 pb-2">
                    <span className="text-reggae-text/70">Stop Loss</span>
                    <span className="font-mono text-reggae-red">${formatPrice(positionData.stop_loss)}</span>
                </div>

                {/* Entry Time */}
                <div className="flex justify-between items-center pb-2">
                    <span className="text-reggae-text/70">Entry Time</span>
                    <span className="font-mono text-xs text-reggae-text/60">
                        {positionData.entry_time ? new Date(positionData.entry_time).toLocaleString() : '---'}
                    </span>
                </div>

                {/* Leverage */}
                {positionData.leverage && (
                    <div className="flex justify-between items-center">
                        <span className="text-reggae-text/70">Leverage</span>
                        <span className="font-mono text-reggae-yellow">{positionData.leverage}x</span>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default PositionTracker; 