# Rolling_Window_Forecast
Performing a rolling window forecast on NIFTY 50 volatilities calculated using both a GARCH(1,1) model and a normally distributed GJR GARCH model from the period 2015-2026.

## Data and Methodology
After comparing three GARCH models in the  [GJR GARCH repository](https://github.com/uzair1509/GJR-GARCH) on the basis of AIC/BIC and residual diagnostics on the basis of existent data, and declaring the normally distributed GJR model as the best fitted, the most suitable next step is to conduct an ouf-of-sample forecast. While conducting the out of sample forecast, data is kept consistent with previous repositories (calculating log returns of the NIFTY 50 index close prices from 2015-2016). Using textbook methods, close prices are split between train and test data where approximately 55% of data is train data and the rest is test data. Upon forecasting variance using the logarithmic returns from both models, the mean squared and mean absolute errors are calculated and the Quasi-Likelihood test is conducted on both models with the following formulas:

$$MSE = \frac{1}{T}\sum_{t=1}^{T}(\hat{\sigma}^2_t - r_t^2)^2$$

$$MAE = \frac{1}{T}\sum_{t=1}^{T}|\hat{\sigma}^2_t - r_t^2|$$

$$QLIKE = \frac{1}{T}\sum_{t=1}^{T}\left(\frac{r_t^2}{\hat{\sigma}^2_t} - \log\frac{r_t^2}{\hat{\sigma}^2_t} - 1\right)$$

