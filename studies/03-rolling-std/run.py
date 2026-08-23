import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from volmodels.data import load_nifty
from volmodels.returns import log_returns

nifty = load_nifty()
r = log_returns(nifty['Close'])

windows = [21, 63, 252]  #roughly a month, a quarter, a year

plt.figure(figsize=(11,5))
for w in windows:
  plt.plot(r.index, r.rolling(w).std(), label=f'{w}-day')
plt.title('Rolling Standard Deviation of Nifty 50 Log Returns')
plt.xlabel('Date')
plt.ylabel('Std Dev (%)')
plt.legend()
plt.tight_layout()
plt.savefig('results/03-rolling-std.png', dpi=150)
plt.close()

for w in windows:
  s = r.rolling(w).std().dropna()
  print(f'{w}-day window:  mean {s.mean():.4f}  min {s.min():.4f}  max {s.max():.4f}')
