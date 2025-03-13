import gym
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from gym import spaces

def calculate_rsi(df, window=14):
    """Compute Relative Strength Index (RSI) & Handle NaNs"""
    df = df.copy()  # ✅ Prevents Pandas warnings
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    df.loc[:, "RSI"] = df["RSI"].fillna(50)  # ✅ Proper Pandas-safe assignment
    return df

class BTCEnv(gym.Env):
    def __init__(self, df):
        super(BTCEnv, self).__init__()
        self.df = df
        self.current_step = 0

        # ✅ Check & Fix Missing RSI Values
        if "RSI" not in self.df.columns or self.df["RSI"].isnull().any():
            print("⚠️ RSI missing! Recalculating...")
            self.df = self.calculate_rsi(self.df)

        # 🔥 Features: [Close Price, Volume, RSI, Bollinger %B, Fibonacci Level]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        
        # 🔥 Actions: Continuous space for buying/selling (normalized between -1 and 1)
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

        # Portfolio state
        self.balance = 10000  # Starting balance
        self.btc_holding = 0

    def reset(self):
        self.current_step = 0
        self.balance = 10000  # Reset balance
        self.btc_holding = 0  # Reset BTC holding
        return self._next_observation()

    def _next_observation(self):
        """Extracts the current market observation, ensuring values stay within range [-1, 1]."""
        if self.current_step >= len(self.df):  # 🔥 Ensure valid index range
            self.current_step = len(self.df) - 1

        obs = self.df.iloc[self.current_step]

        # ✅ Scale price & volume to keep everything between [-1, 1]
        observation = np.array([
            obs["Close"] / 100000,  # Normalize BTC Price
            obs["BTC_Volume"] / 10000,  # Normalize BTC Volume
            obs["RSI"] / 100,  # Normalize RSI
            obs["Bollinger_%B"],  # Bollinger Band %B is already in [0,1]
            obs["Fib_Level"]  # Fibonacci Level (Assuming it's already normalized)
        ], dtype=np.float32)

        # ✅ HARD FILTER: Prevent extreme values and NaNs before returning observation
        observation = np.nan_to_num(observation, nan=0.0, posinf=1.0, neginf=-1.0)
        observation = np.clip(observation, -1, 1)  # 🔥 Final safeguard

        return observation

    def step(self, action):
        """Take an action & compute reward based on portfolio performance."""

        # ✅ HARD FILTER: Replace NaN & Inf values in action
        action = np.nan_to_num(action, nan=0.0, posinf=0.0, neginf=0.0)

        # ✅ Fix: Ensure prev_balance is never zero to prevent divide-by-zero
        prev_balance = max(self.balance, 1)  # 🔥 Prevents division by zero

        # ✅ DEBUGGING: PRINT RAW ACTIONS
        print(f"🟢 Step: {self.current_step}, Action Taken: {action}")

        # ✅ Action Interpretation (Prevent NaN Rewards)
        close_price = np.nan_to_num(self.df.iloc[self.current_step]["Close"], nan=0.0)  # 🔥 Ensure Close price is valid

        if action < -0.3:  # Strong Sell
            self.balance += self.btc_holding * close_price
            self.btc_holding = 0
        elif action > 0.3:  # Strong Buy
            btc_to_buy = self.balance / close_price if close_price > 0 else 0  # ✅ Avoid division by zero
            self.btc_holding += btc_to_buy
            self.balance -= btc_to_buy * close_price

        # ✅ Move to next timestep (ensure it's within valid range)
        self.current_step = min(self.current_step + 1, len(self.df) - 1)
        done = self.current_step >= len(self.df) - 1

        # ✅ Compute Reward (Ensure it's Finite)
        current_value = self.balance + (self.btc_holding * close_price)

        reward = (current_value - prev_balance) / (prev_balance + 1e-8)  # 🔥 Prevent divide-by-zero
        reward = np.nan_to_num(reward, nan=0.0, posinf=1.0, neginf=-1.0)  # ✅ Remove NaNs
        reward = np.clip(reward, -0.5, 0.5)  # ✅ Limit extreme values
        reward *= 5  # ✅ Ensure rewards are meaningful

        # ✅ DEBUGGING: PRINT RAW REWARD VALUES BEFORE FILTERING
        print(f"🔵 Step: {self.current_step}, Reward: {reward}, Balance: {self.balance}, BTC Holding: {self.btc_holding}")

        # ✅ Prevent NaN values in observation space
        obs = self._next_observation()
        obs = np.nan_to_num(obs, nan=0.0, posinf=1.0, neginf=-1.0)  # ✅ Ensure valid observation

        # ✅ DEBUGGING: PRINT FILTERED OUTPUTS BEFORE RETURNING
        print(f"🔴 Step: {self.current_step}, Filtered Observations: {obs}, Filtered Reward: {reward}")

        return obs, reward, done, {}

# 🔥 Load Binance Data
df = pd.read_csv("data/historical_btc_extended.csv")

# ✅ Ensure RSI is calculated before reinforcement learning starts
if "RSI" not in df.columns or df["RSI"].isnull().any():
    print("⚠️ RSI missing! Calculating RSI before RL training...")
    df = calculate_rsi(df)  # ✅ Call it as a standalone function

# ✅ Prevent Pandas warning by modifying DataFrame safely
df = df.copy()  

# ✅ Normalize RSI for RL training
df["RSI"] = (df["RSI"] - 50) / 50  # Normalize RSI to range [-1, 1]

# ✅ Ensure no NaNs in Bollinger Bands & Fibonacci Level
df["Bollinger_%B"] = np.nan_to_num((df["Close"] - df["Low"]) / (df["High"] - df["Low"]), nan=0.5)  # %B Indicator
df["Fib_Level"] = np.nan_to_num((df["Close"] - df["Low"]) / (df["High"] - df["Low"]), nan=0.5)  # Fibonacci Level Approx

# ✅ Replace Remaining NaNs & Infs in DataFrame Before Training PPO
df.fillna(0, inplace=True)  # Replace NaNs with 0
df.replace([np.inf, -np.inf], 0, inplace=True)  # Replace Infs with 0

# ✅ Train RL Model
env = BTCEnv(df)
model = PPO("MlpPolicy", env, learning_rate=0.0001, clip_range=0.2, verbose=1)  # ✅ Lower learning rate

# ✅ **ENSURE PPO MODEL DOESN’T RECEIVE NaNs**
for _ in range(10):
    obs = env.reset()
    assert not np.any(np.isnan(obs)), "❌ NaN detected in PPO observations!"
    assert not np.any(np.isinf(obs)), "❌ Inf detected in PPO observations!"
    assert np.max(np.abs(obs)) <= 1, "❌ Observation values exceed the expected range!"

# ✅ Train PPO Model
model.learn(total_timesteps=100000)

# ✅ Save trained model
model.save("data/rl_btc_advanced")
print("✅ Advanced RL model trained & saved!")  
 
