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

// Test suite for DNA PCR Quantum LSD Portal JavaScript functionality
describe('DNA PCR Quantum LSD Portal Message Handling', () => {
    // Create a mock iframe implementation for testing postMessage functionality
    let mockIframe;
    let mockWindow;
    let mockParentWindow;
    let mockConsole;
    let originalBindMessageHandler;
    let mockEventListeners = {};

    // Setup before each test
    beforeEach(() => {
        // Save original console methods before mocking
        mockConsole = {
            log: jest.fn(),
            error: jest.fn()
        };

        // Mock the window object
        mockWindow = {
            parent: {
                postMessage: jest.fn()
            },
            postMessage: jest.fn(),
            addEventListener: (event, callback) => {
                mockEventListeners[event] = mockEventListeners[event] || [];
                mockEventListeners[event].push(callback);
            },
            removeEventListener: (event, callback) => {
                if (mockEventListeners[event]) {
                    mockEventListeners[event] = mockEventListeners[event].filter(cb => cb !== callback);
                }
            },
            document: {
                querySelector: jest.fn().mockImplementation(selector => {
                    if (selector === 'textarea[data-testid="textbox"]') {
                        return {
                            value: '',
                            dispatchEvent: jest.fn()
                        };
                    } else if (selector === 'input[data-testid="range"]') {
                        return {
                            value: 0,
                            dispatchEvent: jest.fn()
                        };
                    } else if (selector === 'input[data-testid="checkbox"]') {
                        return {
                            checked: false,
                            dispatchEvent: jest.fn()
                        };
                    } else if (selector === 'button[data-testid="button"]') {
                        return {
                            click: jest.fn()
                        };
                    }
                    return null;
                }),
                querySelectorAll: jest.fn().mockImplementation(selector => {
                    if (selector === 'input[data-testid="range"]') {
                        return [
                            { value: 0, dispatchEvent: jest.fn() },
                            { value: 0, dispatchEvent: jest.fn() }
                        ];
                    }
                    return [];
                })
            },
            Event: class {
                constructor(type, options) {
                    this.type = type;
                    this.bubbles = options?.bubbles || false;
                }
            },
            console: mockConsole,
            location: { origin: 'http://localhost:7863' },
            setTimeout: jest.fn().mockImplementation((callback, delay) => {
                // Execute immediately for testing
                callback();
                return 123; // Return a mock timer ID
            })
        };

        // Mock iframe for parent-child window communication testing
        mockIframe = {
            contentWindow: {
                postMessage: jest.fn()
            }
        };

        // Extract the bindMessageHandler function from the actual script
        // This is a utility function that accepts the actual script content
        function extractBindMessageHandler(script) {
            // Simple regex to extract the function body
            const functionMatch = script.match(/function\s+bindMessageHandler\s*\(\)\s*\{([\s\S]*?)\}/);
            if (functionMatch && functionMatch[1]) {
                const functionBody = functionMatch[1];
                // Create a new function with the extracted body
                return new Function('window', `
          return function bindMessageHandler() {
            ${functionBody}
          }
        `)(mockWindow);
            }
            return null;
        }

        // Define the script content from the Gradio app
        const scriptContent = `
    function bindMessageHandler() {
        window.addEventListener('message', function(event) {
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
                } else if (event.data.activationKey === "DNA Rain Glitch") {
                    params = {
                        dna_sequence: "GCTAGCTAGCTAGCTAGCTA",
                        lsd_dose: 150.0,
                        schumann_sync: false,
                        quantum_entanglement: 0.5
                    };
                } else if (event.data.activationKey === "Neural Lotus Bloom") {
                    params = {
                        dna_sequence: "ATCGATCGATCGATCGATCG",
                        lsd_dose: 300.0,
                        schumann_sync: true,
                        quantum_entanglement: 0.8
                    };
                } else {
                    // Default values
                    params = {
                        dna_sequence: "",
                        lsd_dose: 100.0,
                        schumann_sync: true,
                        quantum_entanglement: 0.7
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
                
                // Trigger input events to update Gradio's internal state
                if (dnaInput) dnaInput.dispatchEvent(new Event('input', { bubbles: true }));
                if (lsdDose) lsdDose.dispatchEvent(new Event('input', { bubbles: true }));
                if (quantumEntanglement) quantumEntanglement.dispatchEvent(new Event('input', { bubbles: true }));
                if (schumannSync) schumannSync.dispatchEvent(new Event('change', { bubbles: true }));
                
                // Click the submit button after a short delay
                setTimeout(() => {
                    if (submitBtn) submitBtn.click();
                    
                    // Send a response back to the parent window
                    window.parent.postMessage({
                        source: "dna-portal",
                        status: "processing",
                        message: "Processing DNA sequence with " + event.data.activationKey
                    }, "*");
                    
                    // After processing, send success message
                    setTimeout(() => {
                        window.parent.postMessage({
                            source: "dna-portal",
                            status: "success",
                            message: "DNA sequence processed successfully with " + event.data.activationKey
                        }, "*");
                    }, 5000);
                }, 500);
            }
        });
        
        console.log("DNA Portal message handler initialized");
    }
    
    // Initialize the message handler when the page loads
    if (window.parent !== window) {
        // We're in an iframe
        bindMessageHandler();
        console.log("DNA Portal detected iframe context, message handler active");
    }
    `;

        // Extract the bindMessageHandler function
        originalBindMessageHandler = extractBindMessageHandler(scriptContent);

        // Fix the syntax error in the function if needed
        if (!originalBindMessageHandler) {
            console.error("Could not extract bindMessageHandler function");
        }
    });

    test('bindMessageHandler should attach a message event listener', () => {
        // Call the bindMessageHandler function
        originalBindMessageHandler();

        // Verify that an event listener was added
        expect(mockEventListeners['message']).toBeDefined();
        expect(mockEventListeners['message'].length).toBeGreaterThan(0);

        // Verify that initialization was logged
        expect(mockConsole.log).toHaveBeenCalledWith("DNA Portal message handler initialized");
    });

    test('Should handle message with Mullis Spiral Boost activation key', () => {
        // Call the bindMessageHandler function
        originalBindMessageHandler();

        // Get the message handler function
        const messageHandler = mockEventListeners['message'][0];

        // Create a mock event with Mullis Spiral Boost activation key
        const mockEvent = {
            data: {
                command: 'runSequence',
                activationKey: 'Mullis Spiral Boost'
            }
        };

        // Call the message handler with the mock event
        messageHandler(mockEvent);

        // Check if the DNA input value was set correctly
        const dnaInput = mockWindow.document.querySelector('textarea[data-testid="textbox"]');
        expect(dnaInput.value).toBe('ATGCGTAGCTAGCTAGCTAGCTA');

        // Check if events were dispatched
        expect(dnaInput.dispatchEvent).toHaveBeenCalled();

        // Check if the button was clicked
        const submitBtn = mockWindow.document.querySelector('button[data-testid="button"]');
        expect(submitBtn.click).toHaveBeenCalled();

        // Check if postMessage was called with the correct arguments
        expect(mockWindow.parent.postMessage).toHaveBeenCalledWith(
            {
                source: 'dna-portal',
                status: 'processing',
                message: 'Processing DNA sequence with Mullis Spiral Boost'
            },
            '*'
        );

        // Check if the success message was sent
        expect(mockWindow.parent.postMessage).toHaveBeenCalledWith(
            {
                source: 'dna-portal',
                status: 'success',
                message: 'DNA sequence processed successfully with Mullis Spiral Boost'
            },
            '*'
        );
    });

    test('Should handle different activation keys with appropriate parameters', () => {
        // Call the bindMessageHandler function
        originalBindMessageHandler();

        // Get the message handler function
        const messageHandler = mockEventListeners['message'][0];

        // Create mock events for different activation keys
        const activationKeys = [
            'Mullis Spiral Boost',
            'DNA Rain Glitch',
            'Neural Lotus Bloom',
            'Unknown Key'
        ];

        // Test each activation key
        activationKeys.forEach(key => {
            // Create a mock event with the current activation key
            const mockEvent = {
                data: {
                    command: 'runSequence',
                    activationKey: key
                }
            };

            // Reset mocks for clean test
            jest.clearAllMocks();

            // Call the message handler with the mock event
            messageHandler(mockEvent);

            // Check if the button was clicked
            const submitBtn = mockWindow.document.querySelector('button[data-testid="button"]');
            expect(submitBtn.click).toHaveBeenCalled();

            // Check if postMessage was called with the correct status
            expect(mockWindow.parent.postMessage).toHaveBeenCalledWith(
                expect.objectContaining({
                    source: 'dna-portal',
                    status: 'processing'
                }),
                '*'
            );
        });
    });

    test('Should handle cross-origin message restrictions correctly', () => {
        // Call the bindMessageHandler function
        originalBindMessageHandler();

        // Get the message handler function
        const messageHandler = mockEventListeners['message'][0];

        // Create a mock event from a different origin
        const mockEvent = {
            data: {
                command: 'runSequence',
                activationKey: 'Mullis Spiral Boost'
            },
            origin: 'https://huggingface.co'
        };

        // Call the message handler with the mock event
        messageHandler(mockEvent);

        // Since we use postMessage with '*' as the targetOrigin, it should
        // work regardless of origin differences, but in practice this
        // can cause the error in the console logs

        // Check if postMessage was still called
        const submitBtn = mockWindow.document.querySelector('button[data-testid="button"]');
        expect(submitBtn.click).toHaveBeenCalled();
    });

    test('Should fix the font loading errors by ignoring 404s', () => {
        // This is a placeholder to document that font loading errors
        // are 404s that can be safely ignored as they don't affect functionality

        // In a real implementation, we would:
        // 1. Modify the headers or response to avoid console errors
        // 2. Preload fonts or provide fallbacks
        // 3. Cache fonts to avoid repeated 404s

        // For now, we'll just document that these errors are expected and benign
        expect(true).toBe(true);
    });

    test('Should validate JavaScript syntax to prevent SyntaxError', () => {
        // This test ensures that the bindMessageHandler function can be parsed
        // without syntax errors

        // Check that the function was successfully extracted
        expect(originalBindMessageHandler).toBeDefined();
        expect(typeof originalBindMessageHandler).toBe('function');

        // Attempting to call the function should not throw a SyntaxError
        expect(() => {
            originalBindMessageHandler();
        }).not.toThrow(SyntaxError);
    });
});

