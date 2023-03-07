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
    start = datetime.datetime(2022, 1, 1)

    end = datetime.datetime.today().strftime('%Y-%m-%d')
    # end = datetime.datetime(2020, 7, 10)

    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF / 100
    return [RF, interest_coverage_ratio]


def calculate_cost_of_debt(RF, interest_coverage_ratio):
    if interest_coverage_ratio > 8.5:
        # Rating is AAA
        credit_spread = 0.0063
    if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
        # Rating is AA
        credit_spread = 0.0078
    if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <= 6.5):
        # Rating is A+
        credit_spread = 0.0098
    if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <= 5.49):
        # Rating is A
        credit_spread = 0.0108
    if (interest_coverage_ratio > 3) & (interest_coverage_ratio <= 4.25):
        # Rating is A-
        credit_spread = 0.0122
    if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <= 3):
        # Rating is BBB
        credit_spread = 0.0156
    if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <= 2.5):
        # Rating is BB+
        credit_spread = 0.02
    if (interest_coverage_ratio > 2) & (interest_coverage_ratio <= 2.25):
        # Rating is BB
        credit_spread = 0.0240
    if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <= 2):
        # Rating is B+
        credit_spread = 0.0351
    if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <= 1.75):
        # Rating is B
        credit_spread = 0.0421
    if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <= 1.5):
        # Rating is B-
        credit_spread = 0.0515
    if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <= 1.25):
        # Rating is CCC
        credit_spread = 0.0820
    if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <= 0.8):
        # Rating is CC
        credit_spread = 0.0864
    if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <= 0.65):
        # Rating is C
        credit_spread = 0.1134
    if interest_coverage_ratio <= 0.2:
        # Rating is D
        credit_spread = 0.1512

    cost_of_debt = RF + credit_spread
    return cost_of_debt

#call api for beta & est. market return
def calculate_cost_of_equity(ticker):
    key = os.environ.get('API_KEY')
    stock_ticker = ticker
    # RF
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    # end = datetime.datetime(2020, 7, 10)
    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1]) #debug value?
    RF = RF / 100

    # Beta
    beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{stock_ticker}?apikey={key}')
    beta = beta.json()
    beta = float(beta['profile']['beta'])

    # Market Return
    '''
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    # Drop all Not a number values using drop method.
    SP500.dropna(inplace=True)
    SP500yearlyreturn = (SP500['sp500'].iloc[-1] / SP500['sp500'].iloc[-252]) - 1
    '''

    sp500_avg_return = 0.08

    #cost of equity
    cost_of_equity = RF + (beta * (sp500_avg_return - RF))
    return cost_of_equity


# return wacc
def calculate_WACC(ticker, cost_of_equity, cost_of_debt, capital_structure):
    pass
    #key = os.environ.get('API_KEY')
    #stock_ticker = ticker


    # wacc
    #WACC = (cost_of_debt * (1 - TR) * total_Debts) + (cost_of_equity * total_Equity)
    #return WACC




#deb/equity ratio
#tax rate
def get_tax_rate_and_capital_structure(ticker):
    stock_ticker = ticker
    key = os.environ.get('API_KEY')

    capital_structure = []
    FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{stock_ticker}?apikey={key}').json()
    TR = FR[0]['effectiveTaxRate']
    # capital structure
    BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_ticker}?period=quarter&apikey={key}').json()
    total_Debt = BS[0]['totalDebt'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
    total_Equity = BS[0]['totalStockholdersEquity'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
    capital_structure.append(total_Equity)
    capital_structure.append(total_Debt)
    capital_structure.append(TR)

    return capital_structure


def get_TR_and_CS(ticker):

    fred_key = os.environ.get('FRED_API_KEY')
    key = os.environ.get('API_KEY')

    capital_structure = []

    data = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{ticker}?apikey={key}').json()
    TR = data[0]['effectiveTaxRate']

    D_E = BS = requests.get(
        f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=quarter&apikey={key}').json()

    total_Equity = ''
    capital_structure.append(TR)

    return D_E
    #return capital_structure







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
