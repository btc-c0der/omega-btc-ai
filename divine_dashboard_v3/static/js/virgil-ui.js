/**
 * VIRGIL GRID UI v1.0.0 — Divine JS Framework
 * 
 * "Interactive elements speak the language of truth."
 * OMEGA DESIGN AXIOM 05
 */

(function () {
    'use strict';

    // Initialize all Virgil UI components
    document.addEventListener('DOMContentLoaded', function () {
        initQuoteElements();
        initTerminals();
        initSymbolSequences();
        initStateIndicators();
        initProgressBars();
    });

    /**
     * Initialize quote elements
     * Adds quotation marks to elements with the class 'virgil-quote'
     */
    function initQuoteElements() {
        const quoteElements = document.querySelectorAll('[data-virgil-quote]');

        quoteElements.forEach(el => {
            el.classList.add('virgil-quote');
            // For accessibility, add aria attributes
            el.setAttribute('aria-label', `Quoted concept: ${el.textContent}`);
        });
    }

    /**
     * Initialize terminal elements
     * Adds terminal controls to terminal elements
     */
    function initTerminals() {
        const terminals = document.querySelectorAll('.virgil-terminal:not([data-initialized])');

        terminals.forEach(terminal => {
            // Only add controls if they don't already exist
            if (!terminal.querySelector('.virgil-terminal-header')) {
                // Create terminal header
                const header = document.createElement('div');
                header.className = 'virgil-terminal-header';

                // Create control buttons
                const controls = document.createElement('div');
                controls.className = 'virgil-terminal-controls';

                for (let i = 0; i < 3; i++) {
                    const btn = document.createElement('span');
                    btn.className = 'virgil-terminal-btn';
                    controls.appendChild(btn);
                }

                // Create title if specified
                if (terminal.dataset.title) {
                    const title = document.createElement('div');
                    title.className = 'virgil-terminal-title';
                    title.textContent = terminal.dataset.title;
                    header.appendChild(title);
                }

                header.appendChild(controls);

                // Add header to terminal
                if (terminal.firstChild) {
                    terminal.insertBefore(header, terminal.firstChild);
                } else {
                    terminal.appendChild(header);
                }
            }

            // Mark as initialized
            terminal.setAttribute('data-initialized', 'true');
        });
    }

    /**
     * Initialize symbol sequences
     * Adds styling to symbol sequences
     */
    function initSymbolSequences() {
        const sequences = document.querySelectorAll('[data-symbol-sequence]');

        sequences.forEach(sequence => {
            sequence.classList.add('symbol-sequence');

            const level = sequence.dataset.level || '1';
            sequence.classList.add(`level-${level}`);

            // Apply sacred symbol class to children
            const symbols = sequence.querySelectorAll('[data-symbol]');
            symbols.forEach(symbol => {
                symbol.classList.add('sacred-symbol');
                if (symbol.dataset.symbol) {
                    symbol.classList.add(symbol.dataset.symbol);
                }
            });
        });
    }

    /**
     * Initialize state indicators
     * Adds styling to state indicators
     */
    function initStateIndicators() {
        const indicators = document.querySelectorAll('[data-state]');

        indicators.forEach(indicator => {
            indicator.classList.add('virgil-state-indicator');

            const state = indicator.dataset.state;
            if (state) {
                indicator.classList.add(state);
            }
        });
    }

    /**
     * Initialize progress bars
     * Updates progress bars based on data attributes
     */
    function initProgressBars() {
        const progressBars = document.querySelectorAll('[data-progress]');

        progressBars.forEach(container => {
            const value = container.dataset.progress || '0';
            const labelText = container.dataset.label || 'PROCESSING';

            // Create structure if it doesn't exist
            if (!container.querySelector('.virgil-progress-bar')) {
                // Create label
                const label = document.createElement('div');
                label.className = 'virgil-progress-label';
                label.textContent = labelText;

                // Create progress bar
                const bar = document.createElement('div');
                bar.className = 'virgil-progress-bar';

                // Create fill element
                const fill = document.createElement('div');
                fill.className = 'virgil-progress-fill';
                fill.style.width = `${value}%`;
                bar.appendChild(fill);

                // Create value display
                const valueDisplay = document.createElement('div');
                valueDisplay.className = 'virgil-progress-value';
                valueDisplay.textContent = `${value}%`;

                // Add everything to container
                container.appendChild(label);
                container.appendChild(bar);
                container.appendChild(valueDisplay);

                // Add virgil-progress class
                container.classList.add('virgil-progress');
            } else {
                // Just update existing progress bar
                const fill = container.querySelector('.virgil-progress-fill');
                if (fill) {
                    fill.style.width = `${value}%`;
                }

                const valueDisplay = container.querySelector('.virgil-progress-value');
                if (valueDisplay) {
                    valueDisplay.textContent = `${value}%`;
                }
            }
        });
    }

    // Export to global scope for use in other scripts
    window.VIRGIL = {
        // Helper to create sacred symbol elements
        createSymbol: function (type, text) {
            const symbol = document.createElement('span');
            symbol.classList.add('sacred-symbol', type);
            symbol.textContent = text;
            return symbol;
        },

        // Helper to create symbol sequences
        createSequence: function (type, count, level = count) {
            const sequence = document.createElement('div');
            sequence.classList.add('symbol-sequence', `level-${level}`);

            const symbols = {
                delta: '∆',
                infinity: '∞',
                lightning: '⚡',
                circle: '◯',
                trident: '🔱',
                star: '✧',
                gear: '⚙️'
            };

            const symbolText = symbols[type] || '∆';

            for (let i = 0; i < count; i++) {
                const symbol = this.createSymbol(type, symbolText);
                sequence.appendChild(symbol);
            }

            return sequence;
        },

        // Helper to update progress bars
        updateProgress: function (selector, value) {
            const progressBar = document.querySelector(selector);
            if (progressBar) {
                progressBar.dataset.progress = value;
                initProgressBars(); // Reinitialize to update the bar
            }
        }
    };
})(); 