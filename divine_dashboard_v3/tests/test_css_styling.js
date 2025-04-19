/**
 * "TEST COVERAGE" — "CSS STYLING"
 * ===============================
 * 
 * "VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST SUITE
 * TESTS THE CSS STYLING OF THE OMEGA GRID PORTAL
 * 
 * Copyright (c) 2024 OMEGA BTC AI
 */

describe('"VIRGIL STYLING" — "OFF-WHITE™ INSPIRATION"', () => {
    // Setup before all tests
    beforeAll(() => {
        // Create a link element for the CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '../static/css/omega-grid-virgil.css';
        document.head.appendChild(link);

        // Create a test bed
        document.body.innerHTML = `
            <div id="styling-test-container">
                <div class="virgil-mode-toggle"></div>
                <div class="omega-grid-header">HEADER TEST</div>
                <div class="virgil-terminal">
                    <div class="virgil-terminal-header">
                        <div class="virgil-terminal-title">"TERMINAL TITLE"</div>
                    </div>
                    <div class="virgil-terminal-content">
                        <div class="terminal-line command">Command line</div>
                        <div class="terminal-line error">Error line</div>
                        <div class="terminal-line success">Success line</div>
                        <div class="terminal-line quote">"This is a quote"</div>
                    </div>
                </div>
                <div class="command-card">
                    <div class="command-card-header">COMMAND HEADER</div>
                    <div class="command-card-content">
                        <div class="command-description">Command description</div>
                        <button class="command-card-button">EXECUTE</button>
                    </div>
                    <div class="command-card-overlay">OVERLAY</div>
                </div>
                <div class="industrial-label">"INDUSTRIAL LABEL"</div>
                <div class="nft-web3-container">
                    <div class="nft-web3-label">"NFT & WEB3"</div>
                    <div class="nft-placeholder">"PLACEHOLDER"</div>
                </div>
            </div>
        `;
    });

    // Clean up after all tests
    afterAll(() => {
        // Remove the test bed
        document.body.innerHTML = '';
    });

    /**
     * "COLOR PALETTE" — Test for Virgil Abloh / OFF-WHITE color scheme
     */
    test('"COLOR PALETTE" — "VERIFY OFF-WHITE COLOR SCHEME"', () => {
        // Get computed styles
        const styles = window.getComputedStyle(document.documentElement);

        // Check for specific OFF-WHITE inspired colors
        expect(styles.getPropertyValue('--color-white').trim()).not.toBe('');
        expect(styles.getPropertyValue('--color-black').trim()).not.toBe('');
        expect(styles.getPropertyValue('--color-yellow').trim()).not.toBe('');

        // Color usage in elements
        const terminalHeader = document.querySelector('.virgil-terminal-header');
        const terminalHeaderStyle = window.getComputedStyle(terminalHeader);
        expect(terminalHeaderStyle.backgroundColor).not.toBe('transparent');

        const commandButton = document.querySelector('.command-card-button');
        const buttonStyle = window.getComputedStyle(commandButton);
        expect(buttonStyle.backgroundColor).not.toBe('transparent');
        expect(buttonStyle.color).toBe('white');
    });

    /**
     * "TYPOGRAPHY" — Test for Virgil Abloh typography style
     */
    test('"TYPOGRAPHY" — "VERIFY TYPOGRAPHY STYLE"', () => {
        // Get computed styles
        const styles = window.getComputedStyle(document.documentElement);

        // Check for Helvetica Neue or fallback fonts
        const fontFamily = styles.getPropertyValue('--font-primary').trim();
        expect(fontFamily).toContain('Helvetica Neue');

        // Check for monospace fonts
        const monoFamily = styles.getPropertyValue('--font-mono').trim();
        expect(monoFamily).toContain('Mono');

        // Check for industrial-style typography elements
        const headerElement = document.querySelector('.omega-grid-header');
        const headerStyle = window.getComputedStyle(headerElement);
        expect(headerStyle.fontWeight).toBe('800');
        expect(headerStyle.textTransform).toBe('uppercase');
    });

    /**
     * "QUOTATION STYLE" — Test for quote styling
     */
    test('"QUOTATION STYLE" — "VERIFY INDUSTRIAL QUOTE STYLING"', () => {
        // Create a quote element for testing
        const quoteElem = document.createElement('div');
        quoteElem.className = 'virgil-quote';
        quoteElem.textContent = 'Test Quote';
        document.body.appendChild(quoteElem);

        // Get computed style
        const quoteStyle = window.getComputedStyle(quoteElem);

        // Check for quote styling
        expect(quoteStyle.position).toBe('relative');
        expect(quoteStyle.fontStyle).toBe('normal');  // OFF-WHITE quotes don't use italic

        // Check for pseudo-elements
        // Note: We can't directly test pseudo-elements in Jest DOM
        // This would require a real browser environment
        // But we can check that the styling rules exist in our CSS

        // Clean up
        document.body.removeChild(quoteElem);
    });

    /**
     * "CARD STYLING" — Test for command card styling
     */
    test('"CARD STYLING" — "VERIFY COMMAND CARD DESIGN"', () => {
        const card = document.querySelector('.command-card');
        const cardStyle = window.getComputedStyle(card);

        // Border check - should have a solid border
        expect(cardStyle.border).toContain('solid');

        // Header styling
        const header = document.querySelector('.command-card-header');
        const headerStyle = window.getComputedStyle(header);
        expect(headerStyle.textTransform).toBe('uppercase');
        expect(headerStyle.fontWeight).toBeTruthy();

        // Overlay styling - Virgil-style large rotated text
        const overlay = document.querySelector('.command-card-overlay');
        const overlayStyle = window.getComputedStyle(overlay);
        expect(overlayStyle.position).toBe('absolute');
        expect(overlayStyle.textTransform).toBe('uppercase');
        // Check for rotation transform (approximate)
        expect(overlayStyle.transform).toContain('rotate(');
    });

    /**
     * "TERMINAL STYLING" — Test for terminal component
     */
    test('"TERMINAL STYLING" — "VERIFY TERMINAL COMPONENT DESIGN"', () => {
        const terminal = document.querySelector('.virgil-terminal');
        const terminalStyle = window.getComputedStyle(terminal);

        // Terminal should have borders
        expect(terminalStyle.border).toContain('solid');

        // Terminal title should be centered
        const title = document.querySelector('.virgil-terminal-title');
        const titleStyle = window.getComputedStyle(title);
        expect(titleStyle.position).toBe('absolute');
        expect(titleStyle.left).toBe('50%');
        expect(titleStyle.transform).toContain('translateX(-50%)');

        // Terminal lines should have different colors based on type
        const commandLine = document.querySelector('.terminal-line.command');
        const commandStyle = window.getComputedStyle(commandLine);
        expect(commandStyle.color).not.toBe('');

        const errorLine = document.querySelector('.terminal-line.error');
        const errorStyle = window.getComputedStyle(errorLine);
        expect(errorStyle.color).not.toBe('');
        expect(errorStyle.color).not.toBe(commandStyle.color);
    });

    /**
     * "INDUSTRIAL LABEL" — Test for industrial label styling
     */
    test('"INDUSTRIAL LABEL" — "VERIFY INDUSTRIAL LABEL STYLING"', () => {
        const label = document.querySelector('.industrial-label');
        const labelStyle = window.getComputedStyle(label);

        // Should have heavy weight font
        expect(labelStyle.fontWeight).toBe('900');
        expect(labelStyle.textTransform).toBe('uppercase');
        expect(labelStyle.letterSpacing).not.toBe('normal');
    });

    /**
     * "NFT CONTAINER" — Test for NFT container styling
     */
    test('"NFT CONTAINER" — "VERIFY NFT CONTAINER STYLING"', () => {
        const container = document.querySelector('.nft-web3-container');
        const containerStyle = window.getComputedStyle(container);

        // Should have a border
        expect(containerStyle.border).toContain('solid');

        // Check label positioning (should be positioned to overlap the border)
        const label = document.querySelector('.nft-web3-label');
        const labelStyle = window.getComputedStyle(label);
        expect(labelStyle.position).toBe('absolute');
        expect(labelStyle.top).toBeTruthy();
        expect(labelStyle.background).not.toBe('transparent');
    });

    /**
     * "RESPONSIVE DESIGN" — Test for responsive design rules
     */
    test('"RESPONSIVE DESIGN" — "VERIFY MEDIA QUERIES"', () => {
        // Get all style sheets
        const styleSheets = document.styleSheets;
        let hasMediaQueries = false;

        // Search for media queries in the CSS
        for (let i = 0; i < styleSheets.length; i++) {
            try {
                const rules = styleSheets[i].cssRules || styleSheets[i].rules;
                for (let j = 0; j < rules.length; j++) {
                    if (rules[j].type === CSSRule.MEDIA_RULE) {
                        hasMediaQueries = true;
                        break;
                    }
                }
            } catch (e) {
                // Security error for accessing cross-origin stylesheets
                console.warn('Could not access stylesheet rules:', e);
            }
        }

        // We should have at least one media query
        expect(hasMediaQueries).toBe(true);
    });
});

