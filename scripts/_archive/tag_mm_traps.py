import pandas as pd

def tag_mm_traps():
    """Tag possible Market Maker traps in historical BTC-Schumann data."""

    file_path = "data/historical_data.csv"
    df = pd.read_csv(file_path)

    # Detect Liquidity Grabs (Fakeouts)
    df["Liquidity_Grab"] = (df["BTC_Price"].diff().abs() > 1000) & (df["Schumann"] > 10)

    # Detect Fake Pumps/Dumps
    df["Fake_Pump"] = (df["BTC_Price"].pct_change() > 0.05)  # +5% pump
    df["Fake_Dump"] = (df["BTC_Price"].pct_change() < -0.05)  # -5% dump

    # Detect MM Ranges (Accumulation)
    df["Accumulation"] = (df["BTC_Price"].rolling(10).std() < 200) & (df["Schumann"] > 8)

    # Save tagged data
    df.to_csv("data/tagged_mm_data.csv", index=False)
    print(f"✅ Tagged MM traps & saved to tagged_mm_data.csv!")

# Run tagging
if __name__ == "__main__":
    tag_mm_traps()
