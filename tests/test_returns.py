import numpy as np
import pandas as pd
from volmodels.returns import log_returns, squared_returns

#constant prices --> zero returns
def test_constant_prices_give_zero():
  p = pd.Series([100.0] * 10)
  r = log_returns(p)
  assert np.allclose(r.values, 0)

#n prices --> n-1 returns (first one is NaN and gets dropped)
def test_length():
  p = pd.Series([100.0, 101.0, 102.0, 103.0])
  assert len(log_returns(p)) == len(p) - 1

#log returns are additive: sum over a window == total log change
def test_additivity():
  p = pd.Series([100.0, 110.0, 99.0, 120.0])
  r = log_returns(p, scale=1)
  total = np.log(p.iloc[-1] / p.iloc[0])
  assert np.isclose(r.sum(), total)

def test_squared_returns_nonnegative():
  r = pd.Series([-2.0, 1.5, -0.3])
  assert (squared_returns(r) >= 0).all()