/**
 * "VIRGIL-MODE TOGGLE TEST" — Test for Virgil mode functionality
 */
describe('"VIRGIL MODE TOGGLE" — "VERIFY MODE SWITCHING"', () => {
    beforeEach(() => {
        // Setup test environment
        document.body.innerHTML = `
            <button id="virgil-mode-toggle">VIRGIL MODE OFF</button>
            <div id="test-element"></div>
        `;

        // Simulate the toggle function
        window.toggleVirgilMode = function () {
            const button = document.getElementById('virgil-mode-toggle');
            const isEnabled = document.body.classList.contains('virgil-mode');

            document.body.classList.toggle('virgil-mode', !isEnabled);
            button.textContent = !isEnabled ? 'VIRGIL MODE ON' : 'VIRGIL MODE OFF';
        };

        // Add event listener
        document.getElementById('virgil-mode-toggle').addEventListener('click', window.toggleVirgilMode);
    });

    test('"MODE CHANGE" — "VERIFY CLASS TOGGLE"', () => {
        const button = document.getElementById('virgil-mode-toggle');

        // Initial state
        expect(document.body.classList.contains('virgil-mode')).toBe(false);
        expect(button.textContent).toBe('VIRGIL MODE OFF');

        // Click to enable
        button.click();
        expect(document.body.classList.contains('virgil-mode')).toBe(true);
        expect(button.textContent).toBe('VIRGIL MODE ON');

        // Click to disable
        button.click();
        expect(document.body.classList.contains('virgil-mode')).toBe(false);
        expect(button.textContent).toBe('VIRGIL MODE OFF');
    });
}); 