/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                rasta: {
                    green: '#009B3A',
                    yellow: '#FFDD00',
                    red: '#EF3340',
                    black: '#000000'
                }
            },
            fontFamily: {
                'reggae': ['Reggae One', 'cursive'],
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
} 