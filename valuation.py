import requests
import re
import csv
import json
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import sys
import numpy as np #for pv and fv functions
import os




# from financialmodelingprep API
#Kd = Rf + Credit Spread
#Risk free rate we will use the interest rate offered by a 1 year US T-bill >> scrape if needed
def interest_coverage_and_RF(ticker):
    stock_ticker = ticker
    key = os.environ.get('API_KEY')

    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={key}').json() #income statement
    EBIT = IS[0]['ebitda'] - IS[0]['depreciationAndAmortization'] #index 0 for the most recent year
    interest_expense = IS[0]['interestExpense']
    interest_coverage_ratio = EBIT / interest_expense
    return interest_coverage_ratio

def calculate_cost_of_debt(ticker):

    pass

def calculate_cost_of_equity():
    pass


#return wacc
def calculate_WACC():
    pass


#A DCF valuation for mature dividend paying companies with 10% error marginal
#Consider country codes for different perpetual growthrates
# pass all the extracted data for here as following:
# present cashflows in array
# cashflow growth rate
#wacc

def calculate_DCF():
    pass

def calculate_graham_number():
    pass




