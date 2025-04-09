/**
 * Matrix Rain Animation
 * Creates a Matrix-style falling code animation in canvas background
 */
document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Set canvas size to window size
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // Resize initially and on window resize
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Characters to display (quantum-themed)
    const quantum = '01߸ψΨΦφΩ∞≈≠≡±√∫∂∑∏πετθλμ⟨⟩ħℏ'.split('');

    // Column positions and speeds
    const drops = [];

    // Initialize drops
    function initDrops() {
        const fontSize = 14;
        const columns = Math.floor(canvas.width / fontSize);

        // Clear existing drops
        drops.length = 0;

        // Create new drops
        for (let i = 0; i < columns; i++) {
            drops.push({
                x: i * fontSize,
                y: Math.random() * canvas.height,
                length: Math.floor(Math.random() * 20) + 5,
                speed: Math.random() * 1.5 + 0.5,
                chars: []
            });
        }
    }

    // Initialize animation
    initDrops();
    window.addEventListener('resize', initDrops);

    // Draw the matrix effect
    function draw() {
        // Create semi-transparent overlay to gradually fade previous frames
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Font settings
        ctx.font = '14px monospace';

        // Draw each drop
        drops.forEach(drop => {
            // Generate a random character for the head of the drop
            const randomChar = quantum[Math.floor(Math.random() * quantum.length)];

            // Add new character to the drop's chars array
            drop.chars.unshift(randomChar);

            // Limit the length of the drop
            if (drop.chars.length > drop.length) {
                drop.chars.pop();
            }

            // Draw each character in the drop
            drop.chars.forEach((char, i) => {
                // Calculate opacity based on position in drop
                const opacity = 1 - (i / drop.length);

                // Calculate green intensity based on position
                const green = Math.floor(200 * opacity) + 50;

                // Set color with a purple/blue tint for quantum effect
                ctx.fillStyle = `rgba(100, ${green}, 255, ${opacity})`;

                // Draw the character
                ctx.fillText(char, drop.x, drop.y - i * 14);
            });

            // Move the drop down
            drop.y += drop.speed;

            // Reset the drop if it goes off screen
            if (drop.y - (drop.chars.length * 14) > canvas.height) {
                drop.y = 0;
                drop.length = Math.floor(Math.random() * 20) + 5;
                drop.speed = Math.random() * 1.5 + 0.5;
                drop.chars = [];
            }
        });

        // Request next animation frame
        requestAnimationFrame(draw);
    }

    // Start the animation
    draw();
}); 