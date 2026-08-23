import matplotlib
matplotlib.use('Agg')  #no display needed, we just save files
import matplotlib.pyplot as plt

from volmodels.data import load_nifty
from volmodels.returns import log_returns

nifty = load_nifty()
r = log_returns(nifty['Close'])

#close price
plt.figure(figsize=(10,4))
plt.plot(nifty.index, nifty['Close'])
plt.title('Nifty 50 Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.tight_layout()
plt.savefig('results/01-close-price.png', dpi=150)
plt.close()

#log returns over time
plt.figure(figsize=(10,4))
plt.plot(r.index, r.values)
plt.title('Nifty 50 Log Return')
plt.xlabel('Date')
plt.ylabel('Log Return (%)')
plt.tight_layout()
plt.savefig('results/01-log-returns.png', dpi=150)
plt.close()

#distribution
plt.figure(figsize=(8,4))
plt.hist(r.values, bins=100)
plt.title('Distribution of Nifty 50 Log Returns')
plt.xlabel('Log Return (%)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('results/01-return-histogram.png', dpi=150)
plt.close()

#stylised facts
print(f"Observations: {len(r)}")
print(f"Mean return: {r.mean():.4f}")
print(f"Std dev (volatility): {r.std():.4f}")
print(f"Kurtosis: {r.kurt():.4f}")
print(f"Skewness: {r.skew():.4f}")

