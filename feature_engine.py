import pandas as pd

def candles_to_df(candles):
    if not candles:
        return pd.DataFrame()
    df = pd.DataFrame(candles)
    if 'ts' in df.columns:
        df['ts'] = pd.to_datetime(df['ts'], unit='s')
        df.set_index('ts', inplace=True)
    return df

def add_ema(df, period):
    df[f'ema{period}'] = df['close'].ewm(span=period,adjust=False).mean()

def add_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = tr.rolling(period).mean()

def add_rsi(df, period=14):
    delta = df['close'].diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = -delta.clip(upper=0).rolling(period).mean()
    rs = up/down
    df['rsi'] = 100 - 100/(1+rs)

def compute_features(candles):
    df = candles_to_df(candles)
    if df.empty:
        return {}
    add_ema(df,9); add_ema(df,21); add_atr(df,14); add_rsi(df,14)
    last = df.iloc[-1]
    return {'ema9': float(last['ema9']), 'ema21': float(last['ema21']), 'atr': float(last['atr']), 'rsi': float(last['rsi']), 'close': float(last['close'])}
