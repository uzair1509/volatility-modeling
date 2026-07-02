# GJR-GARCH
  Fitting a GJR GARCH model on NIFTY 50 returns (2015-2026) to study the leverage effect firsthand.

## Overview
  Upon fitting a plain GARCH(1,1) model on 11 years of NIFTY 50 log returns in a previous repository, it was observed that a Ljung-Box test carried out on the model showed leftover ARCH effects. The null hypothesis of no autocorrelation was rejected and it was confirmed that there remained volatility clustering in the model even after fitting. This was due to the modeled assumption of the GARCH(1,1) model which assumes negative and positive shock have symmetric effects on volatility. The preceding assumption has been well recorded as an oversimplification due to the leverage effect which states that negative shocks raise uncertainty in markets which leads to an increase in trading volume and therefore volatility in markets on a greater scale than positive shocks of the same size. In order to capture the leverage effect, the GJR GARCH model is utilized due to the presence of the Gamma parameter which measures how much excess volatility response is triggered as a consequence of negative shocks.

## Data and Methodology
  As stated and explained in the [GARCH (1,1) repository](https://github.com/uzair1509/GARCH_1_1), logarithmic returns are calculated from NIFTY 50 close prices of the past 11 years (2015-2026) for their time additivity effects. First, a plain GARCH(1,1) model is fit to act as control. Then three GJR GARCH models are fit on the log returns with Alpha, Beta, and Gamma lags being set at 1 and standardized residuals assumed to follow Student's t-distribution in one model, skewed-t distribution in the second model, and normal distribution in the last model. 
  
  The Alpha, Beta, and Gamma values are calculated for all the GJR models and shock persistence is calculated. Using the persistence values the shock half life is calculated for the models. The GJR persistence formula differs here with Gamma being a contributor to persistence:
  $$\text{Persistence} = \alpha + \beta + \frac{\gamma}{2}$$

The Gamma term is divided by 2 here based on the assumption that negative and positive shocks in the market have the same occurrence probability. Since we assume half the days do not have a negative shock this means that on half of the days the gamma coefficient is zero (only 1 when shock is negative) hence Gamma's contribution is roughly half its value in the persistence formula.
  
  Moreoever, utilizing the conditional volatility of the models, standardized residuals are calculated using the formula: 
  
  $$z_t = \frac{\varepsilon_t}{\sigma_t}$$
  ```
standardised residuals = residuals / conditional volatility
  ```
  Once the standardized residuals are calculated, the Ljung-Box test is carried out usign 
  Once standardised residuals are calculated the Ljung-Box test can now be carried out using squared standardised residuals and the ARCH LM test using standardised residuals to allow for valid comparison between the models. Moreover, AIC and BIC are calculated for all models to compare goodness of fit, following the same procedure as the [GARCH (1,1) repository](https://github.com/uzair1509/GARCH_1_1).\

  ## Results

  The following results were obtained after all tests including the residual diagnostics were run,

| Model | α | β | γ | AIC | BIC | Persistence | Half-life (days) |
|---|---|---|---|---|---|---|---|
| GARCH(1,1) | 0.1041 | 0.8724 | — | 6925.13 | 6948.75 | 0.9764 | 29.07 |
| GJR-normal | 0.0286 | 0.8569 | 0.1481 | 6865.31 | 6894.83 | 0.9596 | 16.80 |
| GJR-t | ~0 (4.2e-18) | 0.8906 | 0.1370 | 6730.08 | 6765.50 | 0.9591 | 16.60 |
| GJR-skewed-t | ~0 (4.1e-14) | 0.8891 | 0.1423 | 6704.11 | 6745.44 | 0.9602 | 17.07 |

| Model | Ljung-Box p (lag 10) | ARCH-LM p |
|---|---|---|
| GARCH(1,1) | 0.517 | 0.414 |
| GJR-normal | 0.106 | 0.068 |
| GJR-t | 0.013 |

  Printed Gamma p-values are all <0.001 in every GJR model's case (3.6e-4 for normal, 7.7e-7 for t, 1.5e-7 for skewed-t). Since all Gamma values are statistically significant, the presence of the leverage effect is confirmed. Furthermore, since Gamma is significant in all GJR models, evidently, no matter what residual distribution is modeled, the leverage effect exists. 

  Point to be noted here is that as Gamma is added to the variance equation half-life falls from roughly 29 days to roughly 17 days. This signals that half of the long-term modeled shock memory is acutally asymmetry which is not considered by the GARCH (1,1) specification. Lastly shock persistence remains similar amongst all estimates.

  By AIC and BIC criteria, the best ranked model by likelihood is the GJR GARCH with residuals modeled with a skewed-t distribution while the GJR model with a student's t distribution is ranekd second best by the aforementioned criteria. These results are expected as heavier tail distributions are known to improve likelihood estimations. Hence no surprising result is yielded.

  On the contrary, both GJR models modeled on a fat-tailed residual distribution both have an alpha of almost zero with the normal distribution GJR being the only GJR that has an interior alpha value. This happens as the optimizer in the rest of the two GJR models forces respective alphas to their closest non-zero valeus (non-negativity constraint) above the unconstrained optimum. Since the skewed-t and student's t distributions assign higher probability to extreme realizations/events. Here are the eta and lambda values for the skew-t distributed GJR along with their significance:

  |Distribution|Parameter|Value|P-Value|
  |-----|-----|-----|-----|
  |Skewed-T|Eta|7.366|4.88e-13|
  |Skewed-T|Lambda|-0.149|6.37e-07|
  |Student's T|Eta|6.940|6.128e-14|

  
