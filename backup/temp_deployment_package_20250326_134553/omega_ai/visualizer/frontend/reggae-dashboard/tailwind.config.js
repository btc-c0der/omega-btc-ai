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

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Reggae Hacker color palette
                'reggae-green': '#00B52D',    // Green (profits/harmony)
                'reggae-gold': '#FFD700',     // Gold (neutral/energy)
                'reggae-red': '#FF3D00',      // Red (danger/SL zones)
                'reggae-black': '#121212',    // Black background
                'reggae-black-light': '#1E1E1E', // Lighter black for panels
                'reggae-electric-blue': '#3D5AFE', // Electric blue for fiber lines
                'reggae-yellow': '#FFDD00',   // Rasta yellow
                'reggae-text': '#E0E0E0',     // Light text
                'reggae-highlight': '#388E3C', // Highlighted text
                'reggae-orange': '#FF9100',   // Orange accent
                'reggae-darkgreen': '#006400', // Dark green for contrast
            },
            fontFamily: {
                'mono': ['Fira Code', 'ui-monospace', 'monospace'],
                'display': ['Orbitron', 'sans-serif'],
                'body': ['Montserrat', 'sans-serif'],
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'reggae-gradient': 'linear-gradient(to right, #00B52D, #FFDD00, #FF3D00)',
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
            },
            keyframes: {
                glow: {
                    '0%': { textShadow: '0 0 5px rgba(255, 215, 0, 0.7)' },
                    '100%': { textShadow: '0 0 20px rgba(255, 215, 0, 1)' },
                }
            },
        },
    },
    plugins: [],
} 