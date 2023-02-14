import requests
import re
import csv
import json
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import sys
import numpy as np #for pv and fv functions



def get_cashflow_data(ticker):
    stock_ticker = ticker
    # CASHFLOWS AND ESTIMATIONS:
    # extract CF values, populate arrays and predict future CF.
    # Growth factor from financials? Change string >> float and divide with 100 for decimal
    # define terminal value. Perp. growth rate? Scrape WACC ?

    # CF data from marketwatch.com
    headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    mw_cf_url = 'https://www.marketwatch.com/investing/stock/' + stock_ticker + '/financials/cash-flow'
    result = requests.get(mw_cf_url)
    soup = BeautifulSoup(result.content, 'html.parser')

    all_tables = soup.find_all(class_='element element--table table--fixed financials')
    # financials table
    fin_table = all_tables[-1]
    cf_row = fin_table.find_all('tr')
    # cf data
    cf_table = cf_row[-3]
    # result set
    cf_data = cf_table.select('span')

    cf_array = []

    for data in cf_data:
        data.string
        cf_array.append(data)

    #what if trillions?
    str_arr = []
    for i in cf_array:
        str = i.string
        str = str.strip('B')
        str_arr.append(str)

    # past cashflows in billions
    past_cashflows = []
    for cf in str_arr:
        cf = float(cf)
        past_cashflows.append(cf)

    year1 = past_cashflows[1]
    year2 = past_cashflows[2]
    year3 = past_cashflows[3]
    year4 = past_cashflows[4]
    year5 = past_cashflows[0]

    CF_array = []
    CF_array.append(year1)
    CF_array.append(year2)
    CF_array.append(year3)
    CF_array.append(year4)
    CF_array.append(year5)

    return  CF_array


def get_metrics(ticker):
    stock_ticker = ticker
    summary_url = 'https://finance.yahoo.com/quote/' + stock_ticker + '?p=' + stock_ticker + '&.tsrc=fin-srch'
    summary_result = requests.get(summary_url)
    summary_html = BeautifulSoup(summary_result.text, 'html.parser')

    # scrape basic headers
    company_name = summary_html.find('h1').string
    current_price = summary_html.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').string

    # divide table
    right_table = summary_html.find('table', class_='W(100%) M(0) Bdcl(c)')
    tbody_table = []

    # scrape right side of the summary table in to array then chop it to get needed data
    for tr in right_table('tr'):
        for td in tr('td', class_='Ta(end) Fw(600) Lh(14px)'):
            tbody_table.append(td)

    # change data types to floats for calculations !
    # strip letters from strings
    market_cap = tbody_table[0].string

    # if market cap contains 'T' change to billions => *1000
    for i in market_cap:
        if i == 'T':
            market_cap = market_cap.strip('T')
            market_cap = float(market_cap)
            market_cap = market_cap * 1000 #to billions
            
        if i == 'B':
            market_cap = market_cap.strip('B')
            market_cap = float(market_cap)


    earnings_per_share = tbody_table[2].string
    pe_ratio = tbody_table[3].string
    dividen_yield = tbody_table[5].string

    metric_array = []
    metric_array.append(market_cap)
    metric_array.append(earnings_per_share)
    metric_array.append(pe_ratio)
    metric_array.append(dividen_yield)


    return metric_array



#deb/equity ratio
#tax rate
def get_tax_rate_and_capital_structure():
    pass


def check_billions_or_trillions():
    pass

