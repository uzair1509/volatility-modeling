## NSEI-Price-Movement-Tracking
Tracking the movement of prices on the Index of National Stock Exchange of India over a decade (2015-2026)

A foundational project, the first of many leading to the creating of a GARCH model to explore volatility and its influencing factors of the NIFTY 50 Index.

##Overview 
To understand the fundamentals of financial returns, skewness, and kurtosis, a preliminary model is necessary for visual aid.

##Data
Daily close prices of the Nifty 50 Index (Ticker: ^NSEI) downloaded via the Yahoo Finance API, yfinance.

##Methodology
Log returns computed as:
return_t = 100 * log_base_10(price_t/price_t-1)

Log returns are utilized due to additive effect as standard practice. This allows better normality at short horizons.

## Key findings
|Statistic|Value|
Mean daily return|
Daily Volatility (SD)|
Skewness|
|
