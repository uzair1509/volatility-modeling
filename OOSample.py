import numpy as np
import pandas as pd
import yfinance as yf
from arch import arch_model
import warnings as wn

wn.filterwarnings('ignore')

nifty = yf.download('^NSEI', start = '2015-01-01', end = '2026-01-01', progress = False)
nifty['log_ret'] = 100 * (np.log(nifty['Close']/nifty['Close'].shift(1)))
returns = nifty['log_ret'].dropna().values
# note to self: .values converts data --> np array

T = len(returns)
window = 1500
forecast_num = T - window

frcst_garch = np.zeros(forecast_num)
frcst_gjr = np.zeros(forecast_num)
sq_ret = np.zeros(forecast_num) #squared returns

for i in range(forecast_num):
  if i % 100 == 0:
    print(f'{i} out of {forecast_num} days forecasted')
  
  train = returns[i : i + window]
  sq_ret[i] = returns[i + window] ** 2

  garch_11 = arch_model(train, vol = 'GARCH', p = 1, q = 1, mean = 'Constant', dist = 'normal').fit(disp='off')
  frcst_garch[i] = garch_11.forecast(horizon = 1).variance.values[-1,0] #-1,0 location vector last row of first column

  garch_gjr = arch_model(train, vol = 'GARCH', p = 1, o = 1, q = 1, mean = 'Constant', dist = 'normal').fit(disp='off')
  frcst_gjr[i] = garch_gjr.forecast(horizon=1).variance.values[-1,0]

  
#metrics 

def mse(forecast, actual):
  return np.mean((forecast - actual)**2)

def mae(forecast, actual):
  return np.mean(np.abs(forecast - actual))

def qlike(forecast, actual):
   eps = 1e-8 #prevent div by 0
   act = np.maximum(actual, eps)
   frc = np.maximum(forecast, eps)
   return np.mean(act/frc - np.log(act/frc) - 1)

print(f"{'Metric':<10} {'GARCH(1,1)':>15} {'GARCH-GJR-normal':>15} {'Winner':>12}")
print("__EVAL__")
for name, func in [('MSE', mse), ('MAE', mae), ('QLIKE', qlike)]:
  garch = func(frcst_garch, sq_ret)
  gjr = func(frcst_gjr, sq_ret)
  winner = 'GARCH' if garch < gjr else 'GJR'
  print(f"{name:<10} {garch:>15.6f} {gjr:>15.6f} {winner:>12}")
