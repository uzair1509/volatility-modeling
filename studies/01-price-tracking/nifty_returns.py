import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

#nifty data from2 2k15 - 2k26
nifty = yf.download('^NSEI', start = '2015-01-01', end = '2026-01-01')

if isinstance(nifty.columns, pd.MultiIndex):
    nifty.columns = nifty.columns.droplevel(1)

nifty = nifty.dropna()

#plotting
plt.figure(figsize=(10,4)),
plt.plot(nifty.index, nifty['Close'])
plt.title('Nifty 50 Close Price') 
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.show()

#log return compute
nifty['log_return'] = 100 * np.log(nifty['Close']/nifty['Close'].shift(1))
nfty = nifty.dropna()

#log return plot
plt.figure(figsize=(10,4)),
plt.plot(nfty.index, nfty['log_return'])
plt.title('Nifty 50 Log Return') 
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.show()


#histogram plot
plt.figure(figsize=(8,4))
plt.hist(nifty['log_return'], bins=100)
plt.title('Distribution of Nifty 50 Log Returns')
plt.xlabel('Log Return (%)')
plt.ylabel('Frequency')
plt.show()

#stat support
print('Mean return:', nifty['log_return'].mean())
print('Standard deviation (Volatility):', nifty['log_return'].std())
print('Kurtosis:', nifty['log_return'].kurt())
print('Skewness:', nifty['log_return'].skew())
