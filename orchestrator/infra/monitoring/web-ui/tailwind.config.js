/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'rasta': {
                    green: '#00FF00',
                    yellow: '#FFFF00',
                    red: '#FF0000',
                    black: '#000000',
                },
            },
            fontFamily: {
                'divine': ['monospace'],
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
} 