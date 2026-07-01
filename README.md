# GJR-GARCH
  Fitting a GJR GARCH model on NIFTY 50 returns (2015-2026) to study the leverage effect firsthand.

## Overview
  Upon fitting a plain GARCH(1,1) model on 11 years of NIFTY 50 log returns in a previous repository, it was observed that a Ljung-Box test carried out on the model showed leftover ARCH effects. The null hypothesis of no autocorrelation was rejected and it was confirmed that there remained volatility clustering in the model even after fitting. This was due to the modeled assumption of the GARCH(1,1) model which assumes negative and positive shock have symmetric effects on volatility. The preceding assumption has been well recorded as an oversimplification due to the leverage effect which states that negative shocks raise uncertainty in markets which leads to an increase in trading volume and therefore volatility in markets on a greater scale than positive shocks of the same size. In order to capture the leverage effect, the GJR GARCH model is utilized due to the presence of the Gamma parameter which measures how much excess volatility response is triggered as a consequence of negative shocks.

## Data and Methodology
  As stated and explained in the [GARCH (1,1) repository](https://github.com/uzair1509/GARCH_1_1), logarithmic returns are calculated from NIFTY 50 close prices of the past 11 years (2015-2026) for their time additivity effects. First, a plain GARCH(1,1) model is fit to act as control. Then three GJR GARCH models are fit on the log returns with Alpha, Beta, and Gamma lags being set at 1 and standardized residuals assumed to follow Student's t-distribution in one model, skewed-t distribution in the second model, and normal distribution in the last model. 
  
  The Alpha, Beta, and Gamma values are calculated for all the GJR models and shock persistence is calculated. Using the persistence values the shock half life is calculated for the models. The GJR persistence formula differs here with Gamma being a contributor to persistence:
  $$\text{Persistence} = \alpha + \beta + \frac{\gamma}{2}$$

The Gamma term is divided by 2 here based on the assumption that negative and positive shocks in the market have the same occurrence probability. Since we assume half the days do not have a negative shock this means that on half of the dayss the gamma coefficient is zero (only 1 when shock is negative) hence Gamma's contribution is roughly half its value in the persistence formula.
  
  Moreoever, utilizing the conditional volatility of the models, standardized residuals are calculated using the formula: 
  
  $$z_t = \frac{\varepsilon_t}{\sigma_t}$$
  ```
standardised residuals = residuals / conditional volatility
  ```
  Once standardised residuals are calculated the Ljung-Box test can now be carried out using squared standardised residuals and the ARCH LM test using standardised residuals to allow for valid comparison between the models. Moreover, AIC and BIC are calculated for all models to compare goodness of fit, following the same procedure as the [GARCH (1,1) repository](https://github.com/uzair1509/GARCH_1_1).
