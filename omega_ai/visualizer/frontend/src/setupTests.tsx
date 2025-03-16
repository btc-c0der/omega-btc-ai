/// <reference types="jest" />
/// <reference types="react" />

import '@testing-library/jest-dom';
import type { Mock } from 'jest-mock';
import React from 'react';

// Extend Jest matchers
declare global {
    namespace jest {
        interface Matchers<R> {
            toBeInTheDocument(): R;
            toHaveStyle(style: Record<string, any>): R;
        }
    }
}

const mockFn = () => {
    const fn = () => { };
    fn.mockImplementation = () => fn;
    fn.mockReturnValue = () => fn;
    return fn;
};

// Mock ECharts
(global as any).jest = {
    mock: (path: string, factory: () => any) => {
        (global as any)[path] = factory();
    }
};

(global as any)['echarts-for-react'] = {
    __esModule: true,
    default: ({ option }: { option: any }) => (
        <div data-testid="echarts-mock">{JSON.stringify(option)}</div>
    )
};

// Mock React Three Fiber
(global as any)['@react-three/fiber'] = {
    Canvas: ({ children }: { children: React.ReactNode }) => (
        <div data-testid="canvas-mock">{children}</div>
    ),
    useFrame: () => mockFn(),
    useThree: () => ({
        camera: {
            position: { set: mockFn() },
            lookAt: mockFn()
        },
        gl: {
            setSize: mockFn()
        }
    })
};

// Mock React Three Drei
(global as any)['@react-three/drei'] = {
    OrbitControls: () => <div data-testid="orbit-controls-mock" />,
    Text: ({ children }: { children: React.ReactNode }) => (
        <div data-testid="drei-text-mock">{children}</div>
    )
};

// Mock Three.js
(global as any)['three'] = {
    Vector3: mockFn(),
    Color: mockFn(),
    Fog: mockFn(),
    MeshStandardMaterial: mockFn(),
    SphereGeometry: mockFn()
}; 