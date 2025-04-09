/**
 * Matrix Digital Rain Background
 * A cyberpunk-inspired digital rain effect for the background
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    // Resize handler
    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        initMatrix();
    });

    // Characters to use
    const chars = '01010101神聖な量子01010101ΩΔΠφγλθ';
    const fontSize = 14;
    const columns = Math.floor(width / fontSize);

    // Array to track the current y position of each column
    let drops = [];

    // Initialize the matrix
    function initMatrix() {
        drops = [];
        for (let i = 0; i < columns; i++) {
            drops[i] = Math.floor(Math.random() * -height);
        }
    }

    // Matrix digital rain animation
    function drawMatrix() {
        // Semi-transparent black background to create fade effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, width, height);

        // Set text style
        ctx.fillStyle = '#6b46c1'; // Purple color for matrix
        ctx.font = `${fontSize}px monospace`;

        // Draw characters
        for (let i = 0; i < drops.length; i++) {
            // Random character from the chars string
            const char = chars[Math.floor(Math.random() * chars.length)];

            // Draw the character
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);

            // Move the drop down
            drops[i]++;

            // Reset drop to top with random delay when it reaches bottom
            if (drops[i] * fontSize > height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            // Randomly change colors for some characters
            if (Math.random() > 0.95) {
                ctx.fillStyle = '#8b5cf6'; // Lighter purple
            } else if (Math.random() > 0.95) {
                ctx.fillStyle = '#4f46e5'; // Blue-purple
            } else {
                ctx.fillStyle = '#6b46c1'; // Default purple
            }
        }

        // Call animation frame
        requestAnimationFrame(drawMatrix);
    }

    // Start the matrix
    initMatrix();
    drawMatrix();
}); 