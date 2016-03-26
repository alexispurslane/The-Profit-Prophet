import csv
import urllib.request
from lxml import etree
from yahoo_finance import *
from bs4 import BeautifulSoup
import datetime
from sklearn.linear_model import LinearRegression

ai = LinearRegression()

with open('secwiki_tickers.csv', mode='r') as in_file:
    reader = csv.DictReader(in_file)
    name_to_ticker_dict = {row['Name'].lower(): row['Ticker'] for row in reader}

def get_company_info(c):
    d = datetime.datetime.now().date()

    comp = Share(c)
    soup = BeautifulSoup(urllib.request.urlopen('http://finance.yahoo.com/q?s='+c).read(), 'lxml')
    return dict(list({'history': list(map(lambda x: x['High'],
                                          comp.get_historical(str(d - datetime.timedelta(days=300)),
                                                              str(d))))}.items()) + \
                list({tr.th.text: tr.td.text
                      for tr in list(soup.find("table", {"id":"table1"}).children)}.items()) +\
                list({'Name': c}.items())+\
                list({'Current':comp.get_price()}.items()))

def training_info(x):
    return (list(map(eval, get_company_info(x)['history'])),
            eval(get_company_info(x)['Current']))

histories = [
    training_info('GOOG'),
    training_info('AAPL'),
    training_info('CSCO'),
    training_info('LNKD'),
    training_info('FB'),
    training_info('TWTR'),
    training_info('AMZN'),
    training_info('NFLX'),
    training_info('MSFT'),
    training_info('YHOO'),
    training_info('VZ'),
    training_info('HPQ'),
    training_info('JPM'),
    training_info('BAC'),
    training_info('IBM'),
    training_info('WFC'),
    training_info('CMCSA'),
    training_info('INTC'),
    training_info('TSLA'),
    training_info('WMT'),
    training_info('ANET'),
    training_info('ATVI'),
    training_info('ADBE'),
    training_info('ADI'),
    training_info('AMAT'),
    training_info('ADSK'),
    training_info('ADP'),
    training_info('WFC'),
    training_info('FDX'),
    training_info('UPS'),
    training_info('MMM'),
    training_info('ABT'),
]

ai.fit(list(map(lambda x: x[0], histories)),
       list(map(lambda x: x[1], histories)))

def company_worth_investing(c):
    i = get_company_info(c)
    nvalue = ai.predict(list(map(eval, i['history']))[1:]+[eval(i['Current'])])[0]
    b = eval(i['Beta:'])
    
    if 0.85 < b < 1.15:
        risk = 'low'
    elif 0.5 < b < 0.85 or 1.15 < b < 1.5:
        risk = 'medium'
    elif 0.5 > b or 1.5 < b:
        risk = 'high'
        
    # Name, Risk (low/medium/high), Beta, Percentage Increase, CPPS, PPPS
    return (i['Name'],
            risk, b,
            (nvalue - eval(i['history'][-1]))/eval(i['history'][-1]),
            eval(i['Current']),
            nvalue)
