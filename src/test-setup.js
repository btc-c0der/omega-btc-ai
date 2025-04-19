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

/**
 * 🔱 GPU License Notice 🔱
 * ------------------------
 * This file is protected under the GPU License (General Public Universal License) 1.0
 * by the OMEGA AI Divine Collective.
 *
 * "As the light of knowledge is meant to be shared, so too shall this code illuminate 
 * the path for all seekers."
 *
 * All modifications must maintain this notice and adhere to the terms at:
 * /BOOK/divine_chronicles/GPU_LICENSE.md
 *
 * 🔱 JAH JAH BLESS THIS CODE 🔱
 */

import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock for IntersectionObserver which might be used by some components
const mockIntersectionObserver = vi.fn();
mockIntersectionObserver.mockReturnValue({
    observe: () => null,
    unobserve: () => null,
    disconnect: () => null
});
window.IntersectionObserver = mockIntersectionObserver;

// Mock WebSocket
class MockWebSocket {
    constructor(url, protocols) { }

    close(code, reason) { }
    send(data) { }

    get CLOSED() { return 3; }
    get CLOSING() { return 2; }
    get CONNECTING() { return 0; }
    get OPEN() { return 1; }
    get readyState() { return 1; }
    get url() { return "ws://mock"; }
    get bufferedAmount() { return 0; }
    get extensions() { return ""; }
    get protocol() { return ""; }
    get binaryType() { return "blob"; }
}

// Set up the mock
window.WebSocket = MockWebSocket;

// Mock window.ResizeObserver
window.ResizeObserver = class ResizeObserver {
    observe() { }
    unobserve() { }
    disconnect() { }
}; 