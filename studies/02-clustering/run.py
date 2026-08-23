import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox

from volmodels.data import load_nifty
from volmodels.returns import log_returns, squared_returns

nifty = load_nifty()
r = log_returns(nifty['Close'])
r2 = squared_returns(r)

#acf of returns: should die off almost immediately
fig, ax = plt.subplots(figsize=(10,4))
plot_acf(r.values, lags=40, ax=ax)
ax.set_title('ACF of Log Returns')
plt.tight_layout()
plt.savefig('results/02-acf-returns.png', dpi=150)
plt.close()

#acf of squared returns: stays significant for many lags
#this is volatility clustering, and its why we need garch
fig, ax = plt.subplots(figsize=(10,4))
plot_acf(r2.values, lags=40, ax=ax)
ax.set_title('ACF of Squared Log Returns')
plt.tight_layout()
plt.savefig('results/02-acf-squared-returns.png', dpi=150)
plt.close()

lb_r = acorr_ljungbox(r.values, lags=[10, 20], return_df=True)
lb_r2 = acorr_ljungbox(r2.values, lags=[10, 20], return_df=True)

print('Ljung-Box on returns:')
print(lb_r)
print()
print('Ljung-Box on squared returns:')
print(lb_r2)
