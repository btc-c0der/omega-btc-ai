/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

import { useState, useEffect } from 'react';

// Define cosmic cycle phases
export type CosmicPhase = 'new' | 'waxing' | 'full' | 'waning';

interface CosmicCycleData {
    phase: CosmicPhase;
    phaseEmoji: string;
    intensity: number; // 0-100
    nextPhaseTime: Date;
    isFavorable: boolean;
    message: string;
}

/**
 * Custom hook that calculates current cosmic cycle based on 
 * various natural rhythms like moon phases, fibonacci sequences, etc.
 * 
 * In a real app, this would use astronomical APIs or calculations
 * For now, it's simplified for demonstration
 */
export const useCosmicCycles = () => {
    const [cycleData, setCycleData] = useState<CosmicCycleData>({
        phase: 'new',
        phaseEmoji: '🌑',
        intensity: 0,
        nextPhaseTime: new Date(),
        isFavorable: false,
        message: 'Calculating cosmic cycles...'
    });

    useEffect(() => {
        // Calculate cosmic cycle based on current date
        const calculateCycle = () => {
            const now = new Date();
            const dayOfYear = Math.floor(
                (now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000
            );

            // Use Fibonacci modulo to determine cycle
            // (simplified version for demo purposes)
            const fibonacciMod = dayOfYear % 8;

            // Current moon phase (simplified)
            let phase: CosmicPhase;
            let phaseEmoji: string;
            let message: string;

            switch (fibonacciMod) {
                case 0:
                case 1:
                    phase = 'new';
                    phaseEmoji = '🌑';
                    message = 'Time for introspection and planning. New beginnings await.';
                    break;
                case 2:
                case 3:
                    phase = 'waxing';
                    phaseEmoji = '🌓';
                    message = 'Growth period. Favorable for building and expansion.';
                    break;
                case 4:
                case 5:
                    phase = 'full';
                    phaseEmoji = '🌕';
                    message = 'Peak energy. Excellent for significant decisions and actions.';
                    break;
                default:
                    phase = 'waning';
                    phaseEmoji = '🌗';
                    message = 'Release phase. Good for reflection and letting go.';
            }

            // Calculate intensity (0-100)
            // Using sine wave based on day of year
            const intensity = Math.abs(Math.sin(dayOfYear / 365 * Math.PI * 2) * 100);

            // Calculate next phase change time
            const nextPhaseHours = 24 - now.getHours() + Math.floor(Math.random() * 12);
            const nextPhaseTime = new Date(now.getTime() + nextPhaseHours * 60 * 60 * 1000);

            // Determine if favorable based on phase and day of week
            // In a real system, this would be more complex
            const isFavorable = (phase === 'waxing' || phase === 'full') && now.getDay() !== 0;

            // Update state
            setCycleData({
                phase,
                phaseEmoji,
                intensity: Math.round(intensity),
                nextPhaseTime,
                isFavorable,
                message
            });
        };

        // Calculate immediately and then every hour
        calculateCycle();
        const intervalId = setInterval(calculateCycle, 60 * 60 * 1000);

        return () => clearInterval(intervalId);
    }, []);

    return cycleData;
};

export default useCosmicCycles; 