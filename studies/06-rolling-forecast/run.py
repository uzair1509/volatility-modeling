from volmodels.data import load_nifty
from volmodels.returns import log_returns
from volmodels.backtest import rolling_forecast
from volmodels.losses import mse, mae, qlike

nifty = load_nifty()
r = log_returns(nifty['Close'])

df = rolling_forecast(r, window=1500)
df.to_csv('results/rolling_forecast.csv')

print(f"{'Metric':<10} {'GARCH(1,1)':>15} {'GJR-normal':>15} {'Winner':>12}")
for name, func in [('MSE', mse), ('MAE', mae), ('QLIKE', qlike)]:
  g = func(df['garch11'].values, df['sq_ret'].values)
  j = func(df['gjr_normal'].values, df['sq_ret'].values)
  winner = 'GARCH' if g < j else 'GJR'
  print(f"{name:<10} {g:>15.6f} {j:>15.6f} {winner:>12}")