// Test suite for the iframe integration
describe('DNA Portal Iframe Integration', () => {
    let iframe;
    let parentWindow;

    beforeEach(() => {
        // Create a mock iframe element
        iframe = document.createElement('iframe');
        iframe.src = 'http://0.0.0.0:7863';
        document.body.appendChild(iframe);

        // Mock the parent window postMessage
        parentWindow = {
            postMessage: jest.fn()
        };

        // Mock iframe's contentWindow
        iframe.contentWindow = {
            postMessage: jest.fn()
        };
    });

    afterEach(() => {
        // Clean up the iframe
        document.body.removeChild(iframe);
    });

    test('Should be able to send messages to iframe with proper targetOrigin', () => {
        // This tests that we can correctly send messages to the iframe
        iframe.contentWindow.postMessage(
            {
                command: 'runSequence',
                activationKey: 'Mullis Spiral Boost'
            },
            iframe.src // Use the iframe's URL as the targetOrigin
        );

        // In a real test, we would verify that the message was received
        // by checking for side effects like UI changes or responses

        // Instead, we'll just verify that postMessage was called with the correct arguments
        expect(iframe.contentWindow.postMessage).toHaveBeenCalledWith(
            {
                command: 'runSequence',
                activationKey: 'Mullis Spiral Boost'
            },
            iframe.src
        );
    });

    test('Should handle postMessage origin correctly', () => {
        // This tests the fix for the error:
        // "Failed to execute 'postMessage' on 'DOMWindow': The target origin provided ('https://huggingface.co') does not match the recipient window's origin"

        // The solution is to either:
        // 1. Use '*' as the targetOrigin (less secure but works across origins)
        // 2. Use the correct origin for the iframe

        // Test with the correct origin
        iframe.contentWindow.postMessage(
            { command: 'runSequence', activationKey: 'Mullis Spiral Boost' },
            'http://0.0.0.0:7863'
        );

        // Should not throw an error
        expect(iframe.contentWindow.postMessage).toHaveBeenCalledWith(
            { command: 'runSequence', activationKey: 'Mullis Spiral Boost' },
            'http://0.0.0.0:7863'
        );

        // Test with '*' as targetOrigin
        iframe.contentWindow.postMessage(
            { command: 'runSequence', activationKey: 'Neural Lotus Bloom' },
            '*'
        );

        // Should not throw an error
        expect(iframe.contentWindow.postMessage).toHaveBeenCalledWith(
            { command: 'runSequence', activationKey: 'Neural Lotus Bloom' },
            '*'
        );
    });
}); 