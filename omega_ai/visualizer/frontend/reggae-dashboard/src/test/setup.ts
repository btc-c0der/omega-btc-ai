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
    onopen: ((this: WebSocket, ev: Event) => any) | null = null;
    onclose: ((this: WebSocket, ev: CloseEvent) => any) | null = null;
    onmessage: ((this: WebSocket, ev: MessageEvent) => any) | null = null;
    onerror: ((this: WebSocket, ev: Event) => any) | null = null;

    constructor(url: string, protocols?: string | string[]) { }

    close(code?: number, reason?: string): void { }
    send(data: string | ArrayBufferLike | Blob | ArrayBufferView): void { }

    readonly CLOSED: number = 3;
    readonly CLOSING: number = 2;
    readonly CONNECTING: number = 0;
    readonly OPEN: number = 1;
    readonly readyState: number = 1;
    readonly url: string = "ws://mock";
    readonly bufferedAmount: number = 0;
    readonly extensions: string = "";
    readonly protocol: string = "";
    readonly binaryType: BinaryType = "blob";
}

// Set up the mock
window.WebSocket = MockWebSocket as any;

// Mock window.ResizeObserver
window.ResizeObserver = class ResizeObserver {
    observe() { }
    unobserve() { }
    disconnect() { }
}; 