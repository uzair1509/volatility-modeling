import os
import yfinance as yf
import pandas as pd

CACHE = 'data/raw/nifty.csv'

def load_nifty(start='2015-01-01', end='2026-01-01', cache=True):
  #cached copy so we dont hit yfinance on every run
  if cache and os.path.exists(CACHE):
    return pd.read_csv(CACHE, index_col=0, parse_dates=True)

  nifty = yf.download('^NSEI', start=start, end=end, progress=False)

  #yfinance sometimes returns MultiIndex columns, sometimes not
  if isinstance(nifty.columns, pd.MultiIndex):
    nifty.columns = nifty.columns.droplevel(1)

  nifty = nifty.dropna()

  if cache:
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    nifty.to_csv(CACHE)

  return nifty
