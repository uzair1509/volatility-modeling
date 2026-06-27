# GARCH-1-1 Volatility Modeling (NIFTY 50)

## Overview
Upon conducting a Ljung-Box and ACF test previously on the volatility of the National Stock Exchange of India index, NIFTY 50, the next suitable step to capture volatility clustering systematically is using the GARCH model. In this repository a plain GARCH model is utilized as compared to analyzing exogenous variables or the leverage effect in influencing volatilty which are deliberately deferred at this stage for the sake of conceptual buildup. The motivation behind GARCH analysis is simply to understand the effects of shocks on volatility and model it as a process in and of itself rather than plotting a simple 20-day rolling volatility window  which does not explain why volatility clusters.

## Data and Methodology
As referenced in earlier projects, data of close prices is obtained for over a period of 11 years from (2015-2026) for the NIFTY 50 Index. Logarithmic returns are calculated from the close prices due to their time-additivity and ability to be converted back to a cumulative price level, properties which are not allowed by percentage returns. Upon calculation of logarithmic returns a GARCH model is calculated specifying one lag for each of the ARCH terms (last period's squared shock and conditional variance) so upon fitting the model only the previous day's shock and conditional variance is considered. However the effects of clustering on the previous days' volatility are already factored in. Futhermore the model assumes that the standardized residuals Z{t} follow a normal distribution.

