import numpy as np

def log_returns(prices, scale=100):
  #scale=100 gives percent returns, which is what arch expects
  #(keeps the optimiser away from tiny parameter values)
  r = scale * np.log(prices / prices.shift(1))
  return r.dropna()

def squared_returns(returns):
  #variance proxy used to score forecasts in study 06
  return returns ** 2
