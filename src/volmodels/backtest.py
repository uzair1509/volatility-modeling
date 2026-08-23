import numpy as np
import pandas as pd
from arch import arch_model

#specs to fit. each entry is the kwargs passed to arch_model
SPECS = {
  'garch11': {'p': 1, 'q': 1, 'dist': 'normal'},
  'gjr_normal': {'p': 1, 'o': 1, 'q': 1, 'dist': 'normal'},
}

def rolling_forecast(returns, specs=SPECS, window=1500, verbose=True):
  #returns: pandas Series of percent log returns
  #walks the window forward one day at a time, refits, forecasts 1 step ahead

  r = returns.values
  T = len(r)
  n = T - window

  if n <= 0:
    raise ValueError(f"window {window} too large for {T} observations")

  out = {name: np.full(n, np.nan) for name in specs}
  sq_ret = np.zeros(n)
  failures = {name: 0 for name in specs}

  for i in range(n):
    if verbose and i % 100 == 0:
      print(f'{i} out of {n} days forecasted')

    train = r[i : i + window]
    sq_ret[i] = r[i + window] ** 2

    for name, kwargs in specs.items():
      try:
        fit = arch_model(train, vol='GARCH', mean='Constant', **kwargs).fit(disp='off')
        out[name][i] = fit.forecast(horizon=1).variance.values[-1, 0]
      except Exception:
        #leave as nan and count it, rather than silently returning garbage
        failures[name] += 1

  if verbose:
    for name, count in failures.items():
      if count:
        print(f'{name}: {count} of {n} fits failed')

  #index by the date being forecast, so nothing can misalign later
  idx = returns.index[window:]
  df = pd.DataFrame(out, index=idx)
  df['sq_ret'] = sq_ret
  return df
