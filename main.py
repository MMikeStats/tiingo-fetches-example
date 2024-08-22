from tiingo_api import TiingoDataFetcher
from indicators import calculate_ema, stochastic_oscillator

API_KEY = 'YOUR_API_KEY'

def main():
    ticker = 'SPY'
    frequency = '15min'
    last_n_days = 3

    # Fetch data
    fetcher = TiingoDataFetcher(API_KEY)
    df = fetcher.fetch_data(ticker, last_n_days, frequency)
    
    # Calculate EMA
    df = calculate_ema(df, length_ema=30)

    # Calculate Stoch
    df = stochastic_oscillator(df, period_k=10, smooth_k=2, period_d=5)

    print(df)

if __name__ == "__main__":
    main()
