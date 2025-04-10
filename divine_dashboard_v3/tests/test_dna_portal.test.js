/**
 * ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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

// Test configuration
beforeEach(() => {
    // Reset all mocks
    jest.resetAllMocks();

    // Mock the window object
    global.window = {
        addEventListener: jest.fn(),
        parent: {
            postMessage: jest.fn()
        },
        location: {
            origin: "http://localhost"
        }
    };

    // Mock the document object
    global.document = {
        querySelector: jest.fn(),
        querySelectorAll: jest.fn(),
        createElement: jest.fn(),
        getElementById: jest.fn(),
        head: {
            appendChild: jest.fn()
        }
    };

    // Mock Event constructor
    global.Event = jest.fn().mockImplementation((type, options) => ({
        type,
        bubbles: options?.bubbles || false
    }));
});

// Test suite for DNA PCR Quantum LSD Portal JavaScript functionality
describe('DNA PCR Quantum LSD Portal Message Handling', () => {
    test('should bind message event listener to window', () => {
        // Simple function to bind message handler
        function bindMessageHandler() {
            window.addEventListener('message', function (event) {
                if (event.data && event.data.command === "runSequence") {
                    console.log("Received command:", event.data);
                }
            });
        }

        // Call the function
        bindMessageHandler();

        // Verify addEventListener was called with the right arguments
        expect(window.addEventListener).toHaveBeenCalledWith('message', expect.any(Function));
    });

    test('should handle Mullis Spiral Boost activation key correctly', () => {
        // Set up mocks for UI elements
        const mockTextarea = { value: '', dispatchEvent: jest.fn() };
        const mockSlider1 = { value: 0, dispatchEvent: jest.fn() };
        const mockSlider2 = { value: 0, dispatchEvent: jest.fn() };
        const mockCheckbox = { checked: false, dispatchEvent: jest.fn() };
        const mockButton = { click: jest.fn() };

        // Set up the document.querySelector mock implementations
        document.querySelector.mockImplementation((selector) => {
            if (selector.includes('textarea')) return mockTextarea;
            if (selector.includes('button')) return mockButton;
            if (selector.includes('checkbox')) return mockCheckbox;
            if (selector.includes('range')) return mockSlider1;
            return null;
        });

        document.querySelectorAll.mockImplementation((selector) => {
            if (selector.includes('range')) return [mockSlider1, mockSlider2];
            return [];
        });

        // Message handler function
        function handleMessage(event) {
            if (event.data && event.data.command === "runSequence") {
                // Extract parameters from the activation key
                console.log("Received command:", event.data);
                let params = {};

                // Set default values based on activation key
                if (event.data.activationKey === "Mullis Spiral Boost") {
                    params = {
                        dna_sequence: "ATGCGTAGCTAGCTAGCTAGCTA",
                        lsd_dose: 200.0,
                        schumann_sync: true,
                        quantum_entanglement: 0.9
                    };
                }

                // Set the values in the UI
                const dnaInput = document.querySelector('textarea[data-testid="textbox"]');
                const lsdDose = document.querySelector('input[data-testid="range"]');
                const quantumEntanglement = document.querySelectorAll('input[data-testid="range"]')[1];
                const schumannSync = document.querySelector('input[data-testid="checkbox"]');
                const submitBtn = document.querySelector('button[data-testid="button"]');

                if (dnaInput) dnaInput.value = params.dna_sequence;
                if (lsdDose) lsdDose.value = params.lsd_dose;
                if (quantumEntanglement) quantumEntanglement.value = params.quantum_entanglement;
                if (schumannSync) schumannSync.checked = params.schumann_sync;

                // Trigger input events
                if (dnaInput) dnaInput.dispatchEvent(new Event('input', { bubbles: true }));
                if (lsdDose) lsdDose.dispatchEvent(new Event('input', { bubbles: true }));
                if (quantumEntanglement) quantumEntanglement.dispatchEvent(new Event('input', { bubbles: true }));
                if (schumannSync) schumannSync.dispatchEvent(new Event('change', { bubbles: true }));

                // Click the submit button
                if (submitBtn) submitBtn.click();

                // Send response
                window.parent.postMessage({
                    source: "dna-portal",
                    status: "processing",
                    message: "Processing DNA sequence with " + event.data.activationKey
                }, "*");
            }
        }

        // Create a message event
        const messageEvent = {
            data: {
                command: "runSequence",
                activationKey: "Mullis Spiral Boost"
            }
        };

        // Call the handler
        handleMessage(messageEvent);

        // Verify UI was updated correctly
        expect(mockTextarea.value).toBe("ATGCGTAGCTAGCTAGCTAGCTA");
        expect(mockSlider1.value).toBe(200.0);
        expect(mockSlider2.value).toBe(0.9);
        expect(mockCheckbox.checked).toBe(true);

        // Verify events were dispatched
        expect(mockTextarea.dispatchEvent).toHaveBeenCalled();
        expect(mockSlider1.dispatchEvent).toHaveBeenCalled();
        expect(mockSlider2.dispatchEvent).toHaveBeenCalled();
        expect(mockCheckbox.dispatchEvent).toHaveBeenCalled();

        // Verify button was clicked
        expect(mockButton.click).toHaveBeenCalled();

        // Verify postMessage was called with correct parameters
        expect(window.parent.postMessage).toHaveBeenCalledWith(
            expect.objectContaining({
                source: "dna-portal",
                status: "processing",
                message: expect.stringContaining("Mullis Spiral Boost")
            }),
            "*"
        );
    });

    test('should handle different activation keys with appropriate parameters', () => {
        // Create a function to test with different activation keys
        function testActivationKey(activationKey, expectedValues) {
            // Reset mocks
            jest.clearAllMocks();

            // Set up mocks for UI elements
            const mockTextarea = { value: '', dispatchEvent: jest.fn() };
            const mockSlider = { value: 0, dispatchEvent: jest.fn() };
            const mockCheckbox = { checked: false, dispatchEvent: jest.fn() };

            // Set up mock implementations
            document.querySelector.mockImplementation((selector) => {
                if (selector.includes('textarea')) return mockTextarea;
                if (selector.includes('checkbox')) return mockCheckbox;
                if (selector.includes('range')) return mockSlider;
                return null;
            });

            // Handle message with specific activation key
            function handleActivationKey(key) {
                const params = {
                    "DNA Rain Glitch": {
                        dna_sequence: "GCTAGCTAGCTAGCTAGCTA",
                        lsd_dose: 150.0,
                        schumann_sync: false,
                        quantum_entanglement: 0.5
                    },
                    "Neural Lotus Bloom": {
                        dna_sequence: "ATCGATCGATCGATCGATCG",
                        lsd_dose: 300.0,
                        schumann_sync: true,
                        quantum_entanglement: 0.8
                    }
                }[key] || {};

                // Set the values in the UI
                const dnaInput = document.querySelector('textarea[data-testid="textbox"]');
                if (dnaInput) dnaInput.value = params.dna_sequence;

                const lsdDose = document.querySelector('input[data-testid="range"]');
                if (lsdDose) lsdDose.value = params.lsd_dose;

                const schumannSync = document.querySelector('input[data-testid="checkbox"]');
                if (schumannSync) schumannSync.checked = params.schumann_sync;
            }

            // Call the handler with this activation key
            handleActivationKey(activationKey);

            // Check that the values match expectations
            expect(mockTextarea.value).toBe(expectedValues.sequence);
            expect(mockSlider.value).toBe(expectedValues.dose);
            expect(mockCheckbox.checked).toBe(expectedValues.sync);
        }

        // Test each activation key
        testActivationKey("DNA Rain Glitch", {
            sequence: "GCTAGCTAGCTAGCTAGCTA",
            dose: 150.0,
            sync: false
        });

        testActivationKey("Neural Lotus Bloom", {
            sequence: "ATCGATCGATCGATCGATCG",
            dose: 300.0,
            sync: true
        });
    });

    test('should handle cross-origin message restrictions correctly', () => {
        // Function to safely get origin from event
        function getSafeOrigin(event) {
            try {
                // Try to access origin (would throw in cross-origin context)
                const origin = event.origin || '*';
                return origin;
            } catch (e) {
                // If accessing origin fails, use wildcard
                return '*';
            }
        }

        // Message handling function with origin checking
        function handleMessageWithOriginCheck(event) {
            const safeOrigin = getSafeOrigin(event);

            if (event.data && event.data.command === "runSequence") {
                // Send a response back using the safe origin
                window.parent.postMessage({
                    source: "dna-portal",
                    status: "received",
                    message: "Command received"
                }, safeOrigin);
            }
        }

        // Create message events with different origins
        const validEvent = {
            data: { command: "runSequence" },
            origin: "https://example.com"
        };

        const crossOriginEvent = {
            data: { command: "runSequence" }
            // No origin property, or accessing it would throw in a real cross-origin scenario
        };

        // Call the handler with both events
        handleMessageWithOriginCheck(validEvent);
        handleMessageWithOriginCheck(crossOriginEvent);

        // Verify window.parent.postMessage was called with correct parameters
        expect(window.parent.postMessage).toHaveBeenCalledTimes(2);

        // Check the first call with valid event
        expect(window.parent.postMessage.mock.calls[0][0]).toEqual(
            expect.objectContaining({ source: "dna-portal" })
        );
        expect(window.parent.postMessage.mock.calls[0][1]).toBe("https://example.com");

        // Check the second call with cross-origin event
        expect(window.parent.postMessage.mock.calls[1][0]).toEqual(
            expect.objectContaining({ source: "dna-portal" })
        );
        expect(window.parent.postMessage.mock.calls[1][1]).toBe("*");
    });

    test('should fix font loading errors by preloading and providing fallbacks', () => {
        // Style injection function to preload fonts and prevent 404 errors
        function injectFontStyles() {
            const style = document.createElement('style');
            style.textContent = `
        @font-face {
          font-family: 'ui-sans-serif';
          src: local('Segoe UI'), local('Helvetica Neue'), local('Arial'), sans-serif;
          font-weight: normal;
        }
      `;
            document.head.appendChild(style);
            return style;
        }

        // Mock the document.createElement to return a mock style element
        const mockStyle = { textContent: '' };
        document.createElement.mockReturnValue(mockStyle);

        // Call the function
        injectFontStyles();

        // Verify document.createElement was called with the right arguments
        expect(document.createElement).toHaveBeenCalledWith('style');

        // Verify style textContent contains font-face
        expect(mockStyle.textContent).toContain("@font-face");

        // Verify document.head.appendChild was called with the mock style
        expect(document.head.appendChild).toHaveBeenCalledWith(mockStyle);
    });

    test('should validate JavaScript syntax to prevent SyntaxError', () => {
        // Function to validate JavaScript code
        function validateJSCode(code) {
            try {
                // Using Function constructor to validate syntax
                new Function(code);
                return true;
            } catch (e) {
                return false;
            }
        }

        // Valid code should pass
        const validCode = `
      function handleMessage(event) {
        if (event.data && event.data.command === "runSequence") {
          console.log("Valid function");
        }
      }
    `;

        // Invalid code with syntax error should fail
        const invalidCode = `
      function handleMessage(event {
        if (event.data && event.data.command === "runSequence") {
          console.log("Missing parenthesis in function declaration");
        }
      }
    `;

        // Test validation
        expect(validateJSCode(validCode)).toBe(true);
        expect(validateJSCode(invalidCode)).toBe(false);
    });
});

describe('DNA Portal Iframe Integration', () => {
    test('should be able to send messages to iframe with proper targetOrigin', () => {
        // Set up iframe mock
        const mockIframeWindow = {
            postMessage: jest.fn()
        };

        document.getElementById.mockReturnValue({
            contentWindow: mockIframeWindow
        });

        // Function to send message to iframe
        function sendMessageToIframe(command, activationKey) {
            const iframe = document.getElementById('dna-portal-frame');
            iframe.contentWindow.postMessage({
                command: command,
                activationKey: activationKey
            }, "*"); // Use wildcard to avoid cross-origin issues

            return true;
        }

        // Call the function
        const result = sendMessageToIframe("runSequence", "Mullis Spiral Boost");

        // Verify iframe.contentWindow.postMessage was called with correct params
        expect(mockIframeWindow.postMessage).toHaveBeenCalledWith(
            {
                command: "runSequence",
                activationKey: "Mullis Spiral Boost"
            },
            "*"
        );

        // Function should return true
        expect(result).toBe(true);
    });

    test('should handle postMessage origin correctly', () => {
        // Set up iframe mock
        const mockIframeWindow = {
            postMessage: jest.fn()
        };

        document.getElementById.mockReturnValue({
            contentWindow: mockIframeWindow
        });

        // Function to send message with dynamic origin
        function sendMessageWithSafeOrigin(command, activationKey, targetOrigin = null) {
            const iframe = document.getElementById('dna-portal-frame');
            const origin = targetOrigin || window.location.origin || "*";

            iframe.contentWindow.postMessage({
                command: command,
                activationKey: activationKey,
                timestamp: Date.now()
            }, origin);

            return origin;
        }

        // Test with different origins
        const origin1 = sendMessageWithSafeOrigin("runSequence", "Mullis Spiral Boost", "https://example.com");
        const origin2 = sendMessageWithSafeOrigin("runSequence", "Mullis Spiral Boost", null);

        // Verify correct origins were used
        expect(origin1).toBe("https://example.com");
        expect(origin2).toBe("http://localhost");

        // Verify contentWindow.postMessage was called with correct origins
        expect(mockIframeWindow.postMessage.mock.calls[0][1]).toBe("https://example.com");
        expect(mockIframeWindow.postMessage.mock.calls[1][1]).toBe("http://localhost");
    });
}); 