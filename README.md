# Rolling_Window_Forecast
Performing a rolling window forecast on NIFTY 50 volatilities calculated using both a GARCH(1,1) model and a normally distributed GJR GARCH model from the period 2015-2026.

## Data and Methodology
  After comparing three GARCH models in the  [GJR GARCH repository](https://github.com/uzair1509/GJR-GARCH) on the basis of AIC/BIC and residual diagnostics on the basis of existent data, and declaring the normally distributed GJR model as the best fitted, the most suitable next step is to conduct an ouf-of-sample forecast. While conducting the out of sample forecast, data is kept consistent with previous repositories (calculating log returns of the NIFTY 50 index close prices from 2015-2016). Using textbook methods, close prices are split between train and test data where approximately 55% of data is train data and the rest is test data. Upon forecasting variance using the logarithmic returns from both models, the mean squared and mean absolute errors **(MSE and MAE)** are calculated and the Quasi-Likelihood **(QLIKE)** test is conducted on both models. 

$$MSE = \frac{1}{T}\sum_{t=1}^{T}(\hat{\sigma}^2_t - r_t^2)^2$$
The MSE is calculated by obtaining the mean squared difference between the forecasted variance values and the actual variance values. Since the error is squared the metric penalizes large forecasting errors more heavily than small misses.

$$MAE = \frac{1}{T}\sum_{t=1}^{T}|\hat{\sigma}^2_t - r_t^2|$$
The MAE on the other hand does not square the difference between forecast and actual variance valeus but calculated the mean absolute difference between forecast and actual values. Hence it penalizes extreme day misses less than the MSE where the forecast errors are relatively large.

$$QLIKE = \frac{1}{T}\sum_{t=1}^{T}\left(\frac{r_t^2}{\hat{\sigma}^2_t} - \log\frac{r_t^2}{\hat{\sigma}^2_t} - 1\right)$$
The QLIKE test is the preferred metric for variance forecast evaluations

  Even though the normally distributed GJR-GARCH model proved to be better according to in-sample diagnostics, the aim of this repository is to check whether the added Gamma parameter of this model (asymmetry) contributes to a better model fit and better variance forecasting as a final expectation. This is due to the reason that the QLIKE penalizes overestimated and underestimated variances differently exactly how a market behaves. Hence, even with a noisy proxy like squared returns the QLIKE is guaranteed to correctly rank models by specification which the other two metrics do not guarantee with noisy proxies.

  By "rolling-window" forecasting it is meant that the training data being used for fitting the model rolls forward by one day when the variance of the next day from the selected day is calculated. The advantage of rolling-window forecasts upon fixed or expanding window forecasts is that as the window rolls forward the training data being used is relatively recent as compared to the other aforementioned methods. The rolling window size is set to be **1500** days from 2706 usable days (2707 total) as the .dropna() method removes one observation to prevent lookahead bias. This means that approximately 1200 out-of-sample forecasts can be carried out.

  Since volatility is not a tangible or directly measurable quantity a squared returns variance proxy is used instead of realized volatility. Even though the squared returns proxy introduces a good deal of noise, realized volatility can not be used due to data limitations as Yahoo Finance can only provide daily close prices and not intra-day close prices. 
