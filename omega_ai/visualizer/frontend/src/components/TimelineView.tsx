import React from 'react';
import { Box, Typography, List, ListItem, ListItemText } from '@mui/material';

const TimelineView: React.FC = () => {
    // TODO: Implement timeline data fetching from API
    const events: { id: number; text: string }[] = [];

    return (
        <Box sx={{ p: 2, height: '100%', overflow: 'auto' }}>
            {events.length === 0 ? (
                <Typography variant="body1" color="text.secondary">
                    No events to display
                </Typography>
            ) : (
                <List>
                    {events.map((event) => (
                        <ListItem key={event.id} divider>
                            <ListItemText
                                primary={`Event ${event.id}`}
                                secondary={event.text}
                            />
                        </ListItem>
                    ))}
                </List>
            )}
        </Box>
    );
};

export default TimelineView; 