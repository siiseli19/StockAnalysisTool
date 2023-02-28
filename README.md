# StockAnalysisTool
Analysis tool for private use

The goal of this project is to build a tool that streamlines manual work by calculating the fair value of stocks to support investment decisions.
On the side this project helps me to get familiar with financial concepts and gain practical experience utilizing them.

This tool takes a stock ticker as an input. After that cashflows and basic data like market cap etc. are scraped from YahooFinance.com. 
For DCF valuation purposes we need data for calculating WACC which we can use as a discount factor for the cashflows.
To achieve this is came out that the easiest and most efficient way is to utilize FRED API instead of web scraping.

For further development it could be useful to create a function that calculates the Graham Number. 
With GN we could value also financial companies because the DCF method wont apply properly for them.
Also it is worth to consider to automate this program via cloud environment to run it weekly.


