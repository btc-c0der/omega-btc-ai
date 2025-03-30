# Setting Up the Fear & Greed API for OMEGA BTC AI

This guide walks you through setting up and using the Crypto Fear & Greed Index API from RapidAPI.

## About the API

The OMEGA BTC AI dashboard uses the [Crypto Fear & Greed Index API](https://rapidapi.com/onshabogdan-5SUvbWmtd0l/api/crypto-fear-greed-index2) to fetch real-time sentiment data for the cryptocurrency market. This API provides both current and historical data for the Fear & Greed Index.

## Getting Started

### 1. Create a RapidAPI Account

If you don't already have one, create an account at [RapidAPI](https://rapidapi.com/).

### 2. Subscribe to the API

1. Visit the [Crypto Fear & Greed Index API](https://rapidapi.com/onshabogdan-5SUvbWmtd0l/api/crypto-fear-greed-index2) on RapidAPI
2. Click "Subscribe to Test"
3. Choose a pricing plan (there is a free tier available)
4. Complete the subscription process

### 3. Get Your API Key

1. After subscribing, navigate to the API dashboard
2. Find your API key (X-RapidAPI-Key) in the code snippets or "Security" section

### 4. Configure the Application

There are two ways to add your API key to the application:

#### Option A: Environment Variable

Create a `.env.local` file in the root of the project with the following content:

```
REACT_APP_RAPIDAPI_KEY=your_api_key_here
```

#### Option B: Direct Modification

Open `src/services/fearGreedService.ts` and replace `'YOUR_API_KEY_HERE'` with your actual API key:

```typescript
const HEADERS = {
  'X-RapidAPI-Key': 'your_actual_api_key_here',
  'X-RapidAPI-Host': 'crypto-fear-greed-index2.p.rapidapi.com'
};
```

> Note: Option A is preferred for security reasons, especially if your code is stored in a public repository.

## API Endpoints Used

The application uses the following endpoints:

1. **Current Fear & Greed Index:**

   ```
   GET https://crypto-fear-greed-index2.p.rapidapi.com/v1/fgi
   ```

2. **Historical Fear & Greed Index:**

   ```
   GET https://crypto-fear-greed-index2.p.rapidapi.com/v1/fgi/history?limit=30
   ```

## Fallback Mechanism

The application includes a fallback mechanism that provides simulated data if the API calls fail. This ensures that your dashboard will still display Fear & Greed information even if there are API connectivity issues.

## API Rate Limits

Be aware of the rate limits for your chosen pricing plan. The free tier typically includes:

- 100 requests per day
- 5 requests per minute

The application is designed to refresh data periodically, but not so frequently as to exceed these limits.
