import numpy as np
import pandas as pd
from volmodels.backtest import rolling_forecast

def test_no_lookahead():
  #forecasts must not change when future returns are corrupted
  rng = np.random.default_rng(0)
  idx = pd.date_range('2020-01-01', periods=400)
  r = pd.Series(rng.normal(0, 1, 400), index=idx)

  a = rolling_forecast(r, window=300, verbose=False)

  r2 = r.copy()
  r2.iloc[350:] = 99.0
  b = rolling_forecast(r2, window=300, verbose=False)

  #first 50 forecasts use only data before index 350
  assert np.allclose(a['garch11'].values[:50], b['garch11'].values[:50])
