// CSS modules
declare module '*.css';
declare module '*.scss';
declare module '*.sass';

// Image formats
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.png';
declare module '*.svg';
declare module '*.gif';

// 3D model formats
declare module '*.glb';
declare module '*.gltf';

// React DOM Client
declare module 'react-dom/client' {
    export function createRoot(container: Element | Document | DocumentFragment | null): {
        render(element: React.ReactNode): void;
        unmount(): void;
    };
}

// Three.js JSX types
declare namespace JSX {
    interface IntrinsicElements {
        group: any;
        mesh: any;
        ambientLight: any;
        pointLight: any;
        spotLight: any;
        directionalLight: any;
        primitive: any;
        sphereGeometry: any;
        icosahedronGeometry: any;
        boxGeometry: any;
        cylinderGeometry: any;
        meshStandardMaterial: any;
        meshBasicMaterial: any;
        meshPhongMaterial: any;
        hemisphereLight: any;
    }
} 