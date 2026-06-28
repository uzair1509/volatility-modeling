import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from arch import arch_model
import warnings

warnings.filterwarnings('ignore')

nifty = yf.download('^NSEI', start='2015-01-01', end='2026-01-01')
nifty['log_returns'] = 100 * (np.log(nifty['Close'] / nifty['Close'].shift(1)))
returns = nifty['log_returns'].dropna()

test_orders = [(1, 1), (1, 2), (2, 1), (2, 2)]
results = []

for p, q in test_orders:
    model = arch_model(returns, vol='GARCH', p=p, q=q, mean='Constant', dist='normal')
    res = model.fit(disp='off')
    results.append(
        {
            'p': p,
            'q': q,
            'AIC': res.aic,
            'BIC': res.bic,
            'omega': res.params['omega'],
            'alpha': res.params['alpha[1]'],
            'beta': res.params['beta[1]'],
            'mean': res.params['mu'],
        }
    )

comp_df = pd.DataFrame(results)
comp_df = comp_df.sort_values(by=['AIC', 'BIC']).reset_index(drop=True)
print(comp_df)

best_aic = comp_df.loc[comp_df['AIC'].idxmin()]
best_bic = comp_df.loc[comp_df['BIC'].idxmin()]

print(f"\nBest by AIC: GARCH({int(best_aic['p'])},{int(best_aic['q'])}) with AIC:{best_aic['AIC']:.2f}")
print(f"\nBest by BIC: GARCH({int(best_bic['p'])},{int(best_bic['q'])}) with BIC: {best_bic['BIC']:.2f}")

final_model = arch_model(returns, vol='GARCH', p=1, q=1, mean='Constant', dist='normal')
res = final_model.fit(disp='off')

alpha = res.params['alpha[1]']
beta = res.params['beta[1]']
persistence = alpha + beta
half_life = np.log(0.5) / np.log(persistence) if persistence < 1 else np.inf

cond_vol = res.conditional_volatility

nifty = nifty.dropna()
nifty['cond_vol'] = np.nan
nifty.loc[cond_vol.index, 'cond_vol'] = cond_vol

nifty['20_rolling_SD'] = nifty['log_returns'].rolling(20).std()

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)

axes[0].plot(nifty.index, nifty['log_returns'], linewidth=0.3, color='gray')
axes[0].set_ylabel('Daily return (%)')
axes[0].set_title('Nifty 50 Daily Log Returns')
axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

axes[1].plot(nifty.index, nifty['20_rolling_SD'], linewidth=1.0,
             color='steelblue', alpha=0.8, label='20 day rolling vol')
axes[1].plot(nifty.index, nifty['cond_vol'], linewidth=1.0,
             color='darkred', alpha=0.9, label='GARCH(1,1) conditional vol')
axes[1].set_ylabel('Volatility / %')
axes[1].set_xlabel('Date')
axes[1].set_title('GARCH(1,1) Conditional Volatility vs 20 Day rolling SD')
axes[1].legend()

plt.tight_layout()
plt.show()
