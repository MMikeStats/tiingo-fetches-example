import pandas as pd
import ta

def calculate_ema(df, length_ema=5):
    df[f'EMA{length_ema}'] = ta.trend.EMAIndicator(df['close'], window=length_ema).ema_indicator()
    return df

def stochastic_oscillator(df, period_k=14, smooth_k=1, period_d=3):
    # Calculate the Stochastic Oscillator values
    df['%K'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=period_k, smooth_window=smooth_k)
    df['%D'] = df['%K'].rolling(window=period_d).mean()
    
    return df
