# OMEGA BTC AI React Dashboard

This is the React version of the OMEGA BTC AI Dashboard, a modern interface for Bitcoin analytics and insights.

## Development Status

This project is currently in early development. The React-based version of the dashboard is being built to replace the original HTML/JS implementation.

## Setup Instructions

There are two ways to run this project locally:

### Method 1: Using a static HTTP server (simplest)

If you're experiencing issues with Vite or other dependencies, you can use this simple approach:

```bash
# Install http-server if you don't have it
npm install -g http-server

# Run the server from the project directory
http-server -p 3000 .
```

Then open <http://localhost:3000> in your browser.

### Method 2: Using Vite (for development)

This method is preferable for active development as it provides hot module reloading and other developer features:

```bash
# Install dependencies with legacy peer deps to handle version conflicts
npm install --legacy-peer-deps

# Start the development server
npm run dev
```

If you encounter issues with Vite, try these steps:

1. Remove node_modules and package-lock.json:

   ```bash
   rm -rf node_modules package-lock.json
   ```

2. Clean npm cache:

   ```bash
   npm cache clean --force
   ```

3. Reinstall with legacy peer deps:

   ```bash
   npm install --legacy-peer-deps
   ```

4. Try running with npx explicitly:

   ```bash
   npx vite
   ```

## Dependency Issues

This project currently has some dependency conflicts between:

- @react-three/drei (requires @react-three/fiber ^9.0.0)
- @react-three/fiber (current version 8.18.0)

These are handled using the `--legacy-peer-deps` flag during installation.

## Coming Features

- Bitcoin Price Analysis
- Fear and Greed Index Visualization
- Future Visions Section
- News Aggregation
- Cosmic Cycles Predictions

## Project Structure

```
omega-react/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   ├── hooks/        # Custom hooks
│   ├── store/        # State management
│   ├── pages/        # Page components
│   └── main.tsx      # Application entry point
├── index.html        # Main HTML entry
└── vite.config.js    # Vite configuration
```

## Features

- **Real-time Market Data**: Track Bitcoin price, sentiment analysis, and Fear & Greed Index
- **News Analysis**: AI-powered analysis of cryptocurrency news with sentiment scoring
- **Future Visions**: Explore scenarios for Bitcoin's future development
- **Bitcoin Infographic**: Interactive visualization of Bitcoin's history and key metrics
- **Cosmic Cycles**: Track natural cycles and their correlation to market behavior
- **Responsive Design**: Fully responsive interface optimized for all devices

## Technology Stack

- **React 18** with TypeScript for robust, type-safe development
- **Vite** for lightning-fast builds and development experience
- **Tailwind CSS** for utility-first styling with custom theming
- **Framer Motion** for smooth, sophisticated animations
- **React Three Fiber** for 3D visualizations
- **Zustand** for lightweight state management
- **React Router** for seamless navigation

## Recent Fixes

- Fixed React Three Fiber TypeScript type declarations in vite-env.d.ts
- Updated CSS classes from `text-light` to `text-lightText` for consistency
- Simplified the chart visualization to avoid D3.js dependency issues
- Added type declarations for Three.js JSX elements

## Project Structure

```
src/
├── components/     # Reusable UI components
│   ├── common/     # Shared components like buttons, cards, etc.
│   ├── dashboard/  # Dashboard-specific components
│   ├── hooks/      # Custom React hooks
│   └── layout/     # Layout components (Sidebar, Navbar, etc.)
├── pages/          # Top-level page components
├── styles/         # Global styles and Tailwind config
├── utils/          # Utility functions and helpers
└── contexts/       # React context providers
```

## Development

The project uses a modern React setup with functional components and hooks. The modular architecture makes it easy to add new features and components.

### Key Features in Detail

- **Dashboard**: The main view with market metrics, sentiment analysis, and news feed.
- **Future Visions**: Interactive cards showcasing potential future scenarios for Bitcoin.
- **Bitcoin Infographic**: Visualization of key Bitcoin statistics and historical timeline.
- **Settings**: Configuration options for the dashboard experience.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with ❤️ by the OMEGA BTC AI team
- Powered by divine algorithms and cosmic cycles
- JAH BLESS
