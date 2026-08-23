import pandas as pd
from arch import arch_model

from volmodels.data import load_nifty
from volmodels.returns import log_returns

nifty = load_nifty()
r = log_returns(nifty['Close'])

specs = {
  'gjr_normal':   {'o': 1, 'dist': 'normal'},
  'gjr_t':        {'o': 1, 'dist': 't'},
  'gjr_skewt':    {'o': 1, 'dist': 'skewt'},
  'garch_normal': {'o': 0, 'dist': 'normal'},
}

rows = []
for name, kwargs in specs.items():
  fit = arch_model(r.values, vol='GARCH', p=1, q=1, mean='Constant', **kwargs).fit(disp='off')
  print(f'\n===== {name} =====')
  print(fit.summary())

  rows.append({
    'spec': name,
    'alpha': fit.params.get('alpha[1]'),
    'gamma': fit.params.get('gamma[1]'),
    'beta': fit.params.get('beta[1]'),
    'loglik': fit.loglikelihood,
    'aic': fit.aic,
    'bic': fit.bic,
    'converged': fit.convergence_flag == 0,
  })

tbl = pd.DataFrame(rows)
tbl.to_csv('results/05-gjr-specifications.csv', index=False)
print('\n')
print(tbl.to_string(index=False))
