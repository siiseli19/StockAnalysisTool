import datareader as datareader
import requests
import re
import csv
import json
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import pandas_datareader.data as web
import sys
import os
import datetime


# from financialmodelingprep API
# Kd = Rf + Credit Spread
# Risk free rate we will use the interest rate offered by a 1 year US T-bill >> scrape if needed
def interest_coverage_and_RF(ticker):
    stock_ticker = ticker
    key = os.environ.get('API_KEY')

    # Interest coverage
    IS = requests.get(
        f'https://financialmodelingprep.com/api/v3/income-statement/{stock_ticker}?apikey={key}').json()  # income statement
    EBIT = IS[0]['ebitda'] - IS[0]['depreciationAndAmortization']  # index 0 for the most recent year
    interest_expense = IS[0]['interestExpense']
    interest_coverage_ratio = EBIT / interest_expense

    # RF
    start = datetime.datetime(2019, 7, 10)

    end = datetime.datetime.today().strftime('%Y-%m-%d')
    # end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF / 100
    print(RF, interest_coverage_ratio)
    return [RF, interest_coverage_ratio]


def calculate_cost_of_debt(ticker):
    pass


def calculate_cost_of_equity():
    pass


# return wacc
def calculate_WACC():
    pass


# A DCF valuation for mature dividend paying companies with 10% error marginal
# Consider country codes for different perpetual growthrates
# pass all the extracted data for here as following:
# present cashflows in array
# cashflow growth rate
# wacc

def calculate_DCF():
    pass


def calculate_graham_number():
    pass
