import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import RedisFeedMonitor from './RedisFeedMonitor';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('RedisFeedMonitor', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders loading state initially', () => {
        // Mock axios.get to return a promise that doesn't resolve immediately
        mockedAxios.get.mockReturnValue(new Promise(() => { }));

        render(<RedisFeedMonitor />);

        // Check for loading spinner
        expect(screen.getByText('REDIS FEED')).toBeInTheDocument();
        expect(screen.getByText('Disconnected')).toBeInTheDocument();
    });

    it('renders error state when API call fails', async () => {
        // Mock axios.get to reject with an error
        mockedAxios.get.mockRejectedValueOnce(new Error('API Error'));

        render(<RedisFeedMonitor />);

        // Wait for the error state to appear
        await waitFor(() => {
            expect(screen.getByText('Failed to connect to Redis')).toBeInTheDocument();
        });
    });

    it('renders empty state when no keys are returned', async () => {
        // Mock axios.get to return an empty keys array
        mockedAxios.get.mockResolvedValueOnce({ data: { keys: [] } });

        render(<RedisFeedMonitor />);

        // Wait for the empty state to appear
        await waitFor(() => {
            expect(screen.getByText('No Redis keys found')).toBeInTheDocument();
        });
    });

    it('renders Redis keys when data is loaded successfully', async () => {
        // Mock Redis keys data
        const mockRedisKeys = {
            keys: [
                { key: 'test_string', type: 'string', length: 10 },
                { key: 'test_list', type: 'list', length: 5 },
                { key: 'test_hash', type: 'hash', fields: 3 }
            ]
        };

        // Mock axios.get to return the mock data
        mockedAxios.get.mockResolvedValueOnce({ data: mockRedisKeys });

        render(<RedisFeedMonitor />);

        // Wait for the keys to appear
        await waitFor(() => {
            expect(screen.getByText('Connected')).toBeInTheDocument();

            // Check that keys are displayed
            expect(screen.getByText('test_string')).toBeInTheDocument();
            expect(screen.getByText('test_list')).toBeInTheDocument();
            expect(screen.getByText('test_hash')).toBeInTheDocument();

            // Check that types are displayed
            expect(screen.getByText('10 chars')).toBeInTheDocument();
            expect(screen.getByText('5 items')).toBeInTheDocument();
            expect(screen.getByText('3 fields')).toBeInTheDocument();
        });
    });

    it('filters out internal keys', async () => {
        // Mock Redis keys data with internal keys
        const mockRedisKeys = {
            keys: [
                { key: 'test_string', type: 'string', length: 10 },
                { key: 'internal:cache', type: 'hash', fields: 5 }
            ]
        };

        // Mock axios.get to return the mock data
        mockedAxios.get.mockResolvedValueOnce({ data: mockRedisKeys });

        render(<RedisFeedMonitor />);

        // Wait for the keys to appear
        await waitFor(() => {
            // Check that normal key is displayed but internal key is filtered out
            expect(screen.getByText('test_string')).toBeInTheDocument();
            expect(screen.queryByText('internal:cache')).not.toBeInTheDocument();
        });
    });
}); 