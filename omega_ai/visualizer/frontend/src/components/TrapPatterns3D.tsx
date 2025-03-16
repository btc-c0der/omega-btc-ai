import React, { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';
import { Pattern3DData } from '../types/types';

// Mock data for development
const mockPatterns: Pattern3DData[] = Array.from({ length: 50 }, () => ({
    x: Math.random() * 100,  // Price scale
    y: Math.random() * 100,  // Volume scale
    z: Math.random() * 100,  // Time scale
    type: ['FAKE_PUMP', 'FAKE_DUMP', 'LIQUIDITY_GRAB', 'HALF_LIQUIDITY_GRAB'][Math.floor(Math.random() * 4)] as Pattern3DData['type'],
    confidence: 0.5 + Math.random() * 0.5,
}));

const TrapPoint: React.FC<{ pattern: Pattern3DData }> = ({ pattern }) => {
    const meshRef = useRef<THREE.Mesh>(null);

    const color = pattern.type === 'FAKE_PUMP' ? '#ff4d4f' :
        pattern.type === 'FAKE_DUMP' ? '#52c41a' :
            pattern.type === 'LIQUIDITY_GRAB' ? '#1890ff' :
                '#722ed1';

    return (
        <group position={[pattern.x - 50, pattern.y - 50, pattern.z - 50]}>
            <mesh ref={meshRef}>
                <sphereGeometry args={[pattern.confidence * 2, 32, 32]} />
                <meshStandardMaterial
                    color={color}
                    transparent
                    opacity={0.7}
                    roughness={0.3}
                    metalness={0.5}
                />
            </mesh>
            <Text
                position={[0, pattern.confidence * 2 + 1, 0]}
                fontSize={2}
                color={color}
                anchorX="center"
                anchorY="middle"
            >
                {`${pattern.type}\n${Math.round(pattern.confidence * 100)}%`}
            </Text>
        </group>
    );
};

const Grid: React.FC = () => {
    return (
        <group>
            <gridHelper args={[100, 10]} position={[0, -50, 0]} />
            <gridHelper args={[100, 10]} position={[0, 0, -50]} rotation={[Math.PI / 2, 0, 0]} />
            <gridHelper args={[100, 10]} position={[-50, 0, 0]} rotation={[0, 0, Math.PI / 2]} />

            {/* Axes labels */}
            <Text position={[60, -50, 0]} fontSize={5} color="white">
                Price
            </Text>
            <Text position={[-50, 60, 0]} fontSize={5} color="white">
                Volume
            </Text>
            <Text position={[0, -50, 60]} fontSize={5} color="white">
                Time
            </Text>
        </group>
    );
};

const TrapPatterns3D: React.FC = () => {
    return (
        <Canvas
            camera={{ position: [100, 100, 100], fov: 50 }}
            style={{ background: 'transparent' }}
        >
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} intensity={1} />
            <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />

            <Grid />

            {mockPatterns.map((pattern, index) => (
                <TrapPoint key={index} pattern={pattern} />
            ))}

            {/* Add fog for depth perception */}
            <fog attach="fog" args={['#0a1929', 100, 200]} />
        </Canvas>
    );
};

export default TrapPatterns3D; 