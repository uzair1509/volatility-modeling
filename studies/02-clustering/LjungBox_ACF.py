import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox as lb
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# data download
nifty = yf.download('^NSEI', start='2015-01-01', end='2026-01-01', progress=False)

# drop second level if needed
if isinstance(nifty.columns, pd.MultiIndex):
    nifty.columns = nifty.columns.droplevel(1)

# log returns
nifty['log_returns'] = 100 * np.log(nifty['Close'] / nifty['Close'].shift(1))
returns = nifty['log_returns'].dropna()

# ACF
acf_raw = acf(returns, nlags=10)
acf_sq = acf(returns**2, nlags=10)
#ljung_box carry out lag by lag not cumulative
lb_raw_rows = []
lb_sq_rows = []
for k in range (1,11):
  raw_row = lb(returns, lags = [k], return_df = True)
  sq_row = lb(returns**2, lags = [k], return_df = True)
  lb_raw_rows.append(raw_row.iloc[0])
  lb_sq_rows.append(sq_row.iloc[0])

lb_raw = pd.DataFrame(lb_raw_rows)
lb_sq = pd.DataFrame(lb_sq_rows)

#95 percent confidence interval for acf
ci = 1.96 / np.sqrt(len(returns))

#raw returns table
print("Raw ACF Values (Raw Returns) by Lag:")
print(f"{'Lag':<6} {'ACF':>8} {'95% CI':>10} {'Significant?':>14}")
for i in range(1, 11):
    acf_val = acf_raw[i]
    outside_ci = abs(acf_val) > ci
    print(f"{i:<6} {acf_val:>8.4f} ±{ci:>8.4f} {'Y' if outside_ci else 'N':>14}")

#squared returns table
print("\nACF Values (Squared Returns) by Lag:")
print(f"{'Lag':<6} {'ACF':>8} {'95% CI':>10} {'Significant?':>14}")
for i in range(1, 11):
    acf_val = acf_sq[i]
    outside_ci = abs(acf_val) > ci
    print(f"{i:<6} {acf_val:>8.4f} ±{ci:>8.4f} {'Y' if outside_ci else 'N':>14}")

#count significant lags
sum_sig_raw = 0
sum_sig_sq = 0
for lag in range(1, 11):
    if abs(acf_raw[lag]) > ci:
        sum_sig_raw += 1
    if abs(acf_sq[lag]) > ci:
        sum_sig_sq += 1

print(f"\n# Significant Raw ACF Values: {sum_sig_raw}/10")
print(f"# Significant Squared ACF Values: {sum_sig_sq}/10")

#raw ljung_box table
print("Ljung-Box Test (Raw Returns) by Lag:")
print(f"{'Lag':<6} {'LB Stat':>10} {'p-value':>10} {'Significant?':>14}")
for lag in range(1, 11):
    stat = lb_raw.loc[lag, 'lb_stat']
    pval = lb_raw.loc[lag, 'lb_pvalue']
    sig = pval < 0.05
    print(f"{lag:<6} {stat:>10.4f} {pval:>10.4f} {'Y' if sig else 'N':>14}")

#squared ljung_box table
print("\nLjung-Box Test (Squared Returns) by Lag:")
print(f"{'Lag':<6} {'LB Stat':>10} {'p-value':>10} {'Significant?':>14}")
for lag in range(1, 11):
    stat = lb_sq.loc[lag, 'lb_stat']
    pval = lb_sq.loc[lag, 'lb_pvalue']
    sig = pval < 0.05
    print(f"{lag:<6} {stat:>10.4f} {pval:>10.4f} {'Y' if sig else 'N':>14}")

#no. of significant lags found
sum_sig_lb_raw = (lb_raw['lb_pvalue'] < 0.05).sum()
sum_sig_lb_sq = (lb_sq['lb_pvalue'] < 0.05).sum()

print(f"\n# Significant Ljung-Box Raw Returns: {sum_sig_lb_raw}/10")
print(f"# Significant Ljung-Box Squared Returns: {sum_sig_lb_sq}/10")

#acf tables against ci
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

lags_range = range(1, 11)

axes[0].bar(lags_range, acf_raw[1:11], color='steelblue')
axes[0].axhline(ci, color='red', linestyle='--', linewidth=1)
axes[0].axhline(-ci, color='red', linestyle='--', linewidth=1)
axes[0].axhline(0, color='black', linewidth=0.8)
axes[0].set_title('ACF: Raw Returns')
axes[0].set_xlabel('Lag')
axes[0].set_ylabel('Autocorrelation')

axes[1].bar(lags_range, acf_sq[1:11], color='darkorange')
axes[1].axhline(ci, color='red', linestyle='--', linewidth=1)
axes[1].axhline(-ci, color='red', linestyle='--', linewidth=1)
axes[1].axhline(0, color='black', linewidth=0.8)
axes[1].set_title('ACF: Squared Returns')
axes[1].set_xlabel('Lag')

plt.tight_layout()
plt.savefig('acf_comparison.png', dpi=150)
plt.show()


