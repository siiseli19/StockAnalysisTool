import sys
import requests
import re
import csv
import json
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import numpy as np #for pv and fv functions

from functions import get_metrics
from functions import get_cashflow_data
from valuation import interest_coverage_and_RF, calculate_cost_of_debt, calculate_cost_of_equity

#Function to extract stock data from yahoofinance.com
#Takes a stocks ticker as a parameter
#How to take account changing years on page??
#make variables for indicators !! p/e etc..
def extract_stock_data(ticker):


    metric_data = get_metrics(ticker)
    cf_data = get_cashflow_data(ticker)
    IC_and_RF = interest_coverage_and_RF(ticker)


    interest_coverage_ratio = IC_and_RF[1]
    risk_free_rate = IC_and_RF[0]

    cost_of_debt = calculate_cost_of_debt(risk_free_rate, interest_coverage_ratio)
    cost_of_equity = calculate_cost_of_equity(ticker)


    print(cf_data)
    print(metric_data)
    print('--------')
    print(risk_free_rate)
    print(interest_coverage_ratio)
    print(cost_of_debt)
    print(cost_of_equity)

    #increase casflows with growthfactor >> numpy npv function
    #Cost of cap => ROE >> similar companies
    #Cost of debt => interest rate
    #amounts from balance sheets >> scrape gurufocus??
    # WACC = (amountDebt*costDebt) + (abountCap*costCap) * (1-TaxRate)
    #remember to deal with negative cashflows >> not allowed for div. investing
    # abort process if neg. cf detected >> doesnt fit on investment criteria.
    #create alternative solutions like graham number?
    #loop trough past CF and append incremented values to future CF array based on growth factor
    future_cashflows = []
    #simple scrape for testing
    #Scrpe income statement for revenue and EPS performance analysis ??
    #scrape needed data for Graham number/financial sector valuation.
stock = 'TGT'
extract_stock_data(stock)
