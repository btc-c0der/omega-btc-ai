import React from 'react';
import { Box, Typography, useTheme } from '@mui/material';
import { SxProps, Theme } from '@mui/material/styles';

const headerStyles: SxProps<Theme> = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  mb: 3,
};

const Header: React.FC = () => {
  const theme = useTheme();

  return (
    <Box sx={headerStyles}>
      <Box>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
            background: 'linear-gradient(135deg, #3C89E8 0%, #04D584 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 0.5,
          }}
        >
          Omega BTC AI
        </Typography>
        <Typography
          variant="subtitle1"
          sx={{
            color: 'text.secondary',
          }}
        >
          Advanced Market Analysis & Pattern Detection
        </Typography>
      </Box>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 3,
        }}
      >
        <Box>
          <Typography
            variant="body2"
            sx={{ color: 'text.secondary', mb: 0.5 }}
          >
            Last Updated
          </Typography>
          <Typography variant="subtitle2">
            {new Date().toLocaleString()}
          </Typography>
        </Box>
        <Box
          sx={{
            px: 2,
            py: 1,
            borderRadius: 1,
            backgroundColor: 'success.main',
            color: 'white',
          }}
        >
          <Typography variant="subtitle2" fontWeight={600}>
            LIVE
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default Header; 