import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from arch import arch_model

from volmodels.data import load_nifty
from volmodels.returns import log_returns

nifty = load_nifty()
r = log_returns(nifty['Close'])

fit = arch_model(r.values, vol='GARCH', p=1, q=1, mean='Constant', dist='normal').fit(disp='off')
print(fit.summary())

#persistence: alpha + beta. close to 1 means shocks decay slowly
persistence = fit.params['alpha[1]'] + fit.params['beta[1]']
print(f'\nPersistence (alpha + beta): {persistence:.4f}')

plt.figure(figsize=(11,5))
plt.plot(r.index, fit.conditional_volatility)
plt.title('GARCH(1,1) Conditional Volatility')
plt.xlabel('Date')
plt.ylabel('Conditional Volatility (%)')
plt.tight_layout()
plt.savefig('results/04-conditional-volatility.png', dpi=150)
plt.close()
