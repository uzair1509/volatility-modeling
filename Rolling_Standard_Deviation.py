import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#data download
nifty = yf.download('^NSEI', start='2015-01-01', end='2026-01-01', progress=False)
#clean
if isinstance(nifty.columns, pd.MultiIndex):
    nifty.columns = nifty.columns.droplevel(1)
nifty = nifty.dropna()
#compute log returns
nifty['log_return'] = 100 * np.log(nifty['Close']/nifty['Close'].shift(1))
nifty = nifty.dropna()
#compute rolling standard deviation (volatility)
nifty['vol_10d'] = nifty['log_return'].rolling(10).std()
nifty['vol_20d'] = nifty['log_return'].rolling(20).std()
nifty['vol_60d'] = nifty['log_return'].rolling(60).std()
nifty = nifty.dropna()

#baseline: unconditional volatility before COVID
pre_covid_returns = nifty.loc[:'2020-02-15', 'log_return']
baseline_vol = pre_covid_returns.std()

#plot 1: price chart
plt.figure(figsize=(12, 4))
plt.plot(nifty.index, nifty['Close'], color='steelblue')
plt.title('Nifty 50 Close Price')
plt.ylabel('Index Value')
plt.xlabel('Date')
plt.tight_layout()
plt.show()

#plot 2: rolling volatility with baseline
plt.figure(figsize=(12, 5))
plt.plot(nifty.index, nifty['vol_10d'], label='10-day rolling volatility', linewidth=0.8)
plt.plot(nifty.index, nifty['vol_20d'], label='20-day rolling volatility', linewidth=0.8)
plt.plot(nifty.index, nifty['vol_60d'], label='60-day rolling volatility', linewidth=1.2)
plt.axhline(y=baseline_vol, color='black', linestyle='--', linewidth=1, label=f'Pre-COVID unconditional vol ({baseline_vol:.2f}%)')
plt.title('Rolling Volatility at Different Window Lengths')
plt.ylabel('Percentage Volatility')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
plt.show()

#plot 3: covid zoom with baseline
covid_window = nifty.loc['2019-10-01':'2021-01-01']

plt.figure(figsize=(12, 5))
plt.plot(covid_window.index, covid_window['vol_10d'], label='10-day', linewidth=1)
plt.plot(covid_window.index, covid_window['vol_20d'], label='20-day', linewidth=1)
plt.plot(covid_window.index, covid_window['vol_60d'], label='60-day', linewidth=1.5)
plt.axhline(y=baseline_vol, color='black', linestyle='--', linewidth=1, label=f'Pre-COVID unconditional vol ({baseline_vol:.2f}%)')
plt.title('Rolling Volatility Around COVID-19 Crash')
plt.ylabel('Percentage Volatility')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
plt.show()
