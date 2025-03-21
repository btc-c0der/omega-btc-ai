import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect, beforeEach } from 'vitest';
import TrapAlertPanel from './TrapAlertPanel';

describe('TrapAlertPanel', () => {
    // Test with null data (no alerts)
    it('renders empty state when trap data is null', () => {
        render(<TrapAlertPanel trapData={null} />);

        // Check for empty state message
        expect(screen.getByText('No trap alerts detected yet')).toBeInTheDocument();
        expect(screen.getByText('Jah watching over your positions 🙏🏾')).toBeInTheDocument();
    });

    // Test with low probability trap data (should not create alert)
    it('does not create alerts for low probability traps', () => {
        const lowProbTrapData = {
            probability: 0.4,
            trap_type: 'bull_trap',
            confidence: 0.5,
            trend: 'stable',
            jah_message: 'JAH JAH AWARE! WATCHFUL EYE ON MARKET ENERGY!'
        };

        render(<TrapAlertPanel trapData={lowProbTrapData} />);

        // Should still be in empty state
        expect(screen.getByText('No trap alerts detected yet')).toBeInTheDocument();
    });

    // Test with high probability trap data
    it('creates an alert for high probability traps', async () => {
        // Use high probability trap data
        const highProbTrapData = {
            probability: 0.85,
            trap_type: 'bull_trap',
            confidence: 0.9,
            trend: 'increasing',
            jah_message: 'JAH JAH SAY: BABYLON TRAP! HOLD YOUR FIRE, MASSIVE BULL TRAP!'
        };

        render(<TrapAlertPanel trapData={highProbTrapData} />);

        // Should render the alert with the trap type
        expect(await screen.findByText('BULL TRAP')).toBeInTheDocument();

        // Should render the JAH message
        expect(screen.getByText('JAH JAH SAY: BABYLON TRAP! HOLD YOUR FIRE, MASSIVE BULL TRAP!')).toBeInTheDocument();
    });

    // Test rendering multiple alerts
    it('renders multiple alerts when receiving different trap types', async () => {
        const trapData1 = {
            probability: 0.85,
            trap_type: 'bull_trap',
            confidence: 0.9,
            trend: 'increasing',
            jah_message: 'JAH JAH SAY: BABYLON TRAP! HOLD YOUR FIRE, MASSIVE BULL TRAP!'
        };

        const { rerender } = render(<TrapAlertPanel trapData={trapData1} />);

        // Wait for first alert to appear
        expect(await screen.findByText('BULL TRAP')).toBeInTheDocument();

        // Update with a different trap type
        const trapData2 = {
            probability: 0.9,
            trap_type: 'liquidity_grab',
            confidence: 0.85,
            trend: 'stable',
            jah_message: 'JAH JAH SAY: WATCH YA LIQUIDITY! BABYLON THIEF COMING!'
        };

        // Rerender with new data
        rerender(<TrapAlertPanel trapData={trapData2} />);

        // Should render both alerts (the new one and the older one)
        expect(await screen.findByText('LIQUIDITY GRAB')).toBeInTheDocument();
        expect(screen.getByText('JAH JAH SAY: WATCH YA LIQUIDITY! BABYLON THIEF COMING!')).toBeInTheDocument();

        // The previous alert should still be visible in the history
        expect(screen.getAllByText(/BULL TRAP/i).length).toBeGreaterThan(0);
    });
}); 