import React from 'react';
import { render, screen } from '@testing-library/react';
import TrapPatterns3D from '../TrapPatterns3D';
import { Pattern3DData } from '../../types/types';

// Mock Three.js and React Three Fiber
jest.mock('@react-three/fiber', () => ({
    Canvas: ({ children }: { children: React.ReactNode }) => (
        <div data-testid="mock-canvas">{children}</div>
    ),
}));

jest.mock('@react-three/drei', () => ({
    OrbitControls: () => <div data-testid="mock-controls" />,
    Text: ({ children }: { children: React.ReactNode }) => (
        <div data-testid="mock-text">{children}</div>
    ),
}));

// Mock test data
const mockPattern: Pattern3DData = {
    x: 50,
    y: 50,
    z: 50,
    type: 'FAKE_PUMP',
    confidence: 0.85,
};

describe('TrapPatterns3D Component', () => {
    it('renders without crashing', () => {
        render(<TrapPatterns3D />);
        expect(screen.getByTestId('mock-canvas')).toBeInTheDocument();
    });

    it('includes orbit controls', () => {
        render(<TrapPatterns3D />);
        expect(screen.getByTestId('mock-controls')).toBeInTheDocument();
    });

    it('renders grid with axis labels', () => {
        render(<TrapPatterns3D />);
        const labels = screen.getAllByTestId('mock-text');
        const labelTexts = labels.map(label => label.textContent);

        expect(labelTexts).toContain('Price');
        expect(labelTexts).toContain('Volume');
        expect(labelTexts).toContain('Time');
    });

    it('sets up correct lighting', () => {
        const { container } = render(<TrapPatterns3D />);

        // Check for ambient and point lights
        expect(container.innerHTML).toContain('ambientLight');
        expect(container.innerHTML).toContain('pointLight');
    });

    it('renders trap points with correct colors', () => {
        const { container } = render(<TrapPatterns3D />);
        const html = container.innerHTML;

        // Check for color assignments
        expect(html).toContain('#ff4d4f'); // FAKE_PUMP color
        expect(html).toContain('#52c41a'); // FAKE_DUMP color
        expect(html).toContain('#1890ff'); // LIQUIDITY_GRAB color
    });

    it('applies fog for depth perception', () => {
        const { container } = render(<TrapPatterns3D />);
        expect(container.innerHTML).toContain('fog');
    });

    it('positions camera correctly', () => {
        render(<TrapPatterns3D />);
        const canvas = screen.getByTestId('mock-canvas');

        expect(canvas.getAttribute('camera-position')).toBe('[100, 100, 100]');
        expect(canvas.getAttribute('camera-fov')).toBe('50');
    });
}); 