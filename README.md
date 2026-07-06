# Rolling_Window_Forecast
Performing a rolling window forecast on NIFTY 50 volatilities calculated using both a GARCH(1,1) model and a normally distributed GJR GARCH model from the period 2015-2026.

## Data and Methodology
  After comparing three GARCH models in the  [GJR GARCH repository](https://github.com/uzair1509/GJR-GARCH) on the basis of AIC/BIC and residual diagnostics on the basis of existent data, and declaring the normally distributed GJR model as the best fitted, the most suitable next step is to conduct an out-of-sample forecast. While conducting the out of sample forecast, data is kept consistent with previous repositories (calculating log returns of the NIFTY 50 index close prices from 2015-2026). Using textbook methods, close prices are split between train and test data where approximately 55% of data is train data and the rest is test data. Upon forecasting variance using the logarithmic returns from both models, the mean squared and mean absolute errors **(MSE and MAE)** are calculated and the Quasi-Likelihood **(QLIKE)** test is conducted on both models. 

$$MSE = \frac{1}{T}\sum_{t=1}^{T}(\hat{\sigma}^2_t - r_t^2)^2$$
<br>The MSE is calculated by obtaining the mean squared difference between the forecasted variance values and the actual variance values. Since the error is squared the metric penalizes large forecasting errors more heavily than small misses.

$$MAE = \frac{1}{T}\sum_{t=1}^{T}|\hat{\sigma}^2_t - r_t^2|$$
<br>The MAE on the other hand does not square the difference between forecast and actual variance values but calculated the mean absolute difference between forecast and actual values. Hence it penalizes extreme day misses less than the MSE where the forecast errors are relatively large.

$$QLIKE = \frac{1}{T}\sum_{t=1}^{T}\left(\frac{r_t^2}{\hat{\sigma}^2_t} - \log\frac{r_t^2}{\hat{\sigma}^2_t} - 1\right)$$
<br>The QLIKE test is the preferred metric for variance forecast evaluations. This is due to the reason that the QLIKE penalizes overestimated and underestimated variances differently exactly how a market behaves. Hence, even with a noisy proxy like squared returns the QLIKE is guaranteed to correctly rank models by specification which the other two metrics do not guarantee with noisy proxies.

  Even though the normally distributed GJR-GARCH model proved to be better according to in-sample diagnostics, the aim of this repository is to check whether the added Gamma parameter of this model (asymmetry) contributes to a better model fit and better variance forecasting as a final expectation. 

  By "rolling-window" forecasting it is meant that the training data being used for fitting the model rolls forward by one day when the variance of the next day from the selected day is calculated. The advantage of rolling-window forecasts upon fixed or expanding window forecasts is that as the window rolls forward the training data being used is relatively recent as compared to the other aforementioned methods. The rolling window size is set to be **1500** days from 2706 usable days (2707 total) as the .dropna() method removes one observation to prevent lookahead bias. This means that approximately 1200 out-of-sample forecasts can be carried out.

  True daily variance is an unobservable quantity and an empirical proxy is required as a substitute to evaluate forecast accuracy which in this case is squared returns. Even though the squared returns proxy introduces a good deal of noise, realized volatility can not be used due to data limitations as Yahoo Finance can only provide daily close prices and not intra-day close prices. 

## Results
  The following metrics were obtained upon the conduction of the tests:
| Metric | GARCH(1,1) | GJR-normal | Winner |
|---|---|---|---|
| MSE | 3.361787 | 3.404176 | GARCH(1,1) |
| MAE | 0.829978 | 0.827054 | GJR-normal |
| QLIKE | 1.495490 | 1.512371 | GARCH(1,1) |

  As seen, the plain GARCH model outperforms the normally distributed GJR model on 2 metrics out of 3. On the other hand the GJR-normal model outperforms the plain GARCH model by a minuscule difference in the MAE metric which is essentially a tie.
  
  The simple conclusion we land at is that the introduction of asymmetry, although does improve in-sample fit, does not contribute much to improving an out-of-sample fit. The [GJR Repository](https://github.com/uzair1509/GJR-GARCH) did calculate Gamma to be statistically significant which showed that leverage effect did exist in the data, however, the existence of Gamma does not directly guarantee a better out-of-sample fit. This is because at each rolling step added complexity introduces added parameter estimation error.

  Since GARCH(1,1) outperforms on the Quasi-Likelihood metric, this goes to show that the simpler model is the stronger specification according to the preferred metric for out-of-sample forecasting on this set of data.

## Limitations
1. The variance proxy of squared returns being used is a noisy proxy and a better alternative would be to use realized volatility however due to dataset limitations of Yahoo Finance, RV can not be used as discussed above.

2. Forecasts conducted are only a single step ahead, multi-step forecasting may display different results on the metrics.

3. Results may also vary with a different train/test split than a 55/45 split.

## Tools
- Google Colab
- Python
- Yahoo Finance API for data download
- ARCH library for ARCH models
- Pandas and Numpy for data arrangement and calculations
  

   
