import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from arch import arch_model
import warnings
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from scipy import stats

warnings.filterwarnings('ignore')

nifty = yf.download('^NSEI', start='2015-01-01', end='2026-01-01')
nifty['log_returns'] = 100 * (np.log(nifty['Close'] / nifty['Close'].shift(1)))
returns = nifty['log_returns'].dropna()

# GARCH(1,1) plain
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

standardised_resid = res.resid / cond_vol
lb_test = acorr_ljungbox(standardised_resid, lags=10, return_df=True)
lb_test_sq = acorr_ljungbox(standardised_resid**2, lags=10, return_df=True)
arch_lm_garch = het_arch(standardised_resid, nlags=10)

print(lb_test)

# GJR-GARCH(1,1,1) normal
gjr_normal = arch_model(returns, vol='GARCH', p=1, o=1, q=1, mean='Constant', dist='normal')
res_gjr_normal = gjr_normal.fit(disp='off')

alpha_normal = res_gjr_normal.params['alpha[1]']
beta_normal = res_gjr_normal.params['beta[1]']
gamma_normal = res_gjr_normal.params['gamma[1]']
persistence_normal = alpha_normal + beta_normal + gamma_normal / 2
half_life_normal = np.log(0.5) / np.log(persistence_normal) if persistence_normal < 1 else np.inf

cond_vol_normal = res_gjr_normal.conditional_volatility
standard_resid_normal = res_gjr_normal.resid / cond_vol_normal

lb_gjr_normal_sq = acorr_ljungbox(standard_resid_normal**2, lags=10, return_df=True)
arch_lm_gjr_normal = het_arch(standard_resid_normal, nlags=10)

# GJR-GARCH(1,1,1) t distribute
gjr_t = arch_model(returns, vol='GARCH', p=1, o=1, q=1, mean='Constant', dist='t')
res_gjr_t = gjr_t.fit(disp='off')

alpha_t = res_gjr_t.params['alpha[1]']
beta_t = res_gjr_t.params['beta[1]']
gamma_t = res_gjr_t.params['gamma[1]']
persistence_t = alpha_t + beta_t + gamma_t / 2
half_life_t = np.log(0.5) / np.log(persistence_t) if persistence_t < 1 else np.inf

cond_vol_t = res_gjr_t.conditional_volatility
standard_resid_t = res_gjr_t.resid / cond_vol_t

lb_gjr_t_sq = acorr_ljungbox(standard_resid_t**2, lags=10, return_df=True)
arch_lm_gjr_t = het_arch(standard_resid_t, nlags=10)

#GJR-GARCH (1,1,1) skewed t distribution
gjr_skew_t = arch_model(returns, vol = 'GARCH', p=1,o=1, q=1, mean = 'Constant', dist = 'skewt')
res_gjr_skew_t = gjr_skew_t.fit(disp = 'off')

alpha_skew_t = res_gjr_skew_t.params['alpha[1]']
beta_skew_t = res_gjr_skew_t.params['beta[1]']
gamma_skew_t = res_gjr_skew_t.params['gamma[1]']
persistence_skew_t = alpha_skew_t + beta_skew_t + gamma_skew_t / 2
half_life_skew_t = np.log(0.5)/np.log(persistence_skew_t) if persistence_skew_t < 1 else np.inf 

cond_vol_skew_t = res_gjr_skew_t.conditional_volatility
standard_resid_skew_t = res_gjr_skew_t.resid/cond_vol_skew_t

lb_gjr_skew_t_sq = acorr_ljungbox(standard_resid_skew_t**2, lags = 10, return_df = True)
arch_lm_gjr_skew_t = het_arch(standard_resid_skew_t, nlags = 10)

# Comparison table
results_gjr = [
    {
        'type': 'GARCH(1,1)',
        'p': 1, 'o': 0, 'q': 1,
        'AIC': res.aic,
        'BIC': res.bic,
        'omega': res.params['omega'],
        'alpha': alpha,
        'gamma': np.nan,
        'gamma_p': np.nan,
        'beta': beta,
        'mean': res.params['mu'],
        'persistence': persistence,
        'half_life': half_life,
        'lb_pvalue_lag10': lb_test_sq['lb_pvalue'].iloc[-1],
        'arch_lm_pvalue': arch_lm_garch[1],
    },
    {
        'type': 'gjr-normal',
        'p': 1, 'o': 1, 'q': 1,
        'AIC': res_gjr_normal.aic,
        'BIC': res_gjr_normal.bic,
        'omega': res_gjr_normal.params['omega'],
        'alpha': alpha_normal,
        'gamma': gamma_normal,
        'gamma_p': res_gjr_normal.pvalues['gamma[1]'],
        'beta': beta_normal,
        'mean': res_gjr_normal.params['mu'],
        'persistence': persistence_normal,
        'half_life': half_life_normal,
        'lb_pvalue_lag10': lb_gjr_normal_sq['lb_pvalue'].iloc[-1],
        'arch_lm_pvalue': arch_lm_gjr_normal[1],
    },
    {
        'type': 'gjr-t',
        'p': 1, 'o': 1, 'q': 1,
        'AIC': res_gjr_t.aic,
        'BIC': res_gjr_t.bic,
        'omega': res_gjr_t.params['omega'],
        'alpha': alpha_t,
        'gamma': gamma_t,
        'gamma_p': res_gjr_t.pvalues['gamma[1]'],
        'beta': beta_t,
        'mean': res_gjr_t.params['mu'],
        'persistence': persistence_t,
        'half_life': half_life_t,
        'lb_pvalue_lag10': lb_gjr_t_sq['lb_pvalue'].iloc[-1],
        'arch_lm_pvalue': arch_lm_gjr_t[1],
    },
    {
        'type': 'gjr-skewed-t',
        'p': 1, 'o': 1, 'q': 1,
        'AIC': res_gjr_skew_t.aic,
        'BIC': res_gjr_skew_t.bic,
        'omega': res_gjr_skew_t.params['omega'],
        'alpha': alpha_skew_t,
        'gamma': gamma_skew_t,
        'gamma_p': res_gjr_skew_t.pvalues['gamma[1]'],
        'beta': beta_skew_t,
        'mean': res_gjr_skew_t.params['mu'],
        'persistence': persistence_skew_t,
        'half_life': half_life_skew_t,
        'lb_pvalue_lag10': lb_gjr_skew_t_sq['lb_pvalue'].iloc[-1],
        'arch_lm_pvalue': arch_lm_gjr_skew_t[1],
    },
]

comp_gjr_df = pd.DataFrame(results_gjr)
print(comp_gjr_df)

print(f"Gamma (t-dist): {gamma_t:.4f}, p-value: {res_gjr_t.pvalues['gamma[1]']:.4f}, "
      f"significant: {res_gjr_t.pvalues['gamma[1]'] < 0.05}")

print(res_gjr_skew_t.params[['eta', 'lambda']])
print(res_gjr_skew_t.pvalues[['eta', 'lambda']])



