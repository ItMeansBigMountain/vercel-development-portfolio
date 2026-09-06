# Trading Days
- make sure that the dates of fetching the stocks aligns with the amount of trading days



## One year of Data
### 252 trading days
The NYSE and NASDAQ average about 252 trading days a year. This is from 365.25 (days on average per year) * 5/7 (proportion work days per week) - 6 (weekday holidays) - 4*5/7 (fixed date holidays) = 252.03 ≈ 252.




# Stock Market Clustering and Cointegration Analysis (chatGPT 2/24/2023)

This project is designed to perform financial analysis on a collection of Exchange Traded Funds (ETFs). The goal is to identify groups of ETFs that behave similarly based on their return and volatility, and pairs of ETFs that are cointegrated, meaning they move together over time. This analysis can help in building a diverse portfolio and for pairs trading.

## Project Structure

1. **Import Required Libraries**: The required libraries include NumPy, pandas, yfinance, pandas_datareader, sklearn, kneed, statsmodels, and matplotlib for data handling, machine learning, statistics, and visualization.
   
2. **Data Extraction**: Fetches the ETF data from the NASDAQ database through the pandas_datareader and yfinance APIs. If the data is already saved in a local CSV file, the script will use that instead.
   
3. **Data Conditioning**: Drops any columns with null values and sets the date as the index.
   
4. **Feature Engineering**: Calculates the average return and volatility for each ETF based on their historical closing prices.
   
5. **Scaling**: Standardizes the return and volatility values using Scikit-Learn's StandardScaler to ensure they have equal influence on the clustering algorithm.
   
6. **K-Means Clustering**: Determines the optimal number of clusters using the elbow method, then applies K-Means clustering to group ETFs with similar behavior.
   
7. **Cointegration Analysis**: For each pair of ETFs in the same cluster, calculates a statistic called the hedge ratio and checks if the pair is cointegrated. If so, the pair is added to a list of cointegrated pairs.
   
8. **t-SNE Visualization**: Applies the t-SNE algorithm to reduce the dimensionality of the data for visualization. ETFs in the same cluster are shown in the same color, and cointegrated pairs are connected by a line.
   
9. **Result Inspection**: Allows the user to inspect the price trend and spread of any given pair of cointegrated ETFs.

This script provides valuable insights into the dynamics of the ETF market, potentially guiding trading and investment decisions. 

The resulting analysis can be used for the development of portfolio strategies, risk management, and trading systems.
