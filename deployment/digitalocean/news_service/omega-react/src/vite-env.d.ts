/// <reference types="vite/client" />

// React Three Fiber namespace declaration for JSX
declare namespace JSX {
    interface IntrinsicElements {
        // React Three Fiber elements
        group: any;
        mesh: any;
        ambientLight: any;
        pointLight: any;
        spotLight: any;
        directionalLight: any;

        // Geometry elements
        boxGeometry: any;
        sphereGeometry: any;
        planeGeometry: any;
        cylinderGeometry: any;
        coneGeometry: any;
        torusGeometry: any;
        torusKnotGeometry: any;
        textGeometry: any;

        // Material elements
        meshStandardMaterial: any;
        meshPhysicalMaterial: any;
        meshBasicMaterial: any;
        meshLambertMaterial: any;
        meshPhongMaterial: any;
        meshToonMaterial: any;
        meshNormalMaterial: any;

        // Other Three.js elements
        lineBasicMaterial: any;
        lineDashedMaterial: any;
        pointsMaterial: any;
        shadowMaterial: any;
        spriteMaterial: any;
    }
}
